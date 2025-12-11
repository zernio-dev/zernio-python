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
from late import Late

client = Late(api_key="your_api_key")

# List connected accounts
accounts = client.accounts.list()

# Create a scheduled post
from datetime import datetime, timedelta

post = client.posts.create(
    content="Hello from Late!",
    platforms=[{"platform": "twitter", "accountId": "your_account_id"}],
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
| `list_accounts` | Show connected social accounts |
| `create_post` | Create scheduled or immediate post |
| `publish_now` | Publish immediately |
| `cross_post` | Post to multiple platforms |
| `list_posts` | Show your posts |
| `retry_post` | Retry a failed post |
| `generate_upload_link` | Get link to upload media |

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

### AI Content Generation

```bash
pip install late-sdk[ai]
```

```python
from late.ai import ContentGenerator, GenerateRequest

generator = ContentGenerator(provider="openai", api_key="sk-...")

response = generator.generate(
    GenerateRequest(
        prompt="Write a tweet about Python",
        platform="twitter",
        tone="casual",
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
from late.pipelines import CrossPosterPipeline, PlatformConfig

cross_poster = CrossPosterPipeline(client)

results = await cross_poster.post(
    content="Big announcement!",
    platforms=[
        PlatformConfig("twitter", "tw_123"),
        PlatformConfig("linkedin", "li_456", delay_minutes=5),
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
