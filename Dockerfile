# Late MCP HTTP Server - Railway Deployment
# Uses uv for fast, reliable dependency management

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV MALLOC_ARENA_MAX=2

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies (no dev dependencies in production)
RUN uv sync --frozen --no-dev --extra mcp

# Expose port (Railway will set PORT env var)
EXPOSE 8080

# Health check for Railway monitoring (Railway will use /health endpoint)

# Run HTTP server (Railway sets PORT env var automatically)
# exec makes the server PID 1, so the SIGTERM a deploy sends reaches uvicorn and
# in-flight tool calls finish. A shell or `uv run` in between can swallow it.
CMD ["sh", "-c", "exec /app/.venv/bin/late-mcp-http --host 0.0.0.0 --port ${PORT:-8080}"]