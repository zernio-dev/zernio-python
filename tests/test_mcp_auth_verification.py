"""
Regression tests for the Zernio MCP auth outage: auth.py used to collapse
every non-200 upstream status into "invalid token" (``return
response.status_code == 200``) and swallow timeouts (``except Exception:
return False``). ``verify_token`` then returned ``None`` and fastmcp emitted a
401 ``invalid_token`` telling users to clear their credentials and
re-register, even though the Zernio API only emits 402/429 for a credential
it has already authenticated.

These tests drive the real ``_classify`` / ``ZernioTokenVerifier`` against a
fake transport (``httpx.MockTransport`` -- no network, no mocking of our own
functions).
"""

from __future__ import annotations

import hashlib
import time

import httpx
import pytest
from starlette.authentication import AuthenticationError

from late.mcp import auth
from late.mcp.auth import Verification, ZernioTokenVerifier, _classify


@pytest.fixture(autouse=True)
def _clear_verification_cache():
    auth._VERIFIED_AT.clear()
    yield
    auth._VERIFIED_AT.clear()


@pytest.mark.parametrize(
    "status_code,expected",
    [
        (200, Verification.VALID),
        (401, Verification.INVALID),
        (403, Verification.INVALID),
        (402, Verification.VALID),
        (429, Verification.VALID),
        (500, Verification.UNKNOWN),
        (502, Verification.UNKNOWN),
        (503, Verification.UNKNOWN),
        (504, Verification.UNKNOWN),
        (404, Verification.UNKNOWN),
    ],
)
def test_classify_maps_upstream_status_to_outcome(status_code, expected):
    assert _classify(status_code) is expected


async def test_verify_token_accepts_payment_required_key():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(402)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    verifier = ZernioTokenVerifier(client=client)

    access_token = await verifier.verify_token("some-api-key")

    assert access_token is not None
    await client.aclose()


async def test_verify_token_raises_unavailable_for_unknown_token_when_upstream_is_down():
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("boom")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    verifier = ZernioTokenVerifier(client=client)

    with pytest.raises(AuthenticationError):
        await verifier.verify_token("never-seen-before")

    await client.aclose()


async def test_verify_token_honours_recently_valid_token_during_outage():
    def ok_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    warm_client = httpx.AsyncClient(transport=httpx.MockTransport(ok_handler))
    verifier = ZernioTokenVerifier(client=warm_client)
    token = "a-recently-valid-key"
    warm_token = await verifier.verify_token(token)
    assert warm_token is not None
    await warm_client.aclose()

    # Push the cached timestamp past the fresh window (60s) but still inside
    # the grace window (3600s), so the second call below actually exercises
    # the UNKNOWN + grace-cache branch instead of short-circuiting on the
    # fresh-cache check.
    token_key = hashlib.sha256(token.encode()).hexdigest()
    auth._VERIFIED_AT[token_key] = time.monotonic() - (auth._FRESH_TTL_SECONDS + 1)

    def down_handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("boom")

    down_client = httpx.AsyncClient(transport=httpx.MockTransport(down_handler))
    verifier._client = down_client

    access_token = await verifier.verify_token(token)

    assert access_token is not None
    await down_client.aclose()


async def test_verify_token_rejects_a_genuinely_bad_key():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    verifier = ZernioTokenVerifier(client=client)

    assert await verifier.verify_token("a-revoked-key") is None
    await client.aclose()


async def test_invalid_verdict_evicts_the_cached_entry():
    """A key that upstream later rejects must not survive on the grace path."""

    def ok_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    token = "a-key-that-gets-revoked"
    token_key = hashlib.sha256(token.encode()).hexdigest()

    warm_client = httpx.AsyncClient(transport=httpx.MockTransport(ok_handler))
    verifier = ZernioTokenVerifier(client=warm_client)
    assert await verifier.verify_token(token) is not None
    await warm_client.aclose()

    # Past the fresh window so the next call really re-verifies upstream.
    auth._VERIFIED_AT[token_key] = time.monotonic() - (auth._FRESH_TTL_SECONDS + 1)

    def revoked_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401)

    revoked_client = httpx.AsyncClient(transport=httpx.MockTransport(revoked_handler))
    verifier._client = revoked_client
    assert await verifier.verify_token(token) is None
    await revoked_client.aclose()

    assert token_key not in auth._VERIFIED_AT

    # With the entry evicted, an upstream outage must refuse the token rather
    # than honour it from the grace cache.
    def down_handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("boom")

    down_client = httpx.AsyncClient(transport=httpx.MockTransport(down_handler))
    verifier._client = down_client
    with pytest.raises(AuthenticationError):
        await verifier.verify_token(token)
    await down_client.aclose()


def test_verification_cache_is_bounded():
    now = 0.0
    for i in range(auth._VERIFIED_CACHE_MAX + 50):
        auth._remember(f"token-{i}", now)

    assert len(auth._VERIFIED_AT) <= auth._VERIFIED_CACHE_MAX
    # Eviction is LRU, so the oldest inserts are the ones that went.
    assert "token-0" not in auth._VERIFIED_AT
    assert f"token-{auth._VERIFIED_CACHE_MAX + 49}" in auth._VERIFIED_AT
