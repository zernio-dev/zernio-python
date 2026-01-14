"""Constants for Late MCP HTTP server."""

# Server information
SERVICE_NAME = "Late MCP Server"
SERVICE_VERSION = "1.1.2"
TRANSPORT_TYPE = "sse"

# Default server configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080

# Environment variable names
ENV_LATE_API_KEY = "LATE_API_KEY"
ENV_MCP_SERVER_API_KEY = "MCP_SERVER_API_KEY"
ENV_HOST = "HOST"
ENV_PORT = "PORT"

# Endpoints
ENDPOINT_ROOT = "/"
ENDPOINT_HEALTH = "/health"
ENDPOINT_SSE = "/sse"
ENDPOINT_MESSAGES = "/messages/"

# Documentation
DOCS_URL = "https://docs.getlate.dev"
