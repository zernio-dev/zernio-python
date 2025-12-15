"""
Media resource for uploading images and videos.

Supports two upload methods:
- Direct upload: For small files (< 4MB) via API multipart
- Vercel Blob: For large files (up to 5GB) - requires Vercel token
"""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import TYPE_CHECKING

from late.models import (
    MediaLargeUploadResponse,
    MediaUploadResponse,
    UploadTokenResponse,
    UploadTokenStatusResponse,
)

from .base import BaseResource

if TYPE_CHECKING:
    from collections.abc import Callable

    from late.upload import UploadProgress


# Size limit for direct upload (4MB)
DIRECT_UPLOAD_MAX_SIZE = 4 * 1024 * 1024


class MediaResource(BaseResource[MediaUploadResponse]):
    """
    Resource for uploading media files.

    Supports uploading images, videos, and PDFs.

    For small files (< 4MB):
        >>> result = client.media.upload("photo.jpg")
        >>> print(result["files"][0]["url"])

    For large files (4MB - 5GB), use upload_large with Vercel token:
        >>> result = client.media.upload_large(
        ...     "large_video.mp4",
        ...     vercel_token="vercel_blob_rw_xxx"
        ... )
    """

    _BASE_PATH = "/v1/media"

    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"

    def _check_file_size(self, file_path: Path) -> int:
        """Get file size and validate for direct upload."""
        size = file_path.stat().st_size
        if size > DIRECT_UPLOAD_MAX_SIZE:
            from late.upload import LargeFileError

            raise LargeFileError(size, DIRECT_UPLOAD_MAX_SIZE)
        return size

    # -------------------------------------------------------------------------
    # Direct upload (small files < 4MB)
    # -------------------------------------------------------------------------

    def upload(self, file_path: str | Path) -> MediaUploadResponse:
        """
        Upload a single media file (direct upload, max 4MB).

        For files larger than 4MB, use upload_large() with a Vercel token.

        Args:
            file_path: Path to the file to upload

        Returns:
            MediaUploadResponse with 'files' attribute

        Raises:
            LargeFileError: If file exceeds 4MB (use upload_large instead)
        """
        path = Path(file_path)
        self._check_file_size(path)

        mime_type = self._get_mime_type(path)
        with path.open("rb") as f:
            data = self._client._post(
                self._BASE_PATH,
                files={"files": (path.name, f, mime_type)},
            )
        return MediaUploadResponse.model_validate(data)

    def upload_multiple(self, file_paths: list[str | Path]) -> MediaUploadResponse:
        """
        Upload multiple media files at once (direct upload, each < 4MB).

        Args:
            file_paths: List of file paths to upload

        Returns:
            MediaUploadResponse with 'files' attribute

        Raises:
            LargeFileError: If any file exceeds 4MB
        """
        files_list = []
        file_handles = []

        try:
            for file_path in file_paths:
                path = Path(file_path)
                self._check_file_size(path)
                mime_type = self._get_mime_type(path)
                f = path.open("rb")
                file_handles.append(f)
                files_list.append(("files", (path.name, f, mime_type)))

            data = self._client._post(self._BASE_PATH, files=files_list)
            return MediaUploadResponse.model_validate(data)
        finally:
            for f in file_handles:
                f.close()

    def upload_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        mime_type: str | None = None,
    ) -> MediaUploadResponse:
        """
        Upload media from bytes (direct upload, max 4MB).

        Args:
            content: File content as bytes
            filename: Name for the file
            mime_type: Optional MIME type (auto-detected if not provided)

        Returns:
            MediaUploadResponse with 'files' attribute

        Raises:
            LargeFileError: If content exceeds 4MB
        """
        if len(content) > DIRECT_UPLOAD_MAX_SIZE:
            from late.upload import LargeFileError

            raise LargeFileError(len(content), DIRECT_UPLOAD_MAX_SIZE)

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        data = self._client._post(
            self._BASE_PATH,
            files={"files": (filename, content, mime_type)},
        )
        return MediaUploadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Large file upload (Vercel Blob - up to 5GB)
    # -------------------------------------------------------------------------

    def upload_large(
        self,
        file_path: str | Path,
        *,
        vercel_token: str,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> MediaLargeUploadResponse:
        """
        Upload a large file using Vercel Blob (up to 5GB).

        Requires a Vercel Blob read-write token.

        Args:
            file_path: Path to the file to upload
            vercel_token: Vercel Blob token (vercel_blob_rw_xxx)
                         Get one at: https://vercel.com/docs/storage/vercel-blob
            on_progress: Optional callback for progress updates

        Returns:
            MediaLargeUploadResponse with 'url', 'pathname', 'contentType', 'size' attributes

        Example:
            >>> result = client.media.upload_large(
            ...     "video.mp4",
            ...     vercel_token="vercel_blob_rw_xxx",
            ...     on_progress=lambda p: print(f"{p.percentage:.1f}%")
            ... )
            >>> print(result.url)
        """
        from late.upload import UploadFile, VercelBlobUploader

        path = Path(file_path)
        mime_type = self._get_mime_type(path)

        uploader = VercelBlobUploader(vercel_token)
        result = uploader.upload(
            UploadFile(
                filename=path.name,
                content=path,
                mime_type=mime_type,
                size=path.stat().st_size,
            ),
            on_progress=on_progress,
        )

        return MediaLargeUploadResponse(
            url=result.url,
            pathname=result.pathname,
            contentType=result.content_type,
            size=result.size,
            downloadUrl=result.download_url,
        )

    def upload_large_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        vercel_token: str,
        mime_type: str | None = None,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> MediaLargeUploadResponse:
        """
        Upload large content from bytes using Vercel Blob.

        Args:
            content: File content as bytes
            filename: Name for the file
            vercel_token: Vercel Blob token
            mime_type: Optional MIME type
            on_progress: Optional progress callback

        Returns:
            MediaLargeUploadResponse with 'url', 'pathname', 'contentType', 'size' attributes
        """
        from late.upload import UploadFile, VercelBlobUploader

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        uploader = VercelBlobUploader(vercel_token)
        result = uploader.upload(
            UploadFile(
                filename=filename,
                content=content,
                mime_type=mime_type,
                size=len(content),
            ),
            on_progress=on_progress,
        )

        return MediaLargeUploadResponse(
            url=result.url,
            pathname=result.pathname,
            contentType=result.content_type,
            size=result.size,
            downloadUrl=result.download_url,
        )

    # -------------------------------------------------------------------------
    # Upload Token Flow (for Claude Desktop / MCP)
    # -------------------------------------------------------------------------

    def generate_upload_token(self) -> UploadTokenResponse:
        """
        Generate an upload token for browser-based file uploads.

        This is useful when the client cannot directly upload files (e.g., AI assistants).
        The flow is:
        1. Call this method to get an upload URL
        2. User opens the URL in their browser and uploads files
        3. Call check_upload_token() to get the uploaded file URLs

        Returns:
            UploadTokenResponse with 'token', 'uploadUrl', 'expiresAt', 'status' attributes
        """
        data = self._client._post(self._path("upload-token"))
        return UploadTokenResponse.model_validate(data)

    def check_upload_token(self, token: str) -> UploadTokenStatusResponse:
        """
        Check the status of an upload token and get uploaded file URLs.

        Args:
            token: The upload token from generate_upload_token()

        Returns:
            UploadTokenStatusResponse with 'token', 'status', 'files', 'createdAt', 'expiresAt', 'completedAt' attributes
        """
        data = self._client._get(self._path("upload-token"), params={"token": token})
        return UploadTokenStatusResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods - Direct upload
    # -------------------------------------------------------------------------

    async def aupload(self, file_path: str | Path) -> MediaUploadResponse:
        """Upload a single media file asynchronously (max 4MB)."""
        path = Path(file_path)
        self._check_file_size(path)

        mime_type = self._get_mime_type(path)
        with path.open("rb") as f:
            content = f.read()
        data = await self._client._apost(
            self._BASE_PATH,
            files={"files": (path.name, content, mime_type)},
        )
        return MediaUploadResponse.model_validate(data)

    async def aupload_multiple(
        self, file_paths: list[str | Path]
    ) -> MediaUploadResponse:
        """Upload multiple media files asynchronously (each < 4MB)."""
        files_list = []
        for file_path in file_paths:
            path = Path(file_path)
            self._check_file_size(path)
            mime_type = self._get_mime_type(path)
            with path.open("rb") as f:
                content = f.read()
            files_list.append(("files", (path.name, content, mime_type)))

        data = await self._client._apost(self._BASE_PATH, files=files_list)
        return MediaUploadResponse.model_validate(data)

    async def aupload_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        mime_type: str | None = None,
    ) -> MediaUploadResponse:
        """Upload media from bytes asynchronously (max 4MB)."""
        if len(content) > DIRECT_UPLOAD_MAX_SIZE:
            from late.upload import LargeFileError

            raise LargeFileError(len(content), DIRECT_UPLOAD_MAX_SIZE)

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        data = await self._client._apost(
            self._BASE_PATH,
            files={"files": (filename, content, mime_type)},
        )
        return MediaUploadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods - Large file upload
    # -------------------------------------------------------------------------

    async def aupload_large(
        self,
        file_path: str | Path,
        *,
        vercel_token: str,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> MediaLargeUploadResponse:
        """Upload a large file asynchronously using Vercel Blob."""
        from late.upload import UploadFile, VercelBlobUploader

        path = Path(file_path)
        mime_type = self._get_mime_type(path)

        uploader = VercelBlobUploader(vercel_token)
        result = await uploader.aupload(
            UploadFile(
                filename=path.name,
                content=path,
                mime_type=mime_type,
                size=path.stat().st_size,
            ),
            on_progress=on_progress,
        )

        return MediaLargeUploadResponse(
            url=result.url,
            pathname=result.pathname,
            contentType=result.content_type,
            size=result.size,
            downloadUrl=result.download_url,
        )

    async def aupload_large_bytes(
        self,
        content: bytes,
        filename: str,
        *,
        vercel_token: str,
        mime_type: str | None = None,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> MediaLargeUploadResponse:
        """Upload large content from bytes asynchronously."""
        from late.upload import UploadFile, VercelBlobUploader

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

        uploader = VercelBlobUploader(vercel_token)
        result = await uploader.aupload(
            UploadFile(
                filename=filename,
                content=content,
                mime_type=mime_type,
                size=len(content),
            ),
            on_progress=on_progress,
        )

        return MediaLargeUploadResponse(
            url=result.url,
            pathname=result.pathname,
            contentType=result.content_type,
            size=result.size,
            downloadUrl=result.download_url,
        )

    # -------------------------------------------------------------------------
    # Async methods - Upload Token Flow
    # -------------------------------------------------------------------------

    async def agenerate_upload_token(self) -> UploadTokenResponse:
        """Generate an upload token asynchronously."""
        data = await self._client._apost(self._path("upload-token"))
        return UploadTokenResponse.model_validate(data)

    async def acheck_upload_token(self, token: str) -> UploadTokenStatusResponse:
        """Check the status of an upload token asynchronously."""
        data = await self._client._aget(
            self._path("upload-token"), params={"token": token}
        )
        return UploadTokenStatusResponse.model_validate(data)
