# HTTP Deployment Guide

## Overview

The Zernio MCP server can be deployed over HTTP, allowing remote access from any MCP client. Each user provides their own Zernio API key when connecting.

The server's primary transport is **Streamable HTTP** (`POST /mcp`), the modern MCP transport supported by all current clients. Each request/response is self-contained (with optional chunked streaming), so it survives proxies and bridges that drop idle connections. The legacy SSE transport (`GET /sse` + `POST /messages/`) is kept for backward compatibility.

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

# Server info (no auth needed)
curl http://localhost:8080/

# Streamable HTTP endpoint (requires your Zernio API key)
curl -H "Authorization: Bearer your_zernio_api_key" \
     -H "Accept: application/json, text/event-stream" \
     -X POST http://localhost:8080/mcp \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
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
- `MCP_PUBLIC_URL` (default: https://mcp.zernio.com) — the server's canonical public URL, used as the OAuth resource identifier in the discovery metadata. Set it for non-prod deployments (e.g. a Railway preview URL).
- `MCP_ALLOWED_ORIGINS` — comma-separated hostnames appended to the browser Origin allowlist (DNS-rebinding protection).

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

The server is an OAuth 2.0 **resource server** (FastMCP's resource-server model): both plain Zernio API keys and OAuth access tokens issued by zernio.com are accepted as the bearer. Clients without a token (e.g. Claude's connector) receive a `401` whose `WWW-Authenticate` challenge points at the RFC 9728 discovery document at `/.well-known/oauth-protected-resource/mcp`, from which they discover the zernio.com authorization server and run the OAuth flow. The pre-FastMCP discovery path (`/.well-known/oauth-protected-resource`) permanently redirects to the canonical document, so clients holding the old URL keep working.

## Security

- Each user's bearer (API key or OAuth token) is validated against the Zernio API on every request
- The validated bearer is scoped to its request via FastMCP's access-token context (Streamable HTTP runs in stateless mode, so credentials never leak across requests)
- No shared credentials or server-wide API keys
- Browser requests are checked against an Origin allowlist for DNS-rebinding protection (extend with `MCP_ALLOWED_ORIGINS`)
- Health check, server info, and OAuth discovery endpoints are public (no auth required)
- The MCP and legacy SSE endpoints require authentication

## Get Your Zernio API Key

Visit https://zernio.com to sign up and get your API key.
