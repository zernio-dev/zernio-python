from pathlib import Path

import pytest
from fastmcp.utilities.types import get_cached_typeadapter

from late.mcp.server import mcp

REPO_ROOT = Path(__file__).resolve().parent.parent


def _type_adapters_built() -> int:
    return get_cached_typeadapter.cache_info().misses


async def test_listing_tools_builds_no_new_functions_per_request():
    await mcp.list_tools()
    before = _type_adapters_built()

    for _ in range(5):
        await mcp.list_tools()

    assert _type_adapters_built() == before


async def test_resolving_synthetic_tools_builds_no_new_functions_per_request():
    await mcp.get_tool("search_tools")
    await mcp.get_tool("call_tool")
    before = _type_adapters_built()

    for _ in range(5):
        await mcp.get_tool("search_tools")
        await mcp.get_tool("call_tool")

    assert _type_adapters_built() == before


async def test_listing_and_resolving_serve_the_same_synthetic_tools():
    listed = {t.name: t for t in await mcp.list_tools()}

    assert listed["search_tools"].fn is (await mcp.get_tool("search_tools")).fn
    assert listed["call_tool"].fn is (await mcp.get_tool("call_tool")).fn


@pytest.mark.parametrize("dockerfile", ["Dockerfile", "Dockerfile.docker"])
def test_images_cap_glibc_arenas_so_large_responses_do_not_pin_memory(dockerfile):
    assert "ENV MALLOC_ARENA_MAX=2\n" in (REPO_ROOT / dockerfile).read_text()
