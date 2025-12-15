"""
Base HTTP client with sync/async support.
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Any

import httpx

from .exceptions import (
    LateAPIError,
    LateAuthenticationError,
    LateConnectionError,
    LateForbiddenError,
    LateNotFoundError,
    LateRateLimitError,
    LateTimeoutError,
)
from .rate_limiter import RateLimiter

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


class BaseClient:
    """
    Base HTTP client supporting both sync and async operations.

    Uses HTTPX for modern Python HTTP with connection pooling,
    automatic retries, and full HTTP/2 support.
    """

    DEFAULT_BASE_URL = "https://getlate.dev/api"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3
    SDK_VERSION = "1.0.0"

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """
        Initialize the base client.

        Args:
            api_key: Late API key for authentication
            base_url: Base URL for the API (default: https://getlate.dev/api)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retries for failed requests (default: 3)
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._rate_limiter = RateLimiter()

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"late-python-sdk/{self.SDK_VERSION}",
        }

    @property
    def rate_limit_info(self) -> dict[str, Any]:
        """Get current rate limit information."""
        info = self._rate_limiter.info
        return {
            "limit": info.limit,
            "remaining": info.remaining,
            "reset": info.reset.isoformat() if info.reset else None,
        }

    # =========================================================================
    # Sync Client
    # =========================================================================

    @contextmanager
    def _sync_client(self) -> Iterator[httpx.Client]:
        """Create a sync HTTP client context."""
        client = httpx.Client(
            base_url=self.base_url,
            headers=self._headers,
            timeout=self.timeout,
        )
        try:
            yield client
        finally:
            client.close()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        # Update rate limit info
        self._rate_limiter.update_from_headers(response.headers)

        # Handle errors
        if response.status_code == 401:
            raise LateAuthenticationError("Invalid API key")

        if response.status_code == 403:
            error_data = response.json() if response.content else {}
            raise LateForbiddenError(
                error_data.get("error", "Access forbidden - check your plan")
            )

        if response.status_code == 404:
            error_data = response.json() if response.content else {}
            raise LateNotFoundError(error_data.get("error", "Resource not found"))

        if response.status_code == 429:
            raise LateRateLimitError(
                "Rate limit exceeded",
                reset_time=self._rate_limiter.reset_time,
                limit=self._rate_limiter.limit,
                remaining=self._rate_limiter.remaining,
            )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise LateAPIError(
                message=error_data.get("error", f"HTTP {response.status_code}"),
                status_code=response.status_code,
                details=error_data.get("details"),
            )

        # Return parsed JSON or empty dict
        if response.content:
            return response.json()  # type: ignore[no-any-return]
        return {}

    def _request_with_retry(
        self,
        client: httpx.Client,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make a request with automatic retry on transient errors."""
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = client.request(method, path, **kwargs)
                return self._handle_response(response)

            except LateRateLimitError:
                # Don't retry rate limit errors, let caller handle
                raise

            except (LateAuthenticationError, LateNotFoundError, LateForbiddenError):
                # Don't retry client errors
                raise

            except httpx.TimeoutException as e:
                last_error = LateTimeoutError(f"Request timed out: {e}")

            except httpx.ConnectError as e:
                last_error = LateConnectionError(f"Connection failed: {e}")

            except httpx.HTTPStatusError:
                # Already handled in _handle_response
                raise

            # Exponential backoff
            if attempt < self.max_retries - 1:
                wait_time = (2**attempt) * 0.5
                time.sleep(wait_time)

        if last_error:
            raise last_error
        raise LateAPIError("Request failed after retries")

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync GET request."""
        with self._sync_client() as client:
            return self._request_with_retry(client, "GET", path, params=params)

    def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | list[tuple[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync POST request."""
        if files:
            # For file uploads, create a fresh client without Content-Type
            # (httpx sets the correct multipart Content-Type automatically)
            headers = {k: v for k, v in self._headers.items() if k != "Content-Type"}
            with httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                return self._request_with_retry(
                    client, "POST", path, files=files, params=params
                )

        with self._sync_client() as client:
            return self._request_with_retry(
                client, "POST", path, json=data, params=params
            )

    def _put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync PUT request."""
        with self._sync_client() as client:
            return self._request_with_retry(client, "PUT", path, json=data)

    def _delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync DELETE request."""
        with self._sync_client() as client:
            return self._request_with_retry(client, "DELETE", path, params=params)

    # =========================================================================
    # Async Client
    # =========================================================================

    @asynccontextmanager
    async def _async_client(self) -> AsyncIterator[httpx.AsyncClient]:
        """Create an async HTTP client context."""
        client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._headers,
            timeout=self.timeout,
        )
        try:
            yield client
        finally:
            await client.aclose()

    async def _arequest_with_retry(
        self,
        client: httpx.AsyncClient,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make an async request with automatic retry on transient errors."""
        import asyncio

        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(method, path, **kwargs)
                return self._handle_response(response)

            except LateRateLimitError:
                raise

            except (LateAuthenticationError, LateNotFoundError, LateForbiddenError):
                raise

            except httpx.TimeoutException as e:
                last_error = LateTimeoutError(f"Request timed out: {e}")

            except httpx.ConnectError as e:
                last_error = LateConnectionError(f"Connection failed: {e}")

            except httpx.HTTPStatusError:
                raise

            # Exponential backoff
            if attempt < self.max_retries - 1:
                wait_time = (2**attempt) * 0.5
                await asyncio.sleep(wait_time)

        if last_error:
            raise last_error
        raise LateAPIError("Request failed after retries")

    async def _aget(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async GET request."""
        async with self._async_client() as client:
            return await self._arequest_with_retry(client, "GET", path, params=params)

    async def _apost(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | list[tuple[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async POST request."""
        if files:
            # For file uploads, create a fresh client without Content-Type
            headers = {k: v for k, v in self._headers.items() if k != "Content-Type"}
            async with httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                return await self._arequest_with_retry(
                    client, "POST", path, files=files, params=params
                )

        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client, "POST", path, json=data, params=params
            )

    async def _aput(
        self,
        path: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async PUT request."""
        async with self._async_client() as client:
            return await self._arequest_with_retry(client, "PUT", path, json=data)

    async def _adelete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async DELETE request."""
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client, "DELETE", path, params=params
            )
