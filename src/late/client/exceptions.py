"""
Custom exceptions for Late SDK.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


class LateError(Exception):
    """Base exception for Late SDK."""

    pass


class LateAPIError(LateError):
    """Exception raised for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class LateAuthenticationError(LateAPIError):
    """Exception raised for authentication errors (401)."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class LateRateLimitError(LateAPIError):
    """Exception raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        reset_time: datetime | None = None,
        limit: int | None = None,
        remaining: int | None = None,
    ) -> None:
        super().__init__(message, status_code=429)
        self.reset_time = reset_time
        self.limit = limit
        self.remaining = remaining

    def __str__(self) -> str:
        base = f"[429] {self.message}"
        if self.reset_time:
            base += f" (resets at {self.reset_time.isoformat()})"
        return base


class LateNotFoundError(LateAPIError):
    """Exception raised when a resource is not found (404)."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class LateForbiddenError(LateAPIError):
    """Exception raised for forbidden access (403)."""

    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message, status_code=403)


class LateValidationError(LateError):
    """Exception raised for client-side validation errors."""

    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)


class LateConnectionError(LateError):
    """Exception raised for connection errors."""

    pass


class LateTimeoutError(LateError):
    """Exception raised when a request times out."""

    pass
