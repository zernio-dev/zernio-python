"""Contract tests for the support_ask MCP tool (paid Support Assistant diagnosis).

respx mocks only the HTTP boundary; the tool runs against the real Late client
through the in-memory FastMCP client. pollAfterSeconds is 0 in fixtures so the
poll loop never sleeps.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp import server
from late.mcp.server import mcp

RUNS = "https://zernio.com/api/v1/support/runs"

QUEUED = {
    "runId": "run_1",
    "threadId": "thr_1",
    "status": "queued",
    "pollAfterSeconds": 0,
}
COMPLETED = {
    "runId": "run_1",
    "threadId": "thr_1",
    "status": "completed",
    "answer": "Your token expired; reconnect the account.",
    "costUsd": 0.21,
    "maxCostUsd": 1.0,
}


@pytest.fixture(autouse=True)
def _api_key(monkeypatch):
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")


async def _call(name: str, **args) -> str:
    async with Client(mcp) as client:
        result = await client.call_tool(name, args, raise_on_error=False)
    return result.content[0].text


@respx.mock
async def test_completes_and_sends_idempotency_key():
    post = respx.post(RUNS).mock(return_value=httpx.Response(202, json=QUEUED))
    respx.get(f"{RUNS}/run_1").mock(return_value=httpx.Response(200, json=COMPLETED))

    out = json.loads(await _call("support_ask", question="Why did my post fail?"))

    assert out["answer"] == COMPLETED["answer"]
    assert out["costUsd"] == 0.21
    request = post.calls.last.request
    assert request.headers["Idempotency-Key"].startswith("mcp-support-")
    body = json.loads(request.content)
    assert body["message"] == "Why did my post fail?"
    assert body["maxCostUsd"] == 1.0


@respx.mock
async def test_idempotency_key_depends_on_arguments():
    post = respx.post(RUNS).mock(return_value=httpx.Response(202, json=COMPLETED))

    await _call("support_ask", question="A")
    await _call("support_ask", question="A")
    await _call("support_ask", question="B")

    keys = [c.request.headers["Idempotency-Key"] for c in post.calls]
    assert keys[0] == keys[1]
    assert keys[0] != keys[2]


@respx.mock
async def test_wait_zero_returns_next_without_polling():
    respx.post(RUNS).mock(return_value=httpx.Response(202, json=QUEUED))
    get = respx.get(f"{RUNS}/run_1").mock(
        return_value=httpx.Response(200, json=COMPLETED)
    )

    out = json.loads(await _call("support_ask", question="Why?", wait_seconds=0))

    assert out["runId"] == "run_1"
    assert "support_assistant_get_support_answer" in out["next"]
    assert get.call_count == 0


@respx.mock
async def test_insufficient_permissions_returns_api_key_hint():
    respx.post(RUNS).mock(
        return_value=httpx.Response(
            403, json={"error": "Forbidden", "code": "insufficient_permissions"}
        )
    )

    out = await _call("support_ask", question="Why?")

    assert out.startswith("Error:")
    assert "unrestricted Zernio API key" in out


@respx.mock
async def test_rate_limit_says_do_not_retry():
    respx.post(RUNS).mock(return_value=httpx.Response(429, json={"error": "slow"}))

    out = await _call("support_ask", question="Why?")

    assert "Do not retry" in out


async def test_tools_list_pins_support_tools_and_hides_generated_ask():
    async with Client(mcp) as client:
        names = {t.name for t in await client.list_tools()}

    assert "support_ask" in names
    assert "support_assistant_get_support_answer" in names


def test_generated_tools_never_regain_the_unsafe_ask_tool():
    generated = (Path(__file__).parents[1] / "src/late/mcp/generated_tools.py").read_text()

    assert "def support_assistant_list_support_answers(" in generated
    assert "def support_assistant_ask_support_question(" not in generated


def test_support_ask_is_async():
    assert inspect.iscoroutinefunction(server.support_ask)


@respx.mock
async def test_network_error_says_a_retry_replays_the_same_run():
    respx.post(RUNS).mock(side_effect=httpx.ConnectError("boom"))

    out = await _call("support_ask", question="Why did my post fail?")

    assert out.startswith("Error:")
    assert "same run, never a second charge" in out
