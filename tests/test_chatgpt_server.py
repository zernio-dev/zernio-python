"""Contract tests for the ChatGPT plugin surface (late.mcp.chatgpt_server).

OpenAI reviews exactly what tools/list advertises and what tools/call returns,
so these tests pin the reviewable contract: every tool carries all three hint
values plus a securitySchemes entry, the profile tool is marked, structured
results contain only the declared fields, and writes refuse the inputs that
sank the previous submissions (guessed accounts, silent publish, editing a
published post).
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp import chatgpt_server
from late.mcp.chatgpt_server import chatgpt_mcp

API = chatgpt_server.API_BASE

ACCOUNTS = {
    "accounts": [
        {
            "_id": "acc_tw",
            "platform": "twitter",
            "username": "demo",
            "displayName": "Demo",
            "isActive": True,
            "enabled": True,
            "profileUrl": "https://x.com/demo",
            "userId": "u1",
            "profilePicture": "https://img",
            "createdAt": "2026-01-01",
        },
        {
            "_id": "acc_ig",
            "platform": "instagram",
            "username": "demo_ig",
            "isActive": True,
            "needsReconnection": True,
            "enabled": True,
        },
        {
            "_id": "acc_ads",
            "platform": "metaads",
            "username": "ads",
            "isActive": True,
            "enabled": True,
        },
        {
            "_id": "acc_off",
            "platform": "linkedin",
            "username": "off",
            "isActive": True,
            "enabled": False,
        },
    ]
}

POST = {
    "_id": "post_1",
    "userId": "u1",
    "content": "Hello",
    "status": "scheduled",
    "scheduledFor": "2030-01-01T09:00:00.000Z",
    "timezone": "UTC",
    "createdAt": "2026-01-01T00:00:00Z",
    "metadata": {"secret": 1},
    "mediaItems": [{"type": "image", "url": "https://cdn/x.png", "size": 12}],
    "platforms": [
        {
            "platform": "twitter",
            "accountId": {
                "_id": "acc_tw",
                "username": "demo",
                "profilePicture": "https://img",
            },
            "status": "pending",
        }
    ],
}


@pytest.fixture(autouse=True)
def _api_key(monkeypatch):
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")


async def _call(name: str, **args):
    async with Client(chatgpt_mcp) as client:
        return await client.call_tool(name, args, raise_on_error=False)


async def test_every_tool_is_fully_annotated_for_review():
    async with Client(chatgpt_mcp) as client:
        tools = await client.list_tools()
    assert len(tools) == 13
    for tool in tools:
        hints = tool.annotations
        assert hints is not None, tool.name
        assert isinstance(hints.readOnlyHint, bool), tool.name
        assert isinstance(hints.destructiveHint, bool), tool.name
        assert isinstance(hints.openWorldHint, bool), tool.name
        assert tool.meta and tool.meta["securitySchemes"][0]["type"] == "oauth2", (
            tool.name
        )
        assert tool.outputSchema, tool.name
        assert tool.description and tool.description.startswith("Use this"), tool.name
    by_name = {t.name: t for t in tools}
    assert by_name["get_profile"].meta["openai/profile"] is True
    read_only = {n for n, t in by_name.items() if t.annotations.readOnlyHint}
    assert read_only == {
        "get_profile",
        "list_social_accounts",
        "list_posts",
        "get_post",
        "validate_post",
        "get_post_analytics",
        "get_account_analytics",
        "get_best_time_to_post",
    }
    public_writes = {n for n, t in by_name.items() if t.annotations.openWorldHint}
    assert public_writes == {"schedule_post", "publish_post_now", "retry_failed_post"}
    assert by_name["schedule_post"].annotations.destructiveHint is False
    assert by_name["publish_post_now"].annotations.destructiveHint is True


@respx.mock
async def test_list_social_accounts_hides_ads_and_disabled_and_strips_internal_fields():
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(200, json=ACCOUNTS)
    )
    result = await _call("list_social_accounts")
    accounts = result.structured_content["accounts"]
    assert [a["id"] for a in accounts] == ["acc_tw", "acc_ig"]
    assert accounts[1]["status"] == "needs_reconnection"
    dumped = json.dumps(result.structured_content)
    assert (
        "profilePicture" not in dumped
        and "userId" not in dumped
        and "createdAt" not in dumped
    )


@respx.mock
async def test_get_post_unwraps_populated_account_and_keeps_only_declared_fields():
    respx.get(f"{API}/v1/posts/post_1").mock(
        return_value=httpx.Response(200, json={"post": POST})
    )
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(200, json=ACCOUNTS)
    )
    result = await _call("get_post", post_id="post_1")
    post = result.structured_content["post"]
    assert post["targets"][0] == {
        "platform": "twitter",
        "account_id": "acc_tw",
        "username": "demo",
        "status": "pending",
    }
    assert post["media_urls"] == ["https://cdn/x.png"]
    dumped = json.dumps(result.structured_content)
    for leaked in ("userId", "metadata", "createdAt", "profilePicture", "secret"):
        assert leaked not in dumped


@respx.mock
async def test_schedule_post_requires_known_accounts_and_a_timezone():
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(200, json=ACCOUNTS)
    )
    unknown = await _call(
        "schedule_post",
        content="x",
        account_ids=["nope"],
        scheduled_for="2030-01-01T09:00:00Z",
    )
    assert unknown.is_error and "Unknown account id" in unknown.content[0].text

    naive = await _call(
        "schedule_post",
        content="x",
        account_ids=["acc_tw"],
        scheduled_for="2030-01-01T09:00:00",
    )
    assert naive.is_error and "timezone" in naive.content[0].text

    past = await _call(
        "schedule_post",
        content="x",
        account_ids=["acc_tw"],
        scheduled_for="2020-01-01T09:00:00Z",
    )
    assert past.is_error and "past" in past.content[0].text


@respx.mock
async def test_schedule_post_sends_utc_time_and_explicit_targets():
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(200, json=ACCOUNTS)
    )
    create = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(201, json={"post": POST})
    )
    result = await _call(
        "schedule_post",
        content="Hello",
        account_ids=["acc_tw"],
        scheduled_for="2030-01-01T11:00:00+02:00",
        media_urls=["https://cdn/clip.mp4"],
    )
    assert not result.is_error
    body = json.loads(create.calls[0].request.content)
    assert body == {
        "content": "Hello",
        "platforms": [{"platform": "twitter", "accountId": "acc_tw"}],
        "scheduledFor": "2030-01-01T09:00:00Z",
        "timezone": "UTC",
        "mediaItems": [{"type": "video", "url": "https://cdn/clip.mp4"}],
    }
    assert "publishNow" not in body


@respx.mock
async def test_publish_now_is_explicit_and_never_implied_by_schedule_post():
    respx.get(f"{API}/v1/accounts").mock(
        return_value=httpx.Response(200, json=ACCOUNTS)
    )
    create = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(201, json={"post": {**POST, "status": "published"}})
    )
    result = await _call("publish_post_now", content="Hello", account_ids=["acc_tw"])
    assert not result.is_error
    assert json.loads(create.calls[0].request.content)["publishNow"] is True


@respx.mock
async def test_cancel_and_update_refuse_published_posts():
    respx.get(f"{API}/v1/posts/post_1").mock(
        return_value=httpx.Response(200, json={"post": {**POST, "status": "published"}})
    )
    delete = respx.delete(f"{API}/v1/posts/post_1")
    cancelled = await _call("cancel_scheduled_post", post_id="post_1")
    assert cancelled.is_error and "published" in cancelled.content[0].text
    updated = await _call("update_scheduled_post", post_id="post_1", content="new")
    assert updated.is_error and "published" in updated.content[0].text
    assert not delete.called


@respx.mock
async def test_api_errors_surface_the_api_message_not_a_stack_trace():
    respx.get(f"{API}/v1/posts/missing").mock(
        return_value=httpx.Response(
            404, json={"error": {"code": "not_found", "message": "Post not found"}}
        )
    )
    result = await _call("get_post", post_id="missing")
    assert result.is_error
    assert result.content[0].text == "Post not found"


@respx.mock
async def test_best_time_returns_named_days_best_first():
    respx.get(f"{API}/v1/analytics/best-time").mock(
        return_value=httpx.Response(
            200,
            json={
                "slots": [
                    {
                        "day_of_week": 0,
                        "hour": 9,
                        "avg_engagement": 1.5,
                        "post_count": 2,
                    },
                    {
                        "day_of_week": 6,
                        "hour": 18,
                        "avg_engagement": 4.25,
                        "post_count": 1,
                    },
                ]
            },
        )
    )
    result = await _call("get_best_time_to_post")
    slots = result.structured_content["slots"]
    assert slots[0] == {
        "day": "Sunday",
        "hour_utc": 18,
        "avg_engagement": 4.25,
        "post_count": 1,
    }
    assert result.structured_content["based_on_posts"] == 3
