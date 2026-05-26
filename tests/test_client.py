"""Tests for Late client."""

from importlib.metadata import PackageNotFoundError, version

import pytest

from late import Late
from late.client import base as base_module
from late.client.base import BaseClient


class TestLateClient:
    """Tests for the Late client."""

    def test_client_init(self, api_key: str) -> None:
        """Test client initialization."""
        client = Late(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://zernio.com/api"

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


class TestUserAgent:
    """User-Agent must reflect the installed package version, not a hardcoded value."""

    def _installed_version(self) -> str:
        for dist_name in ("zernio-sdk", "late-sdk"):
            try:
                return version(dist_name)
            except PackageNotFoundError:
                continue
        pytest.fail("Neither zernio-sdk nor late-sdk is installed")

    def test_sdk_version_matches_installed_distribution(self) -> None:
        assert self._installed_version() == BaseClient.SDK_VERSION

    def test_sdk_version_is_not_the_old_hardcoded_value(self) -> None:
        # Regression guard: User-Agent used to be pinned at 1.0.0 forever.
        assert BaseClient.SDK_VERSION != "1.0.0"

    def test_user_agent_header_uses_resolved_version(self, api_key: str) -> None:
        client = BaseClient(api_key=api_key)
        assert client._headers["User-Agent"] == f"late-python-sdk/{self._installed_version()}"

    def test_resolve_sdk_version_falls_back_when_no_distribution_installed(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _always_missing(_name: str) -> str:
            raise PackageNotFoundError

        monkeypatch.setattr(base_module, "version", _always_missing)
        assert base_module._resolve_sdk_version() == "0.0.0+unknown"


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
