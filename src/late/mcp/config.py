"""Configuration management for Late MCP HTTP server."""

import os
from dataclasses import dataclass

from late.mcp.constants import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    ENV_HOST,
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

    Note: No environment variables are required for the server.
    Users provide their Late API keys via request headers.
    """
    # No validation needed - users provide API keys in headers
    pass
