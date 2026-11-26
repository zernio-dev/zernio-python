"""HTTP server for Zernio MCP — Streamable HTTP on FastMCP.

Serves the FastMCP application (tool-search transform + OAuth resource-server
auth) over Streamable HTTP at /mcp. Authentication, the RFC 9728
protected-resource metadata, and the 401 WWW-Authenticate challenge are all
provided by FastMCP's RemoteAuthProvider (see late.mcp.auth). DNS-rebinding
Origin protection is layered on as a lightweight ASGI middleware, scoped to the
transport endpoints so the public /health, / and discovery routes stay open.

The legacy SSE transport (GET /sse + POST /messages/) is retired: its sessions
lived in one worker's memory, so with several workers most POST /messages/
reached a worker without the session and got a 404. /sse now serves
Streamable HTTP, for clients that saved the old URL and try Streamable HTTP
there first (Claude.ai does), and a legacy SSE handshake gets a 410 naming
the /mcp URL.
"""

import argparse
import base64
import hashlib
import json
import logging
import os
import re
import sys
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path

import anyio
import uvicorn
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.requests import ClientDisconnect, Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
)
from starlette.routing import Route
from starlette.types import ASGIApp, Receive, Scope, Send

from late.mcp.auth import is_allowed_origin
from late.mcp.chatgpt_server import chatgpt_mcp
from late.mcp.config import ServerConfig, validate_environment
from late.mcp.constants import (
    DOCS_URL,
    ENDPOINT_CHATGPT,
    ENDPOINT_HEALTH,
    ENDPOINT_MCP,
    ENDPOINT_MESSAGES,
    ENDPOINT_OAUTH_PROTECTED_RESOURCE,
    ENDPOINT_OPENAI_APPS_CHALLENGE,
    ENDPOINT_ROOT,
    ENDPOINT_SSE,
    MCP_PUBLIC_URL,
    OAUTH_AUTHORIZATION_SERVER,
    OAUTH_SCOPES,
    OPENAI_APPS_CHALLENGE_TOKEN,
    SERVICE_NAME,
    SERVICE_VERSION,
    TRANSPORT_TYPE,
)
from late.mcp.middleware import ToolTelemetryMiddleware
from late.mcp.non_blocking_logging import (
    LogPump,
    drain_before_exit,
    exit_after_draining_on_signals,
    install_non_blocking_logging,
)
from late.mcp.server import mcp
from late.mcp.telemetry import (
    init_sentry,
    log_tool_calls_to_stdout,
    quiet_routine_logs,
    ship_tool_calls_to_axiom,
)
from late.mcp.workers import all_workers_ready, mark_worker_ready, worker_count

mcp.add_middleware(ToolTelemetryMiddleware("mcp"))
chatgpt_mcp.add_middleware(ToolTelemetryMiddleware("chatgpt"))

_DISCONNECT_EXC_TYPES = (ClientDisconnect, anyio.ClosedResourceError, anyio.BrokenResourceError)
_EMPTY_STREAM_EXCEPTION_MESSAGE = "Received exception from stream: "


def _is_client_disconnect(exc: BaseException | None) -> bool:
    if exc is None:
        return False
    subexceptions = getattr(exc, "exceptions", None)
    if subexceptions:
        return all(_is_client_disconnect(sub) for sub in subexceptions)
    return isinstance(exc, _DISCONNECT_EXC_TYPES)


class ClientDisconnectLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        exc = record.exc_info[1] if record.exc_info else None
        if exc is not None:
            return not _is_client_disconnect(exc)
        return record.getMessage() != _EMPTY_STREAM_EXCEPTION_MESSAGE


_disconnect_filter = ClientDisconnectLogFilter()
for _logger_name in (
    "mcp.server.streamable_http",
    "mcp.server.streamable_http_manager",
    "mcp.server.lowlevel.server",
):
    logging.getLogger(_logger_name).addFilter(_disconnect_filter)


def _render_landing_page() -> str:
    """The landing page at /, with this deployment's URL filled in."""
    logo = (Path(__file__).parent / "logo.svg").read_text()
    url = f"{MCP_PUBLIC_URL}{ENDPOINT_MCP}"
    cursor_config = base64.b64encode(json.dumps({"url": url}).encode()).decode()
    vscode_config = urllib.parse.quote(json.dumps({"type": "http", "url": url}))
    return (
        (Path(__file__).parent / "landing.html")
        .read_text()
        .replace("{{LOGO}}", logo)
        .replace("{{MCP_URL}}", MCP_PUBLIC_URL)
        .replace("{{CURSOR_CONFIG}}", cursor_config)
        .replace("{{VSCODE_CONFIG}}", vscode_config)
        .replace("{{CLAUDE_CONNECTOR_URL}}", urllib.parse.quote(url, safe=""))
    )


_LANDING_PAGE = _render_landing_page()

