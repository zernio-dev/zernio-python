"""Mixed-type body fields reach the API in the type the agent sent. Typed as
`str`, the tool rejected `advantage_audience=true` and a Flow JSON object."""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp

BASE = "https://api.test.com"


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", BASE)


async def _call(method: str, url: str, tool: str, arguments: dict) -> tuple[bool, str, list[dict]]:
    with respx.mock:
        route = respx.route(method=method, url=url).mock(return_value=httpx.Response(200, json={}))
        async with Client(mcp) as client:
            result = await client.call_tool(
                "call_tool", {"name": tool, "arguments": arguments}, raise_on_error=False
            )
        bodies = [json.loads(call.request.content) for call in route.calls]
    return result.is_error, result.content[0].text, bodies


async def _standalone_ad(advantage_audience: object) -> tuple[bool, str, list[dict]]:
    return await _call(
        "POST",
        f"{BASE}/v1/ads/create",
        "ad_campaigns_create_standalone_ad",
        {"account_id": "acc_1", "ad_account_id": "act_1", "advantage_audience": advantage_audience},
    )


# Pydantic's lax bool reads "true" / "1" as True, which the API maps to 1.
@pytest.mark.parametrize(
    ("given", "sent"), [(True, True), (False, False), (1, 1), (0, 0), ("true", True), ("1", True)]
)
async def test_advantage_audience_keeps_bool_or_int(given: object, sent: object) -> None:
    is_error, text, bodies = await _standalone_ad(given)

    assert not is_error, text
    assert bodies[0]["advantageAudience"] == sent
    assert type(bodies[0]["advantageAudience"]) is type(sent)


AD_CREATORS = {
    "messaging_ads_create_messaging_ad": ("/v1/ads/messaging", {}),
    "messaging_ads_create_call_ad": ("/v1/ads/call", {"phone_number": "+14155550123", "link_url": "https://example.com"}),
    "messaging_ads_create_ctwa_ad": ("/v1/ads/ctwa", {}),
}


@pytest.mark.parametrize("tool", AD_CREATORS)
@pytest.mark.parametrize("given", [True, 1])
async def test_every_messaging_ad_creator_sends_advantage_audience_as_given(tool: str, given: object) -> None:
    path, extra = AD_CREATORS[tool]
    arguments = {"account_id": "acc_1", "ad_account_id": "act_1", "name": "Ad", **extra, "advantage_audience": given}

    is_error, text, bodies = await _call("POST", f"{BASE}{path}", tool, arguments)

    assert not is_error, text
    assert type(bodies[0]["advantageAudience"]) is type(given)


async def test_mailer_contact_object_is_sent_as_an_object() -> None:
    is_error, text, bodies = await _call(
        "POST",
        f"{BASE}/v1/accounts/acc_1/gmb-verifications",
        "gmb_verifications_start_google_business_verification",
        {"account_id": "acc_1", "method": "ADDRESS", "mailer_contact": {"name": "Ana"}},
    )

    assert not is_error, text
    assert bodies[0]["mailerContact"] == {"name": "Ana"}


@pytest.mark.parametrize("given", [2, -1, "maybe"])
async def test_advantage_audience_outside_the_api_values_is_rejected(given: object) -> None:
    is_error, text, bodies = await _standalone_ad(given)

    assert is_error
    assert "advantage_audience" in text
    assert bodies == []


FLOW = {"version": "6.0", "screens": [{"id": "LEAD_FORM", "terminal": True}]}


@pytest.mark.parametrize("given", [FLOW, json.dumps(FLOW)])
async def test_flow_json_is_sent_as_given(given: object) -> None:
    is_error, text, bodies = await _call(
        "PUT",
        f"{BASE}/v1/whatsapp/flows/flow_1/json",
        "whatsapp_flows_upload_whats_app_flow_json",
        {"flow_id": "flow_1", "account_id": "acc_1", "flow_json": given},
    )

    assert not is_error, text
    assert bodies[0]["flow_json"] == given


@pytest.mark.parametrize(
    ("tool", "param", "branches"),
    [
        (
            "ad_campaigns_create_standalone_ad",
            "advantage_audience",
            [{"type": "boolean"}, {"type": "integer", "enum": [0, 1]}],
        ),
        *(
            (tool, "advantage_audience", [{"type": "boolean"}, {"type": "integer", "enum": [0, 1]}])
            for tool in (
                "messaging_ads_create_messaging_ad",
                "messaging_ads_create_call_ad",
                "messaging_ads_create_ctwa_ad",
            )
        ),
        (
            "whatsapp_flows_upload_whats_app_flow_json",
            "flow_json",
            [{"type": "object", "additionalProperties": True}, {"type": "string"}],
        ),
        (
            "gmb_verifications_start_google_business_verification",
            "mailer_contact",
            [{"type": "object", "additionalProperties": True}, {"type": "string"}],
        ),
    ],
)
async def test_schema_lists_both_types(tool: str, param: str, branches: list[dict]) -> None:
    advertised = (await mcp.get_tool(tool)).parameters["properties"][param]["anyOf"]

    for branch in branches:
        assert branch in advertised
