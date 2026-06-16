"""
Zernio SDK - Python client for the Zernio API.

Schedule social media posts across multiple platforms.

All original ``Late*`` names are still available for backwards compatibility.
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
    ZernioAPIError,
    ZernioAuthenticationError,
    ZernioConnectionError,
    ZernioError,
    ZernioForbiddenError,
    ZernioNotFoundError,
    ZernioRateLimitError,
    ZernioTimeoutError,
    ZernioValidationError,
)
from .client.late_client import Late, Zernio
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

__version__ = "1.4.161"

__all__ = [
    # Client
    "Zernio",
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
    # Exceptions - Zernio-branded
    "ZernioAPIError",
    "ZernioAuthenticationError",
    "ZernioConnectionError",
    "ZernioError",
    "ZernioForbiddenError",
    "ZernioNotFoundError",
    "ZernioRateLimitError",
    "ZernioTimeoutError",
    "ZernioValidationError",
    # Exceptions - Legacy (backwards-compatible)
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
