from __future__ import annotations

import json
import logging

import httpx
import pytest
from fastmcp import Client, FastMCP

from late.mcp import axiom_sink, telemetry
from late.mcp.axiom_sink import AxiomIngestHandler, axiom_handler_from_env
from late.mcp.telemetry import ToolTelemetryMiddleware


class RecordingIngest:
    def __init__(self, status_code: int = 200) -> None:
        self.requests: list[httpx.Request] = []
        self.status_code = status_code

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(self.status_code, json={"ingested": 1})

    def events(self) -> list[dict]:
        return [
            event for request in self.requests for event in json.loads(request.content)
        ]


def _handler(ingest: RecordingIngest, **kwargs) -> AxiomIngestHandler:
    return AxiomIngestHandler(
        dataset="zernio-mcp",
        token="xaat-test",
        client=httpx.Client(transport=httpx.MockTransport(ingest)),
        flush_interval=3600,
        **kwargs,
    )


def _record(message: str) -> logging.LogRecord:
    return logging.makeLogRecord({"msg": message, "levelno": logging.INFO})


def test_tool_call_lines_reach_the_dataset_in_one_batch_keyed_on_their_own_timestamp() -> (
    None
):
    ingest = RecordingIngest()
    handler = _handler(ingest, static_fields={"release": "abc123", "worker": 7})

    handler.emit(
        _record(
            json.dumps(
                {
                    "event": "mcp_tool_call",
                    "tool": "posts_list",
                    "ts": "2026-11-12T16:00:00.000+00:00",
                }
            )
        )
    )
    handler.emit(
        _record(
            json.dumps(
                {
                    "event": "mcp_tool_call",
                    "tool": "accounts_list",
                    "ts": "2026-11-12T16:00:01.000+00:00",
                }
            )
        )
    )
    handler.flush()

    [request] = ingest.requests
    assert (
        str(request.url)
        == "https://api.axiom.co/v1/datasets/zernio-mcp/ingest?timestamp-field=ts"
    )
    assert request.headers["Authorization"] == "Bearer xaat-test"
    assert [e["tool"] for e in ingest.events()] == ["posts_list", "accounts_list"]
    assert ingest.events()[0]["release"] == "abc123"
    assert ingest.events()[0]["worker"] == 7


def test_lines_that_are_not_json_objects_are_skipped() -> None:
    ingest = RecordingIngest()
    handler = _handler(ingest)

    handler.emit(_record("plain text"))
    handler.emit(_record("[1, 2]"))
    handler.flush()

    assert ingest.requests == []


