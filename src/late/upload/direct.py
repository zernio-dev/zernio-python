"""
Direct upload strategy for small files.

This uploader sends files directly to the API endpoint via multipart/form-data.
Suitable for small files that don't exceed server body size limits (~4MB).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from .config import UploadConfig
from .protocols import (
    FileTooLargeError,
    UploadError,
    UploadFile,
    UploadResult,
)

if TYPE_CHECKING:
    from late.client.base import BaseClient


class DirectUploader:
    """
    Direct multipart upload for small files.

    Uploads files directly to the API endpoint using multipart/form-data.
    Best for files under ~4MB to avoid 413 (Request Entity Too Large) errors.

    Example:
        >>> uploader = DirectUploader(client)
        >>> result = uploader.upload(UploadFile(
        ...     filename="image.jpg",
        ...     content=image_bytes,
        ...     mime_type="image/jpeg"
        ... ))
        >>> print(result.url)
    """

    def __init__(
        self,
        client: BaseClient,
        config: UploadConfig | None = None,
    ) -> None:
        """
        Initialize the direct uploader.

        Args:
            client: The HTTP client for making requests
            config: Upload configuration (uses defaults if not provided)
        """
        self._client = client
        self._config = config or UploadConfig.default()

    @property
    def max_size(self) -> int:
        """Maximum supported file size in bytes."""
        return self._config.limits.direct_max

    @property
    def endpoint(self) -> str:
        """API endpoint for uploads."""
        return self._config.endpoints.media

    def supports_size(self, size: int) -> bool:
        """Check if this uploader supports files of the given size."""
        return size <= self.max_size

    def _read_content(self, file: UploadFile) -> bytes:
        """
        Read content bytes from an UploadFile.

        Handles bytes, Path, and file handle content types.
        """
        content = file.content
        if isinstance(content, bytes):
            return content
        if isinstance(content, Path):
            return content.read_bytes()
        # File handle - read and return to start if seekable
        data = content.read()
        if hasattr(content, "seek"):
            content.seek(0)
        return data

    def _build_multipart_files(
        self, files: list[UploadFile]
    ) -> list[tuple[str, tuple[str, bytes, str]]]:
        """Build multipart files list for httpx."""
        return [
            ("files", (f.filename, self._read_content(f), f.mime_type)) for f in files
        ]

    def _parse_response(self, response: dict[str, Any]) -> list[UploadResult]:
        """Parse API response into UploadResult objects."""
        files_data = response.get("files", [])
        return [
            UploadResult(
                url=f["url"],
                pathname=f.get("pathname", ""),
                content_type=f.get("contentType", ""),
                size=f.get("size", 0),
                download_url=f.get("downloadUrl"),
            )
            for f in files_data
        ]

    def _validate_file(self, file: UploadFile) -> None:
        """Validate file before upload."""
        if file.size and file.size > self.max_size:
            raise FileTooLargeError(file.size, self.max_size)

    # -------------------------------------------------------------------------
    # Sync API
    # -------------------------------------------------------------------------

    def upload(self, file: UploadFile) -> UploadResult:
        """
        Upload a single file.

        Args:
            file: The file to upload

        Returns:
            UploadResult with the uploaded file information

        Raises:
            FileTooLargeError: If file exceeds max_size
            UploadError: On upload failure
        """
        self._validate_file(file)

        try:
            multipart = self._build_multipart_files([file])
            response = self._client._post(self.endpoint, files=multipart)
            results = self._parse_response(response)

            if not results:
                raise UploadError("Server returned no files in response")

            return results[0]

        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e

    def upload_multiple(self, files: list[UploadFile]) -> list[UploadResult]:
        """
        Upload multiple files in a single request.

        Args:
            files: List of files to upload

        Returns:
            List of UploadResults for each file

        Raises:
            FileTooLargeError: If any file exceeds max_size
            UploadError: On upload failure
        """
        for file in files:
            self._validate_file(file)

        try:
            multipart = self._build_multipart_files(files)
            response = self._client._post(self.endpoint, files=multipart)
            return self._parse_response(response)

        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e

    # -------------------------------------------------------------------------
    # Async API
    # -------------------------------------------------------------------------

    async def aupload(self, file: UploadFile) -> UploadResult:
        """Upload a single file asynchronously."""
        self._validate_file(file)

        try:
            multipart = self._build_multipart_files([file])
            response = await self._client._apost(self.endpoint, files=multipart)
            results = self._parse_response(response)

            if not results:
                raise UploadError("Server returned no files in response")

            return results[0]

        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e

    async def aupload_multiple(self, files: list[UploadFile]) -> list[UploadResult]:
        """Upload multiple files asynchronously."""
        for file in files:
            self._validate_file(file)

        try:
            multipart = self._build_multipart_files(files)
            response = await self._client._apost(self.endpoint, files=multipart)
            return self._parse_response(response)

        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e
