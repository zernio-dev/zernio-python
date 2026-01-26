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
| `posts.list_posts()` | List posts visible to the authenticated user |
| `posts.bulk_upload_posts()` | Validate and schedule multiple posts from CSV |
| `posts.create_post()` | Create a draft, scheduled, or immediate post |
| `posts.get_post()` | Get a single post |
| `posts.update_post()` | Update a post |
| `posts.delete_post()` | Delete a post |
| `posts.retry_post()` | Retry publishing a failed or partial post |

### Accounts
| Method | Description |
|--------|-------------|
| `accounts.get_all_accounts_health()` | Check health of all connected accounts |
| `accounts.list_accounts()` | List connected social accounts |
| `accounts.get_account_health()` | Check health of a specific account |
| `accounts.get_follower_stats()` | Get follower stats and growth metrics |
| `accounts.get_google_business_reviews()` | Get Google Business Profile reviews |
| `accounts.get_linked_in_mentions()` | Resolve a LinkedIn profile or company URL to a URN for @mentions |
| `accounts.update_account()` | Update a social account |
| `accounts.delete_account()` | Disconnect a social account |

### Profiles
| Method | Description |
|--------|-------------|
| `profiles.list_profiles()` | List profiles visible to the authenticated user |
| `profiles.create_profile()` | Create a new profile |
| `profiles.get_profile()` | Get a profile by id |
| `profiles.update_profile()` | Update a profile |
| `profiles.delete_profile()` | Delete a profile (must have no connected accounts) |

### Analytics
| Method | Description |
|--------|-------------|
| `analytics.get_analytics()` | Unified analytics for posts |
| `analytics.get_linked_in_aggregate_analytics()` | Get aggregate analytics for a LinkedIn personal account |
| `analytics.get_linked_in_post_analytics()` | Get analytics for a specific LinkedIn post by URN |
| `analytics.get_you_tube_daily_views()` | YouTube daily views breakdown |

### Account Groups
| Method | Description |
|--------|-------------|
| `account_groups.list_account_groups()` | List account groups for the authenticated user |
| `account_groups.create_account_group()` | Create a new account group |
| `account_groups.update_account_group()` | Update an account group |
| `account_groups.delete_account_group()` | Delete an account group |

### Queue
| Method | Description |
|--------|-------------|
| `queue.list_queue_slots()` | Get queue schedules for a profile |
| `queue.create_queue_slot()` | Create a new queue for a profile |
| `queue.get_next_queue_slot()` | Preview the next available queue slot (informational only) |
| `queue.update_queue_slot()` | Create or update a queue schedule |
| `queue.delete_queue_slot()` | Delete a queue schedule |
| `queue.preview_queue()` | Preview upcoming queue slots for a profile |

### Webhooks
| Method | Description |
|--------|-------------|
| `webhooks.create_webhook_settings()` | Create a new webhook |
| `webhooks.get_webhook_logs()` | Get webhook delivery logs |
| `webhooks.get_webhook_settings()` | List all webhooks |
| `webhooks.update_webhook_settings()` | Update a webhook |
| `webhooks.delete_webhook_settings()` | Delete a webhook |
| `webhooks.test_webhook()` | Send test webhook |

### API Keys
| Method | Description |
|--------|-------------|
| `api_keys.list_api_keys()` | List API keys for the current user |
| `api_keys.create_api_key()` | Create a new API key |
| `api_keys.delete_api_key()` | Delete an API key |

### Media
| Method | Description |
|--------|-------------|
| `media.get_media_presigned_url()` | Get a presigned URL for direct file upload (up to 5GB) |
| `media.upload()` | Upload a file from path |
| `media.upload_bytes()` | Upload file from bytes |
| `media.upload_large()` | Upload large file with multipart |
| `media.upload_large_bytes()` | Upload large file from bytes |
| `media.upload_multiple()` | Upload multiple files |

