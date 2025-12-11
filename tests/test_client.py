"""Tests for Late client."""

import pytest

from late import Late


class TestLateClient:
    """Tests for the Late client."""

    def test_client_init(self, api_key: str) -> None:
        """Test client initialization."""
        client = Late(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://getlate.dev/api"

    def test_client_custom_base_url(self, api_key: str) -> None:
        """Test client with custom base URL."""
        client = Late(api_key=api_key, base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"

    def test_client_requires_api_key(self) -> None:
        """Test that API key is required."""
        with pytest.raises(ValueError, match="API key is required"):
            Late(api_key="")

    def test_client_has_resources(self, api_key: str) -> None:
        """Test that client has all resources."""
        client = Late(api_key=api_key)
        assert hasattr(client, "posts")
        assert hasattr(client, "profiles")
        assert hasattr(client, "accounts")
        assert hasattr(client, "users")
        assert hasattr(client, "media")
        assert hasattr(client, "analytics")
        assert hasattr(client, "tools")
        assert hasattr(client, "queue")


class TestModels:
    """Tests for models."""

    def test_models_import(self) -> None:
        """Test that models can be imported."""
        from late.models import (
            Post,
            Profile,
            SocialAccount,
        )

        assert Post is not None
        assert Profile is not None
        assert SocialAccount is not None


class TestAI:
    """Tests for AI module."""

    def test_ai_import(self) -> None:
        """Test that AI module can be imported."""
        from late.ai import ContentGenerator, GenerateRequest, GenerateResponse

        assert ContentGenerator is not None
        assert GenerateRequest is not None
        assert GenerateResponse is not None

    def test_generate_request(self) -> None:
        """Test GenerateRequest dataclass."""
        from late.ai import GenerateRequest

        request = GenerateRequest(
            prompt="Write a tweet",
            platform="twitter",
            tone="professional",
        )
        assert request.prompt == "Write a tweet"
        assert request.platform == "twitter"
        assert request.max_tokens == 500  # default


class TestPipelines:
    """Tests for pipelines."""

    def test_pipelines_import(self) -> None:
        """Test that pipelines can be imported."""
        from late.pipelines import (
            CrossPosterPipeline,
            CSVSchedulerPipeline,
            PlatformConfig,
        )

        assert CSVSchedulerPipeline is not None
        assert CrossPosterPipeline is not None
        assert PlatformConfig is not None

    def test_platform_config(self) -> None:
        """Test PlatformConfig dataclass."""
        from late.pipelines import PlatformConfig

        config = PlatformConfig(
            platform="twitter",
            account_id="acc123",
            delay_minutes=5,
        )
        assert config.platform == "twitter"
        assert config.account_id == "acc123"
        assert config.delay_minutes == 5
