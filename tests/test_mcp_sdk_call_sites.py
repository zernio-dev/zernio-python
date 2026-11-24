"""Hand-written MCP tools call the generated SDK, whose signatures change on
every regen. When the spec made a required parameter optional, the generator
moved it behind `*`, and a positional call that worked the day before raised
TypeError on every use (show_conversation). These tests bind each call site
against the current signatures so a regen that breaks one fails here first."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import httpx
import pytest
import respx
from fastmcp import Client, FastMCP

from late import Late
from late.mcp.apps import APP_URI
from late.mcp.apps.tools import register_tools

MCP_DIR = Path(__file__).resolve().parents[1] / "src" / "late" / "mcp"
HAND_WRITTEN = [p for p in MCP_DIR.rglob("*.py") if p.name != "generated_tools.py"]


def _sdk_calls(path: Path) -> list[tuple[ast.Call, str, str]]:
    """Every `<x>.client.<resource>.<method>(...)` or `client.<resource>.<method>(...)`."""
    calls = []
    for node in ast.walk(ast.parse(path.read_text())):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        resource = node.func.value
        if not isinstance(resource, ast.Attribute):
            continue
        owner = resource.value
        if isinstance(owner, ast.Name) and owner.id == "client":
            calls.append((node, resource.attr, node.func.attr))
    return calls


CALL_SITES = [
    pytest.param(
        call, resource, method, id=f"{path.name}:{call.lineno}:{resource}.{method}"
    )
    for path in HAND_WRITTEN
    for call, resource, method in _sdk_calls(path)
]


def test_call_sites_were_found() -> None:
    assert any(p.id.startswith("tools.py:") for p in CALL_SITES)


@pytest.mark.parametrize(("call", "resource", "method"), CALL_SITES)
def test_call_site_matches_the_sdk_signature(
    call: ast.Call, resource: str, method: str
) -> None:
    sdk = Late(api_key="k")
    target = getattr(getattr(sdk, resource, None), method, None)
    if target is None:
        pytest.skip(f"client.{resource} is not an SDK resource")
    if any(isinstance(a, ast.Starred) for a in call.args) or any(
        k.arg is None for k in call.keywords
    ):
        pytest.skip("*args / **kwargs cannot be checked statically")

    args = [object()] * len(call.args)
    kwargs = {k.arg: object() for k in call.keywords}
    try:
        inspect.signature(target).bind(*args, **kwargs)
    except TypeError as e:
        pytest.fail(f"client.{resource}.{method}(...) no longer fits the SDK: {e}")


@pytest.fixture
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


@pytest.mark.usefixtures("api_env")
async def test_show_conversation_sends_the_account_id() -> None:
    with respx.mock:
        route = respx.get(
            url__startswith="https://api.test.com/v1/inbox/conversations/conv_1/messages"
        ).mock(
            return_value=httpx.Response(
                200, json={"messages": [{"id": "m1", "message": "hi"}]}
            )
        )
        server = FastMCP("apps")
        register_tools(server, APP_URI)
        async with Client(server) as client:
            result = await client.call_tool(
                "show_conversation",
                {"conversation_id": "conv_1", "account_id": "acc_1"},
            )

    assert not result.is_error
    assert route.calls.last.request.url.params["accountId"] == "acc_1"
    assert result.structured_content["data"]["messages"][0]["id"] == "m1"
