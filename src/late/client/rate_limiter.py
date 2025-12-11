"""
Rate limit handling for Late API.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass
class RateLimitInfo:
    """Rate limit information from API response headers."""

    limit: int | None = None
    remaining: int | None = None
    reset: datetime | None = None

    @property
    def is_exhausted(self) -> bool:
        """Check if rate limit is exhausted."""
        return self.remaining is not None and self.remaining <= 0

    @property
    def seconds_until_reset(self) -> float | None:
        """Get seconds until rate limit resets."""
        if self.reset is None:
            return None
        delta = self.reset - datetime.now()
        return max(0.0, delta.total_seconds())


class RateLimiter:
    """
    Rate limiter that tracks API rate limits from response headers.

    Late API returns these headers:
    - X-RateLimit-Limit: Maximum requests per period
    - X-RateLimit-Remaining: Requests remaining in current period
    - X-RateLimit-Reset: Unix timestamp when limit resets
    """

    def __init__(self) -> None:
        self._info: RateLimitInfo = RateLimitInfo()

    @property
    def info(self) -> RateLimitInfo:
        """Get current rate limit information."""
        return self._info

    @property
    def limit(self) -> int | None:
        """Get rate limit."""
        return self._info.limit

    @property
    def remaining(self) -> int | None:
        """Get remaining requests."""
        return self._info.remaining

    @property
    def reset_time(self) -> datetime | None:
        """Get reset time."""
        return self._info.reset

    def update_from_headers(self, headers: Mapping[str, str]) -> None:
        """
        Update rate limit info from response headers.

        Args:
            headers: Response headers from Late API
        """
        limit_str = headers.get("X-RateLimit-Limit")
        remaining_str = headers.get("X-RateLimit-Remaining")
        reset_str = headers.get("X-RateLimit-Reset")

        if limit_str is not None:
            with contextlib.suppress(ValueError):
                self._info.limit = int(limit_str)

        if remaining_str is not None:
            with contextlib.suppress(ValueError):
                self._info.remaining = int(remaining_str)

        if reset_str is not None:
            try:
                timestamp = int(reset_str)
                self._info.reset = datetime.fromtimestamp(timestamp)
            except (ValueError, OSError):
                pass

    def should_wait(self) -> bool:
        """Check if we should wait before making another request."""
        return self._info.is_exhausted

    def get_wait_time(self) -> float:
        """Get recommended wait time in seconds."""
        if not self._info.is_exhausted:
            return 0.0

        seconds = self._info.seconds_until_reset
        if seconds is None:
            return 60.0  # Default wait time

        return seconds + 1.0  # Add buffer
