"""
Smart uploader with automatic strategy selection.

Chooses the best upload method based on file size.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .config import UploadConfig
from .direct import DirectUploader
from .protocols import (
    FileTooLargeError,
    UploadError,
    UploadFile,
    UploadProgress,
    UploadResult,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from late.client.base import BaseClient


class LargeFileError(UploadError):
    """
    Raised when trying to upload a large file without Vercel Blob token.

    Provides clear guidance on how to upload large files.
    """

    def __init__(self, file_size: int, max_direct_size: int) -> None:
        message = (
            f"File size ({file_size:,} bytes) exceeds direct upload limit "
            f"({max_direct_size:,} bytes / {max_direct_size // (1024 * 1024)}MB).\n\n"
            "For files larger than 4MB, provide a Vercel Blob token:\n\n"
            "  from late.upload import SmartUploader\n\n"
            "  uploader = SmartUploader(client, vercel_token='vercel_blob_rw_xxx')\n"
            "  result = uploader.upload(file)\n\n"
            "Get your token at: https://vercel.com/docs/storage/vercel-blob"
        )
        super().__init__(message)
        self.file_size = file_size
        self.max_direct_size = max_direct_size


class SmartUploader:
    """
    Intelligent uploader that selects the best strategy automatically.

    - Files < 4MB: Uses direct multipart upload to API
    - Files >= 4MB: Uses Vercel Blob SDK (requires token)

    Example (small files only):
        >>> uploader = SmartUploader(client)
        >>> result = uploader.upload(small_file)

    Example (with Vercel token for large files):
        >>> uploader = SmartUploader(client, vercel_token="vercel_blob_rw_xxx")
        >>> result = uploader.upload(large_file)  # Auto-selects strategy
    """

    def __init__(
        self,
        client: BaseClient,
        *,
        vercel_token: str | None = None,
        config: UploadConfig | None = None,
    ) -> None:
        """
        Initialize the smart uploader.

        Args:
            client: The Late API client
            vercel_token: Optional Vercel Blob token for large files
            config: Upload configuration
        """
        self._client = client
        self._config = config or UploadConfig.default()
        self._direct = DirectUploader(client, self._config)
        self._vercel_token = vercel_token
        self._vercel_uploader = None

        # Initialize Vercel uploader if token provided
        if vercel_token:
            from .vercel import VercelBlobUploader

            self._vercel_uploader = VercelBlobUploader(vercel_token, self._config)

    @property
    def direct_max_size(self) -> int:
        """Maximum size for direct upload (4MB)."""
        return self._config.limits.direct_max

    @property
    def blob_max_size(self) -> int:
        """Maximum size for Vercel Blob upload (5GB)."""
        return self._config.limits.blob_max

    @property
    def has_vercel_token(self) -> bool:
        """Check if Vercel Blob token is configured."""
        return self._vercel_uploader is not None

    def _select_strategy(self, file: UploadFile) -> str:
        """
        Select the appropriate upload strategy.

        Returns:
            "direct" or "vercel"

        Raises:
            LargeFileError: If file > 4MB and no Vercel token
            FileTooLargeError: If file exceeds all limits
        """
        size = file.size or 0

        # Check absolute maximum
        if size > self.blob_max_size:
            raise FileTooLargeError(size, self.blob_max_size)

        # Small file - use direct upload
        if size <= self.direct_max_size:
            return "direct"

        # Large file - need Vercel token
        if not self.has_vercel_token:
            raise LargeFileError(size, self.direct_max_size)

        return "vercel"

    # -------------------------------------------------------------------------
    # Sync API
    # -------------------------------------------------------------------------

    def upload(
        self,
        file: UploadFile,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> UploadResult:
        """
        Upload a file using the best available strategy.

        Args:
            file: File to upload
            on_progress: Progress callback (Vercel only)

        Returns:
            UploadResult with file URL

        Raises:
            LargeFileError: If file > 4MB and no Vercel token
            FileTooLargeError: If file > 5GB
            UploadError: On upload failure
        """
        strategy = self._select_strategy(file)

        if strategy == "direct":
            return self._direct.upload(file)
        else:
            return self._vercel_uploader.upload(file, on_progress)  # type: ignore

    def upload_multiple(
        self,
        files: list[UploadFile],
        on_progress: Callable[[int, UploadProgress], None] | None = None,
    ) -> list[UploadResult]:
        """Upload multiple files."""
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
        """Upload a file (async)."""
        strategy = self._select_strategy(file)

        if strategy == "direct":
            return await self._direct.aupload(file)
        else:
            return await self._vercel_uploader.aupload(file, on_progress)  # type: ignore

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
