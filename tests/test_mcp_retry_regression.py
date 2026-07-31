"""
Regression tests for zernio-claude-plugin#1: posts_retry / posts_retry_all_failed
never recognized failed posts.

Two bugs conspired:

1. ``posts_retry`` compared the post's status (a generated enum, e.g.
   ``Status10.FAILED``) against the handwritten ``PostStatus.FAILED`` — two
   different enum classes never compare equal, so every failed post was
   rejected with "is not in failed status".
2. ``posts_retry_all_failed`` passed ``PostStatus.FAILED`` into the query
   string, where httpx serialized it via str() as ``status=PostStatus.FAILED``
   instead of ``status=failed`` — so the API matched nothing and the tool
   reported "No failed posts to retry".

These tests drive the real MCP tool functions against a fake in-memory Zernio
API (httpx.MockTransport — no network). The fake API is strict: it only
treats ``status=failed`` (the literal value) as a match, exactly like the real
API, so bug 2 cannot regress silently. It also records every request so we can
assert the exact wire format.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

import late.client.base as client_base
from late import Late
from late.mcp import server as mcp_server

FAILED_POST = {
    "_id": "p1",
    "content": "Hello world",
    "status": "failed",
    "platforms": [{"platform": "twitter", "accountId": "a1"}],
}


class FakeZernioAPI:
    """Minimal in-memory Zernio API with one failed post."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.retried: list[str] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        path = request.url.path

        if request.method == "GET" and path == "/api/v1/posts":
            # Strict, like the real API: only the literal value "failed"
            # matches. "PostStatus.FAILED" (the bug) matches nothing.
            if request.url.params.get("status") == "failed":
                return self._json({"posts": [FAILED_POST], "pagination": {}})
            return self._json({"posts": [], "pagination": {}})

        if request.method == "GET" and path == "/api/v1/posts/p1":
            return self._json({"post": FAILED_POST})

        if request.method == "POST" and path == "/api/v1/posts/p1/retry":
            self.retried.append("p1")
            return self._json({"message": "Post queued for retry"})

        return httpx.Response(404, json={"error": f"unexpected: {path}"})

    @staticmethod
    def _json(body: dict[str, Any]) -> httpx.Response:
        return httpx.Response(
            200,
            content=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )


@pytest.fixture()
def fake_api(monkeypatch: pytest.MonkeyPatch) -> FakeZernioAPI:
    """Route all SDK HTTP traffic to the fake API and wire up the MCP client."""
    api = FakeZernioAPI()
    real_client = httpx.Client

    def patched_client(**kwargs: Any) -> httpx.Client:
        kwargs["transport"] = httpx.MockTransport(api.handler)
        return real_client(**kwargs)

    monkeypatch.setattr(client_base.httpx, "Client", patched_client)
    monkeypatch.setattr(mcp_server, "_get_client", lambda: Late(api_key="test-key"))
    return api


class TestIssue1PostsRetry:
    def test_posts_retry_accepts_failed_post(self, fake_api: FakeZernioAPI) -> None:
        """Bug 1: the status guard rejected every failed post."""
        result = mcp_server.posts_retry("p1")

        assert "queued for retry" in result
        assert "is not in failed status" not in result
        assert fake_api.retried == ["p1"]

    def test_posts_retry_all_failed_finds_the_failed_post(
        self, fake_api: FakeZernioAPI
    ) -> None:
        """Bug 2: the list query serialized the enum wrong and found nothing."""
        result = mcp_server.posts_retry_all_failed()

        assert "Retried 1 post(s)" in result
        assert "No failed posts to retry" not in result
        assert fake_api.retried == ["p1"]

    def test_posts_list_failed_finds_the_failed_post(
        self, fake_api: FakeZernioAPI
    ) -> None:
        """posts_list_failed had bug 2 as well."""
        result = mcp_server.posts_list_failed()

        assert "Found 1 failed post(s)" in result
        assert any(r.url.path == "/api/v1/posts" for r in fake_api.requests)

    def test_status_filter_reaches_api_as_plain_value(
        self, fake_api: FakeZernioAPI
    ) -> None:
        """The wire format itself: status=failed, never status=PostStatus.FAILED."""
        mcp_server.posts_retry_all_failed()

        list_requests = [r for r in fake_api.requests if r.url.path == "/api/v1/posts"]
        assert list_requests, "expected a posts list request"
        for request in list_requests:
            assert request.url.params.get("status") == "failed"
            assert "PostStatus" not in str(request.url)

    def test_posts_retry_reports_clean_status_for_non_failed_post(
        self, fake_api: FakeZernioAPI, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The guard message must show "scheduled", not "Status10.SCHEDULED"."""
        scheduled = dict(FAILED_POST, status="scheduled")

        original = fake_api.handler

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET" and request.url.path == "/api/v1/posts/p1":
                return FakeZernioAPI._json({"post": scheduled})
            return original(request)

        monkeypatch.setattr(fake_api, "handler", handler)

        result = mcp_server.posts_retry("p1")

        assert "is not in failed status" in result
        assert "(current: scheduled)" in result
        assert "Status" not in result.replace("failed status", "")
