"""Turns a file the API streams as raw bytes into MCP content a client can use.

Images become image content and text files text. A PDF becomes its extracted
text. Other files (audio, spreadsheets, archives...) are described in a line
of text instead of sent: no mainstream client hands audio to the model, and
claude.ai rejects a tool result carrying an embedded binary resource.
"""

from __future__ import annotations

import base64
import io
import logging
from typing import TYPE_CHECKING

from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from mcp.types import ImageContent, TextContent

from .response_format import MAX_RESULT_CHARS

if TYPE_CHECKING:
    from mcp.types import ContentBlock

    from late.client.binary_response import BinaryResponse

logger = logging.getLogger(__name__)

# Anthropic's API rejects an image over 5 MB or in another format, which would
# fail the client's whole turn, so those images are only described.
MAX_IMAGE_BYTES = 5 * 1024 * 1024
VIEWABLE_IMAGE_TYPES = frozenset({"image/jpeg", "image/png", "image/gif", "image/webp"})
# Parsing a larger PDF on the hosted server is not worth the memory and CPU.
MAX_PDF_BYTES = 20 * 1024 * 1024
_PDF_TYPES = frozenset({"application/pdf", "application/x-pdf"})


def binary_tool_result(response: BinaryResponse) -> ToolResult:
    mime_type = response.mime_type
    described = (
        f"{response.filename or 'the file'} ({mime_type}, "
        f"{len(response.content):,} bytes)"
    )
    if mime_type.startswith("text/"):
        return _text_result(response, described)
    if mime_type in VIEWABLE_IMAGE_TYPES and len(response.content) <= MAX_IMAGE_BYTES:
        image = ImageContent(
            type="image",
            data=base64.b64encode(response.content).decode("ascii"),
            mimeType=mime_type,
        )
        return _result(f"Downloaded {described}.", image)
    if mime_type in _PDF_TYPES:
        return _result(_pdf_text(response, described))
    return _result(f"Downloaded {described}. {_unreadable_reason(mime_type)}")


def _text_result(response: BinaryResponse, described: str) -> ToolResult:
    text = response.content.decode(response.charset or "utf-8", "replace")
    if len(text) > MAX_RESULT_CHARS:
        raise ToolError(
            f"{described} has {len(text):,} characters, more than the "
            f"{MAX_RESULT_CHARS:,} a tool result can hold. Narrow the request "
            "or ask for JSON instead."
        )
    return _result(text)


def _pdf_text(response: BinaryResponse, described: str) -> str:
    if len(response.content) > MAX_PDF_BYTES:
        return (
            f"Downloaded {described}. It is larger than the "
            f"{MAX_PDF_BYTES // (1024 * 1024)} MB whose text this tool extracts, "
            "so its contents are not shown."
        )
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(response.content))
        page_count = len(reader.pages)
        header = f"Text of {described}, {page_count} page(s):"
        pages = _page_texts(reader, page_count, MAX_RESULT_CHARS - len(header) - 400)
    except Exception as exc:
        # Encrypted, damaged or unusual PDFs: describe the file, don't fail the call.
        logger.info("PDF text extraction failed: %s", type(exc).__name__)
        return (
            f"Downloaded {described}, but its text could not be extracted "
            "(the PDF may be encrypted or damaged)."
        )
    if not pages:
        return (
            f"Downloaded {described}. It has no extractable text (it is probably "
            "a scan or an image), so its contents are not shown."
        )
    return "\n\n".join([header, *pages])


def _page_texts(reader, page_count: int, budget: int) -> list[str]:
    """Each page's text, stopping with a note where the result cap is reached."""
    pages: list[str] = []
    used = 0
    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        block = f"--- Page {number} ---\n{text}"
        if used + len(block) > budget:
            pages.append(block[: max(0, budget - used)])
            rest = (
                f" and pages {number + 1}-{page_count} are not shown"
                if number < page_count
                else ""
            )
            pages.append(
                f"[Text cut at {MAX_RESULT_CHARS:,} characters: page {number} "
                f"is incomplete{rest}.]"
            )
            break
        pages.append(block)
        used += len(block) + 2
    return pages


def _unreadable_reason(mime_type: str) -> str:
    if mime_type.startswith("audio/"):
        return "Audio can't be passed to the model, and no transcript is available."
    if mime_type.startswith("image/"):
        return (
            "The image is too large or in a format the model can't view "
            "(JPEG, PNG, GIF and WebP up to 5 MB are shown)."
        )
    return "Its contents can't be shown here: only images, text and PDFs are."


def _result(text: str, *blocks: ContentBlock) -> ToolResult:
    return ToolResult(
        content=[TextContent(type="text", text=text), *blocks],
        structured_content={"result": text},
    )
