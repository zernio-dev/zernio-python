"""
Exhaustive tests for Late Python SDK.

Tests all functionality: client, resources, models, AI, pipelines, and MCP.
"""

import os

import pytest

# ============================================================================
# CLIENT TESTS
# ============================================================================


class TestClientInitialization:
    """Test client initialization and configuration."""

    def test_client_init_with_api_key(self):
        """Test basic client initialization."""
        from late import Late

        client = Late(api_key="test_key_123")
        assert client.api_key == "test_key_123"
        assert client.base_url == "https://getlate.dev/api"

    def test_client_custom_base_url(self):
        """Test client with custom base URL."""
        from late import Late

        client = Late(api_key="test_key", base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"

    def test_client_requires_api_key(self):
        """Test that empty API key raises error."""
        from late import Late

        with pytest.raises(ValueError, match="API key is required"):
            Late(api_key="")

    def test_client_custom_timeout(self):
        """Test client with custom timeout."""
        from late import Late

        client = Late(api_key="test_key", timeout=60.0)
        assert client.timeout == 60.0

    def test_client_custom_retries(self):
        """Test client with custom max retries."""
        from late import Late

        client = Late(api_key="test_key", max_retries=5)
        assert client.max_retries == 5


class TestClientResources:
    """Test that client has all expected resources."""

    def test_client_has_posts_resource(self, api_key: str):
        """Test posts resource exists."""
        from late import Late
        from late.resources import PostsResource

        client = Late(api_key=api_key)
        assert hasattr(client, "posts")
        assert isinstance(client.posts, PostsResource)

    def test_client_has_profiles_resource(self, api_key: str):
        """Test profiles resource exists."""
        from late import Late
        from late.resources import ProfilesResource

        client = Late(api_key=api_key)
        assert hasattr(client, "profiles")
        assert isinstance(client.profiles, ProfilesResource)

    def test_client_has_accounts_resource(self, api_key: str):
        """Test accounts resource exists."""
        from late import Late
        from late.resources import AccountsResource

        client = Late(api_key=api_key)
        assert hasattr(client, "accounts")
        assert isinstance(client.accounts, AccountsResource)

    def test_client_has_media_resource(self, api_key: str):
        """Test media resource exists."""
        from late import Late
        from late.resources import MediaResource

        client = Late(api_key=api_key)
        assert hasattr(client, "media")
        assert isinstance(client.media, MediaResource)

    def test_client_has_analytics_resource(self, api_key: str):
        """Test analytics resource exists."""
        from late import Late
        from late.resources import AnalyticsResource

        client = Late(api_key=api_key)
        assert hasattr(client, "analytics")
        assert isinstance(client.analytics, AnalyticsResource)

    def test_client_has_tools_resource(self, api_key: str):
        """Test tools resource exists."""
        from late import Late
        from late.resources import ToolsResource

        client = Late(api_key=api_key)
        assert hasattr(client, "tools")
        assert isinstance(client.tools, ToolsResource)

    def test_client_has_queue_resource(self, api_key: str):
        """Test queue resource exists."""
        from late import Late
        from late.resources import QueueResource

        client = Late(api_key=api_key)
        assert hasattr(client, "queue")
        assert isinstance(client.queue, QueueResource)

    def test_client_has_users_resource(self, api_key: str):
        """Test users resource exists."""
        from late import Late
        from late.resources import UsersResource

        client = Late(api_key=api_key)
        assert hasattr(client, "users")
        assert isinstance(client.users, UsersResource)


# ============================================================================
# EXCEPTIONS TESTS
# ============================================================================


class TestExceptions:
    """Test custom exceptions."""

    def test_late_api_error(self):
        """Test LateAPIError creation."""
        from late import LateAPIError

        error = LateAPIError("Test error", status_code=400)
        assert "Test error" in str(error)
        assert error.status_code == 400

    def test_late_api_error_with_details(self):
        """Test LateAPIError with details."""
        from late import LateAPIError

        error = LateAPIError(
            "Bad request",
            status_code=400,
            details={"error": "Invalid data"},
        )
        assert error.details == {"error": "Invalid data"}

    def test_import_all_exceptions(self):
        """Test that all exceptions can be imported."""
        from late.client.exceptions import (
            LateAPIError,
            LateAuthenticationError,
            LateNotFoundError,
            LateRateLimitError,
            LateValidationError,
        )

        assert LateAPIError is not None
        assert LateAuthenticationError is not None
        assert LateNotFoundError is not None
        assert LateRateLimitError is not None
        assert LateValidationError is not None

    def test_authentication_error(self):
        """Test LateAuthenticationError."""
        from late.client.exceptions import LateAuthenticationError

        error = LateAuthenticationError()
        assert error.status_code == 401

    def test_rate_limit_error(self):
        """Test LateRateLimitError."""
        from late.client.exceptions import LateRateLimitError

        error = LateRateLimitError()
        assert error.status_code == 429

    def test_not_found_error(self):
        """Test LateNotFoundError."""
        from late.client.exceptions import LateNotFoundError

        error = LateNotFoundError()
        assert error.status_code == 404


# ============================================================================
# MODELS TESTS
# ============================================================================


class TestModelsImport:
    """Test model imports."""

    def test_import_core_models(self):
        """Test importing core models."""
        from late.models import (
            MediaItem,
            PlatformTarget,
            Post,
            Profile,
            SocialAccount,
        )

        assert Post is not None
        assert Profile is not None
        assert SocialAccount is not None
        assert MediaItem is not None
        assert PlatformTarget is not None

    def test_import_enums(self):
        """Test importing enum models."""
        from late.models import Status, Type, Visibility

        assert Status is not None
        assert Type is not None
        assert Visibility is not None

    def test_import_platform_models(self):
        """Test importing platform-specific models."""
        from late.models import (
            FacebookPlatformData,
            InstagramPlatformData,
            LinkedInPlatformData,
            PinterestPlatformData,
            TikTokSettings,
            TwitterPlatformData,
            YouTubePlatformData,
        )

        assert TikTokSettings is not None
        assert TwitterPlatformData is not None
        assert InstagramPlatformData is not None
        assert FacebookPlatformData is not None
        assert LinkedInPlatformData is not None
        assert YouTubePlatformData is not None
        assert PinterestPlatformData is not None

    def test_import_response_models(self):
        """Test importing response models."""
        from late.models import ErrorResponse, Pagination

        assert Pagination is not None
        assert ErrorResponse is not None


class TestModelsValidation:
    """Test model validation."""

    def test_status_enum_values(self):
        """Test Status enum has expected values."""
        from late.models import Status

        # Enums use uppercase attribute names
        assert hasattr(Status, "DRAFT")
        assert hasattr(Status, "SCHEDULED")
        assert hasattr(Status, "PUBLISHED")
        assert hasattr(Status, "FAILED")
        # Values are lowercase strings
        assert Status.DRAFT.value == "draft"
        assert Status.SCHEDULED.value == "scheduled"

    def test_type_enum_values(self):
        """Test Type enum has expected values."""
        from late.models import Type

        assert hasattr(Type, "IMAGE")
        assert hasattr(Type, "VIDEO")
        assert Type.IMAGE.value == "image"
        assert Type.VIDEO.value == "video"

    def test_tiktok_settings_creation(self):
        """Test TikTokSettings model creation."""
        from late.models import TikTokSettings

        settings = TikTokSettings(
            allow_comment=True,
            allow_duet=True,
            allow_stitch=True,
            privacy_level="PUBLIC",
        )
        assert settings.allow_comment is True
        assert settings.privacy_level == "PUBLIC"

    def test_media_item_creation(self):
        """Test MediaItem with type enum."""
        from late.models import Type
        from late.models._generated.models import MediaItem

        item = MediaItem(type=Type.IMAGE)
        assert item.type == Type.IMAGE


# ============================================================================
# AI TESTS
# ============================================================================


class TestAIImports:
    """Test AI module imports."""

    def test_import_content_generator(self):
        """Test ContentGenerator import."""
        from late.ai import ContentGenerator

        assert ContentGenerator is not None

    def test_import_generate_request(self):
        """Test GenerateRequest import."""
        from late.ai import GenerateRequest

        assert GenerateRequest is not None

    def test_import_generate_response(self):
        """Test GenerateResponse import."""
        from late.ai import GenerateResponse

        assert GenerateResponse is not None

    def test_import_protocols(self):
        """Test protocol imports."""
        from late.ai.protocols import AIProvider, StreamingAIProvider

        assert AIProvider is not None
        assert StreamingAIProvider is not None


class TestGenerateRequest:
    """Test GenerateRequest dataclass."""

    def test_create_basic_request(self):
        """Test creating basic request."""
        from late.ai import GenerateRequest

        request = GenerateRequest(prompt="Write a tweet")
        assert request.prompt == "Write a tweet"
        assert request.max_tokens == 500  # default

    def test_create_request_with_platform(self):
        """Test creating request with platform."""
        from late.ai import GenerateRequest

        request = GenerateRequest(
            prompt="Write content",
            platform="twitter",
        )
        assert request.platform == "twitter"

    def test_create_request_with_tone(self):
        """Test creating request with tone."""
        from late.ai import GenerateRequest

        request = GenerateRequest(
            prompt="Write content",
            tone="professional",
        )
        assert request.tone == "professional"

    def test_create_request_all_fields(self):
        """Test creating request with all fields."""
        from late.ai import GenerateRequest

        request = GenerateRequest(
            prompt="Write a tweet",
            platform="twitter",
            tone="casual",
            max_tokens=280,
        )
        assert request.prompt == "Write a tweet"
        assert request.platform == "twitter"
        assert request.tone == "casual"
        assert request.max_tokens == 280


class TestGenerateResponse:
    """Test GenerateResponse dataclass."""

    def test_create_response(self):
        """Test creating response."""
        from late.ai import GenerateResponse

        response = GenerateResponse(
            text="Generated content",
            provider="openai",
            model="gpt-4",
        )
        assert response.text == "Generated content"
        assert response.provider == "openai"
        assert response.model == "gpt-4"

    def test_response_with_usage(self):
        """Test response with usage stats."""
        from late.ai import GenerateResponse

        response = GenerateResponse(
            text="Content",
            provider="openai",
            model="gpt-4",
            usage={"total_tokens": 100},
        )
        assert response.usage["total_tokens"] == 100


# ============================================================================
# PIPELINES TESTS
# ============================================================================


class TestPipelinesImport:
    """Test pipeline imports."""

    def test_import_csv_scheduler(self):
        """Test CSVSchedulerPipeline import."""
        from late.pipelines import CSVSchedulerPipeline

        assert CSVSchedulerPipeline is not None

    def test_import_cross_poster(self):
        """Test CrossPosterPipeline import."""
        from late.pipelines import CrossPosterPipeline

        assert CrossPosterPipeline is not None

    def test_import_platform_config(self):
        """Test PlatformConfig import."""
        from late.pipelines import PlatformConfig

        assert PlatformConfig is not None

    def test_import_result_types(self):
        """Test result type imports."""
        from late.pipelines import CrossPostResult, ScheduleResult

        assert ScheduleResult is not None
        assert CrossPostResult is not None


class TestPlatformConfig:
    """Test PlatformConfig dataclass."""

    def test_create_basic_config(self):
        """Test creating basic config."""
        from late.pipelines import PlatformConfig

        config = PlatformConfig(
            platform="twitter",
            account_id="acc123",
        )
        assert config.platform == "twitter"
        assert config.account_id == "acc123"
        assert config.delay_minutes == 0  # default

    def test_create_config_with_delay(self):
        """Test creating config with delay."""
        from late.pipelines import PlatformConfig

        config = PlatformConfig(
            platform="linkedin",
            account_id="acc456",
            delay_minutes=10,
        )
        assert config.delay_minutes == 10

    def test_create_config_with_custom_content(self):
        """Test creating config with custom content."""
        from late.pipelines import PlatformConfig

        config = PlatformConfig(
            platform="tiktok",
            account_id="acc789",
            custom_content="Custom TikTok caption",
        )
        assert config.custom_content == "Custom TikTok caption"


class TestScheduleResult:
    """Test ScheduleResult dataclass."""

    def test_create_success_result(self):
        """Test creating successful result."""
        from late.pipelines import ScheduleResult

        result = ScheduleResult(
            row=1,
            success=True,
            post_id="post123",
        )
        assert result.success is True
        assert result.post_id == "post123"
        assert result.row == 1

    def test_create_error_result(self):
        """Test creating error result."""
        from late.pipelines import ScheduleResult

        result = ScheduleResult(
            row=2,
            success=False,
            error="Invalid platform",
        )
        assert result.success is False
        assert result.error == "Invalid platform"


class TestCrossPostResult:
    """Test CrossPostResult dataclass."""

    def test_create_cross_post_result(self):
        """Test creating cross post result."""
        from late.pipelines import CrossPostResult

        result = CrossPostResult(
            platform="twitter",
            success=True,
            post_id="post123",
        )
        assert result.platform == "twitter"
        assert result.success is True

    def test_create_cross_post_error_result(self):
        """Test creating cross post error result."""
        from late.pipelines import CrossPostResult

        result = CrossPostResult(
            platform="linkedin",
            success=False,
            error="Rate limit exceeded",
        )
        assert result.success is False
        assert result.error == "Rate limit exceeded"


# ============================================================================
# MCP TESTS
# ============================================================================


class TestMCPImports:
    """Test MCP module imports."""

    def test_import_mcp_server(self):
        """Test MCP server import."""
        from late.mcp import mcp

        assert mcp is not None

    def test_import_mcp_tools(self):
        """Test MCP tools can be imported."""
        from late.mcp.server import (
            accounts_get,
            accounts_list,
            media_check_upload_status,
            media_generate_upload_link,
            posts_create,
            posts_cross_post,
            posts_delete,
            posts_get,
            posts_list,
            posts_list_failed,
            posts_publish_now,
            posts_retry,
            posts_retry_all_failed,
            posts_update,
            profiles_create,
            profiles_delete,
            profiles_get,
            profiles_list,
            profiles_update,
        )

        # Accounts
        assert accounts_list is not None
        assert accounts_get is not None
        # Profiles
        assert profiles_list is not None
        assert profiles_get is not None
        assert profiles_create is not None
        assert profiles_update is not None
        assert profiles_delete is not None
        # Posts
        assert posts_list is not None
        assert posts_get is not None
        assert posts_create is not None
        assert posts_publish_now is not None
        assert posts_cross_post is not None
        assert posts_update is not None
        assert posts_delete is not None
        assert posts_retry is not None
        assert posts_list_failed is not None
        assert posts_retry_all_failed is not None
        # Media
        assert media_generate_upload_link is not None
        assert media_check_upload_status is not None


# ============================================================================
# RATE LIMITER TESTS
# ============================================================================


class TestRateLimiter:
    """Test rate limiter functionality."""

    def test_rate_limiter_import(self):
        """Test RateLimiter import."""
        from late.client.rate_limiter import RateLimiter

        assert RateLimiter is not None

    def test_rate_limiter_creation(self):
        """Test creating rate limiter."""
        from late.client.rate_limiter import RateLimiter

        limiter = RateLimiter()
        assert limiter is not None
        assert limiter.limit is None
        assert limiter.remaining is None

    def test_rate_limiter_update_from_headers(self):
        """Test updating rate limiter from headers."""
        from late.client.rate_limiter import RateLimiter

        limiter = RateLimiter()
        # Headers use title case as per HTTP standard
        headers = {
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "99",
            "X-RateLimit-Reset": "1734567890",
        }
        limiter.update_from_headers(headers)
        assert limiter.limit == 100
        assert limiter.remaining == 99

    def test_rate_limiter_info(self):
        """Test rate limiter info property."""
        from late.client.rate_limiter import RateLimiter

        limiter = RateLimiter()
        info = limiter.info
        assert info is not None
        assert hasattr(info, "limit")
        assert hasattr(info, "remaining")
        assert hasattr(info, "reset")


# ============================================================================
# INTEGRATION TESTS (require real API key)
# ============================================================================


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY"),
    reason="LATE_API_KEY not set",
)
class TestIntegrationAccounts:
    """Integration tests for accounts resource."""

    def test_list_accounts(self):
        """Test listing accounts from real API."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = client.accounts.list()

        assert "accounts" in response
        assert isinstance(response["accounts"], list)

    def test_accounts_have_required_fields(self):
        """Test accounts have expected fields."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = client.accounts.list()

        if response["accounts"]:
            account = response["accounts"][0]
            assert "_id" in account
            assert "platform" in account


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY"),
    reason="LATE_API_KEY not set",
)
class TestIntegrationProfiles:
    """Integration tests for profiles resource."""

    def test_list_profiles(self):
        """Test listing profiles from real API."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = client.profiles.list()

        assert "profiles" in response
        assert isinstance(response["profiles"], list)


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY"),
    reason="LATE_API_KEY not set",
)
class TestIntegrationPosts:
    """Integration tests for posts resource."""

    def test_list_posts(self):
        """Test listing posts from real API."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = client.posts.list(limit=5)

        assert "posts" in response
        assert isinstance(response["posts"], list)

    def test_list_posts_with_status_filter(self):
        """Test listing posts with status filter."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = client.posts.list(status="published", limit=5)

        assert "posts" in response
        for post in response["posts"]:
            assert post["status"] == "published"


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY") or not os.getenv("OPENAI_API_KEY"),
    reason="LATE_API_KEY or OPENAI_API_KEY not set",
)
class TestIntegrationAI:
    """Integration tests for AI content generation."""

    def test_generate_content(self):
        """Test generating content with OpenAI."""
        from late.ai import ContentGenerator, GenerateRequest

        generator = ContentGenerator(provider="openai")
        response = generator.generate(
            GenerateRequest(
                prompt="Write a one-sentence test message",
                max_tokens=50,
            )
        )

        assert response.text is not None
        assert len(response.text) > 0
        assert response.provider == "openai"


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY"),
    reason="LATE_API_KEY not set",
)
class TestIntegrationMCP:
    """Integration tests for MCP tools."""

    def test_mcp_list_accounts(self):
        """Test MCP list_accounts tool."""
        from late.mcp.server import list_accounts

        result = list_accounts()
        assert "account" in result.lower() or "connected" in result.lower()

    def test_mcp_list_posts(self):
        """Test MCP list_posts tool."""
        from late.mcp.server import list_posts

        result = list_posts(limit=3)
        assert isinstance(result, str)

    def test_mcp_get_account(self):
        """Test MCP get_account tool."""
        from late.mcp.server import get_account

        result = get_account("twitter")
        assert isinstance(result, str)

    def test_mcp_list_failed_posts(self):
        """Test MCP list_failed_posts tool."""
        from late.mcp.server import list_failed_posts

        result = list_failed_posts(limit=5)
        assert isinstance(result, str)

    def test_mcp_get_post(self):
        """Test MCP get_post tool."""
        from late.mcp.server import get_post, list_posts

        # Get a post ID from list
        posts_result = list_posts(limit=1)
        # Extract post ID if available
        if "ID:" in posts_result:
            import re
            match = re.search(r"ID: ([a-f0-9]+)", posts_result)
            if match:
                post_id = match.group(1)
                result = get_post(post_id)
                assert "Post ID:" in result
                assert "Status:" in result


# ============================================================================
# ASYNC TESTS
# ============================================================================


@pytest.mark.skipif(
    not os.getenv("LATE_API_KEY"),
    reason="LATE_API_KEY not set",
)
class TestAsyncClient:
    """Test async client functionality."""

    @pytest.mark.asyncio
    async def test_async_list_accounts(self):
        """Test async listing accounts."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = await client.accounts.alist()

        assert "accounts" in response
        assert isinstance(response["accounts"], list)

    @pytest.mark.asyncio
    async def test_async_list_posts(self):
        """Test async listing posts."""
        from late import Late

        client = Late(api_key=os.getenv("LATE_API_KEY", ""))
        response = await client.posts.alist(limit=3)

        assert "posts" in response
        assert isinstance(response["posts"], list)


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)
class TestAsyncAI:
    """Test async AI functionality."""

    @pytest.mark.asyncio
    async def test_async_generate_content(self):
        """Test async content generation."""
        from late.ai import ContentGenerator, GenerateRequest

        generator = ContentGenerator(provider="openai")
        response = await generator.agenerate(
            GenerateRequest(
                prompt="Write one word",
                max_tokens=10,
            )
        )

        assert response.text is not None
        assert len(response.text) > 0


