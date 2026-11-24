"""Hand-written MCP tools call the generated SDK, whose signatures change on
every regen. When the spec made a required parameter optional, the generator
moved it behind `*`, and a positional call that worked the day before raised
TypeError on every use (show_conversation). These tests bind each call site
against the current signatures, and require every argument that is not a URL
path parameter to be passed by keyword, which survives that kind of change."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
from fastmcp import Client, FastMCP

from late import Late
from late.mcp.apps import APP_URI
from late.mcp.apps.tools import register_tools

MCP_DIR = Path(__file__).resolve().parents[1] / "src" / "late" / "mcp"
HAND_WRITTEN = [p for p in MCP_DIR.rglob("*.py") if p.name != "generated_tools.py"]
SDK = Late(api_key="k")
RESOURCES = {
    name
    for name in dir(SDK)
    if not name.startswith("_") and hasattr(getattr(SDK, name), "_client")
}


def _sdk_calls(path: Path) -> list[tuple[ast.Call, str, str]]:
    """Every `<anything>.<resource>.<method>(...)` where <resource> is an SDK one."""
    calls = []
    for node in ast.walk(ast.parse(path.read_text())):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        resource = node.func.value
        if isinstance(resource, ast.Attribute) and resource.attr in RESOURCES:
            calls.append((node, resource.attr, node.func.attr))
    return calls


CALL_SITES = [
    pytest.param(
        call,
        resource,
        method,
        id=f"{path.relative_to(MCP_DIR)}:{call.lineno}:{resource}.{method}",
    )
    for path in HAND_WRITTEN
    for call, resource, method in _sdk_calls(path)
]


def _method(resource: str, method: str) -> Any:
    target = getattr(getattr(SDK, resource), method, None)
    if target is None:
        pytest.fail(f"client.{resource}.{method} does not exist in the SDK")
    return target


def test_call_sites_were_found() -> None:
    ids = [p.id for p in CALL_SITES]
    assert any(i.startswith("apps/tools.py:") for i in ids)
    assert any(i.startswith("server.py:") for i in ids)


@pytest.mark.parametrize(("call", "resource", "method"), CALL_SITES)
def test_call_site_matches_the_sdk_signature(
    call: ast.Call, resource: str, method: str
) -> None:
    if any(isinstance(a, ast.Starred) for a in call.args) or any(
        k.arg is None for k in call.keywords
    ):
        pytest.skip("*args / **kwargs cannot be bound statically")

    args = [object()] * len(call.args)
    kwargs = {k.arg: object() for k in call.keywords}
    try:
        inspect.signature(_method(resource, method)).bind(*args, **kwargs)
    except TypeError as e:
        pytest.fail(f"client.{resource}.{method}(...) no longer fits the SDK: {e}")


@pytest.mark.parametrize(("call", "resource", "method"), CALL_SITES)
def test_generated_methods_get_only_path_params_positionally(
    call: ast.Call, resource: str, method: str
) -> None:
    """A path parameter is always required, so it stays positional. Anything else
    can turn optional on the next regen and move behind `*`."""
    target = _method(resource, method)
    if "._generated." not in target.__module__:
        pytest.skip("hand-written resource, not regenerated")
    params = list(inspect.signature(target).parameters.values())
    source = inspect.getsource(target)
    for param, arg in zip(params, call.args, strict=False):
        if isinstance(arg, ast.Starred):
            break
        assert "{" + param.name + "}" in source, (
            f"client.{resource}.{method}: pass {param.name}= by keyword, it is not a "
            "path parameter and can become keyword-only on the next regen"
        )


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
