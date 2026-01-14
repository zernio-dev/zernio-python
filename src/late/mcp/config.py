"""Configuration management for Late MCP HTTP server."""

import os
import sys
from dataclasses import dataclass

from late.mcp.constants import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    ENV_HOST,
    ENV_LATE_API_KEY,
    ENV_MCP_SERVER_API_KEY,
    ENV_PORT,
)


@dataclass
class ServerConfig:
    """Server configuration."""

    host: str
    port: int
    debug: bool = False

    @classmethod
    def from_env(cls, host: str | None = None, port: int | None = None, debug: bool = False) -> "ServerConfig":
        """
        Create configuration from environment variables.

        Args:
            host: Override host from environment
            port: Override port from environment
            debug: Enable debug mode

        Returns:
            ServerConfig instance
        """
        return cls(
            host=host or os.getenv(ENV_HOST, DEFAULT_HOST),
            port=port or int(os.getenv(ENV_PORT, str(DEFAULT_PORT))),
            debug=debug,
        )


def validate_environment() -> None:
    """
    Validate required environment variables are set.

    Raises:
        SystemExit: If required variables are missing
    """
    missing = []

    if not os.getenv(ENV_LATE_API_KEY):
        missing.append(ENV_LATE_API_KEY)

    if not os.getenv(ENV_MCP_SERVER_API_KEY):
        missing.append(ENV_MCP_SERVER_API_KEY)

    if missing:
        _print_missing_env_error(missing)
        sys.exit(1)


def _print_missing_env_error(missing: list[str]) -> None:
    """Print error message for missing environment variables."""
    print("❌ Missing required environment variables:", file=sys.stderr)
    for var in missing:
        print(f"   - {var}", file=sys.stderr)

    print("\nSet them before starting the server:", file=sys.stderr)
    print(f"  export {ENV_LATE_API_KEY}=your_late_api_key", file=sys.stderr)
    print(f"  export {ENV_MCP_SERVER_API_KEY}=your_secure_key", file=sys.stderr)

    print("\nGenerate a secure key:", file=sys.stderr)
    print('  python -c "import secrets; print(secrets.token_urlsafe(32))"', file=sys.stderr)
