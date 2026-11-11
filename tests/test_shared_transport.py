import threading

import httpx

from late import Late
from late.mcp import server


class RecordingTransport(httpx.MockTransport):
    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.closed = False
        super().__init__(self._respond)

    def _respond(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(200, json={"ok": True})

    def close(self) -> None:
        self.closed = True


def test_requests_reuse_a_shared_transport_without_closing_it():
    transport = RecordingTransport()
    client = Late(api_key="sk_one", transport=transport)

    client._get("/v1/posts")
    client._post("/v1/posts", data={"content": "hi"})

    assert len(transport.requests) == 2
    assert not transport.closed


def test_clients_sharing_a_transport_keep_their_own_api_key():
    transport = RecordingTransport()

    Late(api_key="sk_one", transport=transport)._get("/v1/posts")
    Late(api_key="sk_two", transport=transport)._get("/v1/posts")

    assert [r.headers["Authorization"] for r in transport.requests] == [
        "Bearer sk_one",
        "Bearer sk_two",
    ]


def test_file_uploads_go_through_the_shared_transport_as_multipart():
    transport = RecordingTransport()
    client = Late(api_key="sk_one", transport=transport)

    client._post("/v1/media", files={"file": ("a.png", b"png", "image/png")})

    (request,) = transport.requests
    assert request.headers["Content-Type"].startswith("multipart/form-data")
    assert not transport.closed


def test_mcp_tool_calls_reuse_one_transport_per_thread(monkeypatch):
    monkeypatch.setenv("ZERNIO_API_KEY", "sk_env")
    other_thread: list[httpx.BaseTransport | None] = []
    worker = threading.Thread(
        target=lambda: other_thread.append(server._get_client()._transport)
    )

    first, second = server._get_client(), server._get_client()
    worker.start()
    worker.join()

    assert first._transport is not None
    assert first._transport is second._transport
    assert other_thread[0] is not first._transport
