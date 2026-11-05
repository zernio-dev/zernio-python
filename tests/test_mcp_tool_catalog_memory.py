from fastmcp.utilities.types import get_cached_typeadapter
from uncalled_for.introspection import _parameter_cache, _signature_cache

from late.mcp.server import mcp


def _retained_function_count() -> tuple[int, int, int]:
    return (
        get_cached_typeadapter.cache_info().currsize,
        len(_signature_cache),
        len(_parameter_cache),
    )


async def test_listing_tools_retains_nothing_per_request():
    await mcp.list_tools()
    before = _retained_function_count()

    for _ in range(5):
        await mcp.list_tools()

    assert _retained_function_count() == before


async def test_resolving_synthetic_tools_retains_nothing_per_request():
    await mcp.get_tool("search_tools")
    await mcp.get_tool("call_tool")
    before = _retained_function_count()

    for _ in range(5):
        await mcp.get_tool("search_tools")
        await mcp.get_tool("call_tool")

    assert _retained_function_count() == before


async def test_listing_and_resolving_serve_the_same_synthetic_tools():
    listed = {t.name: t for t in await mcp.list_tools()}

    assert listed["search_tools"].fn is (await mcp.get_tool("search_tools")).fn
    assert listed["call_tool"].fn is (await mcp.get_tool("call_tool")).fn
