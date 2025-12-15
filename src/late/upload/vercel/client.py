"""
Vercel Blob client using official Vercel SDK.

Wraps the official `vercel.blob` SDK for uploading large files.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from late.upload.protocols import UploadError, UploadFile, UploadProgress, UploadResult
from late.upload.utils import read_file_content

if TYPE_CHECKING:
    from collections.abc import Callable


class VercelBlobClient:
    """
    Client for Vercel Blob using the official SDK.

    Requires a Vercel Blob read-write token (BLOB_READ_WRITE_TOKEN).
    Get one from: https://vercel.com/docs/storage/vercel-blob

    Example:
        >>> client = VercelBlobClient(token="vercel_blob_rw_xxx")
        >>> result = client.upload(file)
    """

    def __init__(self, token: str) -> None:
        """
        Initialize the Vercel Blob client.

        Args:
            token: Vercel Blob read-write token
        """
        if not token:
            raise ValueError(
                "Vercel Blob token required. "
                "Get one at: https://vercel.com/docs/storage/vercel-blob"
            )
        self._token = token

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
            UploadResult with blob URL
        """
        from vercel.blob import BlobClient, UploadProgressEvent

        content = read_file_content(file)
        total_size = len(content)

        # Create progress wrapper
        progress_cb = None
        if on_progress:

            def progress_cb(event: UploadProgressEvent) -> None:
                on_progress(
                    UploadProgress(
                        uploaded_bytes=event.loaded,
                        total_bytes=event.total,
                        part_number=None,
                        total_parts=None,
                    )
                )

        try:
            client = BlobClient(token=self._token)
            result = client.put(
                file.filename,
                content,
                access="public",
                content_type=file.mime_type,
                add_random_suffix=True,
                multipart=total_size > 100 * 1024 * 1024,  # Use multipart for > 100MB
                on_upload_progress=progress_cb,
            )

            return UploadResult(
                url=result.url,
                pathname=result.pathname,
                content_type=result.content_type,
                size=total_size,
                download_url=result.download_url,
                metadata={"provider": "vercel-blob"},
            )

        except Exception as e:
            raise UploadError(f"Vercel Blob upload failed: {e}") from e

    async def aupload(
        self,
        file: UploadFile,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> UploadResult:
        """
        Upload a file to Vercel Blob asynchronously.

        Args:
            file: File to upload
            on_progress: Optional progress callback

        Returns:
            UploadResult with blob URL
        """
        from vercel.blob import AsyncBlobClient, UploadProgressEvent

        content = read_file_content(file)
        total_size = len(content)

        # Create progress wrapper
        progress_cb = None
        if on_progress:

            def progress_cb(event: UploadProgressEvent) -> None:
                on_progress(
                    UploadProgress(
                        uploaded_bytes=event.loaded,
                        total_bytes=event.total,
                        part_number=None,
                        total_parts=None,
                    )
                )

        try:
            client = AsyncBlobClient(token=self._token)
            result = await client.put(
                file.filename,
                content,
                access="public",
                content_type=file.mime_type,
                add_random_suffix=True,
                multipart=total_size > 100 * 1024 * 1024,
                on_upload_progress=progress_cb,
            )

            return UploadResult(
                url=result.url,
                pathname=result.pathname,
                content_type=result.content_type,
                size=total_size,
                download_url=result.download_url,
                metadata={"provider": "vercel-blob"},
            )

        except Exception as e:
            raise UploadError(f"Vercel Blob upload failed: {e}") from e
