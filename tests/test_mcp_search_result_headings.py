"""In search_tools results, a `### ` line must only ever start a tool.

Tool descriptions carry their own headings ("### Platform support"). Left as-is in the flat markdown, a client
that splits results on headings read them as tools and attached messages_create_inbox_conversation's
participant_id/participant_username to messages_send_inbox_message (Grok client, 2026-11-17).
"""

import re

from fastmcp import Client

from late.mcp.server import mcp


async def _search(query: str) -> str:
    async with Client(mcp) as client:
        result = await client.call_tool("search_tools", {"query": query})
    return "\n".join(getattr(item, "text", "") for item in result.content)


async def test_every_result_heading_is_a_tool_name():
    for query in ("send message", "reply to conversation", "inbox message"):
        text = await _search(query)
        headings = re.findall(r"^### (.+)$", text, re.MULTILINE)
        assert headings, query
        assert all(re.fullmatch(r"[a-z0-9_]+", heading) for heading in headings), (
            query,
            headings,
        )


async def test_send_inbox_message_section_lists_its_own_parameters():
    text = await _search("send message")
    section = re.search(
        r"^### messages_send_inbox_message\n(.*?)(?=^### |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert section is not None
    params = re.findall(r"^- `([a-z_]+)`", section.group(1), re.MULTILINE)
    assert params[:3] == ["conversation_id", "account_id", "message"]
    assert "participant_id" not in params
    assert "**Platform support**" in text or "Platform support" not in text
