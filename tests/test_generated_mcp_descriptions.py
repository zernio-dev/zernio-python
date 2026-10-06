"""Spec context (operation description, x-platforms, enums) must reach MCP tools."""

import asyncio
import importlib
from pathlib import Path
from typing import Any, Literal

import pytest
from fastmcp import FastMCP


@pytest.fixture
def generator(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("generate_mcp_tools")


def _register_probe(generator, operation: dict[str, Any]):
    handler = generator.generate_tool_handler(
        "probe_tool",
        "probe",
        "probe",
        operation["summary"],
        generator.extract_parameters(operation),
        True,
        operation["summary"],
        operation.get("description", ""),
        operation.get("x-platforms", []),
    )
    source = "\n".join(
        ["def register(mcp, _get_client):"]
        + [f"    {line}" if line.strip() else "" for line in handler.split("\n")]
    )
    namespace: dict[str, Any] = {
        "Any": Any,
        "Literal": Literal,
        "ToolAnnotations": __import__("mcp.types").types.ToolAnnotations,
    }
    exec(compile(source, "<generated-probe>", "exec"), namespace)
    mcp = FastMCP("probe")
    namespace["register"](mcp, lambda: None)
    return mcp


GOOGLE_ONLY_OPERATION = {
    "summary": "Read a Google campaign's targeting",
    "description": 'Google only; every other platform returns 501.\nQuotes " and a backslash \\ survive.',
    "x-platforms": ["google"],
    "parameters": [
        {
            "name": "campaignId",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
            "description": "Campaign id",
        },
        {
            "name": "platform",
            "in": "query",
            "schema": {"type": "string", "enum": ["google"]},
        },
    ],
}


def test_tool_description_carries_the_operation_description_and_platforms(generator):
    mcp = _register_probe(generator, GOOGLE_ONLY_OPERATION)
    tool = asyncio.run(mcp.list_tools())[0]

    assert tool.description == (
        "Read a Google campaign's targeting\n\n"
        "Google only; every other platform returns 501.\n"
        'Quotes " and a backslash \\ survive.\n\n'
        "Platforms: google"
    )
    assert (
        tool.parameters["properties"]["campaign_id"]["description"]
        == "Campaign id (required)"
    )


def test_a_value_outside_a_string_enum_is_rejected_before_the_api_is_called(generator):
    mcp = _register_probe(generator, GOOGLE_ONLY_OPERATION)

    with pytest.raises(Exception, match="Input should be 'google'"):
        asyncio.run(
            mcp.call_tool(
                "probe_tool", {"campaign_id": "619014164", "platform": "linkedin"}
            )
        )


def test_long_operation_descriptions_are_capped(generator):
    lines = generator.build_tool_description_lines("Summary", "word " * 1000, [])

    description = "\n".join(lines[2:])
    assert len(description) <= generator.MAX_TOOL_DESCRIPTION_CHARS + len(" ...")
    assert description.endswith(" ...")


def test_non_string_enums_keep_their_plain_type(generator):
    assert generator._string_enum_literal({"type": "integer", "enum": [1, 2]}) is None
    assert generator._string_enum_literal({"type": "string"}) is None
    assert (
        generator._string_enum_literal({"type": "string", "enum": ["a", None]})
        == "Literal['a']"
    )


BULK_OPERATION = {
    "summary": "Pause or resume many campaigns",
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["campaigns"],
                    "properties": {
                        "campaigns": {
                            "type": "array",
                            "description": "Campaigns to update.",
                            "items": {
                                "type": "object",
                                "required": ["platformCampaignId", "platform"],
                                "properties": {
                                    "platformCampaignId": {
                                        "type": "string",
                                        "description": "The campaign id on the ad platform.",
                                    },
                                    "platform": {"type": "string", "enum": ["google", "facebook"]},
                                    "labels": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                    },
                }
            }
        }
    },
}


def test_array_of_objects_params_name_their_item_fields(generator):
    mcp = _register_probe(generator, BULK_OPERATION)
    tool = asyncio.run(mcp.list_tools())[0]

    assert tool.parameters["properties"]["campaigns"]["description"] == (
        "Campaigns to update. Each item is an object with keys: "
        "platformCampaignId (string, required) - The campaign id on the ad platform.; "
        "platform (one of: google, facebook; required); "
        "labels (list of string) (required)"
    )


def test_nested_field_summary_is_empty_for_scalars_and_scalar_lists(generator):
    assert generator.describe_nested_fields({"type": "string"}, {}) == ""
    assert generator.describe_nested_fields({"type": "array", "items": {"type": "string"}}, {}) == ""


def test_object_params_name_their_fields(generator):
    schema = {"type": "object", "properties": {"amount": {"type": "number"}}}
    assert generator.describe_nested_fields(schema, {}) == "Object with keys: amount (number)"
