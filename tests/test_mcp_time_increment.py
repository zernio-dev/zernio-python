"""`timeIncrement` is "1 to 90 days per row, or monthly / all_days". The API
body schema is `union([enum, int])` with no coercion, so the tool must send a
JSON number for days: typed as `str`, it rejected `7` and forwarded `"7"`,
which the API answered with a 400."""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp

TOOLS = {
    "metrics_query_meta_ads": (
        "https://api.test.com/v1/metrics/platform-queries/meta-ads",
        {"account_id": "acc_1", "ad_account_id": "act_1"},
    ),
    "ad_insights_create_ad_insights_report": (
        "https://api.test.com/v1/ads/insights/reports",
        {"account_id": "acc_1", "object_id": "act_1"},
    ),
}


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


async def _call(tool: str, time_increment: object) -> tuple[bool, str, list[dict]]:
    url, arguments = TOOLS[tool]
    with respx.mock:
        route = respx.post(url).mock(return_value=httpx.Response(200, json={"data": []}))
        async with Client(mcp) as client:
            result = await client.call_tool(
                "call_tool",
                {"name": tool, "arguments": {**arguments, "time_increment": time_increment}},
                raise_on_error=False,
            )
        bodies = [json.loads(call.request.content) for call in route.calls]
    return result.is_error, result.content[0].text, bodies


@pytest.mark.parametrize("tool", TOOLS)
@pytest.mark.parametrize(
    ("given", "sent"),
    [(1, 1), (90, 90), ("1", 1), ("7", 7), ("monthly", "monthly"), ("all_days", "all_days")],
)
async def test_time_increment_reaches_the_api_as_number_or_enum(tool: str, given: object, sent: object) -> None:
    is_error, text, bodies = await _call(tool, given)

    assert not is_error, text
    assert len(bodies) == 1
    assert bodies[0]["timeIncrement"] == sent
    assert type(bodies[0]["timeIncrement"]) is type(sent)


@pytest.mark.parametrize("tool", TOOLS)
@pytest.mark.parametrize("given", ["weekly", "", 1.5, "seven"])
async def test_invalid_time_increment_is_rejected_before_the_api(tool: str, given: object) -> None:
    is_error, text, bodies = await _call(tool, given)

    assert is_error
    assert "time_increment" in text
    assert bodies == []


@pytest.mark.parametrize("tool", TOOLS)
async def test_time_increment_schema_lists_integer_and_enum(tool: str) -> None:
    schema = (await mcp.get_tool(tool)).parameters["properties"]["time_increment"]

    branches = schema["anyOf"]
    assert {"type": "integer"} in branches
    assert {"type": "string", "enum": ["monthly", "all_days"]} in branches
