from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from types import SimpleNamespace
from typing import TYPE_CHECKING

import httpx
import pytest
import respx
import sentry_sdk
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.transforms.search import BM25SearchTransform
from sentry_sdk.transport import Transport

from late.client.exceptions import LateAPIError
from late.mcp import telemetry
from late.mcp.telemetry import (
    ServerErrorAccessLogFilter,
    ToolTelemetryMiddleware,
    init_sentry,
    quiet_routine_logs,
)
from late.models import AccountsListResponse

if TYPE_CHECKING:
    from sentry_sdk.envelope import Envelope


def _server() -> FastMCP:
    server = FastMCP("t")

    @server.tool
    def fine() -> str:
        return "ok"

    @server.tool
    def rejected() -> str:
        return "❌ Multiple twitter accounts available"

    @server.tool
    def api_failure() -> str:
        raise ToolError("Error: nope") from LateAPIError("nope", status_code=503)

    @server.tool
    def bug() -> str:
        raise KeyError("oops")

    server.add_middleware(ToolTelemetryMiddleware("mcp"))
    return server


def _logged(caplog: pytest.LogCaptureFixture) -> list[dict]:
    return [
        json.loads(record.getMessage())
        for record in caplog.records
        if record.name == "late.mcp.tools"
    ]


class _CapturingTransport(Transport):
    def __init__(self, options: dict | None = None) -> None:
        super().__init__(options)
        self.envelopes: list[Envelope] = []

    def capture_envelope(self, envelope: Envelope) -> None:
        self.envelopes.append(envelope)

    def payloads(self, item_type: str) -> list[dict]:
        return [
            item.payload.json
            for envelope in self.envelopes
            for item in envelope.items
            if item.type == item_type
        ]


@pytest.fixture
def sentry_events(monkeypatch: pytest.MonkeyPatch):
    captured: list[_CapturingTransport] = []
    real_init = sentry_sdk.init

    def init(**options):
        transport = _CapturingTransport(options)
        captured.append(transport)
        return real_init(transport=transport, **options)

    monkeypatch.setattr(telemetry.sentry_sdk, "init", init)
    monkeypatch.setenv("SENTRY_DSN", "https://key@o1.ingest.example.invalid/1")
    assert init_sentry() is True
    yield captured[0]
    real_init(dsn=None)


@pytest.mark.parametrize(
    "tool,fields",
    [
        ("fine", {"outcome": "ok"}),
        ("rejected", {"outcome": "rejected"}),
        (
            "api_failure",
            {"outcome": "error", "error_type": "LateAPIError", "status_code": 503},
        ),
        ("bug", {"outcome": "error", "error_type": "KeyError"}),
    ],
)
async def test_every_tool_call_logs_its_outcome_and_latency(
    caplog, tool, fields
) -> None:
    caplog.set_level(logging.INFO, logger="late.mcp.tools")

    async with Client(_server()) as client:
        await client.call_tool(tool, {}, raise_on_error=False)

    [line] = _logged(caplog)
    assert line["event"] == "mcp_tool_call"
    assert line["surface"] == "mcp"
    assert line["tool"] == tool
    assert isinstance(line["duration_ms"], int)
    assert datetime.fromisoformat(line["ts"]).tzinfo is not None
    assert fields.items() <= line.items()


