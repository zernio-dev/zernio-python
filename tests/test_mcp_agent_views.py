from __future__ import annotations

import importlib
from pathlib import Path

import pytest

ANALYTICS_OPERATION = {
    "operationId": "getAnalytics",
    "parameters": [
        {
            "name": "view",
            "in": "query",
            "schema": {
                "type": "string",
                "enum": ["full", "summary"],
                "default": "full",
            },
            "description": "full returns everything.",
        }
    ],
}


@pytest.fixture
def mcp_generator(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("generate_mcp_tools")


def test_analytics_listing_defaults_to_the_summary_view_for_agents(
    mcp_generator,
) -> None:
    params = mcp_generator._with_agent_view(
        "getAnalytics", mcp_generator.extract_parameters(ANALYTICS_OPERATION, {})
    )
    handler = mcp_generator.generate_tool_handler(
        "analytics_get_analytics",
        "analytics",
        "get_analytics",
        "Get analytics",
        params,
        True,
        "Get analytics",
    )

    assert "view: Literal['full', 'summary'] = \"summary\"" in handler
    assert "view=view" in handler
    assert "Defaults to summary here" in handler


def test_a_spec_without_the_view_parameter_warns_instead_of_silently_skipping(
    mcp_generator, capsys: pytest.CaptureFixture[str]
) -> None:
    params = mcp_generator._with_agent_view("getAnalytics", [])

    assert params == []
    assert "getAnalytics has no `view` parameter" in capsys.readouterr().err


def _operation(operation_id: str, name: str, values: list[str], default: str) -> dict:
    return {
        "operationId": operation_id,
        "parameters": [
            {
                "name": name,
                "in": "query",
                "schema": {"type": "string", "enum": values, "default": default},
                "description": "How much to return.",
            }
        ],
    }


@pytest.mark.parametrize("operation_id", ["listAds", "listAdSets", "listPosts", "getInboxPostComments", "listInboxComments"])
def test_listings_default_to_the_summary_view_for_agents(
    mcp_generator, operation_id: str
) -> None:
    operation = _operation(operation_id, "view", ["full", "summary"], "full")
    params = mcp_generator._with_agent_view(
        operation_id, mcp_generator.extract_parameters(operation, {})
    )

    assert params[0]["default"] == '"summary"'
    assert params[0]["description"].endswith(
        "Defaults to summary here; pass full for everything."
    )


def test_the_ads_tree_defaults_to_campaign_depth_and_says_how_to_drill_down(
    mcp_generator,
) -> None:
    operation = _operation("getAdTree", "depth", ["campaign", "adset", "ad"], "ad")
    params = mcp_generator._with_agent_view(
        "getAdTree", mcp_generator.extract_parameters(operation, {})
    )
    handler = mcp_generator.generate_tool_handler(
        "ads_get_ad_tree",
        "ads",
        "get_ad_tree",
        "Get ad tree",
        params,
        True,
        "Get ad tree",
    )

    assert "depth: Literal['campaign', 'adset', 'ad'] = \"campaign\"" in handler
    assert (
        "Defaults to campaign here; pass adset with campaign_id for one campaign's ad sets, or ad for everything."
        in handler
    )


def test_a_tree_spec_without_the_depth_parameter_warns_and_keeps_its_parameters(
    mcp_generator, capsys: pytest.CaptureFixture[str]
) -> None:
    other = {"name": "page", "description": "Page.", "default": "1"}

    assert mcp_generator._with_agent_view("getAdTree", [other]) == [other]
    assert "getAdTree has no `depth` parameter" in capsys.readouterr().err
