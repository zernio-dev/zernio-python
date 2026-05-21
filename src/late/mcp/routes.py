"""Route handlers for Zernio MCP HTTP server."""

import sys

from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import Receive, Scope, Send

from late.mcp.auth import extract_late_api_key, is_allowed_origin, verify_late_api_key
from late.mcp.constants import (
    DOCS_URL,
    ENDPOINT_HEALTH,
    ENDPOINT_MCP,
    ENDPOINT_MESSAGES,
    ENDPOINT_SSE,
    MCP_PUBLIC_URL,
    OAUTH_AUTHORIZATION_SERVER,
    OAUTH_SCOPES,
    SERVICE_NAME,
    SERVICE_VERSION,
    TRANSPORT_TYPE,
    WWW_AUTHENTICATE_BEARER,
)


async def handle_root(_request: Request) -> JSONResponse:
    """Root endpoint with server information."""
    return JSONResponse(
        {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
            "endpoints": {
                # Modern transport — listed first as the recommended choice.
                "mcp": f"{ENDPOINT_MCP} (POST) - Streamable HTTP transport (recommended)",
                # Legacy transport — kept for backwards compatibility with
                # older clients that haven't migrated off SSE yet.
                "sse": f"{ENDPOINT_SSE} (GET) - SSE connection endpoint (legacy)",
                "messages": f"{ENDPOINT_MESSAGES} (POST) - SSE message handler (legacy)",
                "health": f"{ENDPOINT_HEALTH} (GET) - Health check",
            },
            "documentation": DOCS_URL,
            "authentication": "Required: 'Authorization: Bearer YOUR_API_KEY'",
        }
    )


async def handle_health(_request: Request) -> JSONResponse:
    """Health check endpoint (public, no auth required)."""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "zernio-mcp-http",
            "version": SERVICE_VERSION,
            "transport": TRANSPORT_TYPE,
        }
    )


