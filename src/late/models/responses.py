"""
SDK-specific response models.

These models are NOT generated from OpenAPI and are specific to the SDK implementation.
For API response models, see the generated models in _generated/models.py.
"""

from __future__ import annotations

from pydantic import BaseModel


class MediaLargeUploadResponse(BaseModel):
    """
    Response from media.upload_large() - Vercel Blob upload.

    This is SDK-specific and not from the API, as large file uploads
    go directly to Vercel Blob storage.
    """

    url: str
    pathname: str
    contentType: str
    size: int
    downloadUrl: str
