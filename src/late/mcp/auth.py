"""Authentication module for Zernio MCP HTTP server."""

import hashlib
import logging
import os
import time
from collections import OrderedDict
from enum import Enum
from urllib.parse import urlparse

import httpx
from fastmcp.server.auth import AccessToken, RemoteAuthProvider, TokenVerifier
from starlette.authentication import AuthenticationError
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


logger = logging.getLogger(__name__)

_VERIFY_URL = "https://zernio.com/api/v1/accounts"
_VERIFY_TIMEOUT = 5.0

# Positive-only verification cache: sha256(token) -> monotonic timestamp of the
# last upstream confirmation. Positives only, so an attacker cannot grow it by
# spraying invalid bearers. LRU-capped anyway: the container is long-lived.
# Per process on purpose: Railway runs one uvicorn worker (Dockerfile CMD, no
# --workers), and a shared store would put a new dependency in front of auth,
# which is how you rebuild this same outage.
_VERIFIED_AT: OrderedDict[str, float] = OrderedDict()
_VERIFIED_CACHE_MAX = 10_000
# Mirrors the 60s Redis TTL the API itself keeps on apikey:{keyHash}
# (Schedule-Posts-API libs/api-auth.ts:471), so this adds no revocation window
# the platform does not already have.
_FRESH_TTL_SECONDS = 60.0
# Only used when upstream could not answer. Blast radius is bounded to
# nothing: the MCP stores no data and every tool call re-presents the same
# key to the same API, so a revoked key honoured here still cannot read or
# write anything.
_GRACE_TTL_SECONDS = 3600.0


class Verification(Enum):
    """Upstream's verdict on a bearer token.

    Three-valued on purpose: the incident this replaces collapsed every
    non-200 into False, so 402, 429, 5xx and timeouts all reached the user as
    "your token is invalid, clear it and re-register".
    """

    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"


def _classify(status_code: int) -> Verification:
    """Map an upstream status to a verdict about the TOKEN, not the request.

    401/403 are the only statuses that say anything about token validity.
    402 and 429 are emitted only after the API has already resolved the key
    to a principal (Schedule-Posts-API libs/api-auth.ts:829 "Valid
    credential, but the billing owner is payment-suspended. 402 (not 401) so
    integrators can tell 'fix your card' apart from 'bad key'", and
    authenticateWithRateLimit at :665 rate-limits only after authenticate()
    succeeds), so both PROVE the key is good. Billing and limits are
    enforced per call by the endpoint that owns them. Everything else tells
    us nothing and must not be reported as an auth failure.
    """
    if status_code == 200:
        return Verification.VALID
    if status_code in (401, 403):
        return Verification.INVALID
    if status_code in (402, 429):
        return Verification.VALID
    return Verification.UNKNOWN


def _remember(token_key: str, now: float) -> None:
    _VERIFIED_AT[token_key] = now
    _VERIFIED_AT.move_to_end(token_key)
    while len(_VERIFIED_AT) > _VERIFIED_CACHE_MAX:
        _VERIFIED_AT.popitem(last=False)


async def verify_late_api_key(
    api_key: str, *, client: httpx.AsyncClient | None = None
) -> Verification:
    """Ask the Zernio API whether this bearer is a real credential.

    Function name kept as verify_late_api_key for backwards compatibility.
    Returns a three-valued Verification, NOT a bool: never write
    ``if await verify_late_api_key(...)``, every Enum member is truthy.

    client is injected by tests (httpx.MockTransport); production opens a
    per-call client and must not close an injected one.
    """
    owns_client = client is None
    client = client or httpx.AsyncClient()
    try:
        response = await client.get(
            _VERIFY_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=_VERIFY_TIMEOUT,
        )
    except Exception as exc:
        # Timeouts, DNS and TLS failures say nothing about the token. Logged
        # because the previous silent `return False` is why a 26h auth
        # outage ran with a green /health and no alert.
        logger.warning("Zernio token verification unreachable: %s", type(exc).__name__)
        return Verification.UNKNOWN
    finally:
        if owns_client:
            await client.aclose()

    verdict = _classify(response.status_code)
    if verdict is Verification.UNKNOWN:
        logger.warning(
            "Zernio token verification inconclusive: HTTP %s",
            response.status_code,
        )
    return verdict


class ZernioTokenVerifier(TokenVerifier):
    """Resource-server token verification for the Zernio MCP server.

    Accepts BOTH plain Zernio API keys and OAuth access tokens: both arrive as
    the same bearer string and are validated the same way — a live GET to the
    Zernio API (verify_late_api_key). 402 and 429 also count as valid: the
    Zernio API only emits them after it has already authenticated the
    credential. Deliberately format-agnostic (no JWT decode), which is why a
    static API key works here just as well as an issued OAuth token.
    """

    def __init__(self, *, client: httpx.AsyncClient | None = None) -> None:
        super().__init__()
        self._client = client

    async def verify_token(self, token: str) -> AccessToken | None:
        token_key = hashlib.sha256(token.encode()).hexdigest()
        now = time.monotonic()
        verified_at = _VERIFIED_AT.get(token_key)

        if verified_at is not None and now - verified_at < _FRESH_TTL_SECONDS:
            _VERIFIED_AT.move_to_end(token_key)
            return self._grant(token)

        verdict = await verify_late_api_key(token, client=self._client)

        if verdict is Verification.VALID:
            _remember(token_key, now)
            return self._grant(token)

        if verdict is Verification.INVALID:
            _VERIFIED_AT.pop(token_key, None)
            return None

        # UNKNOWN. Honour a token upstream confirmed recently; refuse to
        # guess about any other one, so an outage never becomes an auth
        # bypass. Raising AuthenticationError yields HTTP 400 with this
        # message. Returning None instead would emit the 401 invalid_token
        # whose text tells users to clear their tokens and re-register,
        # which is the exact damage this fix exists to stop. Any exception
        # type OTHER than AuthenticationError escapes as a 500 with the
        # message swallowed.
        if verified_at is not None and now - verified_at < _GRACE_TTL_SECONDS:
            # Guarded because the await above can suspend for the full verify
            # timeout, and a concurrent request may LRU-evict this key while
            # we are parked. A bare move_to_end would raise KeyError, which is
            # not AuthenticationError and so escapes as a 500.
            if token_key in _VERIFIED_AT:
                _VERIFIED_AT.move_to_end(token_key)
            logger.warning(
                "Granting %s... from cache: upstream unreachable",
                token_key[:12],
            )
            return self._grant(token)
        raise AuthenticationError(
            "Zernio API is temporarily unreachable, so this token could not "
            "be verified. Your credentials are fine; retry in a moment."
        )

    def _grant(self, token: str) -> AccessToken:
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
