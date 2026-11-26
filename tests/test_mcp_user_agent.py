from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import respx
from fastmcp.server.auth import AccessToken
from starlette.requests import Request

from late.client.base import BaseClient
from late.mcp import auth, chatgpt_server, server, user_agent
from late.mcp.user_agent import mcp_user_agent

if TYPE_CHECKING:
    import pytest

_SDK = f"late-python-sdk/{BaseClient.SDK_VERSION}"


def _incoming(monkeypatch: pytest.MonkeyPatch, path: str, header: str | None) -> None:
    headers = [(b"user-agent", header.encode())] if header is not None else []
    request = Request(
        {"type": "http", "path": path, "headers": headers, "query_string": b""}
    )
    monkeypatch.setattr(user_agent, "get_http_request", lambda: request)
    monkeypatch.setattr(user_agent, "get_http_headers", lambda: dict(request.headers))


def _off_http(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_request() -> Request:
        raise RuntimeError("No active HTTP request found.")

    monkeypatch.setattr(user_agent, "get_http_request", no_request)
    monkeypatch.setattr(user_agent, "get_http_headers", lambda: {})


def test_names_the_mcp_surface_and_the_calling_client(monkeypatch):
    _incoming(monkeypatch, "/mcp", "Claude-User/1.0 (+https://claude.ai)")

    assert mcp_user_agent() == "zernio-mcp (mcp; Claude-User)"


def test_requests_on_the_chatgpt_endpoint_name_the_chatgpt_surface(monkeypatch):
    _incoming(monkeypatch, "/chatgpt", "openai-mcp/1.0.0")

    assert mcp_user_agent() == "zernio-mcp (chatgpt; openai-mcp)"


def test_names_only_the_surface_when_the_client_sends_no_user_agent(monkeypatch):
    _incoming(monkeypatch, "/mcp", None)

    assert mcp_user_agent() == "zernio-mcp (mcp)"


def test_off_http_is_the_stdio_surface(monkeypatch):
    _off_http(monkeypatch)

    assert mcp_user_agent() == "zernio-mcp (stdio)"


def test_client_name_cannot_break_out_of_the_comment(monkeypatch):
    _incoming(monkeypatch, "/mcp", "evil) (x; y/1.0")

    assert mcp_user_agent() == "zernio-mcp (mcp; evil x y)"


def test_tool_calls_send_the_mcp_token_ahead_of_the_sdk(monkeypatch):
    _incoming(monkeypatch, "/mcp", "Cursor/1.0.0 (darwin)")
    token = AccessToken(token="sk_test", client_id="c", scopes=[])
    monkeypatch.setattr(server, "get_access_token", lambda: token)

    client = server._get_client()

    assert client._headers["User-Agent"] == f"zernio-mcp (mcp; Cursor) {_SDK}"


def test_stdio_tool_calls_send_the_stdio_surface(monkeypatch):
    _off_http(monkeypatch)
    monkeypatch.setattr(server, "get_access_token", lambda: None)
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")

    client = server._get_client()

    assert client._headers["User-Agent"] == f"zernio-mcp (stdio) {_SDK}"


@respx.mock
async def test_chatgpt_api_calls_send_the_mcp_user_agent(monkeypatch):
    _incoming(monkeypatch, "/chatgpt", "openai-mcp/1.0.0")
    monkeypatch.setattr(chatgpt_server, "_bearer", lambda: "sk_test")
    route = respx.get(f"{chatgpt_server.API_BASE}/v1/profiles").mock(
        return_value=httpx.Response(200, json={})
    )

    await chatgpt_server._api("GET", "/v1/profiles")

    assert (
        route.calls.last.request.headers["User-Agent"]
        == "zernio-mcp (chatgpt; openai-mcp)"
    )


@respx.mock
async def test_token_verification_sends_the_mcp_user_agent(monkeypatch):
    _incoming(monkeypatch, "/mcp", "Claude-User/1.0")
    route = respx.get(auth._VERIFY_URL).mock(return_value=httpx.Response(200, json={}))

    await auth.verify_late_api_key("sk_test")

    assert (
        route.calls.last.request.headers["User-Agent"]
        == "zernio-mcp (mcp; Claude-User)"
    )


@respx.mock
def test_docs_fetch_sends_the_mcp_user_agent(monkeypatch):
    _incoming(monkeypatch, "/mcp", "Cursor/1.0.0")
    monkeypatch.setattr(server, "_docs_cache", {})
    route = respx.get(server._DOCS_URL).mock(
        return_value=httpx.Response(200, text="docs")
    )

    server._get_docs_content()

    assert route.calls.last.request.headers["User-Agent"] == "zernio-mcp (mcp; Cursor)"


def test_the_full_calling_user_agent_is_capped(monkeypatch):
    _incoming(monkeypatch, "/mcp", "Agent/1.0 " + "x" * 500)

    assert user_agent.calling_user_agent() == ("Agent/1.0 " + "x" * 500)[:200]
