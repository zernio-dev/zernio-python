"""A generated tool whose API call fails must come back as an MCP error, so an
agent cannot read a rejected write as a success."""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp

SAFETY_REJECTION = (
    "This Direct Message was not sent because it did not pass a safety check."
)


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


@respx.mock
async def test_rejected_dm_through_call_tool_is_an_mcp_error() -> None:
    respx.post("https://api.test.com/v1/inbox/conversations").mock(
        return_value=httpx.Response(403, json={"error": SAFETY_REJECTION})
    )

    async with Client(mcp) as client:
        result = await client.call_tool(
            "call_tool",
            {
                "name": "messages_create_inbox_conversation",
                "arguments": {
                    "account_id": "acc_1",
                    "participant_username": "someone",
                    "message": "Hey",
                },
            },
            raise_on_error=False,
        )

    assert result.is_error
    assert "[403]" in result.content[0].text
    assert SAFETY_REJECTION in result.content[0].text
