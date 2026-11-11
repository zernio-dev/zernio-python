"""Main-server tools return their text once: no automatic {"result": string}
output schema, so no structuredContent repeating the same text."""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


async def test_no_main_server_tool_declares_an_output_schema() -> None:
    tools = await mcp._local_provider.list_tools()

    assert tools
    assert [t.name for t in tools if t.output_schema] == []


@respx.mock
async def test_a_tool_result_is_sent_as_text_only() -> None:
    respx.get(url__startswith="https://api.test.com/v1/ads").mock(
        return_value=httpx.Response(200, json={"ads": [{"name": "Spring sale"}]})
    )

    async with Client(mcp) as client:
        result = await client.call_tool_mcp(
            "call_tool", {"name": "ad_campaigns_list_ads", "arguments": {}}
        )

    assert not result.isError
    assert result.structuredContent is None
    [block] = result.content
    assert "Spring sale" in block.text
