"""
Regression tests for zernio-claude-plugin#3: accounts_list failed pydantic
validation whenever the connected-account list contained a `phone` account.

GET /v1/accounts returns every SocialAccount on the profile, including the
telephony platforms (`phone`, `sms`, `rcs`) that back the Phone Numbers
product. The generated SocialAccount platform enum only listed the social and
ads platforms, so `AccountsListResponse.model_validate` raised
`accounts.N.platform ... [type=enum, input_value=phone]` and the MCP core tool
errored while the raw passthrough tool (accounts_list_accounts, untyped dict)
kept working.

These tests drive the real typed SDK path (httpx.MockTransport, no network)
with a payload containing a phone account, exactly the shape that failed in
production.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

import late.client.base as client_base
from late import Late
from late.mcp import server as mcp_server
from late.models import AccountsListResponse

PHONE_ACCOUNT = {
    "_id": "a-phone",
    "platform": "phone",
    "profileId": "prof_1",
    "username": "+14155551234",
    "displayName": "Support line",
    "isActive": True,
}

ACCOUNTS_PAYLOAD = {
    "accounts": [
        {
            "_id": "a-ig",
            "platform": "instagram",
            "profileId": "prof_1",
            "username": "acme",
            "isActive": True,
        },
        PHONE_ACCOUNT,
        {
            "_id": "a-sms",
            "platform": "sms",
            "profileId": "prof_1",
            "username": "+14155550000",
            "isActive": True,
        },
    ],
    "hasAnalyticsAccess": False,
}


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Late:
    """Route all SDK HTTP traffic to a fake accounts API and wire up MCP."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and request.url.path == "/api/v1/accounts":
            return httpx.Response(
                200,
                content=json.dumps(ACCOUNTS_PAYLOAD),
                headers={"Content-Type": "application/json"},
            )
        return httpx.Response(404, json={"error": f"unexpected: {request.url.path}"})

    real_client = httpx.Client

    def patched_client(**kwargs: Any) -> httpx.Client:
        kwargs["transport"] = httpx.MockTransport(handler)
        return real_client(**kwargs)

    monkeypatch.setattr(client_base.httpx, "Client", patched_client)
    late = Late(api_key="test-key")
    monkeypatch.setattr(mcp_server, "_get_client", lambda: late)
    return late


@pytest.mark.parametrize("platform", ["phone", "sms", "rcs"])
def test_response_model_accepts_telephony_platforms(platform: str) -> None:
    payload = {
        "accounts": [{**PHONE_ACCOUNT, "platform": platform}],
        "hasAnalyticsAccess": False,
    }
    response = AccountsListResponse.model_validate(payload)
    assert response.accounts[0].platform.value == platform


def test_typed_list_preserves_phone_account_fields(client: Late) -> None:
    response = client.accounts.list()

    assert isinstance(response, AccountsListResponse)
    assert len(response.accounts) == 3
    phone = next(a for a in response.accounts if a.platform.value == "phone")
    assert phone.field_id == "a-phone"
    assert phone.username == "+14155551234"
    assert phone.displayName == "Support line"
    assert phone.isActive is True


@pytest.mark.usefixtures("client")
def test_mcp_accounts_list_returns_all_accounts() -> None:
    result = mcp_server.accounts_list()

    assert "validation error" not in result
    assert "Found 3 connected account(s)" in result
    assert "phone: +14155551234 (ID: a-phone)" in result
    assert "instagram: acme (ID: a-ig)" in result
