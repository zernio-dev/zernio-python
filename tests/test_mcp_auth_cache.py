from __future__ import annotations

import asyncio
import time

import httpx
import pytest

from late.mcp import auth, server
from late.mcp.auth import ZernioTokenVerifier


@pytest.fixture(autouse=True)
def _clear_verification_cache():
    auth._VERIFIED_AT.clear()
    auth._IN_FLIGHT.clear()
    yield
    auth._VERIFIED_AT.clear()
    auth._IN_FLIGHT.clear()


class SlowVerifyUpstream:
    def __init__(self, status_code: int = 200) -> None:
        self.calls = 0
        self.release = asyncio.Event()
        self.status_code = status_code

    async def __call__(self, _request: httpx.Request) -> httpx.Response:
        self.calls += 1
        await self.release.wait()
        return httpx.Response(self.status_code)


async def test_concurrent_requests_with_one_token_share_a_single_upstream_verification():
    upstream = SlowVerifyUpstream()
    client = httpx.AsyncClient(transport=httpx.MockTransport(upstream))
    verifier = ZernioTokenVerifier(client=client)

    pending = [asyncio.create_task(verifier.verify_token("sk_live")) for _ in range(5)]
    await asyncio.sleep(0)
    upstream.release.set()
    granted = await asyncio.gather(*pending)

    assert upstream.calls == 1
    assert sorted(t.claims["resolved_by"] for t in granted) == ["joined"] * 4 + [
        "upstream"
    ]
    assert auth._IN_FLIGHT == {}
    await client.aclose()


async def test_a_cancelled_request_does_not_cancel_the_verification_others_wait_on():
    upstream = SlowVerifyUpstream()
    client = httpx.AsyncClient(transport=httpx.MockTransport(upstream))
    verifier = ZernioTokenVerifier(client=client)

    first = asyncio.create_task(verifier.verify_token("sk_live"))
    second = asyncio.create_task(verifier.verify_token("sk_live"))
    await asyncio.sleep(0)
    first.cancel()
    upstream.release.set()

    assert (await second) is not None
    assert upstream.calls == 1
    await client.aclose()


async def test_a_token_verified_nine_minutes_ago_is_served_from_cache():
    upstream = SlowVerifyUpstream()
    client = httpx.AsyncClient(transport=httpx.MockTransport(upstream))
    verifier = ZernioTokenVerifier(client=client)
    auth._VERIFIED_AT[auth.token_cache_key("sk_live")] = time.monotonic() - 540

    granted = await verifier.verify_token("sk_live")

    assert granted is not None
    assert granted.claims == {"resolved_by": "cache", "waited_ms": 0}
    assert upstream.calls == 0
    await client.aclose()


async def test_an_upstream_verification_reports_how_long_the_request_waited():
    upstream = SlowVerifyUpstream()
    upstream.release.set()
    client = httpx.AsyncClient(transport=httpx.MockTransport(upstream))

    granted = await ZernioTokenVerifier(client=client).verify_token("sk_live")

    assert granted is not None
    assert granted.claims["resolved_by"] == "upstream"
    assert isinstance(granted.claims["waited_ms"], int)
    await client.aclose()


def test_the_verifier_keeps_one_client_with_warm_connections_for_every_verification():
    verifier = ZernioTokenVerifier()

    assert isinstance(verifier._client, httpx.AsyncClient)
    assert verifier._client._transport._pool._keepalive_expiry == 60.0


def test_an_api_401_during_a_tool_call_evicts_the_cached_token_so_the_client_can_refresh():
    auth._VERIFIED_AT[auth.token_cache_key("sk_revoked")] = time.monotonic()
    auth._VERIFIED_AT[auth.token_cache_key("sk_other")] = time.monotonic()
    transport = server._ApiTransport(
        httpx.MockTransport(lambda _request: httpx.Response(401))
    )

    httpx.Client(transport=transport).get(
        "https://zernio.test/api/v1/posts",
        headers={"Authorization": "Bearer sk_revoked"},
    )

    assert auth.token_cache_key("sk_revoked") not in auth._VERIFIED_AT
    assert auth.token_cache_key("sk_other") in auth._VERIFIED_AT


def test_a_successful_tool_call_keeps_the_cached_token():
    auth._VERIFIED_AT[auth.token_cache_key("sk_live")] = time.monotonic()
    transport = server._ApiTransport(
        httpx.MockTransport(lambda _request: httpx.Response(200))
    )

    httpx.Client(transport=transport).get(
        "https://zernio.test/api/v1/posts",
        headers={"Authorization": "Bearer sk_live"},
    )

    assert auth.token_cache_key("sk_live") in auth._VERIFIED_AT
