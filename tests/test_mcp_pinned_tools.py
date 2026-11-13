from __future__ import annotations

from fastmcp import Client

from late.mcp import server


async def test_every_pinned_name_is_a_registered_tool() -> None:
    registered = {t.name for t in await server.mcp.list_tools(run_middleware=False)}

    assert [name for name in server._PINNED_TOOLS if name not in registered] == []


async def test_the_inbox_and_media_url_reads_are_listed_without_a_search() -> None:
    listed = {t.name for t in await server.mcp.list_tools()}

    assert {
        "messages_list_inbox_conversations",
        "messages_get_inbox_conversation_messages",
        "media_get_media_presigned_url",
    } <= listed


async def test_an_unpinned_tool_is_found_by_search_and_not_listed_up_front() -> None:
    listed = {t.name for t in await server.mcp.list_tools()}
    async with Client(server.mcp) as client:
        result = await client.call_tool("search_tools", {"query": "list queue slots"})

    assert "queue_list_queue_slots" not in listed
    assert "queue_list_queue_slots" in result.content[0].text


async def test_agents_that_call_a_newly_pinned_tool_through_call_tool_still_reach_it() -> (
    None
):
    async with Client(server.mcp) as client:
        result = await client.call_tool(
            "call_tool",
            {"name": "messages_get_inbox_conversation_messages", "arguments": {}},
            raise_on_error=False,
        )

    assert "Unknown tool" not in result.content[0].text
    assert "conversation_id" in result.content[0].text
