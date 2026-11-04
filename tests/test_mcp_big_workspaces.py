from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.chatgpt_server import chatgpt_mcp
from late.mcp.server import mcp

API = "https://api.test.com"
POST_RESPONSE = {
    "post": {"_id": "post_1", "content": "hi", "status": "scheduled", "platforms": []},
    "message": "ok",
}


@pytest.fixture(autouse=True)
def _api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


def _account(account_id: str, platform: str = "twitter") -> dict:
    return {
        "_id": account_id,
        "platform": platform,
        "username": "acme",
        "profileId": "prof_1",
        "isActive": True,
    }


def _page(accounts: list[dict], next_cursor: str | None = None) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "accounts": accounts,
            "hasAnalyticsAccess": False,
            "pagination": {"limit": 100, "nextCursor": next_cursor},
        },
    )


async def _text(tool: str, arguments: dict | None = None) -> str:
    async with Client(mcp) as client:
        result = await client.call_tool(tool, arguments or {})
    return result.content[0].text


@respx.mock
async def test_accounts_list_requests_one_bounded_page_and_hands_back_the_cursor() -> (
    None
):
    route = respx.get(f"{API}/v1/accounts").mock(
        return_value=_page(
            [_account("acc_1")],
            next_cursor="v1.next",
        )
    )

    text = await _text("accounts_list")

    assert route.call_count == 1
    assert dict(route.calls.last.request.url.params) == {"limit": "100"}
    assert text.startswith("Showing 1 connected account(s)")
    assert 'cursor="v1.next"' in text


@respx.mock
async def test_accounts_list_forwards_filters_cursor_and_caps_the_page_size() -> None:
    route = respx.get(f"{API}/v1/accounts").mock(return_value=_page([]))

    text = await _text(
        "accounts_list",
        {
            "platform": "Twitter",
            "profile_id": "prof_1",
            "search": " acme ",
            "limit": 5000,
            "cursor": "v1.next",
        },
    )

    assert dict(route.calls.last.request.url.params) == {
        "platform": "twitter",
        "profileId": "prof_1",
        "search": "acme",
        "limit": "500",
        "cursor": "v1.next",
    }
    assert text == "No accounts match these filters."


@respx.mock
async def test_accounts_list_last_page_offers_no_cursor() -> None:
    respx.get(f"{API}/v1/accounts").mock(return_value=_page([_account("acc_1")]))

    text = await _text("accounts_list")

    assert text.startswith("Found 1 connected account(s)")
    assert "cursor" not in text


@respx.mock
async def test_generated_account_listing_is_paged_by_default() -> None:
    route = respx.get(f"{API}/v1/accounts").mock(return_value=_page([]))

    async with Client(mcp) as client:
        await client.call_tool(
            "call_tool", {"name": "accounts_list_accounts", "arguments": {}}
        )

    assert route.calls.last.request.url.params["limit"] == "100"


@pytest.mark.parametrize(
    "arguments,forbidden_param",
    [
        ({"profile_ids": "prof_1", "per_profile": 3}, "limit"),
        ({"sort": "platform"}, "limit"),
    ],
)
@respx.mock
async def test_generated_account_listing_sends_no_limit_when_the_api_forbids_it(
    arguments, forbidden_param
) -> None:
    route = respx.get(f"{API}/v1/accounts").mock(return_value=_page([]))

    async with Client(mcp) as client:
        await client.call_tool(
            "call_tool", {"name": "accounts_list_accounts", "arguments": arguments}
        )

    assert forbidden_param not in route.calls.last.request.url.params


@respx.mock
async def test_profiles_list_is_paged_and_points_at_the_next_page() -> None:
    route = respx.get(f"{API}/v1/profiles").mock(
        return_value=httpx.Response(
            200,
            json={
                "profiles": [{"_id": "prof_1", "name": "Acme"}],
                "total": 33000,
                "skip": 100,
                "limit": 100,
            },
        )
    )

    text = await _text("profiles_list", {"skip": 100})

    assert dict(route.calls.last.request.url.params) == {"limit": "100", "skip": "100"}
    assert text.startswith("Found 33000 profile(s), showing 1")
    assert "skip=101" in text


