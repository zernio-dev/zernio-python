import httpx
import pytest

import late.client.base as client_base
from late.client.exceptions import LateConnectionError, LateTimeoutError
from late.mcp import server


@pytest.fixture
def attempts(monkeypatch):
    sent: list[httpx.Request] = []
    failure: list[Exception] = []

    def fake_request(_client, method, url, **_kwargs):
        sent.append(httpx.Request(method, url))
        raise failure[0]

    monkeypatch.setenv("ZERNIO_API_KEY", "sk_env")
    monkeypatch.setattr(client_base.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(httpx.Client, "request", fake_request)
    return sent, failure


def test_a_read_that_keeps_timing_out_is_attempted_twice(attempts):
    sent, failure = attempts
    failure.append(httpx.ReadTimeout("slow"))

    with pytest.raises(LateTimeoutError):
        server._get_client()._get("/v1/posts")

    assert len(sent) == 2


def test_a_refused_connection_is_attempted_twice(attempts):
    sent, failure = attempts
    failure.append(httpx.ConnectError("refused"))

    with pytest.raises(LateConnectionError):
        server._get_client()._get("/v1/posts")

    assert len(sent) == 2
