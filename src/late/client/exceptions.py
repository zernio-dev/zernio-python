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
        # Surface field name + error code from the API envelope when present.
        # The API returns {error, type, code, param} on validation failures;
        # __str__ used to drop everything but `error`, leaving callers
        # (notably the MCP wrapper, which prints str(exc)) staring at
        # cryptic messages like "Number must be greater than 0" with no clue
        # which field tripped it.
        prefix = f"[{self.status_code}] " if self.status_code else ""
        suffix_parts: list[str] = []
        param = self.details.get("param") if self.details else None
        code = self.details.get("code") if self.details else None
        if param:
            suffix_parts.append(f"field: {param}")
        if code:
            suffix_parts.append(f"code: {code}")
        suffix = f" ({'; '.join(suffix_parts)})" if suffix_parts else ""
        return f"{prefix}{self.message}{suffix}"


class LateAuthenticationError(LateAPIError):
    """Exception raised for authentication errors (401)."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=401, details=details)


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

    def __init__(
        self,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=404, details=details)


class LateForbiddenError(LateAPIError):
    """Exception raised for forbidden access (403)."""

    def __init__(
        self,
        message: str = "Access forbidden",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=403, details=details)


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


# ---------------------------------------------------------------------------
# Zernio-branded aliases (backwards-compatible, all old names still work)
# ---------------------------------------------------------------------------
ZernioError = LateError
ZernioAPIError = LateAPIError
ZernioAuthenticationError = LateAuthenticationError
ZernioRateLimitError = LateRateLimitError
ZernioNotFoundError = LateNotFoundError
ZernioForbiddenError = LateForbiddenError
ZernioValidationError = LateValidationError
ZernioConnectionError = LateConnectionError
ZernioTimeoutError = LateTimeoutError