### Tools
| Method | Description |
|--------|-------------|
| `tools.get_you_tube_transcript()` | Get YouTube video transcript |
| `tools.check_instagram_hashtags()` | Check Instagram hashtags for bans |
| `tools.download_bluesky_media()` | Download Bluesky video |
| `tools.download_facebook_video()` | Download Facebook video |
| `tools.download_instagram_media()` | Download Instagram reel or post |
| `tools.download_linked_in_video()` | Download LinkedIn video |
| `tools.download_tik_tok_video()` | Download TikTok video |
| `tools.download_twitter_media()` | Download Twitter/X video |
| `tools.download_you_tube_video()` | Download YouTube video or audio |

### Users
| Method | Description |
|--------|-------------|
| `users.list_users()` | List team users (root + invited) |
| `users.get_user()` | Get user by id (self or invited) |

### Usage
| Method | Description |
|--------|-------------|
| `usage.get_usage_stats()` | Get plan and usage stats for current account |

### Logs
| Method | Description |
|--------|-------------|
| `logs.list_logs()` | Get publishing logs |
| `logs.get_log()` | Get a single log entry |
| `logs.get_post_logs()` | Get logs for a specific post |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.list_facebook_pages()` | List Facebook Pages after OAuth (Headless Mode) |
| `connect.list_google_business_locations()` | List Google Business Locations after OAuth (Headless Mode) |
| `connect.list_linked_in_organizations()` | Fetch full LinkedIn organization details (Headless Mode) |
| `connect.list_pinterest_boards_for_selection()` | List Pinterest Boards after OAuth (Headless Mode) |
| `connect.list_snapchat_profiles()` | List Snapchat Public Profiles after OAuth (Headless Mode) |
| `connect.get_connect_url()` | Start OAuth connection for a platform |
| `connect.get_facebook_pages()` | List available Facebook pages for a connected account |
| `connect.get_gmb_locations()` | List available Google Business Profile locations for a connected account |
| `connect.get_linked_in_organizations()` | Get available LinkedIn organizations for a connected account |
| `connect.get_pending_o_auth_data()` | Fetch pending OAuth selection data (Headless Mode) |
| `connect.get_pinterest_boards()` | List Pinterest boards for a connected account |
| `connect.get_reddit_subreddits()` | List Reddit subreddits for a connected account |
| `connect.get_telegram_connect_status()` | Generate Telegram access code |
| `connect.update_facebook_page()` | Update selected Facebook page for a connected account |
| `connect.update_gmb_location()` | Update selected Google Business Profile location for a connected account |
| `connect.update_linked_in_organization()` | Switch LinkedIn account type (personal/organization) |
| `connect.update_pinterest_boards()` | Set default Pinterest board on the connection |
| `connect.update_reddit_subreddits()` | Set default subreddit on the connection |
| `connect.complete_telegram_connect()` | Check Telegram connection status |
| `connect.connect_bluesky_credentials()` | Connect Bluesky using app password |
| `connect.handle_o_auth_callback()` | Complete OAuth token exchange manually (for server-side flows) |
| `connect.initiate_telegram_connect()` | Direct Telegram connection (power users) |
| `connect.select_facebook_page()` | Select a Facebook Page to complete the connection (Headless Mode) |
| `connect.select_google_business_location()` | Select a Google Business location to complete the connection (Headless Mode) |
| `connect.select_linked_in_organization()` | Select LinkedIn organization or personal account after OAuth |
| `connect.select_pinterest_board()` | Select a Pinterest Board to complete the connection (Headless Mode) |
| `connect.select_snapchat_profile()` | Select a Snapchat Public Profile to complete the connection (Headless Mode) |

### Reddit
| Method | Description |
|--------|-------------|
| `reddit.get_reddit_feed()` | Fetch subreddit feed via a connected account |
| `reddit.search_reddit()` | Search Reddit posts via a connected account |

### Invites
| Method | Description |
|--------|-------------|
| `invites.create_invite_token()` | Create a team member invite token |

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
