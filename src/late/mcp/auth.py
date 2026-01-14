"""Authentication module for Late MCP HTTP server."""

import httpx
from starlette.requests import Request


def extract_late_api_key(request: Request) -> str | None:
    """
    Extract Late API key from request Authorization header.

    Expects: Authorization: Bearer <your_late_api_key>

    Args:
        request: The incoming Starlette request.

    Returns:
        The extracted API key, or None if not found.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    return None


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
                "https://getlate.dev/api/v1/accounts",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5.0,
            )
            return response.status_code == 200
    except Exception:
        return False