# The page's one inline script is allowed by its hash, so nothing else can run.
_LANDING_SCRIPT_HASH = base64.b64encode(
    hashlib.sha256(
        re.search(r"<script>(.*?)</script>", _LANDING_PAGE, re.S).group(1).encode()
    ).digest()
).decode()
_LANDING_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'none'; "
        f"script-src 'sha256-{_LANDING_SCRIPT_HASH}'; "
        "style-src 'unsafe-inline'; "
        "font-src https://cdn.jsdelivr.net; "
        "img-src https://zernio.com data:; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Strict-Transport-Security": "max-age=31536000",
    # Revalidate every load, like zernio.com, so a deploy shows up at once.
    "Cache-Control": "public, max-age=0, must-revalidate",
    # / answers HTML or JSON by Accept, so caches must key on it.
    "Vary": "Accept",
}


@mcp.custom_route(ENDPOINT_ROOT, methods=["GET"])
async def handle_root(request: Request) -> HTMLResponse | JSONResponse:
    """Root endpoint (public, no auth): the landing page for browsers, server
    information as JSON for everything else."""
    if "text/html" in request.headers.get("accept", ""):
        return HTMLResponse(_LANDING_PAGE, headers=_LANDING_HEADERS)
    return JSONResponse(
        {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
            "endpoints": {
                "mcp": f"{ENDPOINT_MCP} (POST) - Streamable HTTP transport (recommended)",
                "health": f"{ENDPOINT_HEALTH} (GET) - Health check",
            },
            "documentation": DOCS_URL,
            "authentication": "Required: 'Authorization: Bearer YOUR_API_KEY'",
        },
        headers={"Vary": "Accept"},
    )


