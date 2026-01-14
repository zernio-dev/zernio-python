"""Authentication module for Late MCP HTTP server."""

import os
import secrets
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse


def get_server_api_key() -> str:
    """
    Get API key from environment variable.

    Returns:
        The MCP server API key.

    Raises:
        ValueError: If MCP_SERVER_API_KEY is not set.
    """
    api_key = os.getenv("MCP_SERVER_API_KEY")
    if not api_key:
        raise ValueError(
            "MCP_SERVER_API_KEY environment variable not set. "
            "Please set it to secure your MCP server."
        )
    return api_key


def extract_api_key(request: Request) -> Optional[str]:
    """
    Extract API key from request (header or query param).

    Checks in order:
    1. Authorization header (Bearer token)
    2. X-API-Key header
    3. api_key query parameter

    Args:
        request: The incoming Starlette request.

    Returns:
        The extracted API key, or None if not found.
    """
    # Try Authorization header first: "Bearer <key>"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix

    # Try X-API-Key header
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header:
        return api_key_header

    # Try query parameter as fallback
    return request.query_params.get("api_key")


def verify_api_key(request: Request) -> bool:
    """
    Verify API key from request matches server key.

    Uses secrets.compare_digest for timing-attack resistance.

    Args:
        request: The incoming Starlette request.

    Returns:
        True if API key is valid, False otherwise.
    """
    try:
        expected_key = get_server_api_key()
        provided_key = extract_api_key(request)

        if not provided_key:
            return False

        # Use secrets.compare_digest for timing-attack resistance
        return secrets.compare_digest(expected_key, provided_key)
    except Exception:
        # If any error occurs (e.g., env var not set), deny access
        return False


async def require_api_key(request: Request, call_next):
    """
    Middleware to require API key on all requests except health check.

    Args:
        request: The incoming Starlette request.
        call_next: The next middleware or route handler.

    Returns:
        The response from the next handler, or 401 if unauthorized.
    """
    # Allow health check without authentication
    if request.url.path == "/health":
        return await call_next(request)

    # Verify API key for all other requests
    if not verify_api_key(request):
        return JSONResponse(
            {"error": "Invalid or missing API key"}, status_code=401
        )

    return await call_next(request)
