"""Agents send the camelCase names the REST API and docs use (postId, accountId,
contentType); the tools take snake_case. That cost several hundred rejected
calls a day, so a camelCase name a tool would accept in snake_case is renamed.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp

API = "https://api.test.com"


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


async def _call(name: str, arguments: dict) -> tuple[bool, str]:
    async with Client(mcp) as client:
        result = await client.call_tool(name, arguments, raise_on_error=False)
    return result.is_error, result.content[0].text


def _proxied(name: str, arguments: dict) -> dict:
    return {"name": name, "arguments": arguments}


@pytest.mark.parametrize("via_call_tool", [False, True])
@respx.mock
async def test_a_camelcase_argument_is_renamed_to_the_snake_case_parameter(
    via_call_tool: bool,
) -> None:
    route = respx.get(f"{API}/v1/posts/post_1").mock(
        return_value=httpx.Response(200, json={"post": {"_id": "post_1"}})
    )
    arguments = {"postId": "post_1"}

    if via_call_tool:
        is_error, text = await _call("call_tool", _proxied("posts_get_post", arguments))
    else:
        is_error, text = await _call("posts_get_post", arguments)

    assert not is_error, text
    assert route.called


@respx.mock
async def test_every_camelcase_argument_of_a_call_is_renamed() -> None:
    route = respx.get(f"{API}/v1/inbox/conversations/conv_1/messages").mock(
        return_value=httpx.Response(200, json={"messages": []})
    )

    is_error, text = await _call(
        "call_tool",
        _proxied(
            "messages_get_inbox_conversation_messages",
            {"conversationId": "conv_1", "accountId": "acc_1", "sortOrder": "desc"},
        ),
    )

    assert not is_error, text
    params = route.calls.last.request.url.params
    assert params["accountId"] == "acc_1"
    assert params["sortOrder"] == "desc"


@respx.mock
async def test_a_camelcase_body_field_is_renamed() -> None:
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
    respx.get(f"{API}/v1/posts/post_1").mock(
        return_value=httpx.Response(200, json={"post": {"_id": "post_1"}})
    )

    is_error, text = await _call("posts_get", {"postId": "post_1"})

    assert not is_error, text


@respx.mock
async def test_a_camelcase_argument_never_overwrites_the_snake_case_one() -> None:
    route = respx.get(url__startswith=f"{API}/v1/posts/").mock(
        return_value=httpx.Response(200, json={"post": {}})
    )

    is_error, text = await _call(
        "posts_get_post", {"post_id": "post_1", "postId": "post_2"}
    )

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
async def test_call_tool_takes_tool_name_for_name() -> None:
    respx.get(f"{API}/v1/posts/post_1").mock(
        return_value=httpx.Response(200, json={"post": {"_id": "post_1"}})
    )

    is_error, text = await _call(
        "call_tool", {"tool_name": "posts_get_post", "arguments": {"postId": "post_1"}}
    )

    assert not is_error, text
