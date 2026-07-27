"""Hardened variants of FastMCP's search transform for the Zernio server."""

from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp.server.context import Context
from fastmcp.server.transforms import GetToolNext, Transform
from fastmcp.server.transforms.search import BM25SearchTransform
from fastmcp.tools.base import Tool, ToolResult
from fastmcp.utilities.versions import VersionSpec


class LenientCallToolSearchTransform(BM25SearchTransform):
    """BM25 search transform whose call_tool also accepts stringified arguments.

    Some MCP clients (Claude Desktop/Cowork regressions, e.g.
    anthropics/claude-code#26094) serialize object-typed tool parameters as
    JSON strings. The stock call_tool proxy types `arguments` as dict-only,
    so every proxied call from those clients fails schema validation. This
    override widens `arguments` to accept a JSON-encoded string and parses
    it server-side.
    """

    def _make_call_tool(self) -> Tool:
        transform = self

        async def call_tool(
            name: Annotated[str, "The name of the tool to call"],
            arguments: Annotated[
                dict[str, Any] | str | None,
                "Arguments to pass to the tool, as a JSON object. A "
                "JSON-encoded string of that object is also accepted.",
            ] = None,
            ctx: Context = None,  # type: ignore[assignment]
        ) -> ToolResult:
            """Call a tool by name with the given arguments.

            Use this to execute tools discovered via search_tools.
            """
            if name in {transform._call_tool_name, transform._search_tool_name}:
                raise ValueError(
                    f"'{name}' is a synthetic search tool and cannot be "
                    "called via the call_tool proxy"
                )
            return await ctx.fastmcp.call_tool(name, coerce_arguments(arguments))

        return Tool.from_function(fn=call_tool, name=self._call_tool_name)


def coerce_arguments(
    arguments: dict[str, Any] | str | None,
) -> dict[str, Any] | None:
    """Normalize call_tool arguments; raises ValueError on a non-object string."""
    if not isinstance(arguments, str):
        return arguments
    stripped = arguments.strip()
    if not stripped:
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as e:
        raise ValueError(
            "call_tool received `arguments` as a string that is not valid "
            f'JSON: {e}. Pass a JSON object, e.g. {{"limit": 10}}.'
        ) from e
    if not isinstance(parsed, dict):
        raise ValueError(
            "call_tool received `arguments` as a JSON "
            f"{type(parsed).__name__}; it must be a JSON object mapping "
            "parameter names to values."
        )
    return parsed


# Resources the 2026-07 OpenAPI re-tag (API repo #1777) scattered the old
# [Ads] tag into. Old generated MCP tool names were `ads_<op>`; new ones are
# `<resource>_<op>`, with the generator collapsing `<resource>_<resource>_`
# to `<resource>_` (see scripts/generate_mcp_tools.py).
ADS_SPLIT_RESOURCES = (
    "ad_campaigns",
    "ad_accounts",
    "ad_creatives",
    "ad_insights",
    "ad_targeting",
    "conversions",
    "lead_gen",
    "messaging_ads",
    "reach_and_frequency",
)


class LegacyAdsAliasTransform(Transform):
    """Resolve pre-split `ads_*` tool names to their post-re-tag equivalents.

    The re-tag renamed every generated `ads_*` MCP tool with no alias, so
    clients holding pre-split names (cached tool lists, older conversations)
    get `Unknown tool`. Mirrors the deprecated `client.ads.*` forwarding shim
    in late/resources/ads.py, but at the MCP tool-lookup layer.
    """

    async def get_tool(
        self,
        name: str,
        call_next: GetToolNext,
        *,
        version: VersionSpec | None = None,
    ) -> Tool | None:
        tool = await call_next(name, version=version)
        if tool is not None or not name.startswith("ads_"):
            return tool
        for candidate in legacy_ads_candidates(name.removeprefix("ads_")):
            tool = await call_next(candidate, version=version)
            if tool is not None:
                return tool
        return None


def legacy_ads_candidates(suffix: str) -> list[str]:
    """Post-split tool names a legacy `ads_<suffix>` call may map to."""
    candidates = []
    for resource in ADS_SPLIT_RESOURCES:
        candidates.append(f"{resource}_{suffix}")
        if suffix.startswith(f"{resource}_"):
            candidates.append(suffix)
    return candidates
