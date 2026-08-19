"""
Regression tests for the MCP post-reading tools (Crisp session_6e4c63b7).

An integrator reported two defects in the same ticket:

1. The failed-post views read the error from ``post.metadata["error"]``, a key
   the API never populates, and fell back to the literal ``"Unknown error"``.
   The real text lives per platform in ``PlatformTarget.errorMessage``.
   ``posts_list`` did not render an error at all, not even the fallback.
2. ``posts_get``/``posts_list`` raised ``1 validation error for
   PostGetResponse`` on TikTok posts that published fine, because the API
   emits ``platformPostUrl: ""`` when TikTok confirms a publish without a
   numeric video id, and the generated model declared the field as a URI.

The payloads below are the real shapes from the reporting account
(userId 6a4fe17d8adb6036cd5c37c6): a TikTok post failed with the platform's
quota message, and a TikTok post published with a ``p_pub_url~v2.`` publish id
and an empty permalink.

A post holds one entry in ``platforms[]`` per target platform. The entries
below that already published but still carry a stale ``errorMessage`` are
deliberate: production posts do carry that combination, and a platform that
published must never be reported as an error.

Cancelled platforms are covered too. Account-disconnect cleanup writes the
only actionable reason onto that entry, so a failed post targeting a single
platform that got cancelled used to read "Unknown error" while the document
held the answer.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

import late.client.base as client_base
from late import Late
from late.mcp import server as mcp_server

QUOTA_ERROR = "Daily active user quota reached."

# Failed TikTok post. metadata carries billing bookkeeping and no "error" key,
# exactly as the API returns it.
FAILED_POST: dict[str, Any] = {
    "_id": "6a8392cdc6abe639aadbcc21",
    "content": "Free Content DNA report - crezio.ai/report",
    "status": "failed",
    "metadata": {"usageCounted": True, "usageRefunded": True},
    "platforms": [
        {
            "platform": "tiktok",
            "accountId": "6a7e062a77555aae017c9617",
            "status": "failed",
            "errorMessage": QUOTA_ERROR,
            "errorCategory": "user_abuse",
            "errorSource": "platform",
        }
    ],
}

# Published TikTok post whose permalink could not be built: TikTok returned a
# publish id instead of a numeric video id.
EMPTY_URL_POST: dict[str, Any] = {
    "_id": "6a7e23169598cfb3119bb578",
    "content": "Nothing goes viral. Somebody built it to.",
    "status": "published",
    "platforms": [
        {
            "platform": "tiktok",
            "accountId": "6a7e062a77555aae017c9617",
            "status": "published",
            "platformPostId": "p_pub_url~v2.7673609262345750542",
            "platformPostUrl": "",
        }
    ],
}

# Partial failure: one platform published (carrying an errorMessage left over
# from an earlier attempt) and one platform genuinely failed.
MIXED_POST: dict[str, Any] = {
    "_id": "691a85709ed078ff2f35bd16",
    "content": "Cross-posted launch announcement",
    "status": "failed",
    "platforms": [
        {
            "platform": "instagram",
            "accountId": "a1",
            "status": "published",
            "errorMessage": "Publishing failed due to timeout or max retries reached",
            "platformPostUrl": "https://www.instagram.com/reel/ABC123xyz/",
        },
        {
            "platform": "linkedin",
            "accountId": "a2",
            "status": "failed",
            "errorMessage": "Publishing failed due to timeout or max retries reached",
        },
    ],
}

# Failed post whose only platform was cancelled by account-disconnect cleanup.
# That entry carries the one actionable reason, so skipping it leaves the whole
# post reading "Unknown error".
CANCELLED_POST: dict[str, Any] = {
    "_id": "6a74056fa22ac1afb451b7da",
    "content": "Weekly roundup",
    "status": "failed",
    "platforms": [
        {
            "platform": "linkedin",
            "accountId": "a3",
            "status": "cancelled",
            "errorMessage": 'Account "Edward Hollis" was disconnected',
            "errorCategory": "account_issue",
            "errorSource": "user",
        }
    ],
}

# A cancelled platform next to failed ones: the disconnect is the actionable
# line, the timeouts are the generic ones. Neither may displace the other.
MIXED_CANCELLED_POST: dict[str, Any] = {
    "_id": "698f117bdc985b51e808e3e4",
    "content": "Campaign launch",
    "status": "failed",
    "platforms": [
        {
            "platform": "instagram",
            "accountId": "a4",
            "status": "failed",
            "errorMessage": "Publishing failed due to timeout or max retries reached",
        },
        {
            "platform": "facebook",
            "accountId": "a5",
            "status": "cancelled",
            "errorMessage": 'Account "The clam Qalb" was disconnected',
        },
    ],
}

# A draft still holding a cancelled platform: retry never resets a cancelled
# entry, so unfiltered posts_list renders this one too. Deliberate, pinned here.
DRAFT_WITH_CANCELLED_PLATFORM: dict[str, Any] = {
    "_id": "69047ddcbb4db2cc1794478d",
    "content": "Unfinished draft",
    "status": "draft",
    "platforms": [
        {"platform": "youtube", "accountId": "a6", "status": "pending"},
        {
            "platform": "instagram",
            "accountId": "a7",
            "status": "cancelled",
            "errorMessage": 'Account "Cody bailey" was disconnected',
        },
    ],
}

POSTS_BY_ID = {
    p["_id"]: p
    for p in (
        FAILED_POST,
        EMPTY_URL_POST,
        MIXED_POST,
        CANCELLED_POST,
        MIXED_CANCELLED_POST,
        DRAFT_WITH_CANCELLED_PLATFORM,
    )
}


class FakeZernioAPI:
    """In-memory Zernio API serving the payloads above."""

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path

        if request.method == "GET" and path == "/api/v1/posts":
            status = request.url.params.get("status")
            posts = [p for p in POSTS_BY_ID.values() if not status or p["status"] == status]
            return self._json({"posts": posts, "pagination": {}})

        if request.method == "GET" and path.startswith("/api/v1/posts/"):
            post = POSTS_BY_ID.get(path.rsplit("/", 1)[-1])
            if post is not None:
                return self._json({"post": post})

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


@pytest.mark.usefixtures("fake_api")
class TestEmptyPermalinkIsAccepted:
    """Defect 2: an empty permalink must not make the post unreadable."""

    def test_posts_get_returns_the_post(self) -> None:
        result = mcp_server.posts_get("6a7e23169598cfb3119bb578")

        assert "validation error" not in result
        assert "6a7e23169598cfb3119bb578" in result
        assert "published" in result

    def test_posts_list_returns_the_post(self) -> None:
        result = mcp_server.posts_list()

        assert "validation error" not in result
        assert "6a7e23169598cfb3119bb578" in result

    def test_model_accepts_empty_platform_post_url(self) -> None:
        """The generated model itself, so a spec regression fails here first."""
        from late.models import PlatformTarget

        target = PlatformTarget.model_validate(
            {"platform": "tiktok", "status": "published", "platformPostUrl": ""}
        )

        assert target.platformPostUrl == ""

    def test_model_still_accepts_a_real_permalink(self) -> None:
        from late.models import PlatformTarget

        url = "https://www.tiktok.com/@crezio.ai/video/7675444697107614990"
        target = PlatformTarget.model_validate(
            {"platform": "tiktok", "status": "published", "platformPostUrl": url}
        )

        assert str(target.platformPostUrl) == url


@pytest.mark.usefixtures("fake_api")
class TestPlatformErrorIsSurfaced:
    """Defect 1: the real error text lives per platform, not in metadata."""

    def test_posts_get_shows_the_platform_error(self) -> None:
        result = mcp_server.posts_get("6a8392cdc6abe639aadbcc21")

        assert QUOTA_ERROR in result
        assert "Unknown error" not in result

    def test_posts_list_failed_shows_the_platform_error(self) -> None:
        result = mcp_server.posts_list_failed()

        assert QUOTA_ERROR in result
        assert "Unknown error" not in result

    def test_posts_list_shows_the_platform_error(self) -> None:
        """posts_list rendered no error at all, not even the fallback."""
        result = mcp_server.posts_list(status="failed")

        assert QUOTA_ERROR in result

    def test_posts_list_is_quiet_for_healthy_posts(self) -> None:
        result = mcp_server.posts_list(status="published")

        assert "Error" not in result

    def test_error_is_attributed_to_the_failing_platform(self) -> None:
        """A platform that published must not be reported as an error."""
        result = mcp_server.posts_get("691a85709ed078ff2f35bd16")

        error_lines = [line for line in result.splitlines() if "Error" in line]
        assert error_lines, "expected the failed platform to be reported"
        joined = "\n".join(error_lines)
        assert "linkedin" in joined
        assert "instagram" not in joined


@pytest.mark.usefixtures("fake_api")
class TestCancelledPlatformIsSurfaced:
    """Cancelled is the other terminal non-success status.

    Account-disconnect cleanup writes the only actionable reason onto the
    cancelled entry, so a post targeting a single platform that got cancelled
    used to read "Unknown error" while the document held the answer.
    """

    def test_posts_list_failed_shows_the_cancelled_reason(self) -> None:
        result = mcp_server.posts_list_failed()

        assert "Edward Hollis" in result
        assert "Unknown error" not in result

    def test_posts_get_shows_the_cancelled_reason(self) -> None:
        result = mcp_server.posts_get("6a74056fa22ac1afb451b7da")

        assert "Edward Hollis" in result
        assert "linkedin" in result

    def test_cancelled_reason_does_not_displace_the_failed_ones(self) -> None:
        result = mcp_server.posts_get("698f117bdc985b51e808e3e4")

        assert "The clam Qalb" in result
        assert "timeout or max retries reached" in result

    def test_draft_keeps_rendering_its_cancelled_platform(self) -> None:
        """Retry never resets a cancelled entry, so drafts carry them. Declared."""
        result = mcp_server.posts_list(status="draft")

        assert "Cody bailey" in result

    def test_in_progress_platforms_stay_silent(self) -> None:
        """The draft's pending youtube entry must not produce an error line."""
        result = mcp_server.posts_get("69047ddcbb4db2cc1794478d")

        error_lines = [line for line in result.splitlines() if "Error" in line]
        assert len(error_lines) == 1
        assert "youtube" not in error_lines[0]