# ============================================================================
# MEDIA RESOURCE TESTS
# ============================================================================


class TestMediaResourceMethods:
    """Test MediaResource has all expected methods."""

    def test_media_has_upload_method(self, api_key: str):
        """Test media resource has upload method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "upload")
        assert callable(client.media.upload)

    def test_media_has_upload_multiple_method(self, api_key: str):
        """Test media resource has upload_multiple method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "upload_multiple")
        assert callable(client.media.upload_multiple)

    def test_media_has_upload_bytes_method(self, api_key: str):
        """Test media resource has upload_bytes method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "upload_bytes")
        assert callable(client.media.upload_bytes)

    def test_media_has_upload_large_method(self, api_key: str):
        """Test media resource has upload_large method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "upload_large")
        assert callable(client.media.upload_large)

    def test_media_has_upload_large_bytes_method(self, api_key: str):
        """Test media resource has upload_large_bytes method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "upload_large_bytes")
        assert callable(client.media.upload_large_bytes)

    def test_media_has_generate_upload_token_method(self, api_key: str):
        """Test media resource has generate_upload_token method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "generate_upload_token")
        assert callable(client.media.generate_upload_token)

    def test_media_has_check_upload_token_method(self, api_key: str):
        """Test media resource has check_upload_token method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "check_upload_token")
        assert callable(client.media.check_upload_token)

    def test_media_has_async_methods(self, api_key: str):
        """Test media resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.media, "aupload")
        assert hasattr(client.media, "aupload_multiple")
        assert hasattr(client.media, "aupload_bytes")
        assert hasattr(client.media, "aupload_large")
        assert hasattr(client.media, "aupload_large_bytes")
        assert hasattr(client.media, "agenerate_upload_token")
        assert hasattr(client.media, "acheck_upload_token")


