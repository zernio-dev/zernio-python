from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import respx
from fastmcp.server.auth import AccessToken

from late.client.base import BaseClient
from late.mcp import chatgpt_server, server, user_agent
from late.mcp.user_agent import mcp_user_agent

if TYPE_CHECKING:
    import pytest

_SDK = f"late-python-sdk/{BaseClient.SDK_VERSION}"


def _calling_client(monkeypatch: pytest.MonkeyPatch, header: str | None) -> None:
    headers = {"user-agent": header} if header is not None else {}
    monkeypatch.setattr(user_agent, "get_http_headers", lambda: headers)


def test_names_the_surface_and_the_calling_client(monkeypatch):
    _calling_client(monkeypatch, "Claude-User/1.0 (+https://claude.ai)")

    assert mcp_user_agent("mcp") == "zernio-mcp (mcp; Claude-User)"


def test_names_only_the_surface_without_an_http_client(monkeypatch):
    _calling_client(monkeypatch, None)

    assert mcp_user_agent("stdio") == "zernio-mcp (stdio)"


def test_client_name_cannot_break_out_of_the_comment(monkeypatch):
    _calling_client(monkeypatch, "evil) (x; y/1.0")

    assert mcp_user_agent("mcp") == "zernio-mcp (mcp; evil x y)"


def test_hosted_calls_send_the_mcp_surface_ahead_of_the_sdk(monkeypatch):
    _calling_client(monkeypatch, "Cursor/1.0.0 (darwin)")
    token = AccessToken(token="sk_test", client_id="c", scopes=[])
    monkeypatch.setattr(server, "get_access_token", lambda: token)

    client = server._get_client()

    assert client._headers["User-Agent"] == f"zernio-mcp (mcp; Cursor) {_SDK}"


def test_stdio_calls_send_the_stdio_surface(monkeypatch):
    _calling_client(monkeypatch, None)
    monkeypatch.setattr(server, "get_access_token", lambda: None)
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")

    client = server._get_client()

    assert client._headers["User-Agent"] == f"zernio-mcp (stdio) {_SDK}"


@respx.mock
async def test_chatgpt_calls_send_the_chatgpt_surface(monkeypatch):
    _calling_client(monkeypatch, "openai-mcp/1.0.0")
    monkeypatch.setattr(chatgpt_server, "_bearer", lambda: "sk_test")
    route = respx.get(f"{chatgpt_server.API_BASE}/v1/profiles").mock(
        return_value=httpx.Response(200, json={})
    )

    await chatgpt_server._api("GET", "/v1/profiles")

    assert route.calls.last.request.headers["User-Agent"] == (
        "zernio-mcp (chatgpt; openai-mcp)"
    )