def test_sentry_stays_off_without_a_dsn(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    assert init_sentry() is False


async def test_each_tool_call_is_one_named_sentry_transaction(sentry_events) -> None:
    async with Client(_server()) as client:
        await client.call_tool("fine", {})

    transactions = sentry_events.payloads("transaction")
    assert [t["transaction"] for t in transactions] == ["tools/call fine"]
    assert transactions[0]["contexts"]["trace"]["op"] == "mcp.tool"
    assert transactions[0]["contexts"]["trace"]["status"] == "ok"
    assert transactions[0]["tags"]["mcp.outcome"] == "ok"


async def test_api_errors_are_counted_but_only_bugs_become_sentry_issues(
    sentry_events,
) -> None:
    async with Client(_server()) as client:
        await client.call_tool("api_failure", {}, raise_on_error=False)
        await client.call_tool("bug", {}, raise_on_error=False)

    statuses = {
        t["transaction"]: t["contexts"]["trace"]["status"]
        for t in sentry_events.payloads("transaction")
    }
    assert statuses == {
        "tools/call api_failure": "internal_error",
        "tools/call bug": "internal_error",
    }
    [issue] = sentry_events.payloads("event")
    assert issue["exception"]["values"][0]["type"] == "KeyError"


def test_only_tool_calls_are_sampled_for_traces() -> None:
    sample = telemetry._tool_call_sampler(0.5)
    assert sample({"transaction_context": {"op": "mcp.tool"}}) == 0.5
    assert sample({"transaction_context": {"op": "http.server"}}) == 0.0


def test_a_bad_sample_rate_fails_at_startup_not_on_each_tool_call(monkeypatch) -> None:
    monkeypatch.setenv("SENTRY_DSN", "https://key@o1.ingest.example.invalid/1")
    monkeypatch.setenv("SENTRY_TRACES_SAMPLE_RATE", "10%")
    with pytest.raises(ValueError):
        init_sentry()


async def test_a_cancelled_tool_call_is_not_logged_as_ok(caplog) -> None:
    caplog.set_level(logging.INFO, logger="late.mcp.tools")

    async def cancelled_call(_context):
        raise asyncio.CancelledError

    context = SimpleNamespace(message=SimpleNamespace(name="slow"))
    with pytest.raises(asyncio.CancelledError):
        await ToolTelemetryMiddleware("mcp").on_call_tool(context, cancelled_call)

    [line] = _logged(caplog)
    assert line["outcome"] == "cancelled"


async def test_expected_failures_open_no_sentry_issue(sentry_events) -> None:
    server = _server()

    @server.tool
    def bare_tool_error() -> str:
        raise ToolError("Post not found")

    @server.tool
    def takes_a_number(value: int) -> int:
        return value

    async with Client(server) as client:
        await client.call_tool("bare_tool_error", {}, raise_on_error=False)
        await client.call_tool(
            "takes_a_number", {"value": "nope"}, raise_on_error=False
        )
        with pytest.raises(ToolError):
            await client.call_tool("does_not_exist", {})

    assert sentry_events.payloads("event") == []


async def test_an_sdk_model_that_rejects_a_response_is_a_sentry_issue(
    sentry_events,
) -> None:
    server = _server()

    @server.tool
    def rejects_response() -> str:
        AccountsListResponse.model_validate({"accounts": "nope"})
        return "unreachable"

    async with Client(server) as client:
        await client.call_tool("rejects_response", {}, raise_on_error=False)

    [issue] = sentry_events.payloads("event")
    assert issue["exception"]["values"][0]["type"] == "ValidationError"


async def test_a_tool_behind_call_tool_is_logged_under_its_own_name(caplog) -> None:
    caplog.set_level(logging.INFO, logger="late.mcp.tools")
    server = FastMCP("t", transforms=[BM25SearchTransform(max_results=1)])

    @server.tool
    def hidden_tool() -> str:
        return "ok"

    server.add_middleware(ToolTelemetryMiddleware("mcp"))

    async with Client(server) as client:
        await client.call_tool("call_tool", {"name": "hidden_tool", "arguments": {}})

    assert [line["tool"] for line in _logged(caplog)] == ["hidden_tool", "call_tool"]


@respx.mock
async def test_the_bearer_token_never_reaches_logs_or_sentry(
    sentry_events, caplog, monkeypatch: pytest.MonkeyPatch
) -> None:
    caplog.set_level(logging.INFO, logger="late.mcp.tools")
    monkeypatch.setenv("ZERNIO_API_KEY", "sk-secret-token")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")
    respx.get("https://api.test.com/v1/accounts").mock(
        return_value=httpx.Response(500, json={})
    )
    server = FastMCP("t")

    @server.tool
    def lists_accounts() -> str:
        from late.mcp.server import _get_client

        _get_client().accounts.list(limit=1)
        return "ok"

    server.add_middleware(ToolTelemetryMiddleware("mcp"))

    async with Client(server) as client:
        await client.call_tool("lists_accounts", {}, raise_on_error=False)

    sent = json.dumps(
        sentry_events.payloads("transaction") + sentry_events.payloads("event")
    )
    assert "sk-secret-token" not in sent
    assert "sk-secret-token" not in json.dumps(_logged(caplog))


class _RecordingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


@pytest.fixture
def quieted_fastmcp_logs():
    root = logging.getLogger("fastmcp")
    server_logger = logging.getLogger("fastmcp.server.server")
    access_logger = logging.getLogger("uvicorn.access")
    saved = (root.level, list(server_logger.filters), list(access_logger.filters))
    handler = _RecordingHandler()
    server_logger.addHandler(handler)
    quiet_routine_logs()
    yield handler
    server_logger.removeHandler(handler)
    root.setLevel(saved[0])
    server_logger.filters = saved[1]
    access_logger.filters = saved[2]


async def test_expected_tool_failures_write_nothing_beyond_the_tool_call_line(
    quieted_fastmcp_logs,
) -> None:
    server = _server()

    @server.tool
    def raw_api_failure() -> str:
        raise LateAPIError("nope", status_code=400)

    async with Client(server) as client:
        await client.call_tool("raw_api_failure", {}, raise_on_error=False)
        await client.call_tool("api_failure", {}, raise_on_error=False)

    assert quieted_fastmcp_logs.records == []


async def test_a_tool_bug_keeps_its_traceback(quieted_fastmcp_logs) -> None:
    async with Client(_server()) as client:
        await client.call_tool("bug", {}, raise_on_error=False)

    [record] = quieted_fastmcp_logs.records
    assert record.getMessage() == "Error calling tool 'bug'"
    assert record.exc_info[0] is KeyError


async def test_invalid_arguments_name_the_field_but_never_log_its_value(
    quieted_fastmcp_logs,
) -> None:
    server = _server()

    @server.tool
    def takes_a_number(count: int) -> str:
        return str(count)

    async with Client(server) as client:
        await client.call_tool(
            "takes_a_number", {"count": "customer-secret"}, raise_on_error=False
        )

    [record] = quieted_fastmcp_logs.records
    assert record.getMessage() == (
        "Invalid arguments for tool 'takes_a_number': count: int_parsing"
    )


async def test_an_sdk_model_that_rejects_a_response_stays_in_the_logs(
    quieted_fastmcp_logs,
) -> None:
    server = _server()

    @server.tool
    def rejects_response() -> str:
        AccountsListResponse.model_validate({"accounts": "nope"})
        return "unreachable"

    async with Client(server) as client:
        await client.call_tool("rejects_response", {}, raise_on_error=False)

    [record] = quieted_fastmcp_logs.records
    assert "accounts: list_type" in record.getMessage()


@pytest.mark.usefixtures("quieted_fastmcp_logs")
def test_fastmcp_info_lines_such_as_auth_errors_are_silenced() -> None:
    auth_logger = logging.getLogger("fastmcp.server.auth.middleware")

    assert not auth_logger.isEnabledFor(logging.INFO)
    assert auth_logger.isEnabledFor(logging.WARNING)


@pytest.mark.parametrize(
    "status_code,kept",
    [(200, False), (202, False), (401, False), (405, False), (500, True), (503, True)],
)
def test_access_lines_survive_only_for_server_errors(status_code, kept) -> None:
    record = logging.LogRecord(
        name="uvicorn.access",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='%s - "%s %s HTTP/%s" %d',
        args=("127.0.0.1:1", "POST", "/mcp", "1.1", status_code),
        exc_info=None,
    )

    assert ServerErrorAccessLogFilter().filter(record) is kept
