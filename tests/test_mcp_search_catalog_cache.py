import json
import re

import pytest
from fastmcp import Client
from fastmcp.server.transforms.search import BM25SearchTransform, bm25
from fastmcp.server.transforms.search.base import serialize_tools_for_output_json

from late.mcp.server import mcp

QUERIES = [
    "create a post",
    "list inbox conversation messages",
    "get comments on a post",
    "ad campaigns",
]


@pytest.fixture
def transform(monkeypatch):
    (transform,) = mcp.transforms
    monkeypatch.setattr(transform, "_visible_tools", None, raising=False)
    monkeypatch.setattr(transform, "_indexed_tools", ())
    monkeypatch.setattr(transform, "_last_hash", "")
    return transform


async def _search_names(client: Client, query: str) -> list[str]:
    result = await client.call_tool("search_tools", {"query": query})
    # Tool blocks start with "### <snake_case_name>"; descriptions can hold
    # their own ### headings, which are never snake_case.
    return re.findall(
        r"^### ([a-z0-9]+(?:_[a-z0-9]+)+)$", result.content[0].text, re.MULTILINE
    )


async def test_repeated_searches_read_the_tool_catalog_once(transform, monkeypatch):
    reads = 0
    read_catalog = transform.get_tool_catalog

    async def counting_read(ctx):
        nonlocal reads
        reads += 1
        return await read_catalog(ctx)

    monkeypatch.setattr(transform, "get_tool_catalog", counting_read)

    async with Client(mcp) as client:
        for query in QUERIES * 3:
            await _search_names(client, query)

    assert reads == 1


@pytest.mark.usefixtures("transform")
async def test_repeated_searches_hash_the_tool_catalog_once(monkeypatch):
    hashes = 0
    hash_catalog = bm25._catalog_hash

    def counting_hash(tools):
        nonlocal hashes
        hashes += 1
        return hash_catalog(tools)

    monkeypatch.setattr(bm25, "_catalog_hash", counting_hash)

    async with Client(mcp) as client:
        for query in QUERIES * 3:
            await _search_names(client, query)

    assert hashes == 1


async def test_cached_search_ranks_tools_like_fastmcp(transform):
    uncached = BM25SearchTransform(max_results=transform._max_results)

    async with Client(mcp) as client:
        await _search_names(client, QUERIES[0])
        hidden = list(transform._visible_tools)
        assert len(hidden) > 1000

        for query in QUERIES:
            expected = [t.name for t in await uncached._search(hidden, query)]
            assert await _search_names(client, query) == expected


async def test_search_results_are_markdown_and_lighter_than_json(transform):
    async with Client(mcp) as client:
        result = await client.call_tool("search_tools", {"query": QUERIES[1]})
        markdown = result.content[0].text
        tools = await transform._search(transform._visible_tools, QUERIES[1])

    as_json = json.dumps(serialize_tools_for_output_json(tools))
    assert markdown.startswith("### ")
    assert len(markdown) < len(as_json)
