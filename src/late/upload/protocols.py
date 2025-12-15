"""
Upload protocols and interfaces for extensible file upload strategies.

This module defines the contracts that all uploaders must follow,
enabling easy extension with new upload strategies (S3, GCS, etc.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class UploadFile:
    """
    Represents a file to be uploaded.

    Attributes:
        filename: Name of the file (used in Content-Disposition)
        content: File content as bytes, file handle, or path
        mime_type: MIME type of the file
        size: Size in bytes (optional, calculated if not provided)
    """

    filename: str
    content: bytes | BinaryIO | Path
    mime_type: str
    size: int | None = None

    def __post_init__(self) -> None:
        """Calculate size if not provided."""
        if self.size is None:
            if isinstance(self.content, bytes):
                self.size = len(self.content)
            elif isinstance(self.content, Path):
                self.size = self.content.stat().st_size


@dataclass
class UploadResult:
    """
    Result of a successful file upload.

    Attributes:
        url: Public URL of the uploaded file
        pathname: Path/key in the storage system
        content_type: MIME type of the uploaded file
        size: Size in bytes
        download_url: Direct download URL (may differ from url)
        metadata: Additional metadata from the storage provider
    """

    url: str
    pathname: str
    content_type: str
    size: int
    download_url: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class UploadProgress:
    """
    Progress information for chunked/multipart uploads.

    Attributes:
        uploaded_bytes: Bytes uploaded so far
        total_bytes: Total bytes to upload
        part_number: Current part number (for multipart)
        total_parts: Total number of parts
    """

    uploaded_bytes: int
    total_bytes: int
    part_number: int | None = None
    total_parts: int | None = None

    @property
    def percentage(self) -> float:
        """Calculate upload percentage."""
        if self.total_bytes == 0:
            return 100.0
        return (self.uploaded_bytes / self.total_bytes) * 100


@runtime_checkable
class Uploader(Protocol):
    """
    Protocol for synchronous file uploaders.

    Implement this protocol to create custom upload strategies.
    """

    def upload(self, file: UploadFile) -> UploadResult:
        """
        Upload a single file.

        Args:
            file: The file to upload

        Returns:
            UploadResult with the uploaded file information
        """
        ...

    def upload_multiple(self, files: list[UploadFile]) -> list[UploadResult]:
        """
        Upload multiple files.

        Args:
            files: List of files to upload

        Returns:
            List of UploadResults for each file
        """
        ...

    def supports_size(self, size: int) -> bool:
        """
        Check if this uploader supports files of the given size.

        Args:
            size: File size in bytes

        Returns:
            True if this uploader can handle files of this size
        """
        ...


@runtime_checkable
class AsyncUploader(Protocol):
    """
    Protocol for asynchronous file uploaders.

    Implement this protocol for async upload strategies.
    """

    async def aupload(self, file: UploadFile) -> UploadResult:
        """Upload a single file asynchronously."""
        ...

    async def aupload_multiple(self, files: list[UploadFile]) -> list[UploadResult]:
        """Upload multiple files asynchronously."""
        ...

    def supports_size(self, size: int) -> bool:
        """Check if this uploader supports files of the given size."""
        ...


@runtime_checkable
class ProgressUploader(Protocol):
    """
    Protocol for uploaders that support progress tracking.

    Extend Uploader with progress callback support.
    """

    def upload_with_progress(
        self,
        file: UploadFile,
        on_progress: Callable[[UploadProgress], None] | None = None,
    ) -> UploadResult:
        """
        Upload a file with progress tracking.

        Args:
            file: The file to upload
            on_progress: Callback called with progress updates

        Returns:
            UploadResult with the uploaded file information
        """
        ...


@runtime_checkable
class ChunkedUploader(Protocol):
    """
    Protocol for uploaders that support chunked/resumable uploads.

    Useful for very large files where upload might be interrupted.
    """

    def start_chunked_upload(self, file: UploadFile) -> str:
        """
        Initialize a chunked upload session.

        Args:
            file: The file to upload (metadata only at this stage)

        Returns:
            Upload session ID for continuing the upload
        """
        ...

    def upload_chunk(
        self,
        session_id: str,
        chunk: bytes,
        part_number: int,
    ) -> bool:
        """
        Upload a single chunk.

        Args:
            session_id: Upload session ID from start_chunked_upload
            chunk: Chunk data
            part_number: Part number (1-indexed)

        Returns:
            True if chunk was uploaded successfully
        """
        ...

    def complete_chunked_upload(self, session_id: str) -> UploadResult:
        """
        Complete a chunked upload.

        Args:
            session_id: Upload session ID

        Returns:
            UploadResult with the final uploaded file information
        """
        ...

    def abort_chunked_upload(self, session_id: str) -> bool:
        """
        Abort a chunked upload and clean up.

        Args:
            session_id: Upload session ID

        Returns:
            True if abort was successful
        """
        ...


class UploadError(Exception):
    """Base exception for upload errors."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class FileTooLargeError(UploadError):
    """Raised when file exceeds maximum allowed size."""

    def __init__(self, size: int, max_size: int) -> None:
        super().__init__(f"File size {size:,} bytes exceeds maximum {max_size:,} bytes")
        self.size = size
        self.max_size = max_size


class UnsupportedContentTypeError(UploadError):
    """Raised when file type is not supported."""

    def __init__(self, content_type: str, supported: list[str]) -> None:
        super().__init__(
            f"Content type '{content_type}' not supported. "
            f"Supported types: {', '.join(supported)}"
        )
        self.content_type = content_type
        self.supported = supported
