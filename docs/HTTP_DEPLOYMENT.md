# HTTP Deployment Guide

## Overview

The Zernio MCP server can be deployed over HTTP, allowing remote access from any MCP client. Each user provides their own Zernio API key when connecting.

The server exposes **two transports simultaneously**:

| Transport | Endpoint | When to use |
| --- | --- | --- |
| **Streamable HTTP** (recommended) | `POST /mcp` | Modern MCP transport. Survives proxies/bridges that drop idle connections. Use this for Claude Code, `mcp-remote`, and any new client. |
| **SSE** (legacy) | `GET /sse` + `POST /messages/` | Older two-endpoint transport. Kept for backwards compatibility. The long-idle `GET /sse` connection can be killed by load balancers or bridges after a few minutes idle. |

Pick Streamable HTTP unless you have a specific client that only speaks SSE.

## Quick Start

### Local Testing

1. Install dependencies:
```bash
uv sync --extra mcp
```

2. Run HTTP server:
```bash
uv run zernio-mcp-http
```

3. Test the server:
```bash
# Health check (no auth needed)
curl http://localhost:8080/health

# Server info (lists both transports, no auth needed)
curl http://localhost:8080/

# Streamable HTTP endpoint (requires your Zernio API key)
curl -H "Authorization: Bearer your_zernio_api_key" \
     -H "Accept: application/json, text/event-stream" \
     -X POST http://localhost:8080/mcp \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'

# SSE endpoint (legacy)
curl -H "Authorization: Bearer your_zernio_api_key" http://localhost:8080/sse
```

## Railway Deployment

### Using Dockerfile

1. Push code to GitHub
2. Create new Railway project from repo
3. Railway auto-detects Dockerfile and deploys
4. No environment variables needed! (users provide their own API keys)

### Environment Variables

The server doesn't require any environment variables. Users authenticate by providing their Zernio API key when connecting.

Optional variables:
- `HOST` (default: 0.0.0.0)
- `PORT` (default: 8080, Railway sets this automatically)

## Connecting Clients

### Claude Code CLI (recommended: Streamable HTTP)

```bash
# Add the MCP server using the modern Streamable HTTP transport
claude mcp add --transport http zernio https://your-app.railway.app/mcp \
  --header "Authorization: Bearer your_zernio_api_key_here"
```

Configuration in MCP settings:
```json
{
  "zernio": {
    "url": "https://your-app.railway.app/mcp",
    "headers": {
      "Authorization": "Bearer your_zernio_api_key_here"
    }
  }
}
```

### Claude Code CLI (legacy: SSE)

If you need SSE for an older client, the endpoint is `/sse` instead of `/mcp`:

```bash
claude mcp add --transport sse zernio https://your-app.railway.app/sse \
  --header "Authorization: Bearer your_zernio_api_key_here"
```

Note: SSE connections can be dropped by proxies after a few minutes idle. Prefer Streamable HTTP if your client supports it.

### Python Client (Streamable HTTP)

```python
from mcp.client.streamable_http import streamablehttp_client

headers = {
    "Authorization": "Bearer your_zernio_api_key_here"
}

async with streamablehttp_client(
    "https://your-app.railway.app/mcp",
    headers=headers,
) as (read, write, _):
    # Use MCP client
    pass
```

### Python Client (SSE, legacy)

```python
from mcp.client.sse import sse_client

headers = {
    "Authorization": "Bearer your_zernio_api_key_here"
}

async with sse_client(
    "https://your-app.railway.app/sse",
    headers=headers
) as (read, write):
    # Use MCP client
    pass
```

## Authentication

Each user must provide their own Zernio API key when connecting using the standard HTTP Authorization header:

```
Authorization: Bearer YOUR_ZERNIO_API_KEY
```

Example (Streamable HTTP):
```bash
curl -H "Authorization: Bearer sk_your_api_key_here" \
     -H "Accept: application/json, text/event-stream" \
     -X POST https://your-app.railway.app/mcp \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

The server validates the API key by making a test request to the Zernio API. If valid, the request is processed and the API key is used for all operations within that request.

## Security

- Each user's API key is validated against the Zernio API
- API keys are stored per-request using Python's `contextvars` (Streamable HTTP runs in stateless mode, so keys never leak across requests)
- No shared credentials or server-wide API keys
- Health check endpoint is public (no auth required)
- All other endpoints require authentication

## Get Your Zernio API Key

Visit https://zernio.com to sign up and get your API key.
