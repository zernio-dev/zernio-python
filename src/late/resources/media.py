"""
Media resource for uploading images and videos.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .base import BaseResource

if TYPE_CHECKING:
    from ..client.base import BaseClient


class MediaResource(BaseResource[Any]):
    """
    Resource for uploading media files.

    Supports uploading images, videos, and PDFs up to 5GB total.

    Example:
        >>> client = Late(api_key="...")
        >>> # Upload single file
        >>> result = client.media.upload("photo.jpg")
        >>> print(result["files"][0]["url"])
        >>>
        >>> # Upload multiple files
        >>> result = client.media.upload_multiple(["photo1.jpg", "video.mp4"])
        >>>
        >>> # Upload from bytes
        >>> result = client.media.upload_bytes(image_bytes, "image.png")
    """

    _BASE_PATH = "/v1/media"

    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def upload(self, file_path: str | Path) -> dict[str, Any]:
        """
        Upload a single media file.

        Args:
            file_path: Path to the file to upload

        Returns:
            Dict with 'files' array containing uploaded file info
        """
        path = Path(file_path)
        mime_type = self._get_mime_type(path)
        with open(path, "rb") as f:
            return self._client._post(
                self._BASE_PATH,
                files={"files": (path.name, f, mime_type)},
            )

    def upload_multiple(self, file_paths: list[str | Path]) -> dict[str, Any]:
        """
        Upload multiple media files at once.

        Args:
            file_paths: List of file paths to upload

        Returns:
            Dict with 'files' array containing all uploaded files
        """
        files_list = []
        file_handles = []

        try:
            for file_path in file_paths:
                path = Path(file_path)
                mime_type = self._get_mime_type(path)
                f = open(path, "rb")
                file_handles.append(f)
                files_list.append(("files", (path.name, f, mime_type)))

            return self._client._post(self._BASE_PATH, files=files_list)
        finally:
            for f in file_handles:
                f.close()

    def upload_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        mime_type: str | None = None,
    ) -> dict[str, Any]:
        """
        Upload media from bytes.

        Args:
            content: File content as bytes
            filename: Name for the file
            mime_type: Optional MIME type (auto-detected if not provided)

        Returns:
            Dict with 'files' array containing uploaded file info
        """
        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        return self._client._post(
            self._BASE_PATH,
            files={"files": (filename, content, mime_type)},
        )

    # -------------------------------------------------------------------------
    # Upload Token Flow (for Claude Desktop / MCP)
    # -------------------------------------------------------------------------

    def generate_upload_token(self) -> dict[str, Any]:
        """
        Generate an upload token for browser-based file uploads.

        This is useful when the client cannot directly upload files (e.g., AI assistants).
        The flow is:
        1. Call this method to get an upload URL
        2. User opens the URL in their browser and uploads files
        3. Call check_upload_token() to get the uploaded file URLs

        Returns:
            Dict with 'token', 'uploadUrl', 'expiresAt', 'status'
        """
        return self._client._post(self._path("upload-token"))

    def check_upload_token(self, token: str) -> dict[str, Any]:
        """
        Check the status of an upload token and get uploaded file URLs.

        Args:
            token: The upload token from generate_upload_token()

        Returns:
            Dict with 'token', 'status', 'files', 'createdAt', 'expiresAt', 'completedAt'
        """
        return self._client._get(self._path("upload-token"), params={"token": token})

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def aupload(self, file_path: str | Path) -> dict[str, Any]:
        """Upload a single media file asynchronously."""
        path = Path(file_path)
        mime_type = self._get_mime_type(path)
        with open(path, "rb") as f:
            content = f.read()
        return await self._client._apost(
            self._BASE_PATH,
            files={"files": (path.name, content, mime_type)},
        )

    async def aupload_multiple(self, file_paths: list[str | Path]) -> dict[str, Any]:
        """Upload multiple media files asynchronously."""
        files_list = []
        for file_path in file_paths:
            path = Path(file_path)
            mime_type = self._get_mime_type(path)
            with open(path, "rb") as f:
                content = f.read()
            files_list.append(("files", (path.name, content, mime_type)))

        return await self._client._apost(self._BASE_PATH, files=files_list)

    async def aupload_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        mime_type: str | None = None,
    ) -> dict[str, Any]:
        """Upload media from bytes asynchronously."""
        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        return await self._client._apost(
            self._BASE_PATH,
            files={"files": (filename, content, mime_type)},
        )

    async def agenerate_upload_token(self) -> dict[str, Any]:
        """Generate an upload token asynchronously."""
        return await self._client._apost(self._path("upload-token"))

    async def acheck_upload_token(self, token: str) -> dict[str, Any]:
        """Check the status of an upload token asynchronously."""
        return await self._client._aget(self._path("upload-token"), params={"token": token})
