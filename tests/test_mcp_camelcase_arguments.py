"""Agents send the camelCase names the REST API and docs use (postId, accountId,
contentType); the tools take snake_case. That cost several hundred rejected
calls a day, so a camelCase name a tool would accept in snake_case is renamed.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client, FastMCP

from late.mcp.middleware import ArgumentNamesMiddleware
from late.mcp.server import mcp

API = "https://api.test.com"


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


async def _call(name: str, arguments: dict, server: FastMCP = mcp) -> tuple[bool, str]:
    async with Client(server) as client:
        result = await client.call_tool(name, arguments, raise_on_error=False)
    return result.is_error, result.content[0].text


def _proxied(name: str, arguments: dict) -> dict:
    return {"name": name, "arguments": arguments}


def _mock_post(post_id: str = "post_1") -> respx.Route:
    return respx.get(f"{API}/v1/posts/{post_id}").mock(
        return_value=httpx.Response(200, json={"post": {"_id": post_id}})
    )


@pytest.mark.parametrize("via_call_tool", [False, True])
@respx.mock
async def test_post_id_in_camelcase_is_renamed_to_post_id(via_call_tool: bool) -> None:
    route = _mock_post()
    arguments = {"postId": "post_1"}

    if via_call_tool:
        is_error, text = await _call("call_tool", _proxied("posts_get_post", arguments))
    else:
        is_error, text = await _call("posts_get_post", arguments)

    assert not is_error, text
    assert route.call_count == 1


@respx.mock
async def test_every_camelcase_argument_of_a_call_is_renamed() -> None:
    route = respx.get(f"{API}/v1/inbox/conversations/conv_1/messages").mock(
        return_value=httpx.Response(200, json={"messages": []})
    )

    is_error, text = await _call(
        "messages_get_inbox_conversation_messages",
        {"conversationId": "conv_1", "accountId": "acc_1", "sortOrder": "desc"},
    )

    assert not is_error, text
    params = route.calls.last.request.url.params
    assert params["accountId"] == "acc_1"
    assert params["sortOrder"] == "desc"


@respx.mock
async def test_call_tool_takes_tool_name_for_name_and_renames_the_proxied_arguments() -> (
    None
):
    route = _mock_post()

    is_error, text = await _call(
        "call_tool", {"tool_name": "posts_get_post", "arguments": {"postId": "post_1"}}
    )

    assert not is_error, text
    assert route.call_count == 1


@respx.mock
async def test_snake_case_arguments_skip_the_tool_lookup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (middleware,) = [
        m for m in mcp.middleware if isinstance(m, ArgumentNamesMiddleware)
    ]
    looked_up: list[str] = []
    lookup = middleware._tool_parameters

    async def spy(name, context):
        looked_up.append(name)
        return await lookup(name, context)

    monkeypatch.setattr(middleware, "_tool_parameters", spy)
    route = _mock_post()

    is_error, text = await _call("posts_get_post", {"post_id": "post_1"})

    assert not is_error, text
    assert route.call_count == 1
    assert looked_up == []
    # The spy is live: a camelCase call does look the tool up.
    await _call("posts_get_post", {"postId": "post_1"})
    assert looked_up == ["posts_get_post"]


@respx.mock
async def test_a_camelcase_argument_never_overwrites_the_snake_case_one() -> None:
    route = respx.get(url__startswith=f"{API}/v1/posts/").mock(
        return_value=httpx.Response(200, json={"post": {}})
    )

    is_error, text = await _call("posts_get_post", {"post_id": "A", "postId": "B"})

    # Both given: which one the agent meant is unknowable, so the call is
    # rejected as before rather than silently picking one.
    assert is_error
    assert "postId" in text
    assert not route.called


async def test_an_unknown_argument_is_still_rejected() -> None:
    is_error, text = await _call("posts_get_post", {"postIdentifier": "post_1"})

    assert is_error
    assert "postIdentifier" in text


@respx.mock
async def test_nested_keys_are_sent_to_the_api_untouched() -> None:
    route = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(201, json={"post": {"_id": "post_1"}})
    )

    is_error, text = await _call(
        "posts_create_post",
        {
            "content": "hi",
            "scheduledFor": "2030-01-01T09:00:00Z",
            "platforms": [{"accountId": "acc_1", "platform": "twitter"}],
        },
    )

    assert not is_error, text
    body = json.loads(route.calls.last.request.content)
    assert body["scheduledFor"] == "2030-01-01T09:00:00Z"
    assert body["platforms"] == [{"accountId": "acc_1", "platform": "twitter"}]


@respx.mock
async def test_two_keys_claiming_one_parameter_are_both_rejected() -> None:
    route = respx.get(url__startswith=f"{API}/v1/posts/").mock(
        return_value=httpx.Response(200, json={"post": {}})
    )

    is_error, text = await _call("posts_get_post", {"postId": "A", "PostID": "B"})

    assert is_error
    assert "postId" in text and "PostID" in text
    assert not route.called


@respx.mock
async def test_a_body_field_is_renamed() -> None:
    route = respx.post(f"{API}/v1/media/presign").mock(
        return_value=httpx.Response(200, json={"uploadUrl": "https://u"})
    )

    is_error, text = await _call(
        "call_tool",
        _proxied(
            "media_get_media_presigned_url",
            {"filename": "a.png", "contentType": "image/png"},
        ),
    )

    assert not is_error, text
    assert json.loads(route.calls.last.request.content)["contentType"] == "image/png"


@respx.mock
async def test_a_pinned_tool_takes_camelcase_arguments_too() -> None:
    _mock_post()

    is_error, text = await _call("posts_get", {"postId": "post_1"})

    assert not is_error, text


# No Zernio tool has a camelCase parameter or two parameters differing only in
# case or underscores (checked 2026-11-27), so these use a server of their own.
_mixed = FastMCP("mixed")
_mixed.add_middleware(ArgumentNamesMiddleware())


@_mixed.tool
def camel(postId: str, page_size: int = 1) -> str:  # noqa: N803
    return f"{postId}:{page_size}"


@_mixed.tool
def colliding(postId: str = "", post_id: str = "") -> str:  # noqa: N803
    return f"{postId}|{post_id}"


async def test_a_camelcase_parameter_is_passed_as_is() -> None:
    assert await _call("camel", {"postId": "p", "pageSize": 3}, _mixed) == (
        False,
        "p:3",
    )


async def test_a_name_that_folds_to_two_parameters_is_not_renamed() -> None:
    is_error, text = await _call("colliding", {"PostID": "p"}, _mixed)

    assert is_error
    assert "PostID" in text
