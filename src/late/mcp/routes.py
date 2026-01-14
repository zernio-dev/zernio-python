"""Route handlers for Late MCP HTTP server."""

import sys

from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from late.mcp.auth import verify_api_key
from late.mcp.constants import (
    DOCS_URL,
    ENDPOINT_HEALTH,
    ENDPOINT_MESSAGES,
    ENDPOINT_SSE,
    SERVICE_NAME,
    SERVICE_VERSION,
    TRANSPORT_TYPE,
)


async def handle_root(request: Request) -> JSONResponse:
    """Root endpoint with server information."""
    return JSONResponse(
        {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
            "endpoints": {
                "sse": f"{ENDPOINT_SSE} (GET) - SSE connection endpoint",
                "messages": f"{ENDPOINT_MESSAGES} (POST) - Message handler",
                "health": f"{ENDPOINT_HEALTH} (GET) - Health check",
            },
            "documentation": DOCS_URL,
            "authentication": "Required (use X-API-Key header or Bearer token)",
        }
    )


async def handle_health(request: Request) -> JSONResponse:
    """Health check endpoint (public, no auth required)."""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "late-mcp-http",
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
        }
    )


def create_sse_handler(mcp_server, sse_transport: SseServerTransport, debug: bool = False):
    """
    Create SSE connection handler.

    Args:
        mcp_server: MCP server instance
        sse_transport: SSE transport instance
        debug: Enable debug logging

    Returns:
        Async handler function
    """

    async def handle_sse(request: Request) -> Response:
        """Handle SSE connection with authentication."""
        # Verify API key
        if not verify_api_key(request):
            return JSONResponse(
                {"error": "Invalid or missing API key"}, status_code=401
            )

        # Establish SSE connection
        try:
            async with sse_transport.connect_sse(
                request.scope,
                request.receive,
                request._send,
            ) as (read_stream, write_stream):
                await mcp_server.run(
                    read_stream,
                    write_stream,
                    mcp_server.create_initialization_options(),
                )
        except Exception as e:
            if debug:
                print(f"❌ SSE connection error: {e}", file=sys.stderr)
            return JSONResponse(
                {"error": "SSE connection failed"}, status_code=500
            )

        return Response(status_code=200)

    return handle_sse
