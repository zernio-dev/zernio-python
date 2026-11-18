"""A 429 must tell the caller how long to wait, in the API's own words, so an
agent waits instead of retrying into the limit (433,000 429s in a week)."""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx
import pytest
import respx
from fastmcp import Client

from late import Late, LateRateLimitError
from late.client.exceptions import LateAPIError
from late.mcp.chatgpt_server import API_BASE, chatgpt_mcp
from late.mcp.middleware.tool_telemetry import _error_fields
from late.mcp.server import mcp

API_LIMIT = (
    "Limit of 120 requests per 30 s reached for campaign-analytics reads. "
    "Read many campaigns in one request with GET /v1/ads/tree instead of one "
    "request each. Please retry after 12 seconds."
)
META_LIMIT = {
    "error": "Meta throttled this ad account.",
    "type": "rate_limit_error",
    "code": "rate_limited",
    "platform": "meta",
}
GOOGLE_QUOTA = {
    "error": "YouTube Analytics quota for this project is exhausted.",
    "code": "rate_limited",
    "platform": "google",
    "details": {"quotaExhausted": True, "resetsAt": "2026-11-19T08:00:00Z"},
}
MESSAGES = "https://api.test.com/v1/inbox/conversations/conv_1/messages"
TOOL_ARGS = {"conversation_id": "conv_1", "account_id": "acc_1"}


def _api_limit(**headers: str) -> httpx.Response:
    return httpx.Response(429, json={"error": API_LIMIT}, headers=headers)


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


def _sdk_error(response: httpx.Response) -> LateRateLimitError:
    with respx.mock:
        respx.get(url__startswith=MESSAGES).mock(return_value=response)
        with pytest.raises(LateRateLimitError) as caught:
            Late(api_key="k", base_url="https://api.test.com").messages.get_inbox_conversation_messages(
                conversation_id="conv_1", account_id="acc_1"
            )
    return caught.value


async def _tool_error_text(response: httpx.Response) -> str:
    with respx.mock:
        respx.get(url__startswith=MESSAGES).mock(return_value=response)
        async with Client(mcp) as client:
            result = await client.call_tool(
                "call_tool",
                {"name": "messages_get_inbox_conversation_messages", "arguments": TOOL_ARGS},
                raise_on_error=False,
            )
    assert result.is_error
    return result.content[0].text


def test_the_sdk_keeps_the_api_message_and_retry_after() -> None:
    error = _sdk_error(_api_limit(**{"Retry-After": "12", "X-RateLimit-Limit": "120"}))

    assert error.message == API_LIMIT
    assert error.retry_after == 12
    assert error.limit == 120
    assert str(error) == f"[429] {API_LIMIT} (retry after 12s)"


def test_the_sdk_reads_retry_after_given_as_a_date() -> None:
    in_a_minute = datetime.now(timezone.utc) + timedelta(seconds=60)

    error = _sdk_error(_api_limit(**{"Retry-After": format_datetime(in_a_minute, usegmt=True)}))

    assert 55 <= error.retry_after <= 60


def test_a_platform_quota_never_quotes_the_zernio_api_window() -> None:
    error = _sdk_error(
        httpx.Response(429, json=GOOGLE_QUOTA, headers={"X-RateLimit-Reset": str(int(time.time()) + 30)})
    )

    assert error.details["platform"] == "google"
    assert "resets at" not in str(error)


def test_a_bare_429_still_reads_as_a_rate_limit() -> None:
    error = _sdk_error(httpx.Response(429))

    assert error.message == "Rate limit exceeded"
    assert error.retry_after is None
    assert isinstance(error, LateAPIError)


async def test_the_agent_is_told_how_long_to_wait_in_the_apis_words() -> None:
    text = await _tool_error_text(_api_limit(**{"Retry-After": "12"}))

    assert text == f"Error: [429] {API_LIMIT} Wait 12 seconds before calling this again; an earlier call fails the same way."


async def test_a_meta_throttle_says_how_long_to_wait() -> None:
    text = await _tool_error_text(httpx.Response(429, json=META_LIMIT, headers={"Retry-After": "60"}))

    assert "Meta throttled this ad account. (code: rate_limited). Wait 60 seconds" in text
    assert "Wait 60 seconds" in text


async def test_an_exhausted_platform_quota_says_not_to_retry() -> None:
    text = await _tool_error_text(httpx.Response(429, json=GOOGLE_QUOTA))

    assert "connected account's google quota, not a Zernio limit" in text
    assert "until 2026-11-19T08:00:00Z" in text
    assert "Do not retry it now" in text


async def test_other_api_errors_keep_their_message() -> None:
    text = await _tool_error_text(httpx.Response(403, json={"error": "Access denied"}))

    assert text == "Error: [403] Access denied"


def test_tool_telemetry_records_the_retry_after() -> None:
    error = LateRateLimitError("Slow down", retry_after=12)
    wrapped = RuntimeError("tool failed")
    wrapped.__cause__ = error

    assert _error_fields(wrapped) == {
        "error_type": "LateRateLimitError",
        "status_code": 429,
        "retry_after_s": 12,
    }


@respx.mock
async def test_chatgpt_tools_are_told_how_long_to_wait() -> None:
    respx.get(f"{API_BASE}/v1/accounts").mock(return_value=_api_limit(**{"Retry-After": "12"}))

    async with Client(chatgpt_mcp) as client:
        result = await client.call_tool("list_social_accounts", {}, raise_on_error=False)

    assert result.is_error
    assert result.content[0].text.startswith(f"{API_LIMIT} Wait 12 seconds before calling this again")
