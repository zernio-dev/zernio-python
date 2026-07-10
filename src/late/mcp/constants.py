"""Constants for Zernio MCP HTTP server."""

import os

# Server information
SERVICE_NAME = "Zernio MCP Server"
SERVICE_VERSION = "1.2.0"
# Streamable HTTP is the primary transport (single endpoint, request/response
# with optional chunked streaming — no long-idle connection for proxies or
# bridges like mcp-remote to kill). Legacy SSE is still served for backwards
# compatibility: production continues to receive GET /sse connections from
# older client configs. New clients should use Streamable HTTP.
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
ENDPOINT_MCP = "/mcp"
# Legacy SSE transport (two-endpoint protocol: GET /sse + POST /messages/),
# deprecated but kept for backwards compatibility with older client configs.
ENDPOINT_SSE = "/sse"
ENDPOINT_MESSAGES = "/messages/"

# --- OAuth 2.0 protected-resource discovery (RFC 9728 / MCP authorization spec) ---
# This MCP server is a *resource server*: it does not mint tokens, it accepts
# bearer tokens issued by the Zernio authorization server at zernio.com (and
# also accepts plain Zernio API keys — see verify_late_api_key). A spec-
# compliant client (e.g. Claude's connector) handed only the /mcp URL discovers
# the authorization server by:
#   1. reading the `resource_metadata` parameter on the 401 WWW-Authenticate
#      challenge (emitted by FastMCP's RemoteAuthProvider), or
#   2. fetching the path-inserted discovery document that FastMCP serves at
#      /.well-known/oauth-protected-resource/mcp on THIS origin.
# The pre-FastMCP server served the document at the root well-known path below;
# it is kept as a permanent redirect to the canonical document so clients still
# holding the old URL keep working (see http_server).
ENDPOINT_OAUTH_PROTECTED_RESOURCE = "/.well-known/oauth-protected-resource"

# Public URL of this MCP server — the OAuth `resource` identifier. Must be the
# canonical URL clients actually connect to; per RFC 8707/9728 strict clients
# reject metadata whose `resource` doesn't match the server they're talking to.
# Overridable for non-prod deployments (e.g. a Railway preview URL).
MCP_PUBLIC_URL = os.getenv("MCP_PUBLIC_URL", "https://mcp.zernio.com")

# The Zernio authorization server that issues OAuth tokens for this resource.
OAUTH_AUTHORIZATION_SERVER = "https://zernio.com"

# OAuth scopes advertised in protected-resource metadata. Mirrors the set the
# authorization server defines at zernio.com/.well-known/oauth-authorization-server
# (kept in sync with libs/oauth/scopes.ts in the main app). Informational only:
# the client requests scopes from the authorization-server metadata, not from
# here, and scopes are not enforced per-endpoint today.
OAUTH_SCOPES = [
    "posts:read",
    "posts:write",
    "accounts:read",
    "accounts:write",
    "analytics:read",
    "ads:write",
    "messaging:write",
    "automations:write",
]

# Documentation
DOCS_URL = "https://docs.zernio.com"
