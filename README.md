<p align="center">
  <a href="https://getlate.dev">
    <img src="https://getlate.dev/images/icon_light.svg" alt="Late" width="60">
  </a>
</p>

<h1 align="center">Late Python SDK</h1>

<p align="center">
  <a href="https://pypi.org/project/late-sdk/"><img src="https://img.shields.io/pypi/v/late-sdk.svg" alt="PyPI version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  <strong>One API to post everywhere. 13 platforms, zero headaches.</strong>
</p>

The official Python SDK for the [Late API](https://getlate.dev) — schedule and publish social media posts across Instagram, TikTok, YouTube, LinkedIn, X/Twitter, Facebook, Pinterest, Threads, Bluesky, Reddit, Snapchat, Telegram, and Google Business Profile with a single integration.

## Installation

```bash
pip install late-sdk
```

## Quick Start

```python
from late import Late

late = Late(api_key="your-api-key")

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
    api_key="your-api-key",  # Required
    base_url="https://getlate.dev/api",  # Optional, this is the default
    timeout=30.0,  # Optional, request timeout in seconds
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
# Option 1: Direct upload (simplest)
result = late.media.upload("path/to/video.mp4")
media_url = result["publicUrl"]

# Option 2: Upload from bytes
result = late.media.upload_bytes(video_bytes, "video.mp4", "video/mp4")
media_url = result["publicUrl"]

# Create post with media
post = late.posts.create(
    content="Check out this video!",
    media_urls=[media_url],
    platforms=[
        {"platform": "tiktok", "accountId": "acc_xxx"},
        {"platform": "youtube", "accountId": "acc_yyy", "youtubeTitle": "My Video"},
    ],
    publish_now=True,
)
```

### Get Analytics

```python
data = late.analytics.get(period="30d")

print("Analytics:", data)
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
    async with Late(api_key="your-api-key") as late:
        posts = await late.posts.alist(status="scheduled")
        print(f"Found {len(posts['posts'])} scheduled posts")

asyncio.run(main())
```

## Error Handling

```python
from late import Late, LateAPIError, LateRateLimitError, LateValidationError

late = Late(api_key="your-api-key")

try:
    late.posts.create(content="Hello!", platforms=[...])
except LateRateLimitError as e:
    print(f"Rate limited: {e}")
except LateValidationError as e:
    print(f"Invalid request: {e}")
except LateAPIError as e:
    print(f"API error: {e}")
```

## SDK Reference

### Posts
| Method | Description |
|--------|-------------|
| `posts.list()` | List all posts |
| `posts.bulk_upload()` | Upload multiple posts at once |
| `posts.create()` | Create and schedule a post |
| `posts.get()` | Get a specific post |
| `posts.update()` | Update a scheduled post |
| `posts.delete()` | Delete a post |
| `posts.retry()` | Retry a failed post |

### Accounts
| Method | Description |
|--------|-------------|
| `accounts.list()` | List connected social accounts |
| `accounts.get()` | Get a specific account |
| `accounts.get_follower_stats()` | Get follower growth data |

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
| `analytics.get_usage()` | Get API usage statistics |

### Account Groups
| Method | Description |
|--------|-------------|
| `account_groups.list_account_groups()` | List account groups |
| `account_groups.create_account_group()` | Create an account group |
| `account_groups.update_account_group()` | Update an account group |
| `account_groups.delete_account_group()` | Delete an account group |

### Queue
| Method | Description |
|--------|-------------|
| `queue.get_slots()` | List queue time slots |
| `queue.update_slots()` | Update queue slots |
| `queue.delete_slots()` | Delete queue slots |
| `queue.next_slot()` | Get next available slot |
| `queue.preview()` | Preview upcoming queued posts |

### Webhooks
| Method | Description |
|--------|-------------|
| `webhooks.create_webhook_settings()` | Create webhook settings |
| `webhooks.get_webhook_logs()` | Get webhook delivery logs |
| `webhooks.get_webhook_settings()` | Get webhook configuration |
| `webhooks.update_webhook_settings()` | Update webhook settings |
| `webhooks.delete_webhook_settings()` | Delete webhook settings |
| `webhooks.test_webhook()` | Send a test webhook |

### API Keys
| Method | Description |
|--------|-------------|
| `api_keys.list_api_keys()` | List API keys |
| `api_keys.create_api_key()` | Create a new API key |
| `api_keys.delete_api_key()` | Delete an API key |

### Media
| Method | Description |
|--------|-------------|
| `media.check_upload_token()` | Check upload token status |
| `media.generate_upload_token()` | Generate upload token for browser uploads |
| `media.upload()` | Upload a file from path |
| `media.upload_bytes()` | Upload file from bytes |
| `media.upload_large()` | Upload large file with multipart |
| `media.upload_large_bytes()` | Upload large file from bytes |
| `media.upload_multiple()` | Upload multiple files |

### Tools
| Method | Description |
|--------|-------------|
| `tools.bluesky_download()` | Download Bluesky media |
| `tools.facebook_download()` | Download Facebook video |
| `tools.generate_caption()` | Generate caption using AI |
| `tools.instagram_download()` | Download Instagram media |
| `tools.instagram_hashtag_check()` | Check if hashtags are banned |
| `tools.linkedin_download()` | Download LinkedIn video |
| `tools.tiktok_download()` | Download TikTok video |
| `tools.twitter_download()` | Download Twitter/X media |
| `tools.youtube_download()` | Download YouTube video |
| `tools.youtube_transcript()` | Get YouTube video transcript |

### Users
| Method | Description |
|--------|-------------|
| `users.list()` | List team users |
| `users.get()` | Get a specific user |

### Usage
| Method | Description |
|--------|-------------|
| `usage.get_usage_stats()` | Get API usage statistics |

### Logs
| Method | Description |
|--------|-------------|
| `logs.list_logs()` | List publishing logs |
| `logs.get_log()` | Get a specific log entry |
| `logs.get_post_logs()` | Get logs for a specific post |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.list_facebook_pages()` | List Facebook pages |
| `connect.list_google_business_locations()` | List Google Business locations |
| `connect.list_linked_in_organizations()` | List LinkedIn organizations |
| `connect.list_pinterest_boards_for_selection()` | List Pinterest boards |
| `connect.list_snapchat_profiles()` | List Snapchat profiles |
| `connect.get_connect_url()` | Get OAuth URL for a platform |
| `connect.get_linked_in_organizations()` | Get LinkedIn organizations |
| `connect.get_pinterest_boards()` | Get Pinterest boards |
| `connect.get_reddit_subreddits()` | Get Reddit subreddits |
| `connect.get_telegram_connect_status()` | Get Telegram connection status |
| `connect.update_facebook_page()` | Update Facebook page settings |
| `connect.update_linked_in_organization()` | Update LinkedIn organization |
| `connect.update_pinterest_boards()` | Update Pinterest boards |
| `connect.update_reddit_subreddits()` | Update Reddit subreddits |
| `connect.complete_telegram_connect()` | Complete Telegram connection |
| `connect.connect_bluesky_credentials()` | Connect Bluesky with credentials |
| `connect.handle_o_auth_callback()` | Handle OAuth callback |
| `connect.initiate_telegram_connect()` | Start Telegram connection |
| `connect.select_facebook_page()` | Select a Facebook page |
| `connect.select_google_business_location()` | Select a Google Business location |
| `connect.select_linked_in_organization()` | Select a LinkedIn organization |
| `connect.select_pinterest_board()` | Select a Pinterest board |
| `connect.select_snapchat_profile()` | Select a Snapchat profile |

### Reddit
| Method | Description |
|--------|-------------|
| `reddit.get_reddit_feed()` | Get Reddit feed |
| `reddit.search_reddit()` | Search Reddit |

### Invites
| Method | Description |
|--------|-------------|
| `invites.list_platform_invites()` | List platform invites |
| `invites.create_invite_token()` | Create an invite token |
| `invites.create_platform_invite()` | Create a platform invite |
| `invites.delete_platform_invite()` | Delete a platform invite |

## MCP Server (Claude Desktop)

The SDK includes a Model Context Protocol (MCP) server for integration with Claude Desktop. See [MCP documentation](https://docs.getlate.dev/resources/mcp) for setup instructions.

```bash
pip install late-sdk[mcp]
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
