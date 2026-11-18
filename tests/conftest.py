"""Pytest configuration and fixtures."""

import importlib.util
import re
from pathlib import Path

import pytest

# FastMCP 4 needs Python 3.11+, so the MCP server and its tests cannot run on 3.10.
if importlib.util.find_spec("fastmcp") is None:
    _MCP_IMPORT = re.compile(r"^\s*(from|import) (fastmcp|late\.mcp)\b", re.MULTILINE)
    collect_ignore = [
        path.name
        for path in Path(__file__).parent.glob("test_*.py")
        if _MCP_IMPORT.search(path.read_text())
    ]


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return "late_test_key_12345"


@pytest.fixture
def base_url() -> str:
    """Test base URL."""
    return "https://zernio.com/api"
