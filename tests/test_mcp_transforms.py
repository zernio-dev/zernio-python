"""Tests for the MCP search-transform hardening (lenient call_tool + ads aliases)."""

import pytest

fastmcp = pytest.importorskip("fastmcp")

from late.mcp.transforms import (  # noqa: E402
    LegacyAdsAliasTransform,
    coerce_arguments,
    legacy_ads_candidates,
)


class TestCoerceArguments:
    def test_dict_passes_through(self) -> None:
        assert coerce_arguments({"limit": 5}) == {"limit": 5}

    def test_none_passes_through(self) -> None:
        assert coerce_arguments(None) is None

    def test_json_string_is_parsed(self) -> None:
        assert coerce_arguments('{"limit": 5}') == {"limit": 5}

    def test_empty_string_becomes_none(self) -> None:
        assert coerce_arguments("") is None
        assert coerce_arguments("   ") is None

    def test_invalid_json_string_raises(self) -> None:
        with pytest.raises(ValueError, match="not valid JSON"):
            coerce_arguments("{limit: 5}")

    def test_non_object_json_string_raises(self) -> None:
        with pytest.raises(ValueError, match="must be a JSON object"):
            coerce_arguments("[1, 2]")


class TestLegacyAdsCandidates:
    def test_plain_suffix_maps_to_every_split_resource(self) -> None:
        candidates = legacy_ads_candidates("list_ads")
        assert "ad_campaigns_list_ads" in candidates
        assert "ad_insights_list_ads" in candidates

    def test_resource_prefixed_suffix_adds_collapsed_candidate(self) -> None:
        # Generator collapses `conversions_conversions_*` to `conversions_*`,
        # so old `ads_conversions_send_x` must also try `conversions_send_x`.
        candidates = legacy_ads_candidates("conversions_send_x")
        assert "conversions_send_x" in candidates


class TestLegacyAdsAliasTransform:
    @staticmethod
    def _call_next_returning(known: dict[str, object]):
        async def call_next(name: str, *, version=None):
            return known.get(name)

        return call_next

    async def test_known_name_untouched(self) -> None:
        transform = LegacyAdsAliasTransform()
        sentinel = object()
        call_next = self._call_next_returning({"posts_list": sentinel})
        assert await transform.get_tool("posts_list", call_next) is sentinel

    async def test_legacy_ads_name_resolves_to_split_resource(self) -> None:
        transform = LegacyAdsAliasTransform()
        sentinel = object()
        call_next = self._call_next_returning({"ad_campaigns_list_ads": sentinel})
        assert await transform.get_tool("ads_list_ads", call_next) is sentinel

    async def test_unknown_legacy_name_returns_none(self) -> None:
        transform = LegacyAdsAliasTransform()
        call_next = self._call_next_returning({})
        assert await transform.get_tool("ads_nonexistent", call_next) is None

    async def test_non_ads_unknown_name_not_aliased(self) -> None:
        transform = LegacyAdsAliasTransform()
        sentinel = object()
        call_next = self._call_next_returning({"ad_campaigns_list_bogus": sentinel})
        assert await transform.get_tool("list_bogus", call_next) is None


class TestServerWiring:
    async def test_call_tool_schema_accepts_string_arguments(self) -> None:
        """The proxied call_tool must validate stringified arguments (broken
        clients like Cowork send `{"limit": 5}` as a string) instead of
        rejecting them with a dict-vs-string schema error."""
        from fastmcp import Client

        from late.mcp.server import mcp

        async with Client(mcp) as client:
            # A synthetic-tool target trips the guard AFTER schema validation,
            # proving the string form got past the schema without executing
            # any real (network-touching) tool.
            with pytest.raises(Exception, match="synthetic"):
                await client.call_tool(
                    "call_tool",
                    {"name": "search_tools", "arguments": '{"query": "x"}'},
                )

    async def test_ads_read_tools_are_pinned(self) -> None:
        from fastmcp import Client

        from late.mcp.server import mcp

        async with Client(mcp) as client:
            visible = {t.name for t in await client.list_tools()}
        assert {
            "ad_campaigns_get_ad_tree",
            "ad_campaigns_list_ad_campaigns",
            "ad_campaigns_list_ads",
            "ad_insights_get_campaign_analytics",
        } <= visible
