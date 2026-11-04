import atexit
import logging
import queue
import signal
import sys
import threading
from types import FrameType

_LOG_QUEUE_CAPACITY = 10_000
_DRAIN_ON_EXIT_SECONDS = 2.0


class LogPump:
    def __init__(
        self,
        capacity: int = _LOG_QUEUE_CAPACITY,
        notice_handler: logging.Handler | None = None,
    ) -> None:
        self._queue: queue.Queue[tuple[logging.Handler, logging.LogRecord]] = (
            queue.Queue(capacity)
        )
        self._notice_handler = notice_handler or logging.StreamHandler(sys.stderr)
        self._dropped = 0
        threading.Thread(
            target=self._write_forever, name="log-pump", daemon=True
        ).start()

    def submit(self, target: logging.Handler, record: logging.LogRecord) -> None:
        try:
            self._queue.put_nowait((target, record))
        except queue.Full:
            self._dropped += 1

    def drain(self, timeout: float) -> bool:
        finished = threading.Event()

        def wait_for_queue() -> None:
            self._queue.join()
            finished.set()

        threading.Thread(target=wait_for_queue, daemon=True).start()
        return finished.wait(timeout)

    def _write_forever(self) -> None:
        while True:
            target, record = self._queue.get()
            try:
                target.handle(record)
                self._report_dropped()
            except Exception:
                target.handleError(record)
            finally:
                self._queue.task_done()

    def _report_dropped(self) -> None:
        dropped, self._dropped = self._dropped, 0
        if dropped:
            self._notice_handler.handle(
                logging.makeLogRecord(
                    {
                        "name": __name__,
                        "levelno": logging.WARNING,
                        "levelname": "WARNING",
                        "msg": f"Dropped {dropped} log records: the log stream is not keeping up",
                    }
                )
            )


class NonBlockingHandler(logging.Handler):
    def __init__(self, target: logging.Handler, pump: LogPump) -> None:
        super().__init__(target.level)
        self._target = target
        self._pump = pump

    def emit(self, record: logging.LogRecord) -> None:
        self._pump.submit(self._target, record)


def _wrap_handlers(logger: logging.Logger, pump: LogPump) -> None:
    logger.handlers = [
        handler
        if isinstance(handler, NonBlockingHandler)
        else NonBlockingHandler(handler, pump)
        for handler in logger.handlers
    ]


def install_non_blocking_logging(pump: LogPump | None = None) -> LogPump:
    pump = pump or LogPump()
    root = logging.getLogger()
    if not root.handlers:
        root.addHandler(logging.StreamHandler(sys.stderr))
    _wrap_handlers(root, pump)
    for logger in list(logging.Logger.manager.loggerDict.values()):
        if isinstance(logger, logging.Logger):
            _wrap_handlers(logger, pump)
    atexit.register(pump.drain, _DRAIN_ON_EXIT_SECONDS)
    return pump


def exit_after_draining_on_signals(pump: LogPump) -> None:
    def drain_then_exit(signum: int, _frame: FrameType | None) -> None:
        pump.drain(_DRAIN_ON_EXIT_SECONDS)
        signal.signal(signum, signal.SIG_DFL)
        signal.raise_signal(signum)

    signal.signal(signal.SIGTERM, drain_then_exit)
    signal.signal(signal.SIGINT, drain_then_exit)
