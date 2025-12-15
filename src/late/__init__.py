"""
Late SDK - Python client for Late API.

Schedule social media posts across multiple platforms.
"""

from .client.exceptions import (
    LateAPIError,
    LateAuthenticationError,
    LateConnectionError,
    LateError,
    LateForbiddenError,
    LateNotFoundError,
    LateRateLimitError,
    LateTimeoutError,
    LateValidationError,
)
from .client.late_client import Late
from .enums import (
    CaptionTone,
    DayOfWeek,
    FacebookContentType,
    GoogleBusinessCTAType,
    InstagramContentType,
    MediaType,
    Platform,
    PostStatus,
    TikTokCommercialContentType,
    TikTokMediaType,
    TikTokPrivacyLevel,
    Visibility,
)

__version__ = "1.1.0"

__all__ = [
    # Client
    "Late",
    # Enums - Core
    "Platform",
    "PostStatus",
    "MediaType",
    "Visibility",
    # Enums - Platform-specific
    "InstagramContentType",
    "FacebookContentType",
    "TikTokPrivacyLevel",
    "TikTokCommercialContentType",
    "TikTokMediaType",
    "GoogleBusinessCTAType",
    # Enums - Tools & Queue
    "CaptionTone",
    "DayOfWeek",
    # Exceptions
    "LateAPIError",
    "LateAuthenticationError",
    "LateConnectionError",
    "LateError",
    "LateForbiddenError",
    "LateNotFoundError",
    "LateRateLimitError",
    "LateTimeoutError",
    "LateValidationError",
]
