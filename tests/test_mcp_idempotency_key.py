"""Every MCP tool whose operation declares Idempotency-Key must take it as an
argument and send it on the wire, so an agent can retry a timed-out write
without creating a second copy."""

from __future__ import annotations

import asyncio
import importlib
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
import yaml
from fastmcp import Client, FastMCP

from late import Late
from late.mcp.generated_tools import register_generated_tools
from late.mcp.server import mcp

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.test.com"
CALLER_KEY = "holo-retry-3f1c9a"
# These derive a key from their arguments when the caller passes none.
DERIVED_KEY_TOOLS = {
    "ad_campaigns_create_standalone_ad",
    "messaging_ads_create_messaging_ad",
    "messaging_ads_create_call_ad",
    "messaging_ads_create_ctwa_ad",
}


def _generator():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        return importlib.import_module("generate_mcp_tools")
    finally:
        sys.path.remove(str(ROOT / "scripts"))


def _idempotency_key_param(operation: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any] | None:
    for param in operation.get("parameters", []):
        if "$ref" in param:
            param = spec["components"]["parameters"][param["$ref"].rsplit("/", 1)[-1]]
        if param.get("in") == "header" and param.get("name", "").lower() == "idempotency-key":
            return param
    return None


def _idempotent_tools() -> dict[str, bool]:
    """Tool name (derived the way the generator names them) -> whether the spec
    marks the key required, for every operation that declares Idempotency-Key."""
    gen = _generator()
    spec = yaml.safe_load((ROOT / "openapi.yaml").read_text())
    tools: dict[str, bool] = {}
    for path_item in spec["paths"].values():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            operation_id = operation.get("operationId")
            if not operation_id or operation_id in gen.SKIP_OPERATIONS:
                continue
            key_param = _idempotency_key_param(operation, spec)
            if key_param is None:
                continue
            tag = operation.get("tags", ["Other"])[0]
            resource = gen.TAG_TO_RESOURCE.get(tag, tag.lower().replace(" ", "_"))
            tool = f"{resource}_{gen.camel_to_snake(operation_id)}"
            tool = tool.replace(f"{resource}_{resource}_", f"{resource}_", 1)
            tools[tool] = bool(key_param.get("required", False))
    return tools


KEY_REQUIRED_BY_TOOL = _idempotent_tools()
IDEMPOTENT_TOOLS = sorted(KEY_REQUIRED_BY_TOOL)
OPTIONAL_KEY_TOOLS = sorted(t for t, required in KEY_REQUIRED_BY_TOOL.items() if not required)


async def _schemas() -> dict[str, dict[str, Any]]:
    local = FastMCP("schemas")
    register_generated_tools(local, lambda: None)
    async with Client(local) as client:
        return {t.name: t.inputSchema for t in await client.list_tools()}


def _dummy(schema: dict[str, Any]) -> Any:
    for option in schema.get("anyOf", []):
        if option.get("type") != "null":
            return _dummy(option)
    if "enum" in schema:
        return schema["enum"][0]
    return {
        "string": "x_1",
        "integer": 1,
        "number": 1,
        "boolean": True,
        "array": [],
        "object": {},
    }.get(schema.get("type"), "x_1")


def _required_arguments(schema: dict[str, Any]) -> dict[str, Any]:
    props = schema.get("properties", {})
    return {name: _dummy(props[name]) for name in schema.get("required", [])}


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


@pytest.fixture(scope="module")
def schemas() -> dict[str, dict[str, Any]]:
    return asyncio.run(_schemas())


def test_the_spec_still_declares_idempotency_key_on_posts() -> None:
    # Guards the parametrized checks below against silently running on nothing.
    assert "posts_create_post" in IDEMPOTENT_TOOLS
    assert len(IDEMPOTENT_TOOLS) > 50


@pytest.mark.parametrize("tool", IDEMPOTENT_TOOLS)
def test_tool_exposes_idempotency_key_as_the_spec_declares_it(
    tool: str, schemas: dict[str, dict[str, Any]]
) -> None:
    schema = schemas[tool]

    assert "idempotency_key" in schema["properties"]
    assert ("idempotency_key" in schema.get("required", [])) is KEY_REQUIRED_BY_TOOL[tool]


@pytest.mark.parametrize("tool", IDEMPOTENT_TOOLS)
@respx.mock
async def test_caller_key_reaches_the_api_as_the_header(
    tool: str, schemas: dict[str, dict[str, Any]]
) -> None:
    route = respx.route(host="api.test.com").mock(
        return_value=httpx.Response(201, json={"id": "x_1"})
    )
    arguments = {**_required_arguments(schemas[tool]), "idempotency_key": CALLER_KEY}

    async with Client(mcp) as client:
        await client.call_tool(tool, arguments)

    assert route.call_count == 1
    assert route.calls.last.request.headers["Idempotency-Key"] == CALLER_KEY


@pytest.mark.parametrize("tool", sorted(set(OPTIONAL_KEY_TOOLS) - DERIVED_KEY_TOOLS))
@respx.mock
async def test_no_key_is_sent_when_the_caller_passes_none(
    tool: str, schemas: dict[str, dict[str, Any]]
) -> None:
    # A key turns off the API's content duplicate check, so none is invented.
    route = respx.route(host="api.test.com").mock(
        return_value=httpx.Response(201, json={"id": "x_1"})
    )

    async with Client(mcp) as client:
        await client.call_tool(tool, _required_arguments(schemas[tool]))

    assert "Idempotency-Key" not in route.calls.last.request.headers


@pytest.mark.parametrize("tool", sorted(DERIVED_KEY_TOOLS))
@respx.mock
async def test_ad_tools_keep_their_derived_key_without_a_caller_key(
    tool: str, schemas: dict[str, dict[str, Any]]
) -> None:
    route = respx.route(host="api.test.com").mock(
        return_value=httpx.Response(201, json={"id": "x_1"})
    )

    async with Client(mcp) as client:
        await client.call_tool(tool, _required_arguments(schemas[tool]))

    assert route.calls.last.request.headers["Idempotency-Key"].startswith(f"mcp-{tool}-")


@respx.mock
async def test_create_post_retry_with_the_same_key_sends_the_same_header() -> None:
    route = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(201, json={"post": {"_id": "p_1"}})
    )
    arguments = {
        "content": "Spring sale",
        "scheduled_for": "2026-12-01T10:00:00Z",
        "platforms": [{"platform": "facebook", "accountId": "acc_1"}],
        "idempotency_key": CALLER_KEY,
    }

    async with Client(mcp) as client:
        await client.call_tool("posts_create_post", arguments)
        await client.call_tool("posts_create_post", arguments)

    keys = [call.request.headers["Idempotency-Key"] for call in route.calls]
    assert keys == [CALLER_KEY, CALLER_KEY]
    assert route.calls.last.request.read()  # body still sent alongside the header


def test_sdk_create_post_sends_the_header() -> None:
    with respx.mock:
        route = respx.post(f"{API}/v1/posts").mock(
            return_value=httpx.Response(201, json={})
        )
        Late(api_key="k", base_url=API).posts.create_post(
            content="x", idempotency_key=CALLER_KEY
        )

    assert route.calls.last.request.headers["Idempotency-Key"] == CALLER_KEY