class TestUploadModule:
    """Test upload module classes."""

    def test_import_smart_uploader(self):
        """Test SmartUploader import."""
        from late.upload import SmartUploader

        assert SmartUploader is not None

    def test_import_direct_uploader(self):
        """Test DirectUploader import."""
        from late.upload import DirectUploader

        assert DirectUploader is not None

    def test_import_vercel_blob_uploader(self):
        """Test VercelBlobUploader import."""
        from late.upload import VercelBlobUploader

        assert VercelBlobUploader is not None

    def test_import_upload_file(self):
        """Test UploadFile import."""
        from late.upload import UploadFile

        assert UploadFile is not None

    def test_import_upload_result(self):
        """Test UploadResult import."""
        from late.upload import UploadResult

        assert UploadResult is not None

    def test_import_upload_progress(self):
        """Test UploadProgress import."""
        from late.upload import UploadProgress

        assert UploadProgress is not None

    def test_import_large_file_error(self):
        """Test LargeFileError import."""
        from late.upload import LargeFileError

        assert LargeFileError is not None

    def test_upload_progress_creation(self):
        """Test UploadProgress dataclass."""
        from late.upload import UploadProgress

        progress = UploadProgress(
            uploaded_bytes=500,
            total_bytes=1000,
        )
        assert progress.uploaded_bytes == 500
        assert progress.total_bytes == 1000
        assert progress.percentage == 50.0

    def test_large_file_error_creation(self):
        """Test LargeFileError creation."""
        from late.upload import LargeFileError

        error = LargeFileError(file_size=5_000_000, max_direct_size=4_000_000)
        assert "5,000,000" in str(error)
        assert "4,000,000" in str(error) or "4MB" in str(error)


