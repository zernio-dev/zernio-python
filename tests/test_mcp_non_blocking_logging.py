from __future__ import annotations

import io
import logging
import threading
import time

import anyio
import pytest
from starlette.requests import ClientDisconnect

from late.mcp.http_server import ClientDisconnectLogFilter
from late.mcp.non_blocking_logging import (
    LogPump,
    NonBlockingHandler,
    install_non_blocking_logging,
)

try:
    _ExceptionGroup = ExceptionGroup
except NameError:
    from exceptiongroup import ExceptionGroup as _ExceptionGroup


class _BlockedStream(io.StringIO):
    def __init__(self) -> None:
        super().__init__()
        self.unblocked = threading.Event()
        self.write_started = threading.Event()

    def write(self, text: str) -> int:
        self.write_started.set()
        self.unblocked.wait(5)
        return super().write(text)


@pytest.fixture
def isolated_logger():
    logger = logging.getLogger("late.mcp.tests.non_blocking")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers = []
    yield logger
    logger.handlers = []


def test_logging_returns_at_once_while_the_stream_is_blocked(isolated_logger) -> None:
    stream = _BlockedStream()
    target = logging.StreamHandler(stream)
    isolated_logger.addHandler(NonBlockingHandler(target, LogPump()))

    started = time.perf_counter()
    for i in range(100):
        isolated_logger.info("line %s", i)
    elapsed = time.perf_counter() - started

    assert elapsed < 0.5
    stream.unblocked.set()


def test_records_reach_the_stream_in_order_once_it_recovers(isolated_logger) -> None:
    stream = _BlockedStream()
    target = logging.StreamHandler(stream)
    pump = LogPump()
    isolated_logger.addHandler(NonBlockingHandler(target, pump))

    for i in range(5):
        isolated_logger.info("line %s", i)
    stream.unblocked.set()

    assert pump.drain(5)
    assert stream.getvalue().splitlines() == [f"line {i}" for i in range(5)]


def test_a_full_queue_drops_records_and_reports_how_many(isolated_logger) -> None:
    stream = _BlockedStream()
    target = logging.StreamHandler(stream)
    pump = LogPump(capacity=3)
    isolated_logger.addHandler(NonBlockingHandler(target, pump))

    isolated_logger.info("first")
    assert stream.write_started.wait(5)
    for i in range(10):
        isolated_logger.info("line %s", i)
    stream.unblocked.set()

    assert pump.drain(5)
    written = stream.getvalue()
    assert "first" in written
    assert "line 0" in written
    assert "line 9" not in written
    assert "Dropped 7 log records" in written


def test_the_wrapper_keeps_the_level_of_the_handler_it_wraps(isolated_logger) -> None:
    stream = io.StringIO()
    target = logging.StreamHandler(stream)
    target.setLevel(logging.ERROR)
    pump = LogPump()
    isolated_logger.addHandler(NonBlockingHandler(target, pump))

    isolated_logger.info("hidden")
    isolated_logger.error("shown")

    assert pump.drain(5)
    assert stream.getvalue() == "shown\n"


def test_a_handler_that_raises_does_not_stop_later_records(
    isolated_logger, monkeypatch
) -> None:
    monkeypatch.setattr(logging, "raiseExceptions", False)
    stream = io.StringIO()

    class _RaisesOnce(logging.StreamHandler):
        raised = False

        def emit(self, record: logging.LogRecord) -> None:
            if not self.raised:
                self.raised = True
                raise RuntimeError("render failed")
            super().emit(record)

    pump = LogPump()
    isolated_logger.addHandler(NonBlockingHandler(_RaisesOnce(stream), pump))

    isolated_logger.info("lost")
    isolated_logger.info("kept")

    assert pump.drain(5)
    assert stream.getvalue() == "kept\n"


@pytest.fixture
def restored_logging_handlers():
    loggers = [logging.getLogger()] + [
        logger
        for logger in logging.Logger.manager.loggerDict.values()
        if isinstance(logger, logging.Logger)
    ]
    saved = [(logger, list(logger.handlers)) for logger in loggers]
    yield
    for logger, handlers in saved:
        logger.handlers = handlers


def test_install_wraps_named_and_root_handlers_once(restored_logging_handlers) -> None:
    root = logging.getLogger()
    named = logging.getLogger("late.mcp.tests.install")
    root.handlers = [logging.StreamHandler(io.StringIO())]
    named.handlers = [logging.StreamHandler(io.StringIO())]
    pump = LogPump()

    install_non_blocking_logging(pump)
    first_pass = named.handlers[0]
    install_non_blocking_logging(pump)

    assert isinstance(root.handlers[0], NonBlockingHandler)
    assert isinstance(first_pass, NonBlockingHandler)
    assert named.handlers[0] is first_pass


def test_install_gives_an_empty_root_a_non_blocking_handler(
    restored_logging_handlers,
) -> None:
    root = logging.getLogger()
    root.handlers = []

    install_non_blocking_logging(LogPump())

    assert [type(h) for h in root.handlers] == [NonBlockingHandler]


def _error_record(
    msg: str = "boom", exc: BaseException | None = None
) -> logging.LogRecord:
    exc_info = (type(exc), exc, exc.__traceback__) if exc is not None else None
    return logging.LogRecord(
        "mcp.server.streamable_http", logging.ERROR, __file__, 0, msg, None, exc_info
    )


def test_disconnect_filter_drops_a_client_disconnect() -> None:
    assert not ClientDisconnectLogFilter().filter(_error_record(exc=ClientDisconnect()))


def test_disconnect_filter_drops_nested_disconnect_groups() -> None:
    group = _ExceptionGroup(
        "unhandled errors in a TaskGroup",
        [
            _ExceptionGroup(
                "unhandled errors in a TaskGroup", [anyio.ClosedResourceError()]
            )
        ],
    )
    assert not ClientDisconnectLogFilter().filter(_error_record(exc=group))


def test_disconnect_filter_keeps_real_errors() -> None:
    log_filter = ClientDisconnectLogFilter()
    assert log_filter.filter(_error_record(exc=ValueError("boom")))
    mixed = _ExceptionGroup("mixed", [ClientDisconnect(), ValueError("boom")])
    assert log_filter.filter(_error_record(exc=mixed))
    assert log_filter.filter(_error_record(msg="Error handling POST request"))


def test_disconnect_filter_drops_the_empty_stream_exception_line() -> None:
    log_filter = ClientDisconnectLogFilter()
    assert not log_filter.filter(_error_record(msg="Received exception from stream: "))
    assert log_filter.filter(_error_record(msg="Received exception from stream: boom"))
