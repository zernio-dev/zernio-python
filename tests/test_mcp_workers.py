import os

import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient

from late.mcp import http_server, workers
from late.mcp.config import ServerConfig
from late.mcp.http_server import _drain_logs_on_shutdown, build_app


@pytest.fixture
def ready_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(workers.tempfile, "gettempdir", lambda: str(tmp_path))
    return workers._ready_dir()


def _health_status() -> int:
    return TestClient(build_app()).get("/health").status_code


def test_one_process_when_web_concurrency_is_unset(monkeypatch):
    monkeypatch.delenv("WEB_CONCURRENCY", raising=False)

    assert workers.worker_count() == 1


def test_an_empty_web_concurrency_means_one_process(monkeypatch):
    monkeypatch.setenv("WEB_CONCURRENCY", "")

    assert workers.worker_count() == 1


def test_web_concurrency_sets_the_worker_count(monkeypatch):
    monkeypatch.setenv("WEB_CONCURRENCY", "4")

    assert workers.worker_count() == 4


@pytest.mark.usefixtures("ready_dir")
def test_a_single_process_is_healthy_without_ready_markers(monkeypatch):
    monkeypatch.delenv("WEB_CONCURRENCY", raising=False)

    assert _health_status() == 200


def test_health_waits_for_every_worker(monkeypatch, ready_dir):
    monkeypatch.setenv("WEB_CONCURRENCY", "3")

    assert _health_status() == 503

    workers.mark_worker_ready()
    (ready_dir / "other-worker-1").touch()
    assert _health_status() == 503

    (ready_dir / "other-worker-2").touch()
    assert _health_status() == 200


def test_marking_ready_records_this_process(ready_dir):
    workers.mark_worker_ready()

    assert [p.name for p in ready_dir.iterdir()] == [str(os.getpid())]


def test_worker_logs_drain_after_the_app_shuts_down():
    events: list[str] = []

    class FakePump:
        def drain(self, timeout: float) -> bool:
            events.append(f"drain {timeout}")
            return True

    app = Starlette()
    _drain_logs_on_shutdown(app, FakePump())

    with TestClient(app):
        events.append("serving")

    assert events == ["serving", "drain 2.0"]


def test_workers_get_longer_than_their_startup_to_answer_uvicorn(monkeypatch):
    started: dict = {}
    monkeypatch.setattr(http_server.uvicorn, "run", lambda *_, **kw: started.update(kw))

    http_server._serve_workers(ServerConfig(host="127.0.0.1", port=8080), workers=4)

    assert started["workers"] == 4
    assert started["timeout_worker_healthcheck"] >= 30