# ============================================================================
# QUEUE RESOURCE TESTS
# ============================================================================


class TestQueueResourceMethods:
    """Test QueueResource has all expected methods."""

    def test_queue_has_get_slots_method(self, api_key: str):
        """Test queue resource has get_slots method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "get_slots")
        assert callable(client.queue.get_slots)

    def test_queue_has_update_slots_method(self, api_key: str):
        """Test queue resource has update_slots method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "update_slots")
        assert callable(client.queue.update_slots)

    def test_queue_has_delete_slots_method(self, api_key: str):
        """Test queue resource has delete_slots method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "delete_slots")
        assert callable(client.queue.delete_slots)

    def test_queue_has_preview_method(self, api_key: str):
        """Test queue resource has preview method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "preview")
        assert callable(client.queue.preview)

    def test_queue_has_next_slot_method(self, api_key: str):
        """Test queue resource has next_slot method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "next_slot")
        assert callable(client.queue.next_slot)

    def test_queue_has_async_methods(self, api_key: str):
        """Test queue resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.queue, "aget_slots")
        assert hasattr(client.queue, "aupdate_slots")
        assert hasattr(client.queue, "adelete_slots")
        assert hasattr(client.queue, "apreview")
        assert hasattr(client.queue, "anext_slot")


# ============================================================================
# TOOLS RESOURCE TESTS
# ============================================================================


