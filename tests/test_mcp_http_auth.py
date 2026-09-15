"""HTTP authentication must precede MCP processing, including discovery."""

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


HEADERS = {"Accept": "application/json, text/event-stream"}
CHALLENGE = (
    f'resource_metadata="{MCP_PUBLIC_URL}/.well-known/oauth-protected-resource/mcp"'
)
INITIALIZE = {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "probe", "version": "1.0.0"},
}
METHODS = [
    ("initialize", INITIALIZE),
    ("notifications/initialized", {}),
    ("ping", {}),
    ("tools/list", {}),
    ("prompts/list", {}),
    ("resources/list", {}),
    ("resources/read", {"uri": "zernio://docs/overview"}),
    ("resources/templates/list", {}),
    ("tools/call", {"name": "__nonexistent_auth_probe__", "arguments": {}}),
]


def rpc(method, params):
    body = {"jsonrpc": "2.0", "method": method, "params": params}
    if not method.startswith("notifications/"):
        body["id"] = 1
    return body


@pytest.mark.parametrize("path", ["/mcp", "/"])
@pytest.mark.parametrize("method,params", METHODS)
async def test_unauthenticated_mcp_requires_oauth(path, method, params):
    app = build_app()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client,
    ):
        response = await client.post(path, json=rpc(method, params), headers=HEADERS)
    assert response.status_code == 401
    assert CHALLENGE in response.headers["www-authenticate"]


@pytest.mark.parametrize(
    "token,expected",
    [("valid-test-key", 200), ("invalid-test-key", 401), ("anonymous-discovery", 401)],
)
@pytest.mark.parametrize("method,params", METHODS[:1] + METHODS[3:4])
async def test_discovery_verifies_supplied_credentials(
    monkeypatch, token, expected, method, params
):
    seen = []

    async def verify(candidate, **_kwargs):
        seen.append(candidate)
        return (
            auth.Verification.VALID
            if candidate == "valid-test-key"
            else auth.Verification.INVALID
        )

    monkeypatch.setattr(auth, "verify_late_api_key", verify)
    monkeypatch.setattr(auth, "_VERIFIED_AT", OrderedDict())
    app = build_app()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client,
    ):
        response = await client.post(
            "/mcp",
            json=rpc(method, params),
            headers={**HEADERS, "Authorization": f"Bearer {token}"},
        )
    assert seen == [token]
    assert response.status_code == expected
    if expected == 401:
        assert CHALLENGE in response.headers["www-authenticate"]
    else:
        assert (
            '"serverInfo"' if method == "initialize" else '"tools"'
        ) in response.text


@pytest.mark.parametrize(
    "path,status",
    [
        ("/", 200),
        ("/health", 200),
        ("/.well-known/oauth-protected-resource/mcp", 200),
        ("/.well-known/oauth-protected-resource", 308),
        ("/.well-known/mcp/server-card.json", 200),
        ("/mcp/server-card", 200),
        ("/server.json", 200),
    ],
)
async def test_public_http_endpoints(path, status):
    app = build_app()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client,
    ):
        response = await client.get(path)
    assert response.status_code == status
    if status == 308:
        assert (
            response.headers["location"] == "/.well-known/oauth-protected-resource/mcp"
        )
    if path == "/.well-known/oauth-protected-resource/mcp":
        assert response.json()["resource"] == f"{MCP_PUBLIC_URL}/mcp"
        assert response.json()["authorization_servers"]
