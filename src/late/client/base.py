"""
Base HTTP client with sync/async support.
"""

from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager, contextmanager
from importlib.metadata import PackageNotFoundError, version
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


def _resolve_sdk_version() -> str:
    for dist_name in ("zernio-sdk", "late-sdk"):
        try:
            return version(dist_name)
        except PackageNotFoundError:
            continue
    return "0.0.0+unknown"


def _parse_error_body(response: httpx.Response) -> dict[str, Any]:
    """Best-effort parse of an error response body.

    Returns {} when the body is empty, when it isn't valid JSON (e.g. an
    HTML 401 from a proxy in front of the API), or when the parsed value
    isn't a dict.
    """
    if not response.content:
        return {}
    try:
        data = response.json()
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def _with_request_id(headers: dict[str, str] | None) -> dict[str, str]:
    merged = dict(headers or {})
    merged.setdefault("x-request-id", str(uuid.uuid4()))
    return merged


class BaseClient:
    """
    Base HTTP client supporting both sync and async operations.

    Uses HTTPX for modern Python HTTP with connection pooling,
    automatic retries, and full HTTP/2 support.
    """

    DEFAULT_BASE_URL = "https://zernio.com/api"
    DEFAULT_TIMEOUT = 30.0
    # A publishNow create runs the whole cross-platform publish inside the
    # request. One measured Threads publish took 222s against DEFAULT_TIMEOUT's
    # 30s, so httpx aborted while the server was still working and the retry
    # loop replayed the POST - two live posts, and a 409 for the one that
    # actually published. Crisp session_8e5d3e6e-1e10-4a33-95f1-0b1e33d119da.
    DEFAULT_PUBLISH_TIMEOUT = 300.0
    DEFAULT_MAX_RETRIES = 3
    SDK_VERSION = _resolve_sdk_version()

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        publish_timeout: float = DEFAULT_PUBLISH_TIMEOUT,
    ) -> None:
        """
        Initialize the base client.

        Args:
            api_key: Late API key for authentication
            base_url: Base URL for the API (default: https://zernio.com/api)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retries for failed requests (default: 3)
            publish_timeout: Timeout in seconds for publishNow creates, which
                              publish synchronously and can outlast `timeout`
                              (default: 300)
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.publish_timeout = publish_timeout
        self._rate_limiter = RateLimiter()

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"late-python-sdk/{self.SDK_VERSION}",
        }

    def _resolve_timeout(self, data: dict[str, Any] | None) -> float:
        """
        Pick the request timeout by sniffing publishNow out of the JSON body.

        Sniffing a domain field in the transport layer is a deliberate stopgap.
        It is the only place that covers all three publish callers at once - the
        hand-written posts.create, the generated create_post, and the MCP server -
        and it survives regeneration, which base.py does and _generated/ does not.
        The proper fix is for scripts/generate_resources.py to emit an explicit
        timeout= on publish-capable operations; that needs a 58-file regen and is
        deliberately out of scope here.
        """
        return self.publish_timeout if (data or {}).get("publishNow") else self.timeout

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
            error_data = _parse_error_body(response)
            raise LateAuthenticationError(
                error_data.get("error", "Invalid API key"), details=error_data
            )

        if response.status_code == 403:
            error_data = _parse_error_body(response)
            raise LateForbiddenError(
                error_data.get("error", "Access forbidden - check your plan"),
                details=error_data,
            )

        if response.status_code == 404:
            error_data = _parse_error_body(response)
            raise LateNotFoundError(
                error_data.get("error", "Resource not found"), details=error_data
            )

        if response.status_code == 429:
            raise LateRateLimitError(
                "Rate limit exceeded",
                reset_time=self._rate_limiter.reset_time,
                limit=self._rate_limiter.limit,
                remaining=self._rate_limiter.remaining,
            )

        if response.status_code >= 400:
            error_data = _parse_error_body(response)
            # Pass the entire response body through as `details` so callers
            # (and __str__) can surface the field name (`param`), the stable
            # error code (`code`), and platform-specific context. The API
            # returns `{error, type, code, param, ...}` at the top level -
            # not nested under a `details` key - so the previous
            # `error_data.get("details")` was always None.
            raise LateAPIError(
                message=error_data.get("error", f"HTTP {response.status_code}"),
                status_code=response.status_code,
                details=error_data,
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

        # Mint the id once, outside the loop: every attempt must carry the SAME
        # x-request-id or the server cannot match a replay to the original. httpx
        # copies this dict per attempt rather than mutating it, so one assignment
        # here is genuinely reused. setdefault keeps a caller-supplied id.
        kwargs["headers"] = _with_request_id(kwargs.get("headers"))

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
                if method.upper() == "POST":
                    last_error = LateTimeoutError(
                        f"POST {path} timed out and was NOT retried: the request may have "
                        f"completed server-side. Check before retrying; retrying may create "
                        f"a duplicate. ({e})"
                    )
                    # A POST that timed out client-side may have fully succeeded server-side:
                    # replaying it creates a second live post. The server keys idempotency on
                    # x-request-id, but its content-hash dedup runs first and answers 409 while
                    # the original is still publishing, so the window is unreachable. PUT,
                    # PATCH and DELETE stay retryable - they are idempotent by contract.
                    raise last_error from e
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
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a sync GET request."""
        with self._sync_client() as client:
            return self._request_with_retry(
                client, "GET", path, params=params, headers=headers
            )

    def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | list[tuple[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a sync POST request."""
        if files:
            # For file uploads, create a fresh client without Content-Type
            # (httpx sets the correct multipart Content-Type automatically)
            client_headers = {
                k: v for k, v in self._headers.items() if k != "Content-Type"
            }
            with httpx.Client(
                base_url=self.base_url,
                headers=client_headers,
                timeout=self.timeout,
            ) as client:
                return self._request_with_retry(
                    client, "POST", path, files=files, params=params, headers=headers
                )

        with self._sync_client() as client:
            return self._request_with_retry(
                client,
                "POST",
                path,
                json=data,
                params=params,
                headers=headers,
                timeout=self._resolve_timeout(data),
            )

    def _put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync PUT request.

        Accepts both ``data`` (JSON body) and ``params`` (query string). Some
        write endpoints take a body plus query params, e.g. GBP updates carry
        the payload in the body and a ``locationId`` query param that selects
        which location the write targets; without it the API falls back to the
        account's stored location.
        """
        with self._sync_client() as client:
            return self._request_with_retry(
                client, "PUT", path, json=data, params=params
            )

    def _patch(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a sync PATCH request.

        Accepts both ``data`` (JSON body) and ``params`` (query string).
        Most PATCH endpoints use a body, but a few (e.g. the Telegram
        connect poll) use query params only — both must work.
        """
        with self._sync_client() as client:
            return self._request_with_retry(
                client, "PATCH", path, json=data, params=params
            )

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

        # Mint the id once, outside the loop: every attempt must carry the SAME
        # x-request-id or the server cannot match a replay to the original. httpx
        # copies this dict per attempt rather than mutating it, so one assignment
        # here is genuinely reused. setdefault keeps a caller-supplied id.
        kwargs["headers"] = _with_request_id(kwargs.get("headers"))

        for attempt in range(self.max_retries):
            try:
                response = await client.request(method, path, **kwargs)
                return self._handle_response(response)

            except LateRateLimitError:
                raise

            except (LateAuthenticationError, LateNotFoundError, LateForbiddenError):
                raise

            except httpx.TimeoutException as e:
                if method.upper() == "POST":
                    last_error = LateTimeoutError(
                        f"POST {path} timed out and was NOT retried: the request may have "
                        f"completed server-side. Check before retrying; retrying may create "
                        f"a duplicate. ({e})"
                    )
                    # A POST that timed out client-side may have fully succeeded server-side:
                    # replaying it creates a second live post. The server keys idempotency on
                    # x-request-id, but its content-hash dedup runs first and answers 409 while
                    # the original is still publishing, so the window is unreachable. PUT,
                    # PATCH and DELETE stay retryable - they are idempotent by contract.
                    raise last_error from e
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
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an async GET request."""
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client, "GET", path, params=params, headers=headers
            )

    async def _apost(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | list[tuple[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an async POST request."""
        if files:
            # For file uploads, create a fresh client without Content-Type
            client_headers = {
                k: v for k, v in self._headers.items() if k != "Content-Type"
            }
            async with httpx.AsyncClient(
                base_url=self.base_url,
                headers=client_headers,
                timeout=self.timeout,
            ) as client:
                return await self._arequest_with_retry(
                    client, "POST", path, files=files, params=params, headers=headers
                )

        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client,
                "POST",
                path,
                json=data,
                params=params,
                headers=headers,
                timeout=self._resolve_timeout(data),
            )

    async def _aput(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async PUT request.

        Accepts both ``data`` (JSON body) and ``params`` (query string). Some
        write endpoints take a body plus query params, e.g. GBP updates carry
        the payload in the body and a ``locationId`` query param that selects
        which location the write targets; without it the API falls back to the
        account's stored location.
        """
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client, "PUT", path, json=data, params=params
            )

    async def _apatch(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async PATCH request.

        Accepts both ``data`` (JSON body) and ``params`` (query string).
        Most PATCH endpoints use a body, but a few (e.g. the Telegram
        connect poll) use query params only — both must work.
        """
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client, "PATCH", path, json=data, params=params
            )

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
