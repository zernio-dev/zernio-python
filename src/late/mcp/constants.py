"""Constants for Zernio MCP HTTP server."""

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

# Documentation
DOCS_URL = "https://docs.zernio.com"
