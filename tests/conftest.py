"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return "late_test_key_12345"


@pytest.fixture
def base_url() -> str:
    """Test base URL."""
    return "https://getlate.dev/api"
