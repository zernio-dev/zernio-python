# HTTP/SSE Deployment Guide

## Overview

The Late MCP server can be deployed via HTTP/SSE, allowing remote access from any MCP client. Each user provides their own Late API key when connecting.

## Quick Start

### Local Testing

1. Install dependencies:
```bash
uv sync --extra mcp
```

2. Run HTTP server:
```bash
uv run late-mcp-http
```

3. Test the server:
```bash
# Health check (no auth needed)
curl http://localhost:8080/health

# Server info (no auth needed)
curl http://localhost:8080/

# SSE endpoint (requires your Late API key)
curl -H "Authorization: Bearer your_late_api_key" http://localhost:8080/sse
```

## Railway Deployment

### Using Dockerfile

1. Push code to GitHub
2. Create new Railway project from repo
3. Railway auto-detects Dockerfile and deploys
4. No environment variables needed! (users provide their own API keys)

### Environment Variables

The server doesn't require any environment variables. Users authenticate by providing their Late API key when connecting.

Optional variables:
- `HOST` (default: 0.0.0.0)
- `PORT` (default: 8080, Railway sets this automatically)

## Connecting Clients

### Claude Code CLI

```bash
# Add the MCP server
claude mcp add --transport http late https://your-app.railway.app/sse

# When connecting, provide your Late API key via header
# The Claude CLI will prompt for authentication details
```

Configuration in MCP settings:
```json
{
  "late": {
    "url": "https://your-app.railway.app/sse",
    "headers": {
      "Authorization": "Bearer your_late_api_key_here"
    }
  }
}
```

### Python Client

```python
from mcp.client.sse import sse_client

# Provide your Late API key as Bearer token
headers = {
    "Authorization": "Bearer your_late_api_key_here"
}

async with sse_client(
    "https://your-app.railway.app/sse",
    headers=headers
) as (read, write):
    # Use MCP client
    pass
```

## Authentication

Each user must provide their own Late API key when connecting using the standard HTTP Authorization header:

```
Authorization: Bearer YOUR_LATE_API_KEY
```

Example:
```bash
curl -H "Authorization: Bearer sk_your_api_key_here" \
     https://your-app.railway.app/sse
```

The server validates the API key by making a test request to the Late API. If valid, the connection is established and the API key is used for all subsequent operations.

## Security

- Each user's API key is validated against the Late API
- API keys are stored per-connection using Python's contextvars
- No shared credentials or server-wide API keys
- Health check endpoint is public (no auth required)
- All other endpoints require authentication

## Get Your Late API Key

Visit https://getlate.dev to sign up and get your API key.
