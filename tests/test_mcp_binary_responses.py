"""Files the API streams as raw bytes (WhatsApp media, mail attachments, Drive
files) failed with "'utf-8' codec can't decode byte 0xff" because every body
was parsed as JSON. The SDK now returns them as a BinaryResponse and the MCP
tools as image content, text, or a PDF's extracted text."""

from __future__ import annotations

import base64

import httpx
import pytest
import respx
from fastmcp import Client
from mcp.types import ImageContent, TextContent

from late import BinaryResponse, Late
from late.mcp.binary_content import MAX_IMAGE_BYTES, MAX_PDF_BYTES
from late.mcp.response_format import MAX_RESULT_CHARS
from late.mcp.server import mcp

API = "https://api.test.com"
JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9"
OGG = b"OggS\x00\x02" + bytes(range(256))


def _pdf(*pages: list[str]) -> bytes:
    """A minimal real PDF with one text line per entry of each page."""
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(len(pages)))
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>",
    ]
    for i, lines in enumerate(pages):
        ops = "BT /F1 12 Tf 50 750 Td 14 TL " + " ".join(
            f"({line}) Tj T*" for line in lines
        )
        ops += " ET"
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents "
            f"{4 + 2 * i} 0 R /Resources << /Font << /F1 {3 + 2 * len(pages)} 0 R >> >> >>"
        )
        objects.append(f"<< /Length {len(ops)} >>\nstream\n{ops}\nendstream")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets)
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode()
    return out


PDF = _pdf(["Invoice INV-7731", "Total due: 1,337.42 EUR"], ["Due date: 2026-12-05"])


def _file(content: bytes, content_type: str, disposition: str | None = None):
    headers = {"content-type": content_type}
    if disposition:
        headers["content-disposition"] = disposition
    return httpx.Response(200, content=content, headers=headers)


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


# ---------------------------------------------------------------------------
# SDK


# ---------------------------------------------------------------------------
# SDK
# ---------------------------------------------------------------------------


@respx.mock
def test_json_response_is_parsed_as_before() -> None:
    respx.get(f"{API}/v1/whatsapp/media/m1").mock(
        return_value=httpx.Response(
            200,
            content=b'{"ok":true}',
            headers={"content-type": "application/json; charset=utf-8"},
        )
    )

    result = Late(api_key="k", base_url=API).whatsapp.get_whats_app_media("m1", "a1")

    assert result == {"ok": True}
    assert not isinstance(result, BinaryResponse)


@pytest.mark.parametrize("headers", [{}, {"content-type": "application/problem+json"}])
@respx.mock
def test_body_without_content_type_or_json_suffix_is_parsed_as_json(
    headers: dict[str, str],
) -> None:
    respx.get(f"{API}/v1/whatsapp/media/m1").mock(
        return_value=httpx.Response(200, content=b'{"ok":true}', headers=headers)
    )

    result = Late(api_key="k", base_url=API).whatsapp.get_whats_app_media("m1", "a1")

    assert result == {"ok": True}


@respx.mock
def test_binary_response_keeps_bytes_type_and_filename() -> None:
    respx.get(f"{API}/v1/whatsapp/media/m1").mock(
        return_value=_file(JPEG, "image/jpeg", 'attachment; filename="photo.jpg"')
    )

    result = Late(api_key="k", base_url=API).whatsapp.get_whats_app_media("m1", "a1")

    assert isinstance(result, BinaryResponse)
    assert result.content == JPEG
    assert result.content_type == "image/jpeg"
    assert result.filename == "photo.jpg"
    assert result.url == f"{API}/v1/whatsapp/media/m1?accountId=a1"
    assert result["content"] == JPEG


@respx.mock
async def test_async_binary_response_keeps_bytes_type_and_filename() -> None:
    respx.get(f"{API}/v1/whatsapp/media/m1").mock(
        return_value=_file(OGG, "audio/ogg; codecs=opus")
    )

    result = await Late(api_key="k", base_url=API).whatsapp.aget_whats_app_media(
        "m1", "a1"
    )

    assert isinstance(result, BinaryResponse)
    assert result.content == OGG
    assert result.mime_type == "audio/ogg"
    assert result.filename is None


def test_rfc_5987_filename_is_decoded() -> None:
    response = _file(
        PDF,
        "application/pdf",
        "attachment; filename=\"r?sum?.pdf\"; filename*=UTF-8''r%C3%A9sum%C3%A9.pdf",
    )

    assert BinaryResponse.from_response(response).filename == "résumé.pdf"


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------


async def _call(tool: str, arguments: dict[str, str], **kwargs):
    async with Client(mcp) as client:
        return await client.call_tool(tool, arguments, **kwargs)


WHATSAPP_MEDIA = (
    "whatsapp_get_whats_app_media",
    {"media_id": "m1", "account_id": "a1"},
)
EMAIL_ATTACHMENT = (
    "email_download_email_attachment",
    {"attachment_id": "att1", "account_id": "a1", "message_id": "msg1"},
)
DRIVE_FILE = ("files_download_file", {"file_id": "f1", "account_id": "a1"})


def _only_text(result) -> str:
    [block] = result.content
    assert isinstance(block, TextContent)
    assert result.structured_content == {"result": block.text}
    return block.text


