"""API text cut in the middle of an emoji must still reach the client: a lone
surrogate in a tool result made the streamable HTTP writer fail to encode it."""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.middleware.well_formed_output import well_formed
from late.mcp.server import mcp

HALF_EMOJI_BODY = b'{"messages":[{"text":"Great launch \\ud83d"}]}'


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


def test_lone_surrogate_becomes_replacement_character() -> None:
    assert well_formed("Great launch \ud83d") == "Great launch �"


def test_split_surrogate_pair_is_rejoined() -> None:
    assert well_formed("🚀") == "\U0001f680"


def test_well_formed_text_is_unchanged() -> None:
    text = "Great launch \U0001f680 café"
    assert well_formed(text) is text


@respx.mock
async def test_tool_result_with_half_an_emoji_is_utf8_encodable() -> None:
    respx.get(url__startswith="https://api.test.com/").mock(
        return_value=httpx.Response(
            200, content=HALF_EMOJI_BODY, headers={"content-type": "application/json"}
        )
    )

    async with Client(mcp) as client:
        result = await client.call_tool(
            "messages_get_inbox_conversation_messages",
            {"conversation_id": "conv_1", "account_id": "acc_1"},
        )

    text = result.content[0].text
    text.encode("utf-8")
    assert "Great launch �" in text


@respx.mock
async def test_tool_error_with_half_an_emoji_is_utf8_encodable() -> None:
    respx.get(url__startswith="https://api.test.com/").mock(
        return_value=httpx.Response(
            400,
            content=b'{"error":"Bad caption \\ud83d"}',
            headers={"content-type": "application/json"},
        )
    )

    async with Client(mcp) as client:
        result = await client.call_tool(
            "messages_get_inbox_conversation_messages",
            {"conversation_id": "conv_1", "account_id": "acc_1"},
            raise_on_error=False,
        )

    assert result.is_error
    text = result.content[0].text
    text.encode("utf-8")
    assert "Bad caption �" in text
