<p align="center">
  <a href="https://getlate.dev">
    <img src="https://getlate.dev/images/icon_light.svg" alt="Late" width="60">
  </a>
</p>

<h1 align="center">Late Python SDK</h1>

<p align="center">
  <a href="https://pypi.org/project/getlate/"><img src="https://img.shields.io/pypi/v/getlate.svg" alt="PyPI version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  <strong>One API to post everywhere. 13 platforms, zero headaches.</strong>
</p>

The official Python SDK for the [Late API](https://getlate.dev) — schedule and publish social media posts across Instagram, TikTok, YouTube, LinkedIn, X/Twitter, Facebook, Pinterest, Threads, Bluesky, Reddit, Snapchat, Telegram, and Google Business Profile with a single integration.

## Installation

```bash
pip install getlate
```

## Quick Start

```python
from late import Late

late = Late()  # Uses LATE_API_KEY env var

# Publish to multiple platforms with one call
post = late.posts.create(
    content="Hello world from Late!",
    platforms=[
        {"platform": "twitter", "accountId": "acc_xxx"},
        {"platform": "linkedin", "accountId": "acc_yyy"},
        {"platform": "instagram", "accountId": "acc_zzz"},
    ],
    publish_now=True,
)

print(f"Published to {len(post['post']['platforms'])} platforms!")
```

## Configuration

```python
late = Late(
    api_key="your-api-key",  # Defaults to os.environ["LATE_API_KEY"]
    base_url="https://getlate.dev/api",
    timeout=60.0,
)
```

## Examples

### Schedule a Post

```python
post = late.posts.create(
    content="This post will go live tomorrow at 10am",
    platforms=[{"platform": "instagram", "accountId": "acc_xxx"}],
    scheduled_for="2025-02-01T10:00:00Z",
)
```

### Platform-Specific Content

Customize content per platform while posting to all at once:

```python
post = late.posts.create(
    content="Default content",
    platforms=[
        {
            "platform": "twitter",
            "accountId": "acc_twitter",
            "platformSpecificContent": "Short & punchy for X",
        },
        {
            "platform": "linkedin",
            "accountId": "acc_linkedin",
            "platformSpecificContent": "Professional tone for LinkedIn with more detail.",
        },
    ],
    publish_now=True,
)
```

### Upload Media

```python
# 1. Get presigned upload URL
presign = late.media.get_presigned_url(
    filename="video.mp4",
    content_type="video/mp4",
)

# 2. Upload your file
import httpx
httpx.put(presign["uploadUrl"], content=video_bytes, headers={"Content-Type": "video/mp4"})

# 3. Create post with media
post = late.posts.create(
    content="Check out this video!",
    media_urls=[presign["publicUrl"]],
    platforms=[
        {"platform": "tiktok", "accountId": "acc_xxx"},
        {"platform": "youtube", "accountId": "acc_yyy", "youtubeTitle": "My Video"},
    ],
    publish_now=True,
)
```

### Get Analytics

```python
data = late.analytics.get(post_id="post_xxx")

print("Views:", data["analytics"]["views"])
print("Likes:", data["analytics"]["likes"])
print("Engagement Rate:", data["analytics"]["engagementRate"])
```

### List Connected Accounts

```python
data = late.accounts.list()

for account in data["accounts"]:
    print(f"{account['platform']}: @{account['username']}")
```

### Async Support

```python
import asyncio
from late import Late

async def main():
    async with Late() as late:
        posts = await late.posts.alist(status="scheduled")
        print(f"Found {len(posts['posts'])} scheduled posts")

asyncio.run(main())
```

## Error Handling

```python
from late import Late
from late.exceptions import LateApiError, RateLimitError, ValidationError

try:
    late.posts.create(content="Hello!", platforms=[...])
except RateLimitError as e:
    print(f"Rate limited. Retry in {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid request: {e.errors}")
except LateApiError as e:
    print(f"Error {e.status_code}: {e.message}")
```

## SDK Reference

### Posts
| Method | Description |
|--------|-------------|
| `posts.list()` | List all posts |
| `posts.create()` | Create and schedule a post |
| `posts.get()` | Get a specific post |
| `posts.update()` | Update a scheduled post |
| `posts.delete()` | Delete a post |
| `posts.retry()` | Retry a failed post |
| `posts.bulk_upload()` | Upload multiple posts at once |

### Accounts
| Method | Description |
|--------|-------------|
| `accounts.list()` | List connected social accounts |
| `accounts.get()` | Get a specific account |
| `accounts.get_follower_stats()` | Get follower growth data |
| `accounts.get_health()` | Check health of an account |

### Profiles
| Method | Description |
|--------|-------------|
| `profiles.list()` | List workspace profiles |
| `profiles.create()` | Create a new profile |
| `profiles.get()` | Get a specific profile |
| `profiles.update()` | Update a profile |
| `profiles.delete()` | Delete a profile |

### Analytics
| Method | Description |
|--------|-------------|
| `analytics.get()` | Get post performance metrics |
| `analytics.get_youtube_daily_views()` | Get YouTube daily view breakdown |

### Account Groups
| Method | Description |
|--------|-------------|
| `account_groups.list()` | List account groups |
| `account_groups.create()` | Create an account group |
| `account_groups.update()` | Update an account group |
| `account_groups.delete()` | Delete an account group |

### Queue
| Method | Description |
|--------|-------------|
| `queue.list_slots()` | List queue time slots |
| `queue.create_slot()` | Create a queue slot |
| `queue.update_slot()` | Update a queue slot |
| `queue.delete_slot()` | Delete a queue slot |
| `queue.preview()` | Preview upcoming queued posts |
| `queue.get_next_slot()` | Get next available slot |

### Webhooks
| Method | Description |
|--------|-------------|
| `webhooks.get_settings()` | Get webhook configuration |
| `webhooks.create_settings()` | Create webhook settings |
| `webhooks.update_settings()` | Update webhook settings |
| `webhooks.delete_settings()` | Delete webhook settings |
| `webhooks.test()` | Send a test webhook |
| `webhooks.get_logs()` | Get webhook delivery logs |

### API Keys
| Method | Description |
|--------|-------------|
| `api_keys.list()` | List API keys |
| `api_keys.create()` | Create a new API key |
| `api_keys.delete()` | Delete an API key |

### Media
| Method | Description |
|--------|-------------|
| `media.get_presigned_url()` | Get presigned URL for file upload |

### Tools
| Method | Description |
|--------|-------------|
| `tools.download_youtube()` | Download YouTube video |
| `tools.get_youtube_transcript()` | Get YouTube video transcript |
| `tools.download_instagram()` | Download Instagram media |
| `tools.check_instagram_hashtags()` | Check if hashtags are banned |
| `tools.download_tiktok()` | Download TikTok video |
| `tools.download_twitter()` | Download Twitter/X media |
| `tools.download_facebook()` | Download Facebook video |
| `tools.download_linkedin()` | Download LinkedIn video |
| `tools.download_bluesky()` | Download Bluesky media |

### Users
| Method | Description |
|--------|-------------|
| `users.list()` | List team users |
| `users.get()` | Get a specific user |

### Usage
| Method | Description |
|--------|-------------|
| `usage.get_stats()` | Get API usage statistics |

### Logs
| Method | Description |
|--------|-------------|
| `logs.list()` | List publishing logs |
| `logs.get()` | Get a specific log entry |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.get_url()` | Get OAuth URL for a platform |
| `connect.handle_callback()` | Handle OAuth callback |

### Reddit
| Method | Description |
|--------|-------------|
| `reddit.search()` | Search Reddit |
| `reddit.get_feed()` | Get Reddit feed |

### Invites
| Method | Description |
|--------|-------------|
| `invites.create_token()` | Create an invite token |
| `invites.list()` | List platform invites |
| `invites.create()` | Create a platform invite |
| `invites.delete()` | Delete a platform invite |

## MCP Server (Claude Desktop)

The SDK includes a Model Context Protocol (MCP) server for integration with Claude Desktop. See [MCP documentation](docs/MCP.md) for setup instructions.

```bash
pip install getlate[mcp]
```

## Requirements

- Python 3.10+
- [Late API key](https://getlate.dev) (free tier available)

## Links

- [Documentation](https://docs.getlate.dev)
- [Dashboard](https://getlate.dev/dashboard)
- [Changelog](https://docs.getlate.dev/changelog)

## License

Apache-2.0
