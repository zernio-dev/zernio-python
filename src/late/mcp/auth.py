"""Authentication module for Zernio MCP HTTP server."""

import os
from urllib.parse import urlparse

import httpx
from starlette.requests import Request

# Origin allowlist for DNS-rebinding protection (MCP spec / Anthropic Connectors
# Directory requirement). Matched as exact host or subdomain suffix. Extend at
# runtime with MCP_ALLOWED_ORIGINS (comma-separated hostnames).
_DEFAULT_ALLOWED_ORIGIN_SUFFIXES = (
    "claude.ai",
    "claude.com",
    "anthropic.com",
    "chatgpt.com",
    "openai.com",
    "localhost",
    "127.0.0.1",
)


def _allowed_origin_suffixes() -> tuple[str, ...]:
    """Return the configured Origin allowlist (defaults + MCP_ALLOWED_ORIGINS)."""
    extra = os.getenv("MCP_ALLOWED_ORIGINS", "")
    extras = tuple(h.strip().lower() for h in extra.split(",") if h.strip())
    return _DEFAULT_ALLOWED_ORIGIN_SUFFIXES + extras


def is_allowed_origin(request: Request) -> bool:
    """Validate the request's Origin header to prevent DNS-rebinding attacks.

    The threat is a malicious web page in a browser scripting requests to the
    MCP server; browsers always attach an Origin header to such cross-site
    requests. Non-browser callers (native MCP clients, mcp-remote, and
    server-to-server callers like Anthropic's connector backend) send no Origin
    and are allowed through — they can't be driven by a hostile web page.

    Returns True when there is no Origin header or when the Origin host matches
    an allowlisted domain (exact or subdomain); False for a present but
    unrecognised browser Origin.
    """
    origin = request.headers.get("Origin")
    if not origin:
        return True
    host = (urlparse(origin).hostname or "").lower()
    if not host:
        return False
    return any(host == s or host.endswith("." + s) for s in _allowed_origin_suffixes())


def extract_late_api_key(request: Request) -> str | None:
    """
    Extract Zernio API key from request Authorization header.

    Expects: Authorization: Bearer <your_api_key>

    Function name kept as extract_late_api_key for backwards compatibility.

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
    Verify Zernio API key by making a test request to Zernio API.

    Function name kept as verify_late_api_key for backwards compatibility.

    Args:
        api_key: The Zernio API key to verify.

    Returns:
        True if API key is valid, False otherwise.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://zernio.com/api/v1/accounts",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5.0,
            )
            return response.status_code == 200
    except Exception:
        return False
