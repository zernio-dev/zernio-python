"""Authentication module for Zernio MCP HTTP server."""

import os
from urllib.parse import urlparse

import httpx
from fastmcp.server.auth import AccessToken, RemoteAuthProvider, TokenVerifier
from starlette.requests import Request

from late.mcp.constants import (
    DOCS_URL,
    MCP_PUBLIC_URL,
    OAUTH_AUTHORIZATION_SERVER,
    OAUTH_SCOPES,
    SERVICE_NAME,
)

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


class ZernioTokenVerifier(TokenVerifier):
    """Resource-server token verification for the Zernio MCP server.

    Accepts BOTH plain Zernio API keys and OAuth access tokens: both arrive as
    the same bearer string and are validated the same way — a live GET to the
    Zernio API (verify_late_api_key). HTTP 200 => valid. Deliberately
    format-agnostic (no JWT decode), which is why a static API key works here
    just as well as an issued OAuth token.
    """

    async def verify_token(self, token: str) -> AccessToken | None:
        if not await verify_late_api_key(token):
            return None
        return AccessToken(token=token, client_id="zernio", scopes=list(OAUTH_SCOPES))


def build_auth_provider() -> RemoteAuthProvider:
    """Build the FastMCP resource-server auth provider.

    RemoteAuthProvider makes this server an OAuth 2.0 resource server: it
    auto-serves /.well-known/oauth-protected-resource (RFC 9728), emits the 401
    WWW-Authenticate challenge pointing clients back at that document, and
    delegates token validation to ZernioTokenVerifier. The authorization server
    itself (token / authorize / register) lives at zernio.com.
    """
    return RemoteAuthProvider(
        token_verifier=ZernioTokenVerifier(),
        authorization_servers=[OAUTH_AUTHORIZATION_SERVER],
        base_url=MCP_PUBLIC_URL,
        scopes_supported=list(OAUTH_SCOPES),
        resource_name=SERVICE_NAME,
        resource_documentation=DOCS_URL,
    )
