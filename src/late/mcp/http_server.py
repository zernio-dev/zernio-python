"""HTTP server for Zernio MCP — Streamable HTTP (+ legacy SSE) on FastMCP.

Serves the FastMCP application (tool-search transform + OAuth resource-server
auth) over Streamable HTTP at /mcp. Authentication, the RFC 9728
protected-resource metadata, and the 401 WWW-Authenticate challenge are all
provided by FastMCP's RemoteAuthProvider (see late.mcp.auth). DNS-rebinding
Origin protection is layered on as a lightweight ASGI middleware, scoped to the
transport endpoints so the public /health, / and discovery routes stay open.

The legacy SSE transport (GET /sse + POST /messages/) is deprecated but still
served for backwards compatibility — production continues to receive SSE
connections from older client configs. Its routes come from the same FastMCP
instance (mcp.http_app(transport="sse")), so tools and auth are identical to
the Streamable HTTP endpoint.
"""

import argparse
import sys

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from late.mcp.auth import is_allowed_origin
from late.mcp.config import ServerConfig, validate_environment
from late.mcp.constants import (
    DOCS_URL,
    ENDPOINT_HEALTH,
    ENDPOINT_MCP,
    ENDPOINT_MESSAGES,
    ENDPOINT_OAUTH_PROTECTED_RESOURCE,
    ENDPOINT_ROOT,
    ENDPOINT_SSE,
    SERVICE_NAME,
    SERVICE_VERSION,
    TRANSPORT_TYPE,
)
from late.mcp.server import mcp


@mcp.custom_route(ENDPOINT_ROOT, methods=["GET"])
async def handle_root(_request: Request) -> JSONResponse:
    """Root endpoint with server information (public, no auth)."""
    return JSONResponse(
        {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
            "endpoints": {
                "mcp": f"{ENDPOINT_MCP} (POST) - Streamable HTTP transport (recommended)",
                "sse": f"{ENDPOINT_SSE} (GET) - SSE connection endpoint (legacy, deprecated)",
                "messages": f"{ENDPOINT_MESSAGES} (POST) - SSE message handler (legacy, deprecated)",
                "health": f"{ENDPOINT_HEALTH} (GET) - Health check",
            },
            "documentation": DOCS_URL,
            "authentication": "Required: 'Authorization: Bearer YOUR_API_KEY'",
        }
    )


@mcp.custom_route(ENDPOINT_HEALTH, methods=["GET"])
async def handle_health(_request: Request) -> JSONResponse:
    """Health check endpoint (public, no auth)."""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "zernio-mcp-http",
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
        }
    )


@mcp.custom_route(ENDPOINT_OAUTH_PROTECTED_RESOURCE, methods=["GET"])
async def handle_oauth_protected_resource_legacy(_request: Request) -> RedirectResponse:
    """Legacy RFC 9728 discovery path (public, no auth).

    The pre-FastMCP server served the protected-resource metadata here;
    FastMCP's RemoteAuthProvider serves the canonical document at the
    path-inserted URL (/.well-known/oauth-protected-resource/mcp), which is
    also what the 401 WWW-Authenticate challenge advertises. Permanently
    redirect so clients still holding the old URL keep working.
    """
    return RedirectResponse(
        f"{ENDPOINT_OAUTH_PROTECTED_RESOURCE}{ENDPOINT_MCP}", status_code=308
    )


_ORIGIN_GUARDED_PATHS = (
    ENDPOINT_MCP.rstrip("/"),
    ENDPOINT_SSE.rstrip("/"),
    ENDPOINT_MESSAGES.rstrip("/"),
)


class OriginGuardMiddleware:
    """DNS-rebinding protection, scoped to the transport endpoints.

    Browsers attach an Origin header to cross-site requests; native MCP clients
    and server-to-server callers send none (and are allowed). Only the MCP,
    SSE, and SSE-message endpoints are gated — /health, / and the OAuth
    discovery docs stay public.

    Implemented as a pure ASGI middleware (not BaseHTTPMiddleware) so it never
    buffers the Streamable HTTP response body.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope)
            path = request.url.path.rstrip("/")
            guarded = any(
                path == g or path.startswith(g + "/") for g in _ORIGIN_GUARDED_PATHS
            )
            if guarded and not is_allowed_origin(request):
                response = JSONResponse({"error": "Origin not allowed"}, status_code=403)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


def build_app() -> Starlette:
    """Build the FastMCP Streamable HTTP ASGI app with Origin protection.

    FastMCP's own host/origin checks are opened up ('*') so they never reject
    production traffic (the app sits behind mcp.zernio.com / Railway); the
    OriginGuardMiddleware is the sole DNS-rebinding gate, using our allowlist
    (auth.is_allowed_origin, honouring MCP_ALLOWED_ORIGINS).
    """
    app = mcp.http_app(
        path=ENDPOINT_MCP,
        transport="http",
        stateless_http=True,
        allowed_hosts=["*"],
        allowed_origins=["*"],
    )

    # Legacy SSE transport, deprecated but kept for backwards compatibility
    # (production still receives GET /sse from older client configs). Built
    # from the same FastMCP instance so tools and auth are identical; only the
    # /sse and /messages routes are grafted onto the main app, where they run
    # under its middleware stack and shared server lifespan.
    sse_app = mcp.http_app(
        path=ENDPOINT_SSE,
        transport="sse",
        allowed_hosts=["*"],
        allowed_origins=["*"],
    )
    # Graft /sse, /messages, and the SSE discovery doc (the /sse 401 challenge
    # advertises the path-inserted metadata for its own endpoint).
    sse_paths = (
        ENDPOINT_SSE.rstrip("/"),
        ENDPOINT_MESSAGES.rstrip("/"),
        f"{ENDPOINT_OAUTH_PROTECTED_RESOURCE}{ENDPOINT_SSE}",
    )
    app.router.routes.extend(
        r for r in sse_app.routes if getattr(r, "path", "") in sse_paths
    )

    app.add_middleware(OriginGuardMiddleware)
    return app


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Zernio MCP HTTP Server (Streamable HTTP)")
    parser.add_argument("--host", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, help="Port to listen on (default: 8080)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def main() -> None:
    """Entry point for the HTTP server (Streamable HTTP)."""
    validate_environment()
    args = parse_args()
    config = ServerConfig.from_env(host=args.host, port=args.port, debug=args.debug)

    app = build_app()

    print("Zernio MCP HTTP Server starting...", file=sys.stderr)
    print(f"   Streamable HTTP: http://{config.host}:{config.port}{ENDPOINT_MCP}", file=sys.stderr)
    print(f"   Health check:    http://{config.host}:{config.port}{ENDPOINT_HEALTH}", file=sys.stderr)

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="debug" if config.debug else "info",
    )


if __name__ == "__main__":
    main()
