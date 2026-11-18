"""The BM25 synthetic meta-tools must carry ToolAnnotations.

fastmcp builds search_tools/call_tool without annotations (still true in
3.4.4, 3.4.5 and 4.0.0b1). Clients that gate approval on hints then treat
them as needing confirmation: codex-cli auto-denies unannotated tools in
non-interactive `codex exec` runs and reports "user cancelled MCP tool call".

These assertions are also the canary for the private-method override in
_AnnotatedBM25SearchTransform: if a fastmcp upgrade renames _make_search_tool
or _make_call_tool, the overrides become dead code and this test fails loudly
instead of the annotations silently disappearing from tools/list.
"""

from late.mcp.server import mcp


async def _synthetic_tools():
    transform, _ = mcp.transforms
    return {t.name: t for t in await transform.transform_tools([])}


async def test_search_tools_is_annotated_read_only():
    annotations = (await _synthetic_tools())["search_tools"].annotations

    assert annotations is not None
    assert annotations.read_only_hint is True
    assert annotations.destructive_hint is False
    assert annotations.open_world_hint is False


async def test_call_tool_is_annotated_destructive():
    # The proxy can dispatch to any hidden tool, including writes to external
    # platforms, so it must not claim to be read-only.
    annotations = (await _synthetic_tools())["call_tool"].annotations

    assert annotations is not None
    assert annotations.read_only_hint is False
    assert annotations.destructive_hint is True
    assert annotations.open_world_hint is True
