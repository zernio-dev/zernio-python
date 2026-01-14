"""HTTP/SSE server for Late MCP."""

import argparse
import sys

import uvicorn
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route

from late.mcp.config import ServerConfig, validate_environment
from late.mcp.constants import (
    ENDPOINT_HEALTH,
    ENDPOINT_MESSAGES,
    ENDPOINT_ROOT,
    ENDPOINT_SSE,
)
from late.mcp.routes import create_sse_handler, handle_health, handle_root


def create_app(mcp_server, debug: bool = False) -> Starlette:
    """
    Create Starlette application with SSE transport.

    Args:
        mcp_server: MCP server instance
        debug: Enable debug mode

    Returns:
        Configured Starlette application
    """
    sse_transport = SseServerTransport(ENDPOINT_MESSAGES)
    sse_handler = create_sse_handler(mcp_server, sse_transport, debug)

    return Starlette(
        debug=debug,
        routes=[
            Route(ENDPOINT_ROOT, endpoint=handle_root, methods=["GET"]),
            Route(ENDPOINT_HEALTH, endpoint=handle_health, methods=["GET"]),
            Route(ENDPOINT_SSE, endpoint=sse_handler),
            Mount(ENDPOINT_MESSAGES, app=sse_transport.handle_post_message),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Late MCP HTTP/SSE Server")
    parser.add_argument("--host", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, help="Port to listen on (default: 8080)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def print_startup_info(config: ServerConfig) -> None:
    """Print server startup information."""
    print("🚀 Late MCP HTTP Server starting...")
    print(f"   Host: {config.host}")
    print(f"   Port: {config.port}")
    print(f"   SSE endpoint: http://{config.host}:{config.port}{ENDPOINT_SSE}")
    print(f"   Health check: http://{config.host}:{config.port}{ENDPOINT_HEALTH}")
    print(f"   Debug mode: {'enabled' if config.debug else 'disabled'}")
    print()
    print("📡 Ready to accept MCP connections!")


def main() -> None:
    """Entry point for HTTP/SSE server."""
    # Validate environment
    validate_environment()

    # Parse arguments
    args = parse_args()

    # Create configuration
    config = ServerConfig.from_env(host=args.host, port=args.port, debug=args.debug)

    # Import and get MCP server
    try:
        from late.mcp.server import mcp

        mcp_server = mcp._mcp_server
    except (ImportError, AttributeError) as e:
        print(f"❌ Failed to access MCP server: {e}", file=sys.stderr)
        sys.exit(1)

    # Create app
    app = create_app(mcp_server, debug=config.debug)

    # Print startup info
    print_startup_info(config)

    # Run server
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="debug" if config.debug else "info",
    )


if __name__ == "__main__":
    main()
