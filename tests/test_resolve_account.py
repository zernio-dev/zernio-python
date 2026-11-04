from __future__ import annotations

import httpx
import pytest
import respx

from late import Late
from late.mcp.server import _resolve_account

API = "https://api.test.com"


def _account(account_id: str, platform: str = "twitter", username: str = "") -> dict:
    return {
        "_id": account_id,
        "platform": platform,
        "username": username,
        "profileId": "prof_1",
        "isActive": True,
    }


def _page(accounts: list[dict], next_cursor: str | None = None) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "accounts": accounts,
            "hasAnalyticsAccess": False,
            "pagination": {"limit": 25, "nextCursor": next_cursor},
        },
    )


@pytest.fixture
def client() -> Late:
    return Late(api_key="test-key", base_url=API)


@respx.mock
def test_account_id_is_used_as_given_without_any_lookup(client: Late) -> None:
    route = respx.get(f"{API}/v1/accounts")

    target = _resolve_account(client, "Twitter", account_id="acc_2")

    assert target.field_id == "acc_2"
    assert target.platform == "twitter"
    assert route.call_count == 0


@respx.mock
def test_platform_lookup_filters_on_the_server_and_bounds_the_page(
    client: Late,
) -> None:
    route = respx.get(f"{API}/v1/accounts").mock(
        return_value=_page([_account("acc_1", username="acme")])
    )

    target = _resolve_account(client, "Twitter")

    assert target.field_id == "acc_1"
    assert route.call_count == 1
    assert dict(route.calls.last.request.url.params) == {
        "platform": "twitter",
        "limit": "25",
    }


@respx.mock
def test_profile_id_scopes_the_lookup(client: Late) -> None:
    route = respx.get(f"{API}/v1/accounts").mock(
        return_value=_page([_account("acc_p1")])
    )

    target = _resolve_account(client, "twitter", profile_id="prof_acme")

    assert target.field_id == "acc_p1"
    assert route.call_count == 1
    assert route.calls.last.request.url.params["profileId"] == "prof_acme"


@respx.mock
def test_ambiguous_selection_lists_every_candidate(client: Late) -> None:
    respx.get(f"{API}/v1/accounts").mock(
        return_value=_page(
            [
                _account("acc_1", username="acme"),
                _account("acc_2", username="beta"),
            ]
        )
    )

    with pytest.raises(ValueError) as exc_info:
        _resolve_account(client, "twitter")

    message = str(exc_info.value)
    assert "Multiple twitter accounts" in message
    assert "acc_1" in message and "acc_2" in message
    assert "acme" in message and "beta" in message
    assert "only the first" not in message


@respx.mock
def test_ambiguous_selection_in_a_huge_workspace_says_the_list_is_cut(
    client: Late,
) -> None:
    respx.get(f"{API}/v1/accounts").mock(
        return_value=_page(
            [_account(f"acc_{i}") for i in range(25)],
            next_cursor="v1.more",
        )
    )

    with pytest.raises(ValueError, match="only the first 25") as exc_info:
        _resolve_account(client, "twitter")

    assert "search or profile_id" in str(exc_info.value)


@respx.mock
def test_no_match_without_profile_spends_no_second_request(client: Late) -> None:
    route = respx.get(f"{API}/v1/accounts").mock(return_value=_page([]))

    with pytest.raises(ValueError, match="No twitter account found"):
        _resolve_account(client, "twitter")

    assert route.call_count == 1


@respx.mock
def test_no_match_in_a_profile_names_the_platforms_it_does_have(client: Late) -> None:
    route = respx.get(f"{API}/v1/accounts").mock(
        side_effect=[_page([]), _page([_account("acc_p", platform="linkedin")])]
    )

    with pytest.raises(
        ValueError, match="in profile prof_x. Available platforms: linkedin"
    ):
        _resolve_account(client, "twitter", profile_id="prof_x")

    assert route.call_count == 2
    assert "platform" not in route.calls.last.request.url.params


@pytest.mark.parametrize(
    "platform",
    [
        "facebook",
        "instagram",
        "metaads",
        "tiktok",
        "linkedin",
        "youtube",
        "twitter",
        "pinterest",
        "shopify",
        "threads",
        "wordpress",
        "reddit",
        "googlebusiness",
        "whatsapp",
    ],
)
@respx.mock
def test_the_real_response_shape_parses_for_every_platform_a_big_workspace_holds(
    client: Late, platform: str
) -> None:
    row = {
        "_id": "6a3e870a9d9472faaef39608",
        "userId": "6a2661ef2994be396ea2e335",
        "profileId": {
            "_id": "6a3e86edff60ac2caa0a6252",
            "name": "Gemma",
            "externalId": None,
        },
        "platform": platform,
        "platformUserId": "abc",
        "username": "acme",
        "displayName": "Acme",
        "profilePicture": None,
        "isActive": True,
        "metadata": {"accountType": "personal"},
        "enabled": True,
        "adsStatus": "connected",
        "byokCredentials": {"isActive": False},
    }
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(
            200,
            json={
                "accounts": [row],
                "hasAnalyticsAccess": True,
                "pagination": {
                    "limit": 25,
                    "nextCursor": "v1.WyI2YTNlODcwYTlkOTQ3MmZhYWVmMzk2MDgiXQ",
                },
            },
        )
    )

    response = client.accounts.list(platform=platform, limit=25)

    assert response.accounts[0].field_id == row["_id"]
    assert response.pagination.nextCursor == "v1.WyI2YTNlODcwYTlkOTQ3MmZhYWVmMzk2MDgiXQ"
    assert _resolve_account(client, platform).field_id == row["_id"]
