# Late MCP HTTP Server - Railway Deployment
# Uses uv for fast, reliable dependency management

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies (no dev dependencies in production)
RUN uv sync --frozen --no-dev --extra mcp

# Expose port (Railway will set PORT env var)
EXPOSE 8080

# Health check for Railway monitoring (Railway will use /health endpoint)

# Run HTTP server (Railway sets PORT env var automatically)
CMD ["sh", "-c", "uv run late-mcp-http --host 0.0.0.0 --port ${PORT:-8080}"]