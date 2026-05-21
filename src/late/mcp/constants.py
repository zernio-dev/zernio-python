"""Constants for Zernio MCP HTTP server."""

import os

# Server information
SERVICE_NAME = "Zernio MCP Server"
SERVICE_VERSION = "1.2.0"
# Both transports are exposed simultaneously. SSE is kept for backwards
# compatibility with older clients; Streamable HTTP is the modern transport
# (recommended for Claude Code, mcp-remote, and any client behind a proxy
# that closes long-idle connections).
TRANSPORT_TYPE = "sse+streamable-http"

# Default server configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080

# Environment variable names
ENV_HOST = "HOST"
ENV_PORT = "PORT"

# Endpoints
ENDPOINT_ROOT = "/"
ENDPOINT_HEALTH = "/health"
# Legacy SSE transport (two-endpoint protocol: GET /sse + POST /messages/).
# The GET /sse connection is held open for server -> client messages, which
# is the part that gets killed by idle timeouts on proxies / mcp-remote.
ENDPOINT_SSE = "/sse"
ENDPOINT_MESSAGES = "/messages/"
# Modern Streamable HTTP transport (single endpoint, request/response with
# optional chunked streaming). No long-idle connection => survives proxies
# that drop idle TCP. This is the MCP-recommended transport going forward.
ENDPOINT_MCP = "/mcp"

# --- OAuth 2.0 protected-resource discovery (RFC 9728 / MCP authorization spec) ---
# This MCP server is a *resource server*: it does not mint tokens, it accepts
# bearer tokens issued by the Zernio authorization server at zernio.com (and
# also accepts plain Zernio API keys — see verify_late_api_key). A spec-
# compliant client (e.g. Claude's connector) handed only the /mcp URL discovers
# the authorization server by:
#   1. reading the `resource_metadata` parameter on our 401 WWW-Authenticate, or
#   2. fetching /.well-known/oauth-protected-resource on THIS origin.
# Both must be served from the resource server's own origin, which is why this
# metadata lives here on mcp.zernio.com and not only on zernio.com.
ENDPOINT_OAUTH_PROTECTED_RESOURCE = "/.well-known/oauth-protected-resource"

# Public URL of this MCP server — the OAuth `resource` identifier. Must be the
# canonical URL clients actually connect to; per RFC 8707/9728 strict clients
# reject metadata whose `resource` doesn't match the server they're talking to.
# Overridable for non-prod deployments (e.g. a Railway preview URL).
MCP_PUBLIC_URL = os.getenv("MCP_PUBLIC_URL", "https://mcp.zernio.com")

# The Zernio authorization server that issues OAuth tokens for this resource.
OAUTH_AUTHORIZATION_SERVER = "https://zernio.com"

# OAuth scopes advertised in protected-resource metadata. Mirrors the set the
# authorization server defines at zernio.com/.well-known/oauth-authorization-server.
OAUTH_SCOPES = ["posts:read", "posts:write", "accounts:read", "analytics:read"]

# Single source of truth for the 401 WWW-Authenticate challenge (used by both
# transports). The `resource_metadata` parameter (RFC 9728 §5.1) points clients
# at our protected-resource document so they can run OAuth discovery; clients
# that already hold a static API key just send it and skip discovery entirely.
WWW_AUTHENTICATE_BEARER = (
    'Bearer realm="zernio-mcp", '
    f'resource_metadata="{MCP_PUBLIC_URL}{ENDPOINT_OAUTH_PROTECTED_RESOURCE}"'
)

# Documentation
DOCS_URL = "https://docs.zernio.com"
