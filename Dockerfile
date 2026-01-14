# Late MCP HTTP Server - Railway Deployment
# Uses uv for fast, reliable dependency management

FROM ghcr.io/astral-sh/uv:python3.12-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies (no dev dependencies in production)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --extra mcp

# Expose port (Railway will set PORT env var)
EXPOSE 8080

# Health check for Railway monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/health', timeout=2.0)"

# Run HTTP server
CMD ["uv", "run", "late-mcp-http", "--host", "0.0.0.0", "--port", "8080"]
