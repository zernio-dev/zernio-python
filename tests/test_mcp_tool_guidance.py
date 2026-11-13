import pytest
from fastmcp import Client

from late.mcp.server import mcp


async def _call(name: str, arguments: dict) -> tuple[bool, str]:
    async with Client(mcp) as client:
        result = await client.call_tool(name, arguments, raise_on_error=False)
    return result.is_error, result.content[0].text


@pytest.mark.parametrize(
    ("guess", "real"),
    [
        ("inbox_list_conversations", "messages_list_inbox_conversations"),
        ("inboxListConversations", "messages_list_inbox_conversations"),
        ("inbox-get-conversation-messages", "messages_get_inbox_conversation_messages"),
        ("ads_list_ads", "ad_campaigns_list_ads"),
        ("comment_automations_list", "comment_automations_list_comment_automations"),
    ],
)
async def test_a_guessed_tool_name_suggests_the_real_tool(guess, real):
    is_error, text = await _call(guess, {})

    assert is_error
    assert f"Unknown tool {guess!r}" in text
    assert real in text


async def test_a_guessed_name_through_call_tool_suggests_the_real_tool():
    is_error, text = await _call(
        "call_tool", {"name": "inbox_list_conversations", "arguments": {}}
    )

    assert is_error
    assert "messages_list_inbox_conversations" in text


async def test_call_tool_runs_a_proxied_search_instead_of_refusing_it():
    is_error, text = await _call(
        "call_tool",
        {"name": "search_tools", "arguments": {"query": "search inbox conversations"}},
    )

    assert not is_error
    assert "messages_search_inbox_conversations" in text


async def test_call_tool_still_refuses_to_call_itself():
    is_error, _ = await _call("call_tool", {"name": "call_tool", "arguments": {}})

    assert is_error


async def test_the_instructions_explain_how_to_find_tools():
    async with Client(mcp) as client:
        instructions = client.initialize_result.instructions

    assert "FINDING TOOLS" in instructions
    assert "Never guess tool names" in instructions