@respx.mock
async def test_image_is_returned_as_image_content() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(JPEG, "image/jpeg", 'inline; filename="receipt.jpg"')
    )

    result = await _call(*WHATSAPP_MEDIA)

    note, image = result.content
    assert isinstance(note, TextContent)
    assert note.text == f"Downloaded receipt.jpg (image/jpeg, {len(JPEG)} bytes)."
    assert isinstance(image, ImageContent)
    assert image.mimeType == "image/jpeg"
    assert base64.b64decode(image.data) == JPEG
    assert result.structured_content == {"result": note.text}


@respx.mock
async def test_image_reaches_the_client_through_call_tool() -> None:
    respx.get(url__startswith=API).mock(return_value=_file(JPEG, "image/jpeg"))
    name, arguments = WHATSAPP_MEDIA

    result = await _call("call_tool", {"name": name, "arguments": arguments})

    assert isinstance(result.content[1], ImageContent)
    assert base64.b64decode(result.content[1].data) == JPEG


@pytest.mark.parametrize("tool", [EMAIL_ATTACHMENT, DRIVE_FILE, WHATSAPP_MEDIA])
@respx.mock
async def test_pdf_is_returned_as_its_text(tool) -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(PDF, "application/pdf", 'attachment; filename="invoice.pdf"')
    )

    text = _only_text(await _call(*tool))

    assert text == (
        f"Text of invoice.pdf (application/pdf, {len(PDF):,} bytes), 2 page(s):\n\n"
        "--- Page 1 ---\nInvoice INV-7731\nTotal due: 1,337.42 EUR\n\n"
        "--- Page 2 ---\nDue date: 2026-12-05"
    )


@respx.mock
async def test_pdf_text_over_the_result_cap_says_where_it_was_cut() -> None:
    line = "x" * 200
    pdf = _pdf(*[[f"Page marker {n}", *[line] * 30] for n in range(1, 21)])
    respx.get(url__startswith=API).mock(return_value=_file(pdf, "application/pdf"))

    text = _only_text(await _call(*EMAIL_ATTACHMENT))

    assert len(text) <= MAX_RESULT_CHARS
    assert "Page marker 1\n" in text
    assert "Page marker 20" not in text
    assert text.endswith("are not shown.]")
    assert (
        "[Text cut at 80,000 characters: page 14 is incomplete and pages 15-20" in text
    )


@respx.mock
async def test_pdf_without_text_says_it_is_probably_a_scan() -> None:
    respx.get(url__startswith=API).mock(return_value=_file(_pdf([]), "application/pdf"))

    text = _only_text(await _call(*EMAIL_ATTACHMENT))

    assert "no extractable text (it is probably a scan" in text


@respx.mock
async def test_damaged_pdf_is_described_not_an_error() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(b"%PDF-1.4\n\xff\xfe not really a pdf", "application/pdf")
    )

    result = await _call(*EMAIL_ATTACHMENT)

    assert not result.is_error
    assert "could not be extracted" in _only_text(result)


@respx.mock
async def test_pdf_over_the_parsing_limit_is_described() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(b"\x00" * (MAX_PDF_BYTES + 1), "application/pdf")
    )

    text = _only_text(await _call(*EMAIL_ATTACHMENT))

    assert "larger than the 20 MB whose text this tool extracts" in text


@respx.mock
async def test_voice_note_is_described_without_audio_content() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(OGG, "audio/ogg; codecs=opus")
    )

    text = _only_text(await _call(*WHATSAPP_MEDIA))

    assert text == (
        f"Downloaded the file (audio/ogg, {len(OGG)} bytes). Audio can't be passed "
        "to the model, and no transcript is available."
    )


@pytest.mark.parametrize(
    ("content_type", "size"),
    [("image/heic", 100), ("image/jpeg", MAX_IMAGE_BYTES + 1)],
)
@respx.mock
async def test_image_a_model_cannot_view_is_described(
    content_type: str, size: int
) -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(b"\xff" * size, content_type)
    )

    text = _only_text(await _call(*WHATSAPP_MEDIA))

    assert "too large or in a format the model can't view" in text


@respx.mock
async def test_other_files_are_described_and_never_embedded() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(
            b"PK\x03\x04" + b"\x00" * 64,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            'attachment; filename="report.xlsx"',
        )
    )

    text = _only_text(await _call(*DRIVE_FILE))

    assert text.startswith("Downloaded report.xlsx (application/vnd.openxml")
    assert text.endswith("only images, text and PDFs are.")


@respx.mock
async def test_csv_is_returned_as_text() -> None:
    csv = "phone_number,opted_out_at\n+34600000000,2026-11-01\n"
    respx.get(url__startswith=API).mock(
        return_value=_file(csv.encode(), "text/csv; charset=utf-8")
    )

    result = await _call("sms_list_sms_opt_outs", {"format": "csv"})

    assert _only_text(result) == csv


@respx.mock
async def test_text_over_the_result_cap_is_a_clear_error() -> None:
    respx.get(url__startswith=API).mock(
        return_value=_file(b"a" * (MAX_RESULT_CHARS + 1), "text/csv")
    )

    result = await _call(
        "sms_list_sms_opt_outs", {"format": "csv"}, raise_on_error=False
    )

    assert result.is_error
    assert "ask for JSON instead" in result.content[0].text
