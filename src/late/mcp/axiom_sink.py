import json
import logging
import os
import threading
from typing import Any

import httpx

_INGEST_URL = "https://api.axiom.co/v1/datasets/{dataset}/ingest"
_FLUSH_INTERVAL_SECONDS = 5.0
_MAX_BATCH = 1_000
_MAX_BUFFERED = 20_000
_INGEST_TIMEOUT_SECONDS = 10.0

logger = logging.getLogger(__name__)


class AxiomIngestHandler(logging.Handler):
    emits_without_blocking = True

    def __init__(
        self,
        *,
        dataset: str,
        token: str,
        static_fields: dict[str, Any] | None = None,
        client: httpx.Client | None = None,
        flush_interval: float = _FLUSH_INTERVAL_SECONDS,
    ) -> None:
        super().__init__(logging.INFO)
        self._url = _INGEST_URL.format(dataset=dataset)
        self._headers = {"Authorization": f"Bearer {token}"}
        self._static_fields = static_fields or {}
        self._client = client or httpx.Client(timeout=_INGEST_TIMEOUT_SECONDS)
        self._flush_interval = flush_interval
        self._buffer: list[dict[str, Any]] = []
        self._buffer_lock = threading.Lock()
        self._send_lock = threading.Lock()
        self._dropped = 0
        self._wake = threading.Event()
        threading.Thread(
            target=self._flush_forever, name="axiom-ingest", daemon=True
        ).start()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            event = json.loads(record.getMessage())
        except ValueError:
            return
        if not isinstance(event, dict):
            return
        with self._buffer_lock:
            if len(self._buffer) >= _MAX_BUFFERED:
                self._dropped += 1
                return
            self._buffer.append({**self._static_fields, **event})
            if len(self._buffer) >= _MAX_BATCH:
                self._wake.set()

    def flush(self) -> None:
        with self._send_lock:
            batch, dropped = self._take_buffer()
            if dropped:
                batch.append(
                    {
                        **self._static_fields,
                        "event": "mcp_axiom_dropped",
                        "dropped": dropped,
                    }
                )
            for start in range(0, len(batch), _MAX_BATCH):
                self._send(batch[start : start + _MAX_BATCH])

    def close(self) -> None:
        self.flush()
        super().close()

    def _take_buffer(self) -> tuple[list[dict[str, Any]], int]:
        with self._buffer_lock:
            batch, self._buffer = self._buffer, []
            dropped, self._dropped = self._dropped, 0
        return batch, dropped

    def _send(self, events: list[dict[str, Any]]) -> None:
        try:
            response = self._client.post(
                self._url,
                params={"timestamp-field": "ts"},
                headers=self._headers,
                json=events,
            )
        except Exception as exc:
            logger.warning(
                "Axiom ingest failed, %d events lost: %s",
                len(events),
                type(exc).__name__,
            )
            return
        if response.status_code >= 400:
            logger.warning(
                "Axiom ingest rejected %d events: HTTP %s",
                len(events),
                response.status_code,
            )

    def _flush_forever(self) -> None:
        while True:
            self._wake.wait(self._flush_interval)
            self._wake.clear()
            self.flush()


def axiom_handler_from_env() -> AxiomIngestHandler | None:
    token = os.getenv("AXIOM_TOKEN")
    dataset = os.getenv("AXIOM_DATASET")
    if not token or not dataset:
        return None
    return AxiomIngestHandler(
        dataset=dataset,
        token=token,
        static_fields={
            "release": (os.getenv("RAILWAY_GIT_COMMIT_SHA") or "")[:12] or None,
            "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME") or "production",
            "worker": os.getpid(),
        },
    )
