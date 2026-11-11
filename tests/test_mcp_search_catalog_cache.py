import json

import pytest
from fastmcp import Client
from fastmcp.server.transforms.search import BM25SearchTransform, bm25

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
    return [tool["name"] for tool in json.loads(result.content[0].text)]


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
