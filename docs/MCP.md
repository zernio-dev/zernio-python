# MCP Server (Claude Desktop Integration)

Schedule posts directly from Claude Desktop using natural language with the Late MCP server.

## Quick Setup

### 1. Install uv (package manager)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Add to Claude Desktop config

Open the config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "late": {
      "command": "uvx",
      "args": ["--from", "getlate[mcp]", "late-mcp"],
      "env": {
        "LATE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> Get your API key at [zernio.com/dashboard/api-keys](https://zernio.com/dashboard/api-keys)

### 3. Restart Claude Desktop

Done! Ask Claude things like:
- *"Post 'Hello world!' to Twitter"*
- *"Schedule a LinkedIn post for tomorrow at 9am"*
- *"Show my connected accounts"*

## Alternative: Using pip

If you prefer pip over uvx:

```bash
pip install getlate[mcp]
```

```json
{
  "mcpServers": {
    "late": {
      "command": "python",
      "args": ["-m", "late.mcp"],
      "env": {
        "LATE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Uploading Media

Since Claude can't access local files, use the browser upload flow:

1. Ask Claude: *"I want to post an image to Instagram"*
2. Claude gives you an upload link -> open it in your browser
3. Upload your file and tell Claude *"done"*
4. Claude creates the post with your media

## Available Commands

| Command | Description |
|---------|-------------|
| `accounts_list` | Show connected social accounts |
| `posts_create` | Create scheduled, immediate, or draft post |
| `posts_publish_now` | Publish immediately |
| `posts_cross_post` | Post to multiple platforms |
| `posts_list` | Show your posts |
| `posts_retry` | Retry a failed post |
| `media_generate_upload_link` | Get link to upload media |

These core commands are always visible. The full Zernio API catalog (~400 tools) is reachable on demand through tool search: `search_tools` finds a capability by description and `call_tool` invokes it — and every underlying tool also stays directly callable by name.

## Remote Access (HTTP)

The remote MCP server speaks **Streamable HTTP** (`POST /mcp`) — the modern single-endpoint transport supported by all current MCP clients. It survives idle timeouts on proxies and bridges like `mcp-remote`. The legacy SSE transport (`GET /sse`) is kept for backward compatibility.

For deployment and client setup, see the [HTTP Deployment Guide](HTTP_DEPLOYMENT.md).
