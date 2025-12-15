"""
Integration tests for all SDK resources.

These tests mock HTTP responses to validate that:
1. The SDK correctly builds requests (URLs, params, payloads)
2. The SDK correctly handles responses
3. All CRUD operations work as expected

To run with real API (requires LATE_API_KEY env var):
    pytest tests/test_integration.py --run-real-api
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

import httpx
import pytest
import respx

from late import Late
from late.client.exceptions import (
    LateAPIError,
    LateAuthenticationError,
    LateNotFoundError,
    LateRateLimitError,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def client() -> Late:
    """Create a Late client for testing."""
    return Late(api_key="test_api_key", base_url="https://api.test.com")


@pytest.fixture
def mock_post() -> dict[str, Any]:
    """Sample post response."""
    return {
        "_id": "post_123",
        "content": "Test post content",
        "status": "scheduled",
        "platforms": [
            {"platform": "twitter", "accountId": "acc_123", "status": "pending"}
        ],
        "scheduledFor": "2024-12-25T10:00:00Z",
        "timezone": "UTC",
        "createdAt": "2024-12-01T10:00:00Z",
        "updatedAt": "2024-12-01T10:00:00Z",
    }


@pytest.fixture
def mock_profile() -> dict[str, Any]:
    """Sample profile response."""
    return {
        "_id": "profile_123",
        "name": "Test Profile",
        "description": "A test profile",
        "color": "#4CAF50",
        "isDefault": False,
        "createdAt": "2024-12-01T10:00:00Z",
    }


@pytest.fixture
def mock_account() -> dict[str, Any]:
    """Sample account response."""
    return {
        "_id": "acc_123",
        "platform": "twitter",
        "username": "testuser",
        "displayName": "Test User",
        "profileId": "profile_123",
    }


# =============================================================================
# Posts Resource Tests
# =============================================================================


class TestPostsResource:
    """Tests for the Posts resource."""

    @respx.mock
    def test_list_posts(self, client: Late, mock_post: dict) -> None:
        """Test listing posts."""
        route = respx.get("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "posts": [mock_post],
                    "pagination": {"page": 1, "limit": 10, "total": 1, "pages": 1},
                },
            )
        )

        result = client.posts.list()

        assert route.called
        assert len(result.posts) == 1
        assert result.posts[0].field_id == "post_123"
        assert result.pagination.total == 1

    @respx.mock
    def test_list_posts_with_filters(self, client: Late, mock_post: dict) -> None:
        """Test listing posts with all filters."""
        route = respx.get("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(200, json={"posts": [mock_post], "pagination": {}})
        )

        client.posts.list(
            page=2,
            limit=20,
            status="scheduled",
            platform="twitter",
            profile_id="prof_123",
            created_by="user_123",
            date_from="2024-01-01",
            date_to="2024-12-31",
            include_hidden=True,
        )

        assert route.called
        request = route.calls[0].request
        url_str = str(request.url)
        assert "page=2" in url_str
        assert "limit=20" in url_str
        assert "status=scheduled" in url_str
        assert "platform=twitter" in url_str
        assert "profileId=prof_123" in url_str
        assert "createdBy=user_123" in url_str
        assert "dateFrom=2024-01-01" in url_str
        assert "dateTo=2024-12-31" in url_str
        # Boolean is serialized as lowercase 'true' or 'True'
        assert "includeHidden=true" in url_str or "includeHidden=True" in url_str

    @respx.mock
    def test_get_post(self, client: Late, mock_post: dict) -> None:
        """Test getting a single post."""
        route = respx.get("https://api.test.com/v1/posts/post_123").mock(
            return_value=httpx.Response(200, json={"post": mock_post})
        )

        result = client.posts.get("post_123")

        assert route.called
        assert result.post.field_id == "post_123"

    @respx.mock
    def test_create_post_scheduled(self, client: Late, mock_post: dict) -> None:
        """Test creating a scheduled post."""
        route = respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(
                201, json={"message": "Post scheduled successfully", "post": mock_post}
            )
        )

        scheduled_time = datetime.now() + timedelta(hours=1)
        result = client.posts.create(
            content="Test post",
            platforms=[{"platform": "twitter", "accountId": "acc_123"}],
            scheduled_for=scheduled_time,
            timezone="America/New_York",
        )

        assert route.called
        assert result.message == "Post scheduled successfully"

        # Verify request payload
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["content"] == "Test post"
        assert body["platforms"][0]["platform"] == "twitter"
        assert "scheduledFor" in body
        assert body["timezone"] == "America/New_York"

    @respx.mock
    def test_create_post_publish_now(self, client: Late, mock_post: dict) -> None:
        """Test creating and publishing a post immediately."""
        published_post = {**mock_post, "status": "published"}
        route = respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(
                201, json={"message": "Post published successfully", "post": published_post}
            )
        )

        client.posts.create(
            content="Publish now!",
            platforms=[{"platform": "twitter", "accountId": "acc_123"}],
            publish_now=True,
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["publishNow"] is True

    @respx.mock
    def test_create_post_as_draft(self, client: Late, mock_post: dict) -> None:
        """Test creating a draft post."""
        draft_post = {**mock_post, "status": "draft"}
        route = respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(
                201, json={"message": "Draft saved", "post": draft_post}
            )
        )

        client.posts.create(
            content="Draft content",
            platforms=[{"platform": "twitter", "accountId": "acc_123"}],
            is_draft=True,
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["isDraft"] is True

    @respx.mock
    def test_create_post_with_all_options(self, client: Late, mock_post: dict) -> None:
        """Test creating a post with all optional parameters."""
        route = respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(201, json={"message": "Created", "post": mock_post})
        )

        client.posts.create(
            content="Full post",
            platforms=[
                {
                    "platform": "twitter",
                    "accountId": "acc_123",
                    "customContent": "Custom for Twitter",
                }
            ],
            title="My Title",
            media_items=[{"type": "image", "url": "https://example.com/image.jpg"}],
            scheduled_for="2024-12-25T10:00:00Z",
            timezone="UTC",
            tags=["tag1", "tag2"],
            hashtags=["#python", "#sdk"],
            mentions=["@user1"],
            crossposting_enabled=False,
            metadata={"custom": "data"},
            tiktok_settings={"privacyLevel": "public"},
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["title"] == "My Title"
        assert body["mediaItems"][0]["type"] == "image"
        assert body["tags"] == ["tag1", "tag2"]
        assert body["hashtags"] == ["#python", "#sdk"]
        assert body["mentions"] == ["@user1"]
        assert body["crosspostingEnabled"] is False
        assert body["metadata"]["custom"] == "data"
        assert body["tiktokSettings"]["privacyLevel"] == "public"

    @respx.mock
    def test_update_post(self, client: Late, mock_post: dict) -> None:
        """Test updating a post."""
        updated_post = {**mock_post, "content": "Updated content"}
        route = respx.put("https://api.test.com/v1/posts/post_123").mock(
            return_value=httpx.Response(
                200, json={"message": "Post updated", "post": updated_post}
            )
        )

        client.posts.update(
            "post_123",
            content="Updated content",
            scheduled_for=datetime.now() + timedelta(days=1),
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["content"] == "Updated content"
        assert "scheduledFor" in body

    @respx.mock
    def test_delete_post(self, client: Late) -> None:
        """Test deleting a post."""
        route = respx.delete("https://api.test.com/v1/posts/post_123").mock(
            return_value=httpx.Response(200, json={"message": "Post deleted successfully"})
        )

        result = client.posts.delete("post_123")

        assert route.called
        assert result.message == "Post deleted successfully"

    @respx.mock
    def test_retry_post(self, client: Late, mock_post: dict) -> None:
        """Test retrying a failed post."""
        route = respx.post("https://api.test.com/v1/posts/post_123/retry").mock(
            return_value=httpx.Response(200, json={"message": "Retrying", "post": mock_post})
        )

        result = client.posts.retry("post_123")

        assert route.called
        assert result.message == "Retrying"


# =============================================================================
# Profiles Resource Tests
# =============================================================================


class TestProfilesResource:
    """Tests for the Profiles resource."""

    @respx.mock
    def test_list_profiles(self, client: Late, mock_profile: dict) -> None:
        """Test listing profiles."""
        route = respx.get("https://api.test.com/v1/profiles").mock(
            return_value=httpx.Response(200, json={"profiles": [mock_profile]})
        )

        result = client.profiles.list()

        assert route.called
        assert len(result.profiles) == 1
        assert result.profiles[0].name == "Test Profile"

    @respx.mock
    def test_get_profile(self, client: Late, mock_profile: dict) -> None:
        """Test getting a single profile."""
        route = respx.get("https://api.test.com/v1/profiles/profile_123").mock(
            return_value=httpx.Response(200, json={"profile": mock_profile})
        )

        result = client.profiles.get("profile_123")

        assert route.called
        assert result.profile.field_id == "profile_123"

    @respx.mock
    def test_create_profile(self, client: Late, mock_profile: dict) -> None:
        """Test creating a profile."""
        route = respx.post("https://api.test.com/v1/profiles").mock(
            return_value=httpx.Response(
                201, json={"message": "Profile created", "profile": mock_profile}
            )
        )

        client.profiles.create(
            name="New Profile",
            description="A new profile",
            color="#FF5722",
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["name"] == "New Profile"
        assert body["description"] == "A new profile"
        assert body["color"] == "#FF5722"

    @respx.mock
    def test_update_profile(self, client: Late, mock_profile: dict) -> None:
        """Test updating a profile."""
        updated_profile = {**mock_profile, "name": "Updated Name", "isDefault": True}
        route = respx.put("https://api.test.com/v1/profiles/profile_123").mock(
            return_value=httpx.Response(
                200, json={"message": "Profile updated", "profile": updated_profile}
            )
        )

        client.profiles.update(
            "profile_123",
            name="Updated Name",
            is_default=True,
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["name"] == "Updated Name"
        assert body["isDefault"] is True

    @respx.mock
    def test_delete_profile(self, client: Late) -> None:
        """Test deleting a profile."""
        route = respx.delete("https://api.test.com/v1/profiles/profile_123").mock(
            return_value=httpx.Response(200, json={"message": "Profile deleted"})
        )

        result = client.profiles.delete("profile_123")

        assert route.called
        assert result.message == "Profile deleted"


# =============================================================================
# Accounts Resource Tests
# =============================================================================


class TestAccountsResource:
    """Tests for the Accounts resource."""

    @respx.mock
    def test_list_accounts(self, client: Late, mock_account: dict) -> None:
        """Test listing accounts."""
        route = respx.get("https://api.test.com/v1/accounts").mock(
            return_value=httpx.Response(
                200, json={"accounts": [mock_account], "hasAnalyticsAccess": False}
            )
        )

        result = client.accounts.list()

        assert route.called
        assert len(result.accounts) == 1
        assert result.accounts[0].platform == "twitter"

    @respx.mock
    def test_list_accounts_by_profile(self, client: Late, mock_account: dict) -> None:
        """Test listing accounts filtered by profile."""
        route = respx.get("https://api.test.com/v1/accounts").mock(
            return_value=httpx.Response(200, json={"accounts": [mock_account]})
        )

        client.accounts.list(profile_id="profile_123")

        assert route.called
        request = route.calls[0].request
        assert "profileId=profile_123" in str(request.url)

    @respx.mock
    def test_get_account(self, client: Late, mock_account: dict) -> None:
        """Test getting a single account."""
        route = respx.get("https://api.test.com/v1/accounts/acc_123").mock(
            return_value=httpx.Response(200, json={"account": mock_account})
        )

        result = client.accounts.get("acc_123")

        assert route.called
        assert result.account.field_id == "acc_123"

    @respx.mock
    def test_get_follower_stats(self, client: Late) -> None:
        """Test getting follower statistics."""
        route = respx.get("https://api.test.com/v1/accounts/follower-stats").mock(
            return_value=httpx.Response(
                200,
                json={
                    "stats": [
                        {"accountId": "acc_123", "followersCount": 1000, "change": 50}
                    ]
                },
            )
        )

        client.accounts.get_follower_stats(account_ids=["acc_123", "acc_456"])

        assert route.called
        request = route.calls[0].request
        # URL may encode the comma as %2C
        url_str = str(request.url)
        assert "accountIds=" in url_str
        assert "acc_123" in url_str
        assert "acc_456" in url_str


# =============================================================================
# Media Resource Tests
# =============================================================================


class TestMediaResource:
    """Tests for the Media resource."""

    @respx.mock
    def test_generate_upload_token(self, client: Late) -> None:
        """Test generating an upload token."""
        route = respx.post("https://api.test.com/v1/media/upload-token").mock(
            return_value=httpx.Response(
                200,
                json={
                    "token": "tok_123",
                    "uploadUrl": "https://upload.example.com/tok_123",
                    "expiresAt": "2024-12-01T11:00:00Z",
                    "status": "pending",
                },
            )
        )

        result = client.media.generate_upload_token()

        assert route.called
        assert result.token == "tok_123"
        assert result.uploadUrl is not None

    @respx.mock
    def test_check_upload_token(self, client: Late) -> None:
        """Test checking upload token status."""
        route = respx.get("https://api.test.com/v1/media/upload-token").mock(
            return_value=httpx.Response(
                200,
                json={
                    "token": "tok_123",
                    "status": "completed",
                    "files": [{"url": "https://cdn.example.com/image.jpg", "type": "image"}],
                },
            )
        )

        result = client.media.check_upload_token("tok_123")

        assert route.called
        request = route.calls[0].request
        assert "token=tok_123" in str(request.url)
        assert result.status.value == "completed"
        assert len(result.files) == 1


# =============================================================================
# Queue Resource Tests
# =============================================================================


class TestQueueResource:
    """Tests for the Queue resource."""

    @respx.mock
    def test_get_slots(self, client: Late) -> None:
        """Test getting queue slots."""
        route = respx.get("https://api.test.com/v1/queue/slots").mock(
            return_value=httpx.Response(
                200,
                json={
                    "schedule": {
                        "timezone": "UTC",
                        "slots": [{"dayOfWeek": 1, "time": "09:00"}],
                        "active": True,
                    }
                },
            )
        )

        client.queue.get_slots(profile_id="profile_123")

        assert route.called
        request = route.calls[0].request
        assert "profileId=profile_123" in str(request.url)

    @respx.mock
    def test_update_slots(self, client: Late) -> None:
        """Test updating queue slots."""
        route = respx.put("https://api.test.com/v1/queue/slots").mock(
            return_value=httpx.Response(200, json={"message": "Queue updated"})
        )

        client.queue.update_slots(
            profile_id="profile_123",
            timezone="America/New_York",
            slots=[
                {"dayOfWeek": 1, "time": "09:00"},
                {"dayOfWeek": 3, "time": "14:00"},
            ],
            active=True,
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["profileId"] == "profile_123"
        assert body["timezone"] == "America/New_York"
        assert len(body["slots"]) == 2

    @respx.mock
    def test_next_slot(self, client: Late) -> None:
        """Test getting next available slot."""
        route = respx.get("https://api.test.com/v1/queue/next-slot").mock(
            return_value=httpx.Response(
                200, json={"nextSlot": "2024-12-02T09:00:00Z", "timezone": "UTC"}
            )
        )

        result = client.queue.next_slot()

        assert route.called
        assert result.nextSlot is not None


# =============================================================================
# Analytics Resource Tests
# =============================================================================


class TestAnalyticsResource:
    """Tests for the Analytics resource."""

    @respx.mock
    def test_get_analytics(self, client: Late) -> None:
        """Test getting analytics."""
        route = respx.get("https://api.test.com/v1/analytics").mock(
            return_value=httpx.Response(
                200,
                json={
                    "analytics": [
                        {"postId": "post_123", "impressions": 1000, "engagements": 50}
                    ]
                },
            )
        )

        client.analytics.get(period="30d")

        assert route.called
        request = route.calls[0].request
        assert "period=30d" in str(request.url)

    @respx.mock
    def test_get_usage(self, client: Late) -> None:
        """Test getting usage stats."""
        route = respx.get("https://api.test.com/v1/usage-stats").mock(
            return_value=httpx.Response(
                200,
                json={
                    "postsThisMonth": 50,
                    "postsLimit": 100,
                    "uploadsThisMonth": 25,
                    "uploadsLimit": 50,
                },
            )
        )

        result = client.analytics.get_usage()

        assert route.called
        assert result["postsThisMonth"] == 50


# =============================================================================
# Tools Resource Tests
# =============================================================================


class TestToolsResource:
    """Tests for the Tools resource."""

    @respx.mock
    def test_youtube_download(self, client: Late) -> None:
        """Test YouTube download."""
        route = respx.get("https://api.test.com/v1/tools/youtube/download").mock(
            return_value=httpx.Response(
                200, json={"url": "https://cdn.example.com/video.mp4", "title": "Video"}
            )
        )

        client.tools.youtube_download("https://youtube.com/watch?v=abc123")

        assert route.called
        request = route.calls[0].request
        assert "url=https" in str(request.url)

    @respx.mock
    def test_youtube_transcript(self, client: Late) -> None:
        """Test YouTube transcript."""
        route = respx.get("https://api.test.com/v1/tools/youtube/transcript").mock(
            return_value=httpx.Response(
                200, json={"transcript": "Hello world...", "language": "en"}
            )
        )

        client.tools.youtube_transcript(
            "https://youtube.com/watch?v=abc123", lang="en"
        )

        assert route.called
        request = route.calls[0].request
        assert "lang=en" in str(request.url)

    @respx.mock
    def test_instagram_download(self, client: Late) -> None:
        """Test Instagram download."""
        route = respx.get("https://api.test.com/v1/tools/instagram/download").mock(
            return_value=httpx.Response(200, json={"url": "https://cdn.example.com/reel.mp4"})
        )

        client.tools.instagram_download("https://instagram.com/reel/abc123")

        assert route.called

    @respx.mock
    def test_tiktok_download(self, client: Late) -> None:
        """Test TikTok download."""
        route = respx.get("https://api.test.com/v1/tools/tiktok/download").mock(
            return_value=httpx.Response(200, json={"url": "https://cdn.example.com/video.mp4"})
        )

        client.tools.tiktok_download("https://tiktok.com/@user/video/123", no_watermark=True)

        assert route.called
        request = route.calls[0].request
        assert "noWatermark=true" in str(request.url)

    @respx.mock
    def test_generate_caption(self, client: Late) -> None:
        """Test AI caption generation."""
        route = respx.post("https://api.test.com/v1/tools/caption-generator").mock(
            return_value=httpx.Response(
                200, json={"captions": ["A beautiful sunset over the ocean."]}
            )
        )

        client.tools.generate_caption(
            "https://example.com/image.jpg",
            tone="professional",
            prompt="Describe this image",
        )

        assert route.called
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body["imageUrl"] == "https://example.com/image.jpg"
        assert body["tone"] == "professional"
        assert body["prompt"] == "Describe this image"


# =============================================================================
# Users Resource Tests
# =============================================================================


class TestUsersResource:
    """Tests for the Users resource."""

    @respx.mock
    def test_list_users(self, client: Late) -> None:
        """Test listing users."""
        route = respx.get("https://api.test.com/v1/users").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": [
                        {"_id": "user_123", "email": "test@example.com", "role": "admin"}
                    ]
                },
            )
        )

        result = client.users.list()

        assert route.called
        assert len(result.users) == 1

    @respx.mock
    def test_get_user(self, client: Late) -> None:
        """Test getting a user."""
        route = respx.get("https://api.test.com/v1/users/user_123").mock(
            return_value=httpx.Response(
                200, json={"user": {"_id": "user_123", "email": "test@example.com"}}
            )
        )

        result = client.users.get("user_123")

        assert route.called
        assert result.user.field_id == "user_123"


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    def test_authentication_error(self, client: Late) -> None:
        """Test 401 authentication error."""
        respx.get("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(401, json={"error": "Invalid API key"})
        )

        with pytest.raises(LateAuthenticationError) as exc_info:
            client.posts.list()

        assert "Invalid API key" in str(exc_info.value)

    @respx.mock
    def test_not_found_error(self, client: Late) -> None:
        """Test 404 not found error."""
        respx.get("https://api.test.com/v1/posts/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": "Post not found"})
        )

        with pytest.raises(LateNotFoundError) as exc_info:
            client.posts.get("nonexistent")

        assert "Post not found" in str(exc_info.value)

    @respx.mock
    def test_rate_limit_error(self, client: Late) -> None:
        """Test 429 rate limit error."""
        respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(
                429,
                json={"error": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
        )

        with pytest.raises(LateRateLimitError) as exc_info:
            client.posts.create(
                content="Test",
                platforms=[{"platform": "twitter", "accountId": "acc_123"}],
            )

        assert exc_info.value.status_code == 429

    @respx.mock
    def test_generic_api_error(self, client: Late) -> None:
        """Test generic API error."""
        respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(400, json={"error": "Invalid content"})
        )

        with pytest.raises(LateAPIError) as exc_info:
            client.posts.create(
                content="",
                platforms=[{"platform": "twitter", "accountId": "acc_123"}],
            )

        assert exc_info.value.status_code == 400


# =============================================================================
# Async Tests
# =============================================================================


class TestAsyncOperations:
    """Tests for async operations."""

    @pytest.fixture
    def async_client(self) -> Late:
        """Create an async Late client for testing."""
        return Late(api_key="test_api_key", base_url="https://api.test.com")

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_list_posts(self, async_client: Late, mock_post: dict) -> None:
        """Test async list posts."""
        route = respx.get("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(200, json={"posts": [mock_post], "pagination": {}})
        )

        async with async_client:
            result = await async_client.posts.alist()

        assert route.called
        assert len(result.posts) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_create_post(self, async_client: Late, mock_post: dict) -> None:
        """Test async create post."""
        route = respx.post("https://api.test.com/v1/posts").mock(
            return_value=httpx.Response(201, json={"message": "Created", "post": mock_post})
        )

        async with async_client:
            result = await async_client.posts.acreate(
                content="Async post",
                platforms=[{"platform": "twitter", "accountId": "acc_123"}],
                publish_now=True,
            )

        assert route.called
        assert result.message == "Created"

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_profile_crud(self, async_client: Late, mock_profile: dict) -> None:
        """Test async profile CRUD operations."""
        # Create
        respx.post("https://api.test.com/v1/profiles").mock(
            return_value=httpx.Response(201, json={"profile": mock_profile})
        )
        # Update
        respx.put("https://api.test.com/v1/profiles/profile_123").mock(
            return_value=httpx.Response(200, json={"profile": mock_profile})
        )
        # Delete
        respx.delete("https://api.test.com/v1/profiles/profile_123").mock(
            return_value=httpx.Response(200, json={"message": "Deleted"})
        )

        async with async_client:
            # Create
            result = await async_client.profiles.acreate(name="Test")
            assert result.profile.field_id == "profile_123"

            # Update
            result = await async_client.profiles.aupdate("profile_123", name="Updated")
            assert result.profile.field_id == "profile_123"

            # Delete
            result = await async_client.profiles.adelete("profile_123")
            assert result.message == "Deleted"


# =============================================================================
# Base Resource Tests
# =============================================================================


class TestBaseResourceHelpers:
    """Tests for base resource helper methods."""

    def test_build_params_filters_none(self, client: Late) -> None:
        """Test that _build_params filters out None values."""
        params = client.posts._build_params(
            page=1,
            limit=10,
            status=None,
            platform="twitter",
        )

        assert "page" in params
        assert "limit" in params
        assert "platform" in params
        assert "status" not in params

    def test_build_params_converts_to_camel_case(self, client: Late) -> None:
        """Test that _build_params converts snake_case to camelCase."""
        params = client.posts._build_params(
            profile_id="123",
            date_from="2024-01-01",
            include_hidden=True,
        )

        assert "profileId" in params
        assert "dateFrom" in params
        assert "includeHidden" in params
        assert "profile_id" not in params

    def test_build_payload_handles_datetime(self, client: Late) -> None:
        """Test that _build_payload serializes datetime objects."""
        dt = datetime(2024, 12, 25, 10, 0, 0)
        payload = client.posts._build_payload(
            content="Test",
            scheduled_for=dt,
        )

        assert payload["scheduledFor"] == "2024-12-25T10:00:00"

    def test_path_helper(self, client: Late) -> None:
        """Test the _path helper method."""
        assert client.posts._path() == "/v1/posts"
        assert client.posts._path("123") == "/v1/posts/123"
        assert client.posts._path("123", "retry") == "/v1/posts/123/retry"