def test_a_full_buffer_drops_new_lines_and_reports_how_many(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(axiom_sink, "_MAX_BUFFERED", 2)
    ingest = RecordingIngest()
    handler = _handler(ingest)

    for tool in ("a", "b", "c", "d"):
        handler.emit(_record(json.dumps({"event": "mcp_tool_call", "tool": tool})))
    handler.flush()

    events = ingest.events()
    assert [e.get("tool") for e in events if e["event"] == "mcp_tool_call"] == [
        "a",
        "b",
    ]
    assert {"event": "mcp_axiom_dropped", "dropped": 2} in events


def test_a_failed_ingest_loses_the_batch_without_raising(
    caplog: pytest.LogCaptureFixture,
) -> None:
    def unreachable(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("boom")

    handler = AxiomIngestHandler(
        dataset="zernio-mcp",
        token="xaat-test",
        client=httpx.Client(transport=httpx.MockTransport(unreachable)),
        flush_interval=3600,
    )
    handler.emit(_record(json.dumps({"event": "mcp_tool_call"})))

    handler.flush()
    handler.flush()

    assert "Axiom ingest failed, 1 events lost: ConnectTimeout" in caplog.text


def test_a_rejected_ingest_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    handler = _handler(RecordingIngest(status_code=403))
    handler.emit(_record(json.dumps({"event": "mcp_tool_call"})))

    handler.flush()

    assert "Axiom ingest rejected 1 events: HTTP 403" in caplog.text


def test_batches_are_split_at_the_ingest_size_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(axiom_sink, "_MAX_BATCH", 2)
    ingest = RecordingIngest()
    handler = _handler(ingest)

    for tool in ("a", "b", "c"):
        handler.emit(_record(json.dumps({"event": "mcp_tool_call", "tool": tool})))
    handler.flush()

    assert [len(json.loads(r.content)) for r in ingest.requests] == [2, 1]


def test_closing_the_handler_sends_what_is_buffered() -> None:
    ingest = RecordingIngest()
    handler = _handler(ingest)
    handler.emit(_record(json.dumps({"event": "mcp_tool_call", "tool": "last"})))

    handler.close()

    assert [e["tool"] for e in ingest.events()] == ["last"]


@pytest.mark.parametrize(
    "env", [{}, {"AXIOM_TOKEN": "xaat"}, {"AXIOM_DATASET": "zernio-mcp"}]
)
def test_nothing_is_shipped_without_both_token_and_dataset(
    monkeypatch: pytest.MonkeyPatch, env: dict
) -> None:
    monkeypatch.delenv("AXIOM_TOKEN", raising=False)
    monkeypatch.delenv("AXIOM_DATASET", raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)

    assert axiom_handler_from_env() is None


def test_an_unexpected_send_error_is_logged_and_the_next_flush_still_sends(
    caplog: pytest.LogCaptureFixture,
) -> None:
    attempts: list[int] = []

    def first_call_explodes(_request: httpx.Request) -> httpx.Response:
        attempts.append(1)
        if len(attempts) == 1:
            raise RuntimeError("unexpected")
        return httpx.Response(200)

    handler = AxiomIngestHandler(
        dataset="zernio-mcp",
        token="xaat-test",
        client=httpx.Client(transport=httpx.MockTransport(first_call_explodes)),
        flush_interval=3600,
    )
    handler.emit(_record(json.dumps({"event": "mcp_tool_call"})))
    handler.flush()
    handler.emit(_record(json.dumps({"event": "mcp_tool_call"})))
    handler.flush()

    assert "Axiom ingest failed, 1 events lost: RuntimeError" in caplog.text
    assert len(attempts) == 2


def test_the_log_pump_does_not_wrap_the_axiom_handler(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from late.mcp.non_blocking_logging import LogPump, _wrap_handlers

    handler = _handler(RecordingIngest())
    probe = logging.getLogger("late.mcp.tests.axiom-pump-probe")
    monkeypatch.setattr(probe, "handlers", [handler])

    _wrap_handlers(probe, LogPump())

    assert probe.handlers == [handler]


@pytest.fixture
def tool_logger_at_info(monkeypatch: pytest.MonkeyPatch):
    tool_logger = logging.getLogger("late.mcp.tools")
    original_level = tool_logger.level
    monkeypatch.setattr(tool_logger, "handlers", [])
    monkeypatch.setattr(tool_logger, "propagate", False)
    monkeypatch.setattr(tool_logger, "disabled", False)
    tool_logger.setLevel(logging.INFO)
    yield tool_logger
    tool_logger.setLevel(original_level)


@pytest.mark.usefixtures("tool_logger_at_info")
async def test_a_tool_call_ends_up_as_one_event_in_the_dataset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ingest = RecordingIngest()
    handler = _handler(ingest)
    monkeypatch.setattr(telemetry, "axiom_handler_from_env", lambda: handler)

    assert telemetry.ship_tool_calls_to_axiom()
    server = FastMCP("t")
    server.add_middleware(ToolTelemetryMiddleware("mcp"))

    @server.tool
    def fine() -> str:
        return "ok"

    async with Client(server) as client:
        await client.call_tool("fine", {})
    handler.flush()

    [event] = ingest.events()
    assert (event["event"], event["tool"], event["outcome"]) == (
        "mcp_tool_call",
        "fine",
        "ok",
    )
    assert isinstance(event["duration_ms"], int)
