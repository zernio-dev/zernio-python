"""`?tools=` on the server URL selects what tools/list returns.

Absent: the pinned tools plus search_tools/call_tool. `all`: every tool,
paginated. A comma-separated list: exactly those tools, and an unknown name is
an error that suggests the closest real names.
"""

import json
from collections import OrderedDict
from contextlib import asynccontextmanager

import httpx
import pytest

from late.mcp import auth, server
from late.mcp.http_server import build_app

pytestmark = pytest.mark.anyio

HEADERS = {
    "Accept": "application/json, text/event-stream",
    "Authorization": "Bearer valid-test-key",
}


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def _valid_key(monkeypatch):
    async def verify(_candidate, **_kwargs):
        return auth.Verification.VALID

    monkeypatch.setattr(auth, "verify_late_api_key", verify)
    monkeypatch.setattr(auth, "_VERIFIED_AT", OrderedDict())


# Not a fixture: the app's lifespan must be entered and exited in the test's
# own task, which an async fixture's teardown does not guarantee.
@asynccontextmanager
async def mcp_client():
    app = build_app()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as http,
    ):
        yield http


async def list_tools(client, query="", cursor=None):
    params = {"cursor": cursor} if cursor else {}
    response = await client.post(
        f"/mcp{query}",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": params},
        headers=HEADERS,
    )
    assert response.status_code == 200
    return rpc_body(response)


def rpc_body(response):
    data = [line for line in response.text.splitlines() if line.startswith("data: ")]
    return json.loads(data[-1].removeprefix("data: "))


async def list_all_pages(client, query):
    names, cursor, pages = [], None, 0
    while True:
        result = (await list_tools(client, query, cursor))["result"]
        names += [t["name"] for t in result["tools"]]
        pages += 1
        cursor = result.get("nextCursor")
        if not cursor:
            return names, pages


async def test_default_listing_is_pinned_tools_and_search_on_one_page():
    async with mcp_client() as client:
        result = (await list_tools(client))["result"]

    names = {t["name"] for t in result["tools"]}
    assert names == {*server._PINNED_TOOLS, server._SEARCH_TOOL, server._CALL_TOOL}
    assert "nextCursor" not in result


async def test_all_lists_every_tool_across_pages():
    async with mcp_client() as client:
        names, pages = await list_all_pages(client, "?tools=all")

    assert len(names) == len(set(names))
    assert set(server._PINNED_TOOLS) < set(names)
    assert "ad_campaigns_get_ad_tree" in names
    assert server._SEARCH_TOOL not in names
    assert pages == -(-len(names) // server._TOOLS_PAGE_SIZE) > 1


async def test_named_tools_are_listed_exactly_with_full_schemas():
    query = "?tools=ad_campaigns_get_ad_tree,posts_create,ad_campaigns_get_ad_tree"
    async with mcp_client() as client:
        result = (await list_tools(client, query))["result"]

    assert [t["name"] for t in result["tools"]] == [
        "ad_campaigns_get_ad_tree",
        "posts_create",
    ]
    assert all(t["inputSchema"]["type"] == "object" for t in result["tools"])
    assert all(t["description"] for t in result["tools"])


async def test_unknown_tool_name_is_an_error_with_suggestions():
    async with mcp_client() as client:
        body = await list_tools(client, "?tools=posts_create,ad_campaigns_get_ad_trees")

    assert "result" not in body
    assert body["error"]["code"] == -32602
    message = body["error"]["message"]
    assert "ad_campaigns_get_ad_trees (closest: ad_campaigns_get_ad_tree" in message
    assert "posts_create" not in message


async def test_empty_tools_param_falls_back_to_default():
    async with mcp_client() as client:
        result = (await list_tools(client, "?tools="))["result"]

    assert server._SEARCH_TOOL in {t["name"] for t in result["tools"]}


async def test_tool_not_in_the_list_is_still_callable_by_name():
    # Selection shapes the listing only: hidden tools were always callable by
    # name, so a short list must not turn into an access control it never was.
    async with mcp_client() as client:
        response = await client.post(
            "/mcp?tools=posts_create",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "zernio_overview", "arguments": {}},
            },
            headers=HEADERS,
        )

    body = rpc_body(response)
    assert "error" not in body
    assert body["result"]["isError"] is False
