<p align="center">
  <img src="https://getlate.dev/images/icon_light.svg" alt="Late" width="80" />
</p>

<h1 align="center">Late Python SDK</h1>

<p align="center">
  Python SDK for <a href="https://getlate.dev">Late API</a> - Schedule social media posts across multiple platforms.
</p>

## Installation

```bash
pip install late-sdk
```

## Quick Start

```python
from datetime import datetime, timedelta
from late import Late, Platform

client = Late(api_key="your_api_key")

# List connected accounts
accounts = client.accounts.list()

# Create a scheduled post
post = client.posts.create(
    content="Hello from Late!",
    platforms=[{"platform": Platform.TWITTER, "accountId": "your_account_id"}],
    scheduled_for=datetime.now() + timedelta(hours=1),
)
```

---

## 🤖 Claude Desktop Integration (MCP)

Schedule posts directly from Claude Desktop using natural language.

### Setup in 3 Steps

**1. Install uv** (package manager)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Add to Claude Desktop config**

Open the config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this:

```json
{
  "mcpServers": {
    "late": {
      "command": "uvx",
      "args": ["--from", "late-sdk[mcp]", "late-mcp"],
      "env": {
        "LATE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> Get your API key at [getlate.dev/dashboard/api-keys](https://getlate.dev/dashboard/api-keys)

**3. Restart Claude Desktop**

Done! Ask Claude things like:
- *"Post 'Hello world!' to Twitter"*
- *"Schedule a LinkedIn post for tomorrow at 9am"*
- *"Show my connected accounts"*

<details>
<summary><b>Alternative: Using pip instead of uvx</b></summary>

```bash
pip install late-sdk[mcp]
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

</details>

### Uploading Images/Videos

Since Claude can't access local files, use the browser upload flow:

1. Ask Claude: *"I want to post an image to Instagram"*
2. Claude gives you an upload link → open it in your browser
3. Upload your file and tell Claude *"done"*
4. Claude creates the post with your media

### Available Commands

| Command | What it does |
|---------|--------------|
| `accounts_list` | Show connected social accounts |
| `posts_create` | Create scheduled, immediate, or draft post |
| `posts_publish_now` | Publish immediately |
| `posts_cross_post` | Post to multiple platforms |
| `posts_list` | Show your posts |
| `posts_retry` | Retry a failed post |
| `media_generate_upload_link` | Get link to upload media |

---

## 🌐 Remote Access (HTTP/SSE)

Deploy the MCP server to access it remotely from Claude Code CLI or custom clients.

### Quick Deploy to Railway

1. **Push to GitHub** and connect to Railway
2. **Set environment variables:**
   - `LATE_API_KEY` - Your Late API key
   - `MCP_SERVER_API_KEY` - Secure random key (generate with command below)

3. **Generate secure key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

4. **Railway auto-deploys** using the Dockerfile

### Connect from Claude Code CLI

```bash
# Add your deployed server
claude mcp add --transport http late https://your-app.railway.app/sse

# Authenticate
/mcp
```

### Local HTTP Server

```bash
# Set environment variables
export LATE_API_KEY=your_api_key
export MCP_SERVER_API_KEY=your_secure_key

# Install with HTTP support
uv sync --extra mcp

# Run HTTP server
uv run late-mcp-http
```

Server runs on `http://0.0.0.0:8080` with endpoints:
- `/health` - Health check (public)
- `/sse` - SSE connection (requires API key)
- `/messages/` - Message handler (requires API key)

📖 [Full HTTP deployment guide →](docs/HTTP_DEPLOYMENT.md)

---

## SDK Features

### Async Support

```python
import asyncio
from late import Late

async def main():
    async with Late(api_key="...") as client:
        posts = await client.posts.alist(status="scheduled")

asyncio.run(main())
```

### AI Content Generation (Experimental)

```bash
pip install late-sdk[ai]
```

```python
from late import Platform, CaptionTone
from late.ai import ContentGenerator, GenerateRequest

generator = ContentGenerator(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o-mini",  # or gpt-4o, gpt-4-turbo, etc.
)

response = generator.generate(
    GenerateRequest(
        prompt="Write a tweet about Python",
        platform=Platform.TWITTER,
        tone=CaptionTone.CASUAL,
    )
)

print(response.text)
```

### CSV Scheduling

```python
from late import Late
from late.pipelines import CSVSchedulerPipeline

client = Late(api_key="...")
pipeline = CSVSchedulerPipeline(client)

# Validate first
results = pipeline.schedule("posts.csv", dry_run=True)

# Then schedule
results = pipeline.schedule("posts.csv")
```

### Cross-Posting

```python
from late import Platform
from late.pipelines import CrossPosterPipeline, PlatformConfig

cross_poster = CrossPosterPipeline(client)

results = await cross_poster.post(
    content="Big announcement!",
    platforms=[
        PlatformConfig(Platform.TWITTER, "tw_123"),
        PlatformConfig(Platform.LINKEDIN, "li_456", delay_minutes=5),
    ],
)
```

---

## API Reference

### Resources

| Resource | Methods |
|----------|---------|
| `client.posts` | `list`, `get`, `create`, `update`, `delete`, `retry` |
| `client.profiles` | `list`, `get`, `create`, `update`, `delete` |
| `client.accounts` | `list`, `get` |
| `client.media` | `upload`, `upload_multiple` |
| `client.analytics` | `get`, `get_usage` |
| `client.tools` | `youtube_download`, `instagram_download`, `tiktok_download`, `generate_caption` |
| `client.queue` | `get_slots`, `preview`, `next_slot` |

### Client Options

```python
client = Late(
    api_key="...",
    timeout=30.0,      # seconds
    max_retries=3,
)
```

---

## Links

- [Late Website](https://getlate.dev)
- [API Documentation](https://docs.getlate.dev)
- [Get API Key](https://getlate.dev/dashboard/api-keys)

## License

MIT
