"""Authentication module for Late MCP HTTP server."""

import httpx
from starlette.requests import Request


def extract_late_api_key(request: Request) -> str | None:
    """
    Extract Late API key from request.

    Checks in order:
    1. X-Late-API-Key header
    2. Authorization header (Bearer token)
    3. X-API-Key header
    4. api_key query parameter

    Args:
        request: The incoming Starlette request.

    Returns:
        The extracted API key, or None if not found.
    """
    # Try X-Late-API-Key header first (most specific)
    late_key = request.headers.get("X-Late-API-Key")
    if late_key:
        return late_key

    # Try Authorization header: "Bearer <key>"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]

    # Try X-API-Key header
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header:
        return api_key_header

    # Try query parameter as fallback
    return request.query_params.get("api_key")


async def verify_late_api_key(api_key: str) -> bool:
    """
    Verify Late API key by making a test request to Late API.

    Args:
        api_key: The Late API key to verify.

    Returns:
        True if API key is valid, False otherwise.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.getlate.dev/api/accounts",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5.0,
            )
            return response.status_code == 200
    except Exception:
        return False
