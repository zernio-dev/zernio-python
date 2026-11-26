"""Protected-resource metadata (RFC 9728) served by the MCP HTTP server."""

import httpx
from starlette.applications import Starlette
from starlette.testclient import TestClient

from late.mcp.auth import build_auth_provider
from late.mcp.constants import OAUTH_AUTHORIZATION_SERVER
from late.mcp.middleware.missing_scope import relink_instructions


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


def test_metadata_advertises_the_google_and_microsoft_and_commerce_scopes() -> None:
    # Clients such as ChatGPT and Cursor request exactly the advertised scopes, so a scope
    # missing here means no MCP user can ever reach the calendar, files or commerce routes.
    assert {"calendar:write", "files:write", "commerce:write"} <= set(_metadata()["scopes_supported"])


AREA_READ_SCOPES = [
    "commerce:read",
    "calendar:read",
    "files:read",
    "campaigns:read",
    "money:read",
    "automations:read",
]


def test_metadata_advertises_the_area_read_scopes_at_the_end() -> None:
    # Appended after messaging:read to match libs/oauth/scopes.ts in Schedule-Posts-API (#10954).
    assert _metadata()["scopes_supported"][-6:] == AREA_READ_SCOPES


def test_every_area_scope_has_a_relink_purpose() -> None:
    # A token narrowed to an area's :read reaches its write tools, whose first declared scope is the :write.
    area_write_scopes = [scope.replace(":read", ":write") for scope in AREA_READ_SCOPES]
    for scope in AREA_READ_SCOPES + area_write_scopes:
        assert f"use this ({scope})" not in relink_instructions(scope)


def test_metadata_scopes_match_the_live_authorization_server() -> None:
    supported = httpx.get(
        f"{OAUTH_AUTHORIZATION_SERVER}/.well-known/oauth-authorization-server",
        timeout=10,
    ).json()["scopes_supported"]
    assert _metadata()["scopes_supported"] == supported