class TestToolsResourceMethods:
    """Test ToolsResource has all expected methods."""

    def test_tools_has_youtube_download_method(self, api_key: str):
        """Test tools resource has youtube_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "youtube_download")
        assert callable(client.tools.youtube_download)

    def test_tools_has_youtube_transcript_method(self, api_key: str):
        """Test tools resource has youtube_transcript method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "youtube_transcript")
        assert callable(client.tools.youtube_transcript)

    def test_tools_has_instagram_download_method(self, api_key: str):
        """Test tools resource has instagram_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "instagram_download")
        assert callable(client.tools.instagram_download)

    def test_tools_has_instagram_hashtag_check_method(self, api_key: str):
        """Test tools resource has instagram_hashtag_check method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "instagram_hashtag_check")
        assert callable(client.tools.instagram_hashtag_check)

    def test_tools_has_tiktok_download_method(self, api_key: str):
        """Test tools resource has tiktok_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "tiktok_download")
        assert callable(client.tools.tiktok_download)

    def test_tools_has_twitter_download_method(self, api_key: str):
        """Test tools resource has twitter_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "twitter_download")
        assert callable(client.tools.twitter_download)

    def test_tools_has_facebook_download_method(self, api_key: str):
        """Test tools resource has facebook_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "facebook_download")
        assert callable(client.tools.facebook_download)

    def test_tools_has_linkedin_download_method(self, api_key: str):
        """Test tools resource has linkedin_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "linkedin_download")
        assert callable(client.tools.linkedin_download)

    def test_tools_has_bluesky_download_method(self, api_key: str):
        """Test tools resource has bluesky_download method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "bluesky_download")
        assert callable(client.tools.bluesky_download)

    def test_tools_has_generate_caption_method(self, api_key: str):
        """Test tools resource has generate_caption method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "generate_caption")
        assert callable(client.tools.generate_caption)

    def test_tools_has_async_methods(self, api_key: str):
        """Test tools resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.tools, "ayoutube_download")
        assert hasattr(client.tools, "ayoutube_transcript")
        assert hasattr(client.tools, "ainstagram_download")
        assert hasattr(client.tools, "ainstagram_hashtag_check")
        assert hasattr(client.tools, "atiktok_download")
        assert hasattr(client.tools, "atwitter_download")
        assert hasattr(client.tools, "afacebook_download")
        assert hasattr(client.tools, "alinkedin_download")
        assert hasattr(client.tools, "abluesky_download")
        assert hasattr(client.tools, "agenerate_caption")


# ============================================================================
# PROFILES RESOURCE METHODS TESTS
# ============================================================================


class TestProfilesResourceMethods:
    """Test ProfilesResource has all expected methods."""

    def test_profiles_has_list_method(self, api_key: str):
        """Test profiles resource has list method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "list")
        assert callable(client.profiles.list)

    def test_profiles_has_get_method(self, api_key: str):
        """Test profiles resource has get method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "get")
        assert callable(client.profiles.get)

    def test_profiles_has_create_method(self, api_key: str):
        """Test profiles resource has create method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "create")
        assert callable(client.profiles.create)

    def test_profiles_has_update_method(self, api_key: str):
        """Test profiles resource has update method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "update")
        assert callable(client.profiles.update)

    def test_profiles_has_delete_method(self, api_key: str):
        """Test profiles resource has delete method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "delete")
        assert callable(client.profiles.delete)

    def test_profiles_has_async_methods(self, api_key: str):
        """Test profiles resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.profiles, "alist")
        assert hasattr(client.profiles, "aget")
        assert hasattr(client.profiles, "acreate")
        assert hasattr(client.profiles, "aupdate")
        assert hasattr(client.profiles, "adelete")


# ============================================================================
# ACCOUNTS RESOURCE METHODS TESTS
# ============================================================================


class TestAccountsResourceMethods:
    """Test AccountsResource has all expected methods."""

    def test_accounts_has_list_method(self, api_key: str):
        """Test accounts resource has list method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.accounts, "list")
        assert callable(client.accounts.list)

    def test_accounts_has_get_method(self, api_key: str):
        """Test accounts resource has get method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.accounts, "get")
        assert callable(client.accounts.get)

    def test_accounts_has_get_follower_stats_method(self, api_key: str):
        """Test accounts resource has get_follower_stats method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.accounts, "get_follower_stats")
        assert callable(client.accounts.get_follower_stats)

    def test_accounts_has_async_methods(self, api_key: str):
        """Test accounts resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.accounts, "alist")
        assert hasattr(client.accounts, "aget")
        assert hasattr(client.accounts, "aget_follower_stats")


# ============================================================================
# POSTS RESOURCE METHODS TESTS
# ============================================================================


class TestPostsResourceMethods:
    """Test PostsResource has all expected methods."""

    def test_posts_has_list_method(self, api_key: str):
        """Test posts resource has list method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "list")
        assert callable(client.posts.list)

    def test_posts_has_get_method(self, api_key: str):
        """Test posts resource has get method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "get")
        assert callable(client.posts.get)

    def test_posts_has_create_method(self, api_key: str):
        """Test posts resource has create method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "create")
        assert callable(client.posts.create)

    def test_posts_has_update_method(self, api_key: str):
        """Test posts resource has update method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "update")
        assert callable(client.posts.update)

    def test_posts_has_delete_method(self, api_key: str):
        """Test posts resource has delete method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "delete")
        assert callable(client.posts.delete)

    def test_posts_has_retry_method(self, api_key: str):
        """Test posts resource has retry method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "retry")
        assert callable(client.posts.retry)

    def test_posts_has_bulk_upload_method(self, api_key: str):
        """Test posts resource has bulk_upload method."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "bulk_upload")
        assert callable(client.posts.bulk_upload)

    def test_posts_has_async_methods(self, api_key: str):
        """Test posts resource has async methods."""
        from late import Late

        client = Late(api_key=api_key)
        assert hasattr(client.posts, "alist")
        assert hasattr(client.posts, "aget")
        assert hasattr(client.posts, "acreate")
        assert hasattr(client.posts, "aupdate")
        assert hasattr(client.posts, "adelete")
        assert hasattr(client.posts, "aretry")
