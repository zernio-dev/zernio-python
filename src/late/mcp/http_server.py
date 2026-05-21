"""HTTP server for Zernio MCP — exposes both SSE (legacy) and Streamable HTTP (modern) transports."""

import argparse
import contextlib
import sys
from collections.abc import AsyncIterator

import uvicorn
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount, Route

from late.mcp.config import ServerConfig, validate_environment
from late.mcp.constants import (
    ENDPOINT_HEALTH,
    ENDPOINT_MCP,
    ENDPOINT_MESSAGES,
    ENDPOINT_OAUTH_PROTECTED_RESOURCE,
    ENDPOINT_ROOT,
    ENDPOINT_SSE,
)
from late.mcp.routes import (
    create_sse_handler,
    create_streamable_http_handler,
    handle_health,
    handle_oauth_protected_resource,
    handle_root,
)


def create_app(mcp_server, debug: bool = False) -> Starlette:
    """
    Create Starlette application exposing both MCP transports.

    Two transports are mounted simultaneously so existing SSE clients keep
    working while new clients can pick the modern transport:

    - GET  /sse        + POST /messages/  -> legacy SSE transport
    - POST /mcp                            -> Streamable HTTP transport (recommended)

    The Streamable HTTP session manager runs in stateless mode (each request
    is fully independent). Its lifecycle is bound to the Starlette lifespan —
    `session_manager.run()` must be entered before requests are served and
    exited on shutdown, otherwise its internal task group is uninitialised.

    Args:
        mcp_server: MCP server instance (the low-level `Server`, not FastMCP).
        debug: Enable debug mode

    Returns:
        Configured Starlette application
    """
    # --- Legacy SSE transport ---
    sse_transport = SseServerTransport(ENDPOINT_MESSAGES)
    sse_handler = create_sse_handler(mcp_server, sse_transport, debug)

    # --- Modern Streamable HTTP transport ---
    # Stateless mode: each request creates a fresh transport and tears it
    # down afterwards. We pick stateless because our auth model sets the API
    # key in a ContextVar per-request — in stateful mode the long-running
    # server task is started on the first request and would not see API keys
    # set on subsequent requests.
    streamable_session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        stateless=True,
    )
    streamable_handler = create_streamable_http_handler(streamable_session_manager, debug)

    @contextlib.asynccontextmanager
    async def lifespan(_app: Starlette) -> AsyncIterator[None]:
        """Drive the Streamable HTTP session manager's task group for the app's lifetime."""
        async with streamable_session_manager.run():
            yield

    return Starlette(
        debug=debug,
        lifespan=lifespan,
        routes=[
            Route(ENDPOINT_ROOT, endpoint=handle_root, methods=["GET"]),
            Route(ENDPOINT_HEALTH, endpoint=handle_health, methods=["GET"]),
            # OAuth 2.0 protected-resource metadata (RFC 9728). Public, no auth.
            # Lets clients given only the /mcp URL discover the zernio.com
            # authorization server and run the OAuth flow.
            Route(
                ENDPOINT_OAUTH_PROTECTED_RESOURCE,
                endpoint=handle_oauth_protected_resource,
                methods=["GET"],
            ),
            # Streamable HTTP — single endpoint, modern transport.
            # We use Route (not Mount) because Mount on "/mcp" forces a 307
            # redirect to "/mcp/", and most HTTP clients drop the request
            # body / downgrade POST to GET on redirect. Route accepts an
            # ASGI callable as `endpoint`, which is what we want.
            # POST = client requests, GET = server-initiated streams,
            # DELETE = explicit session termination (Streamable HTTP spec).
            Route(ENDPOINT_MCP, endpoint=streamable_handler, methods=["GET", "POST", "DELETE"]),
            # SSE (legacy) — two-endpoint protocol, kept for backwards compat.
            Route(ENDPOINT_SSE, endpoint=sse_handler),
            Mount(ENDPOINT_MESSAGES, app=sse_transport.handle_post_message),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Zernio MCP HTTP Server (SSE + Streamable HTTP)")
    parser.add_argument("--host", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, help="Port to listen on (default: 8080)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def print_startup_info(config: ServerConfig) -> None:
    """Print server startup information."""
    print("Zernio MCP HTTP Server starting...")
    print(f"   Host: {config.host}")
    print(f"   Port: {config.port}")
    print(f"   Streamable HTTP endpoint (recommended): http://{config.host}:{config.port}{ENDPOINT_MCP}")
    print(f"   SSE endpoint (legacy): http://{config.host}:{config.port}{ENDPOINT_SSE}")
    print(f"   Health check: http://{config.host}:{config.port}{ENDPOINT_HEALTH}")
    print(f"   Debug mode: {'enabled' if config.debug else 'disabled'}")
    print()
    print("Ready to accept MCP connections!")


def main() -> None:
    """Entry point for the HTTP server (serves both SSE and Streamable HTTP)."""
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
        print(f"Failed to access MCP server: {e}", file=sys.stderr)
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
