"""
Raw file bodies the API returns instead of JSON (media, attachments, receipts).
"""

from __future__ import annotations

from email.message import Message
from email.utils import collapse_rfc2231_value
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx


class BinaryResponse(dict[str, Any]):
    """
    A non-JSON response body: its bytes, content type and filename.

    It is a dict (keys ``content``, ``content_type``, ``filename`` and ``url``)
    so it fits the ``dict[str, Any]`` every resource method returns; the
    attributes read the same keys.
    """

    def __init__(
        self,
        content: bytes,
        content_type: str,
        filename: str | None = None,
        url: str | None = None,
    ) -> None:
        super().__init__(
            content=content, content_type=content_type, filename=filename, url=url
        )

    @classmethod
    def from_response(cls, response: httpx.Response) -> BinaryResponse:
        return cls(
            content=response.content,
            content_type=response.headers.get(
                "content-type", "application/octet-stream"
            ),
            filename=_filename(response.headers.get("content-disposition")),
            url=_request_url(response),
        )

    @property
    def content(self) -> bytes:
        return self["content"]  # type: ignore[no-any-return]

    @property
    def content_type(self) -> str:
        """The Content-Type header as sent, parameters included."""
        return self["content_type"]  # type: ignore[no-any-return]

    @property
    def mime_type(self) -> str:
        """The bare media type, e.g. ``audio/ogg`` for ``audio/ogg; codecs=opus``."""
        return self.content_type.split(";", 1)[0].strip().lower()

    @property
    def charset(self) -> str | None:
        message = Message()
        message["content-type"] = self.content_type
        return message.get_content_charset()

    @property
    def filename(self) -> str | None:
        """The filename from Content-Disposition, if the API sent one."""
        return self["filename"]  # type: ignore[no-any-return]

    @property
    def url(self) -> str | None:
        return self["url"]  # type: ignore[no-any-return]


def is_json_content_type(content_type: str | None) -> bool:
    """Whether a body with this Content-Type is parsed as JSON.

    A missing header counts as JSON, as every response was parsed before.
    """
    if content_type is None:
        return True
    mime_type = content_type.split(";", 1)[0].strip().lower()
    return mime_type == "application/json" or mime_type.endswith("+json")


def _request_url(response: httpx.Response) -> str | None:
    try:
        return str(response.request.url)
    except RuntimeError:  # a Response built without a request
        return None


def _filename(content_disposition: str | None) -> str | None:
    if not content_disposition:
        return None
    message = Message()
    message["content-disposition"] = content_disposition
    params = message.get_params(header="content-disposition") or []
    filenames = [value for key, value in params if key == "filename"]
    # RFC 6266: the RFC 5987 form (filename*=UTF-8''...), parsed as a tuple,
    # wins over the plain ASCII fallback whatever their order.
    encoded = [value for value in filenames if isinstance(value, tuple)]
    chosen = encoded or filenames
    return collapse_rfc2231_value(chosen[0]) if chosen else None