@mcp.custom_route(ENDPOINT_HEALTH, methods=["GET"])
async def handle_health(_request: Request) -> JSONResponse:
    """Health check endpoint (public, no auth)."""
    if not all_workers_ready():
        return JSONResponse({"status": "starting"}, status_code=503)
    return JSONResponse(
        {
            "status": "healthy",
            "service": "zernio-mcp-http",
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
            "commit": os.getenv("RAILWAY_GIT_COMMIT_SHA"),
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
    "websiteUrl": "https://zernio.com",
    "repository": {"url": "https://github.com/zernio-dev/zernio-python", "source": "github"},
    "remotes": [{"type": "streamable-http", "url": f"{MCP_PUBLIC_URL}{ENDPOINT_MCP}"}],
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


@mcp.custom_route(ENDPOINT_OPENAI_APPS_CHALLENGE, methods=["GET"])
async def handle_openai_apps_challenge(_request: Request) -> PlainTextResponse:
    """OpenAI plugin domain-verification token (public, no auth).

    The portal fetches this path and compares the body byte-for-byte with the
    token it issued, so the response is the bare token: no JSON, no newline.
    """
    if not OPENAI_APPS_CHALLENGE_TOKEN:
        return PlainTextResponse("", status_code=404)
    return PlainTextResponse(OPENAI_APPS_CHALLENGE_TOKEN)


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


_ORIGIN_GUARDED_PATHS = (
    ENDPOINT_MCP.rstrip("/"),
    ENDPOINT_SSE.rstrip("/"),
    ENDPOINT_CHATGPT.rstrip("/"),
)


class OriginGuardMiddleware:
    """DNS-rebinding protection, scoped to the transport endpoints.

    Browsers attach an Origin header to cross-site requests; native MCP clients
    and server-to-server callers send none (and are allowed). Only the MCP
    transport endpoints are gated — /health, / and the OAuth discovery docs
    stay public.

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


def _graft_streamable_endpoint(app: Starlette, server: FastMCP, path: str) -> None:
    """Serve `server` over Streamable HTTP at `path` inside the main app.

    The endpoint gets its own route and its own path-inserted discovery
    document (/.well-known/oauth-protected-resource/<path>, whose `resource`
    is the URL the client connected to; MCP clients reject metadata naming
    another resource). A Streamable HTTP session manager only works inside
    its lifespan, so the main app's lifespan is wrapped to run both.
    """
    endpoint_app = server.http_app(
        path=path,
        transport="http",
        stateless_http=True,
        allowed_hosts=["*"],
        allowed_origins=["*"],
    )
    endpoint_paths = (
        path.rstrip("/"),
        f"{ENDPOINT_OAUTH_PROTECTED_RESOURCE}{path}",
    )
    app.router.routes.extend(
        r for r in endpoint_app.routes if getattr(r, "path", "") in endpoint_paths
    )

    main_lifespan = app.router.lifespan_context
    endpoint_lifespan = endpoint_app.router.lifespan_context

    @asynccontextmanager
    async def combined_lifespan(starlette_app: Starlette):
        async with main_lifespan(starlette_app), endpoint_lifespan(endpoint_app):
            yield

    app.router.lifespan_context = combined_lifespan


_SSE_RETIRED_BODY = {
    "error": "sse_transport_removed",
    "message": (
        "The legacy SSE transport (GET /sse + POST /messages/) has been removed. "
        f"Connect with Streamable HTTP at {MCP_PUBLIC_URL}{ENDPOINT_MCP} instead. "
        f"Claude Code: claude mcp add --transport http zernio {MCP_PUBLIC_URL}{ENDPOINT_MCP}. "
        f"mcp-remote: npx -y mcp-remote {MCP_PUBLIC_URL}{ENDPOINT_MCP}."
    ),
    "endpoint": f"{MCP_PUBLIC_URL}{ENDPOINT_MCP}",
    "documentation": DOCS_URL,
}


async def handle_sse_get(request: Request) -> JSONResponse:
    """GET /sse: 410 for the legacy SSE handshake, 405 for Streamable HTTP.

    A Streamable HTTP client sends MCP-Protocol-Version on every request after
    initialize, including the GET it opens for server messages, and gets the
    405 /mcp gives it (stateless, no server stream). A legacy SSE client opens
    with a bare GET and gets the migration message.
    """
    if "mcp-protocol-version" in request.headers:
        return JSONResponse(
            {"error": "Method Not Allowed"},
            status_code=405,
            headers={"Allow": "POST, DELETE"},
        )
    return JSONResponse(_SSE_RETIRED_BODY, status_code=410)


async def handle_sse_messages(_request: Request) -> JSONResponse:
    """POST /messages/: the legacy SSE message endpoint, removed."""
    return JSONResponse(_SSE_RETIRED_BODY, status_code=410)


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

    # /sse keeps working for clients that saved the old URL and speak
    # Streamable HTTP there (Claude.ai tries it before falling back to SSE).
    # GET routes are matched first, so a legacy SSE handshake gets the 410.
    app.router.routes.extend(
        [
            Route(ENDPOINT_SSE, handle_sse_get, methods=["GET", "HEAD"]),
            Route(ENDPOINT_MESSAGES.rstrip("/"), handle_sse_messages, methods=["GET", "POST"]),
            Route(ENDPOINT_MESSAGES, handle_sse_messages, methods=["GET", "POST"]),
        ]
    )
    _graft_streamable_endpoint(app, mcp, ENDPOINT_SSE)
    _graft_streamable_endpoint(app, chatgpt_mcp, ENDPOINT_CHATGPT)

    # add_middleware order: last added runs first. RootAlias must rewrite the
    # path before OriginGuard matches on it. FastMCP authenticates all MCP
    # requests, including initialize and catalog discovery, before processing.
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


def _configure_process(debug: bool) -> None:
    init_sentry()
    log_tool_calls_to_stdout()
    ship_tool_calls_to_axiom()
    if not debug:
        quiet_routine_logs()


def _drain_logs_on_shutdown(app: Starlette, pump: LogPump) -> None:
    serve_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(starlette_app: Starlette):
        async with serve_lifespan(starlette_app) as state:
            yield state
        drain_before_exit(pump)

    app.router.lifespan_context = lifespan


def build_worker_app() -> Starlette:
    """uvicorn factory, run once inside each worker process.

    Logging and Sentry are per process, so each worker sets them up itself.
    Log draining runs at lifespan shutdown instead of from a signal handler:
    uvicorn owns SIGTERM in a worker while it serves, and a handler installed
    here would replace its graceful shutdown and cut in-flight requests.
    """
    _configure_process(debug=False)
    pump = install_non_blocking_logging()
    app = build_app()
    _drain_logs_on_shutdown(app, pump)
    mark_worker_ready()
    return app


def _serve_workers(config: ServerConfig, workers: int) -> None:
    print(f"   Workers:         {workers}", file=sys.stderr)
    uvicorn.run(
        "late.mcp.http_server:build_worker_app",
        factory=True,
        host=config.host,
        port=config.port,
        workers=workers,
        log_level="info",
        # uvicorn kills a worker that misses its 5 s default ping. A worker can
        # only answer once it has imported the tool catalog, 4-5 s on Railway,
        # so the default killed every worker in a loop and failed a deploy.
        timeout_worker_healthcheck=60,
    )


def main() -> None:
    """Entry point for the HTTP server (Streamable HTTP)."""
    validate_environment()
    args = parse_args()
    config = ServerConfig.from_env(host=args.host, port=args.port, debug=args.debug)

    print("Zernio MCP HTTP Server starting...", file=sys.stderr)
    print(f"   Streamable HTTP: http://{config.host}:{config.port}{ENDPOINT_MCP}", file=sys.stderr)
    print(f"   Health check:    http://{config.host}:{config.port}{ENDPOINT_HEALTH}", file=sys.stderr)

    workers = worker_count()
    if workers > 1:
        _serve_workers(config, workers)
        return

    _configure_process(config.debug)
    app = build_app()
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host=config.host,
            port=config.port,
            log_level="debug" if config.debug else "info",
            # uvicorn otherwise parses WEB_CONCURRENCY itself and crashes on "".
            workers=1,
        )
    )
    exit_after_draining_on_signals(install_non_blocking_logging())
    server.run()
    if not server.started:
        sys.exit(1)


if __name__ == "__main__":
    main()
