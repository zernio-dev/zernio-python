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


_NESTED_REFUSAL = "call_tool runs other tools; don't wrap call_tool in itself."


@pytest.mark.parametrize(
    "inner",
    [
        {"name": "posts_list", "arguments": {"limit": 5}},
        {"name": "call_tool", "arguments": {"name": "posts_list", "arguments": {}}},
    ],
    ids=["one-level", "two-levels"],
)
async def test_call_tool_wrapped_in_itself_names_the_tool_to_call(inner):
    is_error, text = await _call("call_tool", {"name": "call_tool", "arguments": inner})

    assert is_error
    assert text == (
        f"{_NESTED_REFUSAL} Call call_tool with name='posts_list' and its arguments directly."
    )


async def test_call_tool_wrapped_around_a_search_points_to_search_tools():
    is_error, text = await _call(
        "call_tool",
        {
            "name": "call_tool",
            "arguments": {"name": "search_tools", "arguments": {"query": "posts"}},
        },
    )

    assert is_error
    assert text == f"{_NESTED_REFUSAL} Call search_tools directly with its arguments."


@pytest.mark.parametrize(
    "arguments",
    [
        {"name": "call_tool"},
        {"name": "call_tool", "arguments": {}},
        {"name": "call_tool", "arguments": {"name": "  "}},
        {"name": "call_tool", "arguments": {"name": "call_tool"}},
    ],
    ids=["no-arguments", "empty-arguments", "blank-name", "only-call-tool"],
)
async def test_call_tool_wrapped_in_itself_without_an_inner_tool_points_to_search(arguments):
    is_error, text = await _call("call_tool", arguments)

    assert is_error
    assert text == (
        f"{_NESTED_REFUSAL} Call search_tools with what you want to do, "
        "then call_tool with the exact name it returns."
    )


async def test_the_instructions_explain_how_to_find_tools():
    async with Client(mcp) as client:
        instructions = client.instructions

    assert "FINDING TOOLS" in instructions
    assert "Never guess tool names" in instructions
