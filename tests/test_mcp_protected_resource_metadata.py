"""Protected-resource metadata (RFC 9728) served by the MCP HTTP server."""

import httpx
from starlette.applications import Starlette
from starlette.testclient import TestClient

from late.mcp.auth import build_auth_provider
from late.mcp.constants import OAUTH_AUTHORIZATION_SERVER


def _metadata(scopes: list[str] | None = None) -> dict:
    app = Starlette(routes=build_auth_provider(scopes).get_routes("/mcp"))
    response = TestClient(app).get("/.well-known/oauth-protected-resource/mcp")
    assert response.status_code == 200
    return response.json()


def test_authorization_server_is_the_issuer_string_byte_for_byte() -> None:
    # MCP SDK 2.x clients (Hermes Agent 0.21+) reject "https://zernio.com/" against
    # the issuer "https://zernio.com" with "Authorization server metadata issuer mismatch".
    assert _metadata()["authorization_servers"] == [OAUTH_AUTHORIZATION_SERVER]
    assert not OAUTH_AUTHORIZATION_SERVER.endswith("/")


def test_metadata_keeps_the_resource_scopes_and_narrowing() -> None:
    body = _metadata()
    assert body["resource"] == "https://mcp.zernio.com/mcp"
    assert body["bearer_methods_supported"] == ["header"]
    assert "posts:write" in body["scopes_supported"]
    assert body["resource_name"]
    assert _metadata(["posts:write"])["scopes_supported"] == ["posts:write"]


def test_authorization_server_matches_the_live_issuer() -> None:
    issuer = httpx.get(
        f"{OAUTH_AUTHORIZATION_SERVER}/.well-known/oauth-authorization-server",
        timeout=10,
    ).json()["issuer"]
    assert _metadata()["authorization_servers"] == [issuer]
