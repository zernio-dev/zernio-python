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
import json
import sys

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from late.mcp.auth import ANONYMOUS_DISCOVERY_BEARER, is_allowed_origin
from late.mcp.config import ServerConfig, validate_environment
from late.mcp.constants import (
    DOCS_URL,
    ENDPOINT_HEALTH,
    ENDPOINT_MCP,
    ENDPOINT_MESSAGES,
    ENDPOINT_OAUTH_PROTECTED_RESOURCE,
    ENDPOINT_ROOT,
    ENDPOINT_SSE,
    MCP_PUBLIC_URL,
    OAUTH_AUTHORIZATION_SERVER,
    OAUTH_SCOPES,
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


_SERVER_CARD = {
    "$schema": "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/server-card.schema.json",
    "name": "zernio",
    "title": "Zernio Social Media API",
    "version": SERVICE_VERSION,
    "description": (
        "Post, schedule, and analyze social media content across 15+ platforms "
        "plus ad management on 7 ad networks, via MCP."
    ),
    "icon": "https://media.zernio.com/site-assets/brand/icon-primary.png",
    "serverInfo": {
        "name": "zernio",
        "title": "Zernio Social Media API",
        "version": SERVICE_VERSION,
        "vendor": "Zernio",
        "homepage": "https://zernio.com",
        "documentation": DOCS_URL,
        "contact": {"email": "support@zernio.com", "url": "https://zernio.com/contact"},
    },
    "transport": {"type": "streamable-http", "endpoint": f"{MCP_PUBLIC_URL}{ENDPOINT_MCP}"},
    "authentication": {
        "type": "oauth2",
        "authorization_endpoint": f"{OAUTH_AUTHORIZATION_SERVER}/oauth/authorize",
        "token_endpoint": f"{OAUTH_AUTHORIZATION_SERVER}/api/oauth/token",
        "registration_endpoint": f"{OAUTH_AUTHORIZATION_SERVER}/api/oauth/register",
        "scopes_supported": list(OAUTH_SCOPES),
    },
    "capabilities": {
        "tools": {"listChanged": True},
        "resources": {"listChanged": True, "subscribe": False},
        "prompts": {"listChanged": False},
    },
    "links": {
        "canonical": "https://zernio.com/.well-known/mcp/server-card.json",
        "serviceDesc": "https://zernio.com/openapi.json",
        "serviceDoc": DOCS_URL,
        "status": "https://status.zernio.com",
    },
}


@mcp.custom_route("/.well-known/mcp/server-card.json", methods=["GET"])
async def handle_server_card(_request: Request) -> JSONResponse:
    """MCP server card on the server's own origin (public, no auth)."""
    return JSONResponse(_SERVER_CARD, headers={"Cache-Control": "public, max-age=3600"})


@mcp.custom_route("/mcp/server-card", methods=["GET"])
async def handle_server_card_alias(_request: Request) -> JSONResponse:
    """Alias path some scanners probe for the manifest (public, no auth)."""
    return JSONResponse(_SERVER_CARD, headers={"Cache-Control": "public, max-age=3600"})


@mcp.custom_route("/server.json", methods=["GET"])
async def handle_registry_manifest(_request: Request) -> JSONResponse:
    """MCP Registry manifest, mirroring the repo-root server.json (public)."""
    return JSONResponse(
        {
            "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
            "name": "com.zernio/zernio",
            "title": "Zernio",
            "description": "Schedule, publish, and analyze social media across 15+ platforms, plus inbox, ads, and analytics.",
            "version": "1.0.0",
            "repository": {"url": "https://github.com/zernio-dev/zernio-python", "source": "github"},
            "remotes": [{"type": "streamable-http", "url": f"{MCP_PUBLIC_URL}{ENDPOINT_MCP}"}],
        },
        headers={"Cache-Control": "public, max-age=3600"},
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


# JSON-RPC methods that carry no user data and are safe to serve without a
# bearer: the connection handshake plus catalog listings/reads. tools/call is
# deliberately absent — an unauthenticated tools/call still gets the HTTP 401
# + WWW-Authenticate challenge, which is what triggers a client's OAuth flow
# (MCP auth spec: clients begin authorization on any 401, mid-session
# included). Discovery succeeding anonymously must not change that.
_ANONYMOUS_METHODS = frozenset(
    {
        "initialize",
        "notifications/initialized",
        "ping",
        "tools/list",
        "prompts/list",
        "resources/list",
        "resources/read",
        "resources/templates/list",
    }
)

# Only parse bodies up to this size when deciding anonymity; larger
# unauthenticated bodies skip the parse and hit the normal 401.
_ANONYMOUS_MAX_BODY_BYTES = 64 * 1024


class RootAliasMiddleware:
    """Serve the MCP transport on the bare origin as well as /mcp.

    Some clients and scanners (is-agentic's Ora among them) are handed
    `https://mcp.zernio.com` and connect to `/` directly, where the JSON info
    route answered 405 to POST. Alias protocol traffic to /mcp: every POST,
    and GET/DELETE only when the client asks for an event stream, so the plain
    GET / info document keeps working for browsers.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"].rstrip("/") == "":
            method = scope.get("method")
            accept = next(
                (v for k, v in scope["headers"] if k.lower() == b"accept"), b""
            )
            if method == "POST" or (
                method in ("GET", "DELETE") and b"text/event-stream" in accept
            ):
                scope = dict(scope)
                scope["path"] = ENDPOINT_MCP
                scope["raw_path"] = ENDPOINT_MCP.encode()
        await self.app(scope, receive, send)


class AnonymousDiscoveryMiddleware:
    """Let discovery-only JSON-RPC requests through without credentials.

    Scanners, agent registries, and MCP clients probe `initialize` and the
    list methods before any auth flow. FastMCP's bearer middleware rejects
    those with an empty-body 401, so a public catalog is invisible to anything
    that cannot complete OAuth (headless crawlers). For an unauthenticated
    POST to the MCP endpoint whose single JSON-RPC message is in
    _ANONYMOUS_METHODS, inject the local discovery bearer (auth.py verifies it
    without an upstream call and grants no scopes); everything else passes
    through untouched and keeps the 401 challenge.

    Pure ASGI (not BaseHTTPMiddleware) so the streamable-HTTP response is
    never buffered; only the REQUEST body is read, then replayed.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self._eligible(scope):
            await self.app(scope, receive, send)
            return

        consumed: list[dict] = []
        body = b""
        complete = True
        while True:
            message = await receive()
            consumed.append(message)
            if message["type"] != "http.request":
                complete = False
                break
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break
            if len(body) > _ANONYMOUS_MAX_BODY_BYTES:
                complete = False
                break

        if complete and len(body) <= _ANONYMOUS_MAX_BODY_BYTES and self._is_discovery(body):
            scope = dict(scope)
            scope["headers"] = [
                *scope["headers"],
                (b"authorization", b"Bearer " + ANONYMOUS_DISCOVERY_BEARER.encode()),
            ]

        replay = iter(consumed)

        async def replaying_receive() -> dict:
            for message in replay:
                return message
            return await receive()

        await self.app(scope, replaying_receive, send)

    @staticmethod
    def _eligible(scope: Scope) -> bool:
        if scope["type"] != "http" or scope.get("method") != "POST":
            return False
        if scope["path"].rstrip("/") != ENDPOINT_MCP.rstrip("/"):
            return False
        return not any(k.lower() == b"authorization" for k, _ in scope["headers"])

    @staticmethod
    def _is_discovery(body: bytes) -> bool:
        try:
            parsed = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            return False
        return isinstance(parsed, dict) and parsed.get("method") in _ANONYMOUS_METHODS


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

    # add_middleware order: last added runs first. RootAlias must rewrite the
    # path before OriginGuard matches on it; AnonymousDiscovery runs last so
    # it sees the aliased path too.
    app.add_middleware(AnonymousDiscoveryMiddleware)
    app.add_middleware(OriginGuardMiddleware)
    app.add_middleware(RootAliasMiddleware)
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