@respx.mock
async def test_posting_with_an_account_id_spends_only_the_post_request() -> None:
    listing = respx.get(f"{API}/v1/accounts")
    create = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json=POST_RESPONSE)
    )

    text = await _text(
        "posts_create",
        {
            "content": "hi",
            "platform": "twitter",
            "account_id": "acc_1",
            "is_draft": True,
        },
    )

    assert listing.call_count == 0
    assert create.call_count == 1
    assert b'"accountId":"acc_1"' in create.calls.last.request.content.replace(
        b" ", b""
    )
    assert "Post ID: post_1" in text


@respx.mock
async def test_api_rejection_of_an_account_on_another_platform_reaches_the_caller() -> (
    None
):
    respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(
            400, json={"error": "Account acc_1 does not match platform twitter"}
        )
    )

    async with Client(mcp) as client:
        result = await client.call_tool(
            "posts_create",
            {
                "content": "hi",
                "platform": "twitter",
                "account_id": "acc_1",
                "is_draft": True,
            },
            raise_on_error=False,
        )

    assert result.is_error
    assert "does not match platform twitter" in result.content[0].text


@respx.mock
async def test_cross_post_looks_up_only_the_targets_without_an_id() -> None:
    listing = respx.get(f"{API}/v1/accounts").mock(
        return_value=_page([_account("acc_li", "linkedin")])
    )
    respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json=POST_RESPONSE)
    )

    await _text(
        "posts_cross_post",
        {
            "content": "hi",
            "platforms": "twitter,linkedin",
            "account_ids": "acc_tw,",
            "is_draft": True,
        },
    )

    assert listing.call_count == 1
    assert listing.calls.last.request.url.params["platform"] == "linkedin"


@respx.mock
async def test_chatgpt_listing_is_one_bounded_page_with_a_cursor(monkeypatch) -> None:
    monkeypatch.setattr("late.mcp.chatgpt_server._bearer", lambda: "test_api_key")
    route = respx.get(url__startswith="https://zernio.com/api/v1/accounts").mock(
        return_value=_page(
            [_account("acc_1")],
            next_cursor="v1.next",
        )
    )

    async with Client(chatgpt_mcp) as client:
        result = await client.call_tool("list_social_accounts", {"platform": "Twitter"})

    assert route.call_count == 1
    assert dict(route.calls.last.request.url.params) == {
        "limit": "100",
        "platform": "twitter",
    }
    assert result.structured_content["next_cursor"] == "v1.next"


@respx.mock
async def test_chatgpt_post_created_stays_a_success_when_the_username_lookup_fails(
    monkeypatch,
) -> None:
    monkeypatch.setattr("late.mcp.chatgpt_server._bearer", lambda: "test_api_key")
    respx.get(url__startswith="https://zernio.com/api/v1/accounts").mock(
        return_value=httpx.Response(503, json={"error": "statement timeout"})
    )
    respx.get("https://zernio.com/api/v1/posts/post_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "post": {
                    "_id": "post_1",
                    "status": "scheduled",
                    "platforms": [{"platform": "twitter", "accountId": "acc_1"}],
                }
            },
        )
    )

    async with Client(chatgpt_mcp) as client:
        result = await client.call_tool("get_post", {"post_id": "post_1"})

    assert not result.is_error
    assert result.structured_content["post"]["targets"][0]["account_id"] == "acc_1"


@respx.mock
async def test_chatgpt_skips_the_account_listing_when_posts_carry_their_account(
    monkeypatch,
) -> None:
    monkeypatch.setattr("late.mcp.chatgpt_server._bearer", lambda: "test_api_key")
    listing = respx.get(url__startswith="https://zernio.com/api/v1/accounts")
    respx.get("https://zernio.com/api/v1/posts/post_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "post": {
                    "_id": "post_1",
                    "status": "scheduled",
                    "platforms": [
                        {
                            "platform": "twitter",
                            "accountId": {"_id": "acc_1", "username": "acme"},
                        }
                    ],
                }
            },
        )
    )

    async with Client(chatgpt_mcp) as client:
        result = await client.call_tool("get_post", {"post_id": "post_1"})

    assert listing.call_count == 0
    assert result.structured_content["post"]["targets"][0]["username"] == "acme"
