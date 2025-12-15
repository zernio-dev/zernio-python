"""
Vercel Blob uploader - main entry point.

Uses the official Vercel SDK to upload files to Vercel Blob storage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from late.upload.config import UploadConfig
from late.upload.protocols import (
    FileTooLargeError,
    UploadError,
    UploadFile,
    UploadProgress,
    UploadResult,
)

from .client import VercelBlobClient

if TYPE_CHECKING:
    from collections.abc import Callable


class VercelBlobUploader:
    """
    Upload files to Vercel Blob storage.

    Uses the official Vercel SDK. Supports files up to 5GB.

    Requires a Vercel Blob read-write token (BLOB_READ_WRITE_TOKEN).
    Get one from: https://vercel.com/docs/storage/vercel-blob

    Example:
        >>> uploader = VercelBlobUploader(token="vercel_blob_rw_xxx")
        >>> result = uploader.upload(UploadFile(
        ...     filename="video.mp4",
        ...     content=Path("large_video.mp4"),
        ...     mime_type="video/mp4",
        ...     size=500_000_000
        ... ))
        >>> print(result.url)
    """

    def __init__(
        self,
        token: str,
        config: UploadConfig | None = None,
    ) -> None:
        """
        Initialize the Vercel Blob uploader.

        Args:
            token: Vercel Blob read-write token
            config: General upload configuration
        """
        self._config = config or UploadConfig.default()
        self._client = VercelBlobClient(token)

    @property
    def max_size(self) -> int:
        """Maximum supported file size (5GB)."""
        return self._config.limits.blob_max

    def supports_size(self, size: int) -> bool:
        """Check if this uploader supports files of the given size."""
        return size <= self.max_size

    def _validate(self, file: UploadFile) -> None:
        """Validate file before upload."""
        if file.size and file.size > self.max_size:
            raise FileTooLargeError(file.size, self.max_size)

    # -------------------------------------------------------------------------
    # Sync API
    # -------------------------------------------------------------------------

    def upload(
        self,
        file: UploadFile,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> UploadResult:
        """
        Upload a file to Vercel Blob.

        Args:
            file: File to upload
            on_progress: Optional progress callback

        Returns:
            UploadResult with blob URL and metadata

        Raises:
            FileTooLargeError: If file exceeds 5GB
            UploadError: On upload failure
        """
        self._validate(file)

        try:
            return self._client.upload(file, on_progress)
        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e

    def upload_multiple(
        self,
        files: list[UploadFile],
        on_progress: Callable[[int, UploadProgress], None] | None = None,
    ) -> list[UploadResult]:
        """
        Upload multiple files.

        Args:
            files: List of files to upload
            on_progress: Callback with (file_index, progress)

        Returns:
            List of UploadResults
        """
        results = []
        for idx, file in enumerate(files):
            cb = (lambda p, i=idx: on_progress(i, p)) if on_progress else None
            results.append(self.upload(file, cb))
        return results

    # -------------------------------------------------------------------------
    # Async API
    # -------------------------------------------------------------------------

    async def aupload(
        self,
        file: UploadFile,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> UploadResult:
        """Upload a file to Vercel Blob (async)."""
        self._validate(file)

        try:
            return await self._client.aupload(file, on_progress)
        except (FileTooLargeError, UploadError):
            raise
        except Exception as e:
            raise UploadError(str(e), cause=e) from e

    async def aupload_multiple(
        self,
        files: list[UploadFile],
        on_progress: Callable[[int, UploadProgress], None] | None = None,
    ) -> list[UploadResult]:
        """Upload multiple files (async)."""
        results = []
        for idx, file in enumerate(files):
            cb = (lambda p, i=idx: on_progress(i, p)) if on_progress else None
            results.append(await self.aupload(file, cb))
        return results