async def handle_oauth_protected_resource(_request: Request) -> JSONResponse:
    """
    OAuth 2.0 Protected Resource Metadata (RFC 9728) — public, no auth required.

    Served from this MCP server's own origin so a client given only the `/mcp`
    endpoint URL can discover the Zernio authorization server and run the OAuth
    flow (this is what Claude's connector needs; without it, it can't find our
    OAuth and reports "couldn't reach the server"). `resource` is THIS server's
    canonical URL, not zernio.com's: RFC 8707/9728 require it to identify the
    resource the client is actually talking to, and strict clients reject a
    mismatch. The authorization server itself (token/authorize/register +
    its own metadata) lives at zernio.com — we only point clients to it here.
    """
    return JSONResponse(
        {
            "resource": MCP_PUBLIC_URL,
            "authorization_servers": [OAUTH_AUTHORIZATION_SERVER],
            "scopes_supported": OAUTH_SCOPES,
            "bearer_methods_supported": ["header"],
        },
        headers={"Cache-Control": "public, max-age=3600"},
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
        # DNS-rebinding protection: reject browser requests from un-allowlisted
        # origins before doing anything else.
        if not is_allowed_origin(request):
            return JSONResponse({"error": "Origin not allowed"}, status_code=403)

        # 401 responses carry the shared bearer challenge (WWW_AUTHENTICATE_BEARER)
        # whose `resource_metadata` parameter points clients at our OAuth
        # protected-resource document — see the docstring on `_send_json_error`
        # below for the full rationale.
        bearer_challenge = {"WWW-Authenticate": WWW_AUTHENTICATE_BEARER}
        api_key = extract_late_api_key(request)
        if not api_key:
            return JSONResponse(
                {"error": "Missing API key. Provide via Authorization header: 'Authorization: Bearer YOUR_API_KEY'"},
                status_code=401,
                headers=bearer_challenge,
            )

        # Verify API key by making test request
        if not await verify_late_api_key(api_key):
            return JSONResponse(
                {"error": "Invalid API key"},
                status_code=401,
                headers=bearer_challenge,
            )

        # Store API key in request state for use in MCP tools
        request.state.late_api_key = api_key

        # Establish SSE connection
        try:
            # Import here to set context variable before running MCP
            from late.mcp.server import set_late_api_key

            set_late_api_key(api_key)

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
                print(f"SSE connection error: {e}", file=sys.stderr)
            return JSONResponse(
                {"error": "SSE connection failed"}, status_code=500
            )

        return Response(status_code=200)

    return handle_sse


async def _send_json_error(scope: Scope, receive: Receive, send: Send, status: int, message: str) -> None:
    """
    Send a JSON error response over raw ASGI.

    Used by the Streamable HTTP wrapper because the session manager expects
    a raw ASGI callable, not a Starlette endpoint — so we can't just `return
    JSONResponse(...)` from the wrapper.

    On 401 we add the shared bearer challenge (WWW_AUTHENTICATE_BEARER), which
    carries a `resource_metadata` parameter (RFC 9728 §5.1) pointing at our
    /.well-known/oauth-protected-resource document. This supports two kinds of
    client without conflict:
      - clients that already hold a static Zernio API key (mcp-remote with
        --header, Claude Code) just send it on the retry and skip discovery;
      - clients with no pre-supplied token (Claude's GUI connector) follow
        `resource_metadata` to discover the zernio.com authorization server and
        run the OAuth flow. The token they obtain is accepted here because
        verify_late_api_key validates any bearer against the Zernio API, which
        recognises both API keys and OAuth access tokens.
    """
    headers = {"WWW-Authenticate": WWW_AUTHENTICATE_BEARER} if status == 401 else None
    response = JSONResponse({"error": message}, status_code=status, headers=headers)
    await response(scope, receive, send)


class StreamableHTTPAuthHandler:
    """
    Auth-wrapped ASGI handler for the Streamable HTTP transport.

    Streamable HTTP is the modern MCP transport. Unlike SSE, it does not hold
    a long-idle connection open — each request/response is self-contained
    (with optional chunked streaming for the response). This makes it robust
    against proxies and bridges (e.g. mcp-remote in Claude Code) that close
    idle TCP connections after a few minutes.

    The session manager is configured in stateless mode so each request is
    independent. This sidesteps the ContextVar lifetime issue we'd hit in
    stateful mode: the API key set on request N would not be visible to the
    long-running server task started on request 1.

    Implemented as a callable class (not a plain async function) because
    Starlette's `Route` introspects callable endpoints — a plain function
    gets wrapped as a `(request)`-style endpoint rather than treated as a
    raw ASGI app. A class instance bypasses that detection and is invoked
    directly with `(scope, receive, send)`.
    """

    def __init__(self, session_manager: StreamableHTTPSessionManager, debug: bool = False) -> None:
        """
        Args:
            session_manager: A StreamableHTTPSessionManager bound to the MCP
                server instance. Its `.run()` lifespan must be entered by
                the Starlette app — see `http_server.create_app`.
            debug: Enable debug logging for handler errors.
        """
        self._session_manager = session_manager
        self._debug = debug

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Build a Request just to extract headers — we don't consume the body
        # here (the session manager will do that downstream).
        request = Request(scope, receive)

        # DNS-rebinding protection: reject browser requests from un-allowlisted
        # origins before auth or body handling.
        if not is_allowed_origin(request):
            await _send_json_error(scope, receive, send, 403, "Origin not allowed")
            return

        api_key = extract_late_api_key(request)
        if not api_key:
            await _send_json_error(
                scope,
                receive,
                send,
                401,
                "Missing API key. Provide via Authorization header: 'Authorization: Bearer YOUR_API_KEY'",
            )
            return

        if not await verify_late_api_key(api_key):
            await _send_json_error(scope, receive, send, 401, "Invalid API key")
            return

        # Set the API key in the ContextVar before delegating. In stateless
        # mode the session manager spawns a fresh per-request server task
        # via anyio's task group, which propagates the current context — so
        # MCP tools will see this key when they call _get_client().
        from late.mcp.server import set_late_api_key

        set_late_api_key(api_key)

        try:
            await self._session_manager.handle_request(scope, receive, send)
        except Exception as e:
            if self._debug:
                print(f"Streamable HTTP request error: {e}", file=sys.stderr)
            # If the session manager already started sending a response we
            # can't send another — re-raise to let the framework log it.
            raise


def create_streamable_http_handler(session_manager: StreamableHTTPSessionManager, debug: bool = False) -> StreamableHTTPAuthHandler:
    """Backwards-compatible factory wrapping `StreamableHTTPAuthHandler`."""
    return StreamableHTTPAuthHandler(session_manager, debug)
