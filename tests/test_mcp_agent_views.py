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
            "schema": {"type": "string", "enum": ["full", "summary"], "default": "full"},
            "description": "full returns everything.",
        }
    ],
}


@pytest.fixture
def mcp_generator(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("generate_mcp_tools")


def test_analytics_listing_defaults_to_the_summary_view_for_agents(mcp_generator) -> None:
    params = mcp_generator._with_agent_view("getAnalytics", mcp_generator.extract_parameters(ANALYTICS_OPERATION, {}))
    handler = mcp_generator.generate_tool_handler(
        "analytics_get_analytics", "analytics", "get_analytics", "Get analytics", params, True, "Get analytics"
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
