"""Long POSTs outlive the default timeout, and an agent's retry must not create a second ad."""

from __future__ import annotations

import re
from pathlib import Path

import httpx
import pytest
import respx
from fastmcp import Client

from late import Late
from late.mcp.idempotency import same_arguments_key
from late.mcp.server import mcp

API = "https://api.test.com"
GENERATED_TOOLS = Path(__file__).parents[1] / "src/late/mcp/generated_tools.py"
LONG_RUNNING_PATHS = [
    "/v1/ads/boost",
    "/v1/ads/call",
    "/v1/ads/create",
    "/v1/ads/ctwa",
    "/v1/ads/messaging",
    "/v1/ads/videos",
    "/v1/media/prepare",
    "/v1/ads/120/duplicate",
    "/v1/ads/ad-sets/120/duplicate",
    "/v1/ads/campaigns/120/duplicate",
    "/v1/posts/p1/retry",
]
STANDALONE_AD = {"account_id": "acc_1", "ad_account_id": "act_1", "name": "Spring"}


def _read_timeout(route: respx.Route) -> float:
    return route.calls[0].request.extensions["timeout"]["read"]


def _tool_source(tool: str) -> str:
    source = GENERATED_TOOLS.read_text()
    start = source.index(f"def {tool}(")
    next_tool = source.find("@mcp.tool(", start)
    return source[start:next_tool]


async def _key_sent_for(route: respx.Route, arguments: dict[str, str]) -> str:
    async with Client(mcp) as client:
        await client.call_tool("ad_campaigns_create_standalone_ad", arguments)
    return route.calls.last.request.headers["Idempotency-Key"]


@pytest.fixture
def client() -> Late:
    return Late(api_key="test_api_key", base_url=API)


@pytest.fixture
def create_ad_route(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")
    with respx.mock(assert_all_called=False) as router:
        yield router.post("https://zernio.com/api/v1/ads/create").mock(
            return_value=httpx.Response(201, json={"ad": {"id": "ad_1"}})
        )


@pytest.mark.parametrize("path", LONG_RUNNING_PATHS)
@respx.mock
def test_long_posts_wait_for_the_publish_timeout(client: Late, path: str) -> None:
    route = respx.post(f"{API}{path}").mock(return_value=httpx.Response(201, json={}))

    client._post(path, data={"name": "Spring"})

    assert _read_timeout(route) == client.publish_timeout


@pytest.mark.parametrize("path", LONG_RUNNING_PATHS)
@respx.mock
async def test_async_long_posts_wait_for_the_publish_timeout(
    client: Late, path: str
) -> None:
    route = respx.post(f"{API}{path}").mock(return_value=httpx.Response(201, json={}))

    await client._apost(path, data={"name": "Spring"})

    assert _read_timeout(route) == client.publish_timeout


@pytest.mark.parametrize(
    "path",
    [
        "/v1/ads/campaigns",
        "/v1/inbox/comments/post_1",
        "/v1/workflows/w1/duplicate",
        "/v1/posts/p1/unpublish",
    ],
)
@respx.mock
def test_other_posts_keep_the_default_timeout(client: Late, path: str) -> None:
    route = respx.post(f"{API}{path}").mock(return_value=httpx.Response(201, json={}))

    client._post(path, data={"name": "Spring"})

    assert _read_timeout(route) == client.timeout


@respx.mock
def test_publish_now_still_waits_for_the_publish_timeout(client: Late) -> None:
    route = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(201, json={})
    )

    client._post("/v1/posts", data={"publishNow": True})

    assert _read_timeout(route) == client.publish_timeout


@respx.mock
def test_a_longer_configured_timeout_is_not_shortened_on_ad_creates() -> None:
    client = Late(api_key="test_api_key", base_url=API, timeout=600.0)
    route = respx.post(f"{API}/v1/ads/create").mock(
        return_value=httpx.Response(201, json={})
    )

    client._post("/v1/ads/create", data={"name": "Spring"})

    assert _read_timeout(route) == 600.0


async def test_identical_tool_calls_send_the_same_idempotency_key(
    create_ad_route: respx.Route,
) -> None:
    first = await _key_sent_for(create_ad_route, STANDALONE_AD)
    second = await _key_sent_for(create_ad_route, dict(reversed(STANDALONE_AD.items())))

    assert first == second
    assert first.startswith("mcp-ad_campaigns_create_standalone_ad-")


async def test_changing_an_argument_creates_another_ad(
    create_ad_route: respx.Route,
) -> None:
    first = await _key_sent_for(create_ad_route, STANDALONE_AD)
    second = await _key_sent_for(create_ad_route, {**STANDALONE_AD, "name": "Autumn"})

    assert first != second


@pytest.mark.parametrize(
    "tool",
    [
        "ad_campaigns_create_standalone_ad",
        "messaging_ads_create_messaging_ad",
        "messaging_ads_create_call_ad",
        "messaging_ads_create_ctwa_ad",
    ],
)
def test_ad_create_tools_send_a_key_and_tell_the_agent_about_the_replay(
    tool: str,
) -> None:
    source = _tool_source(tool)

    assert re.search(rf'same_arguments_key\(\s*"{tool}"', source)
    assert "an identical call within 24 hours returns the first result" in source


def test_boost_sends_no_key_because_a_key_turns_off_the_api_duplicate_check() -> None:
    assert "same_arguments_key" not in _tool_source("ad_campaigns_boost_post")


def test_key_fits_the_api_limit_and_ignores_argument_order() -> None:
    key = same_arguments_key("a" * 100, {"b": 1, "a": [1, {"c": None}]})

    assert key == same_arguments_key("a" * 100, {"a": [1, {"c": None}], "b": 1})
    assert len(key) <= 255
