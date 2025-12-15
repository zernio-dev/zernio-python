"""
Upload module for Late SDK.

Provides flexible file upload strategies:
- DirectUploader: For small files (< 4MB) via API multipart
- VercelBlobUploader: For large files (up to 5GB) via Vercel Blob SDK
- SmartUploader: Automatic strategy selection based on file size

Example (simple - small files):
    >>> from late import Late
    >>> client = Late(api_key="...")
    >>> result = client.media.upload("small_image.jpg")

Example (large files - requires Vercel Blob token):
    >>> result = client.media.upload_large(
    ...     "large_video.mp4",
    ...     vercel_token="vercel_blob_rw_xxx"
    ... )

Example (smart uploader with auto-selection):
    >>> from late.upload import SmartUploader, UploadFile
    >>> uploader = SmartUploader(client, vercel_token="vercel_blob_rw_xxx")
    >>> result = uploader.upload(file)  # Auto-selects strategy
"""

from .config import (
    ALLOWED_CONTENT_TYPES,
    ALLOWED_DOCUMENT_TYPES,
    ALLOWED_IMAGE_TYPES,
    ALLOWED_VIDEO_TYPES,
    UploadConfig,
    UploadEndpoints,
    UploadLimits,
    get_content_category,
    is_content_type_allowed,
)
from .direct import DirectUploader
from .protocols import (
    FileTooLargeError,
    UnsupportedContentTypeError,
    UploadError,
    UploadFile,
    UploadProgress,
    UploadResult,
)
from .smart import LargeFileError, SmartUploader
from .vercel import VercelBlobUploader

__all__ = [
    # Main uploaders
    "SmartUploader",
    "DirectUploader",
    "VercelBlobUploader",
    # Data types
    "UploadFile",
    "UploadResult",
    "UploadProgress",
    # Configuration
    "UploadConfig",
    "UploadLimits",
    "UploadEndpoints",
    # Content type helpers
    "ALLOWED_CONTENT_TYPES",
    "ALLOWED_IMAGE_TYPES",
    "ALLOWED_VIDEO_TYPES",
    "ALLOWED_DOCUMENT_TYPES",
    "is_content_type_allowed",
    "get_content_category",
    # Exceptions
    "UploadError",
    "FileTooLargeError",
    "LargeFileError",
    "UnsupportedContentTypeError",
]
