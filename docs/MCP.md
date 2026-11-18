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

These core commands are always visible. The full Zernio API catalog (~400 tools) is reachable on demand through tool search: `search_tools` finds a capability by description and `call_tool` invokes it — and every underlying tool also stays directly callable by name. An unknown tool name returns the closest real tools instead of a bare error, and `call_tool` asked to run `search_tools` runs the search.

### Choosing which tools are listed

Integrations that run their own tool discovery can replace the default listing with `?tools=` on the server URL (Streamable HTTP):

| URL | `tools/list` returns |
|-----|----------------------|
| `https://mcp.zernio.com/mcp` | The core tools plus `search_tools` / `call_tool` |
| `https://mcp.zernio.com/mcp?tools=posts_create,ad_campaigns_get_ad_tree` | Exactly those tools, with their full definitions |
| `https://mcp.zernio.com/mcp?tools=all` | Every tool, paginated: follow `nextCursor` |

An unknown name in `?tools=` makes `tools/list` fail with the closest real names, so a renamed or removed tool shows up when the client loads its tools rather than mid-conversation. The selection only shapes the listing: every tool stays callable by name.

`feedback_submit_feedback` is always visible too: agents report bugs, missing features and documentation gaps with it. Reports filed through the MCP server are labelled `zernio-mcp` plus the client's user agent, so triage can tell them apart from direct API reports.

## Remote Access (HTTP)

The remote MCP server speaks **Streamable HTTP** (`POST /mcp`) — the modern single-endpoint transport supported by all current MCP clients. It survives idle timeouts on proxies and bridges like `mcp-remote`. The legacy SSE transport is retired: `GET /sse` answers 410 with the `/mcp` URL, and `/sse` serves Streamable HTTP for clients that saved the old URL.

For deployment and client setup, see the [HTTP Deployment Guide](HTTP_DEPLOYMENT.md).
