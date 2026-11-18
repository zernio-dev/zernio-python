"""The legacy SSE transport is retired; the /sse URL serves Streamable HTTP."""

from collections import OrderedDict

import httpx
import pytest

from late.mcp import auth
from late.mcp.constants import MCP_PUBLIC_URL
from late.mcp.http_server import build_app

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


STREAMABLE = {"Accept": "application/json, text/event-stream"}
INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "probe", "version": "1.0.0"},
    },
}


async def request(method, path, **kwargs):
    app = build_app()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client,
    ):
        return await client.request(method, path, **kwargs)


@pytest.mark.parametrize(
    "method,path",
    [("GET", "/sse"), ("POST", "/messages/"), ("POST", "/messages")],
)
async def test_the_sse_handshake_gets_a_410_naming_the_mcp_url(method, path):
    response = await request(
        method, path, headers={"Accept": "text/event-stream"}, json={}
    )
    assert response.status_code == 410
    assert response.json()["error"] == "sse_transport_removed"
    assert response.json()["endpoint"] == f"{MCP_PUBLIC_URL}/mcp"
    assert "claude mcp add --transport http" in response.json()["message"]


async def test_a_streamable_http_get_on_sse_gets_the_405_mcp_gives():
    response = await request(
        "GET", "/sse", headers={"MCP-Protocol-Version": "2025-06-18"}
    )
    assert response.status_code == 405


async def test_streamable_http_on_sse_is_challenged_with_its_own_metadata():
    response = await request("POST", "/sse", json=INITIALIZE, headers=STREAMABLE)
    assert response.status_code == 401
    assert (
        f'resource_metadata="{MCP_PUBLIC_URL}/.well-known/oauth-protected-resource/sse"'
        in response.headers["www-authenticate"]
    )

    metadata = await request("GET", "/.well-known/oauth-protected-resource/sse")
    assert metadata.status_code == 200
    assert metadata.json()["resource"] == f"{MCP_PUBLIC_URL}/sse"


async def test_streamable_http_on_sse_serves_the_mcp_server(monkeypatch):
    async def verify(_candidate, **_kwargs):
        return auth.Verification.VALID

    monkeypatch.setattr(auth, "verify_late_api_key", verify)
    monkeypatch.setattr(auth, "_VERIFIED_AT", OrderedDict())
    response = await request(
        "POST",
        "/sse",
        json=INITIALIZE,
        headers={**STREAMABLE, "Authorization": "Bearer valid-test-key"},
    )
    assert response.status_code == 200
    assert '"serverInfo"' in response.text
