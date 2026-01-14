# HTTP/SSE Deployment Guide

## Quick Start

### Local Testing

1. Install dependencies:
```bash
uv sync --extra mcp
```

2. Set environment variables:
```bash
export LATE_API_KEY=your_late_api_key
export MCP_SERVER_API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

3. Run HTTP server:
```bash
uv run late-mcp-http
```

4. Test the server:
```bash
# Health check (no auth needed)
curl http://localhost:8080/health

# Server info
curl http://localhost:8080/

# SSE endpoint (with auth)
curl -H "X-API-Key: your_key" http://localhost:8080/sse
```

## Railway Deployment

### Option 1: Using Dockerfile (Recommended)

1. Push to GitHub
2. Create new Railway project from repo
3. Set environment variables in Railway:
   - `LATE_API_KEY`
   - `MCP_SERVER_API_KEY`
4. Railway auto-detects Dockerfile and deploys

### Option 2: Using Railpack (Auto)

Railway will automatically:
- Detect `pyproject.toml` and `uv.lock`
- Install dependencies with `uv`
- Run `late-mcp-http` command

## Connecting Clients

### Claude Code CLI
```bash
claude mcp add --transport http late https://your-app.railway.app/sse
```

### Python Client
```python
from mcp.client.sse import sse_client

async with sse_client("https://your-app.railway.app/sse") as (read, write):
    # Use MCP client
    pass
```

## Authentication

Add API key via:
- Header: `Authorization: Bearer your_key`
- Header: `X-API-Key: your_key`
- Query: `?api_key=your_key`
