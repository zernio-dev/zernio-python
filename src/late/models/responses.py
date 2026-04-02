"""
SDK-specific response models.

These models are NOT generated from OpenAPI and are specific to the SDK implementation.
For API response models, see the generated models in _generated/models.py.
"""

from __future__ import annotations

from enum import Enum

from pydantic import AnyUrl, BaseModel

# ---------------------------------------------------------------------------
# Tools endpoint models (endpoints removed from OpenAPI spec but still
# functional for existing customers)
# ---------------------------------------------------------------------------


class DownloadFormat(BaseModel):
    formatId: str | None = None
    ext: str | None = None
    resolution: str | None = None
    filesize: int | None = None
    quality: str | None = None


class DownloadResponse(BaseModel):
    url: AnyUrl | None = None
    title: str | None = None
    thumbnail: AnyUrl | None = None
    duration: int | None = None
    formats: list[DownloadFormat] | None = None


class TranscriptSegment(BaseModel):
    text: str | None = None
    start: float | None = None
    duration: float | None = None


class TranscriptResponse(BaseModel):
    transcript: str | None = None
    segments: list[TranscriptSegment] | None = None
    language: str | None = None


class HashtagStatus(str, Enum):
    SAFE = "safe"
    BANNED = "banned"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"


class HashtagInfo(BaseModel):
    hashtag: str | None = None
    status: HashtagStatus | None = None
    postCount: int | None = None


class HashtagCheckResponse(BaseModel):
    hashtags: list[HashtagInfo] | None = None


class CaptionResponse(BaseModel):
    caption: str | None = None


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
