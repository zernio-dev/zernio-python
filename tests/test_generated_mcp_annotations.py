"""Hints and OAuth scopes the generator puts on every tool.

OpenAI's plugin review checks readOnlyHint, destructiveHint and openWorldHint
on each tool, and ChatGPT asks for the OAuth scope a tool declares.
"""

from __future__ import annotations

import asyncio
import importlib
from pathlib import Path

import pytest
from fastmcp import FastMCP

from late.mcp.generated_tools import TOOL_OAUTH_SCOPE, register_generated_tools


@pytest.fixture(scope="module")
def generator():
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    try:
        yield importlib.import_module("generate_mcp_tools")
    finally:
        sys.path.pop(0)


@pytest.fixture(scope="module")
def tools():
    server = FastMCP("generated")
    register_generated_tools(server, lambda: None)
    return {tool.name: tool for tool in asyncio.run(server.list_tools())}


def test_a_read_declares_the_read_scope_and_a_write_the_write_scope(generator):
    both = ["posts:read", "posts:write"]

    assert generator.declared_oauth_scope(both, True) == "posts:read"
    assert generator.declared_oauth_scope(both, False) == "posts:write"
    assert (
        generator.declared_oauth_scope(["messaging:write"], True) == "messaging:write"
    )
    assert generator.declared_oauth_scope([], True) is None


def test_a_post_that_only_queries_is_read_only(tools):
    hints = tools["metrics_query_meta_ads"].annotations

    assert hints.readOnlyHint is True
    assert hints.destructiveHint is False
    assert hints.openWorldHint is False


def test_a_search_of_public_content_is_open_world(tools):
    hints = tools["reddit_search_reddit"].annotations

    assert hints.readOnlyHint is True
    assert hints.openWorldHint is True


def test_a_send_is_a_destructive_open_world_write(tools):
    hints = tools["messages_send_inbox_message"].annotations

    assert hints.readOnlyHint is False
    assert hints.destructiveHint is True
    assert hints.openWorldHint is True


def test_every_tool_sets_all_three_hints(tools):
    for name, tool in tools.items():
        hints = tool.annotations
        assert isinstance(hints.readOnlyHint, bool), name
        assert isinstance(hints.destructiveHint, bool), name
        assert isinstance(hints.openWorldHint, bool), name


def test_the_inbox_needs_the_messaging_scope():
    assert TOOL_OAUTH_SCOPE["messages_list_inbox_conversations"] == "messaging:write"
    assert TOOL_OAUTH_SCOPE["accounts_get_account_health"] == "accounts:read"
