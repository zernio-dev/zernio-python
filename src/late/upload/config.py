"""
Configuration for upload module.

Centralized configuration with sensible defaults and easy customization.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from late.enums import MediaType


@dataclass(frozen=True)
class UploadLimits:
    """
    Size limits for different upload methods.

    All values are in bytes. Use the helper class methods for
    convenient size specifications.

    Example:
        >>> limits = UploadLimits.default()
        >>> custom = UploadLimits(direct_max=UploadLimits.mb(10))
    """

    direct_max: int = 4 * 1024 * 1024  # 4MB - server body limit
    blob_max: int = 5 * 1024 * 1024 * 1024  # 5GB - Vercel Blob limit
    multipart_threshold: int = 100 * 1024 * 1024  # 100MB - use chunked above this
    chunk_size: int = 5 * 1024 * 1024  # 5MB - chunk size for multipart

    @classmethod
    def kb(cls, n: int) -> int:
        """Convert kilobytes to bytes."""
        return n * 1024

    @classmethod
    def mb(cls, n: int) -> int:
        """Convert megabytes to bytes."""
        return n * 1024 * 1024

    @classmethod
    def gb(cls, n: int) -> int:
        """Convert gigabytes to bytes."""
        return n * 1024 * 1024 * 1024

    @classmethod
    def default(cls) -> UploadLimits:
        """Create default limits configuration."""
        return cls()


@dataclass(frozen=True)
class UploadEndpoints:
    """
    API endpoints for upload operations.

    Example:
        >>> endpoints = UploadEndpoints.default()
        >>> custom = UploadEndpoints(media="/api/v2/media")
    """

    media: str = "/v1/media"
    client_upload: str = "/v1/media"  # Same endpoint, different flow

    @classmethod
    def default(cls) -> UploadEndpoints:
        """Create default endpoints configuration."""
        return cls()


@dataclass(frozen=True)
class UploadConfig:
    """
    Complete upload configuration.

    Combines limits and endpoints into a single configuration object.
    Immutable by design to prevent accidental modifications.

    Example:
        >>> config = UploadConfig.default()
        >>> # Custom configuration
        >>> config = UploadConfig(
        ...     limits=UploadLimits(direct_max=UploadLimits.mb(8)),
        ...     endpoints=UploadEndpoints(media="/api/v2/media"),
        ... )
    """

    limits: UploadLimits = field(default_factory=UploadLimits.default)
    endpoints: UploadEndpoints = field(default_factory=UploadEndpoints.default)
    auto_select_strategy: bool = True  # Automatically choose uploader based on size
    verify_upload: bool = True  # Verify upload completed successfully

    @classmethod
    def default(cls) -> UploadConfig:
        """Create default configuration."""
        return cls()


# Supported content types for uploads
ALLOWED_IMAGE_TYPES: frozenset[str] = frozenset(
    {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
        "image/gif",
    }
)

ALLOWED_VIDEO_TYPES: frozenset[str] = frozenset(
    {
        "video/mp4",
        "video/mpeg",
        "video/quicktime",
        "video/avi",
        "video/x-msvideo",
        "video/webm",
        "video/x-m4v",
    }
)

ALLOWED_DOCUMENT_TYPES: frozenset[str] = frozenset(
    {
        "application/pdf",
    }
)

ALLOWED_CONTENT_TYPES: frozenset[str] = (
    ALLOWED_IMAGE_TYPES | ALLOWED_VIDEO_TYPES | ALLOWED_DOCUMENT_TYPES
)


def is_content_type_allowed(content_type: str) -> bool:
    """Check if a content type is allowed for upload."""
    return content_type.lower() in ALLOWED_CONTENT_TYPES


def get_content_category(content_type: str) -> MediaType | None:
    """
    Get the category of a content type.

    Returns:
        MediaType.IMAGE, MediaType.VIDEO, MediaType.DOCUMENT, or None if not allowed
    """
    content_type = content_type.lower()
    if content_type in ALLOWED_IMAGE_TYPES:
        return MediaType.IMAGE
    if content_type in ALLOWED_VIDEO_TYPES:
        return MediaType.VIDEO
    if content_type in ALLOWED_DOCUMENT_TYPES:
        return MediaType.DOCUMENT
    return None
