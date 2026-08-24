"""Anonymous discovery on the Streamable HTTP endpoint.

Unauthenticated discovery requests (initialize, catalog lists/reads) must
succeed so scanners and registries can see the server, while anything else —
tools/call above all — must keep the HTTP 401 + WWW-Authenticate challenge
that triggers client OAuth flows.
"""

import httpx
import pytest

from late.mcp.http_server import build_app

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def rpc(method: str, params: dict | None = None, id: int | None = 1) -> dict:
    body: dict = {"jsonrpc": "2.0", "method": method, "params": params or {}}
    if id is not None:
        body["id"] = id
    return body


async def request(app, json_body, headers=None):
    transport = httpx.ASGITransport(app=app)
    async with (
        httpx.AsyncClient(transport=transport, base_url="http://test") as client,
        app.router.lifespan_context(app),
    ):
        return await client.post("/mcp", json=json_body, headers=headers or HEADERS)


async def test_anonymous_initialize_succeeds():
    response = await request(
        build_app(),
        rpc(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "probe", "version": "1.0.0"},
            },
        ),
    )
    assert response.status_code == 200
    assert '"serverInfo"' in response.text


async def test_anonymous_resources_list_returns_resources():
    response = await request(build_app(), rpc("resources/list"))
    assert response.status_code == 200
    assert "zernio://docs/overview" in response.text


async def test_anonymous_resources_read_returns_content():
    response = await request(
        build_app(), rpc("resources/read", {"uri": "zernio://docs/overview"})
    )
    assert response.status_code == 200
    assert "text/markdown" in response.text


async def test_root_post_aliases_to_mcp_endpoint():
    app = build_app()
    transport = httpx.ASGITransport(app=app)
    async with (
        httpx.AsyncClient(transport=transport, base_url="http://test") as client,
        app.router.lifespan_context(app),
    ):
        response = await client.post(
            "/",
            json=rpc(
                "initialize",
                {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "probe", "version": "1.0.0"},
                },
            ),
            headers=HEADERS,
        )
    assert response.status_code == 200
    assert '"serverInfo"' in response.text


async def test_root_get_without_event_stream_still_serves_info():
    app = build_app()
    transport = httpx.ASGITransport(app=app)
    async with (
        httpx.AsyncClient(transport=transport, base_url="http://test") as client,
        app.router.lifespan_context(app),
    ):
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["service"]


async def test_anonymous_tools_call_keeps_401_challenge():
    response = await request(
        build_app(), rpc("tools/call", {"name": "accounts_list", "arguments": {}})
    )
    assert response.status_code == 401
    assert "resource_metadata" in response.headers.get("www-authenticate", "")
