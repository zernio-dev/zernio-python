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
| `posts.list_posts()` | List posts |
| `posts.bulk_upload_posts()` | Bulk upload from CSV |
| `posts.create_post()` | Create post |
| `posts.get_post()` | Get post |
| `posts.update_post()` | Update post |
| `posts.delete_post()` | Delete post |
| `posts.retry_post()` | Retry failed post |
| `posts.unpublish_post()` | Unpublish post |

### Accounts
| Method | Description |
|--------|-------------|
| `accounts.get_all_accounts_health()` | Check accounts health |
| `accounts.list_accounts()` | List accounts |
| `accounts.get_account_health()` | Check account health |
| `accounts.get_follower_stats()` | Get follower stats |
| `accounts.get_google_business_reviews()` | Get reviews |
| `accounts.get_linked_in_mentions()` | Resolve LinkedIn mention |
| `accounts.update_account()` | Update account |
| `accounts.delete_account()` | Disconnect account |

### Profiles
| Method | Description |
|--------|-------------|
| `profiles.list_profiles()` | List profiles |
| `profiles.create_profile()` | Create profile |
| `profiles.get_profile()` | Get profile |
| `profiles.update_profile()` | Update profile |
| `profiles.delete_profile()` | Delete profile |

### Analytics
| Method | Description |
|--------|-------------|
| `analytics.get_analytics()` | Get post analytics |
| `analytics.get_best_time_to_post()` | Get best times to post |
| `analytics.get_content_decay()` | Get content performance decay |
| `analytics.get_daily_metrics()` | Get daily aggregated metrics |
| `analytics.get_linked_in_aggregate_analytics()` | Get LinkedIn aggregate stats |
| `analytics.get_linked_in_post_analytics()` | Get LinkedIn post stats |
| `analytics.get_linked_in_post_reactions()` | Get LinkedIn post reactions |
| `analytics.get_post_timeline()` | Get post analytics timeline |
| `analytics.get_posting_frequency()` | Get posting frequency vs engagement |
| `analytics.get_you_tube_daily_views()` | Get YouTube daily views |

### Account Groups
| Method | Description |
|--------|-------------|
| `account_groups.list_account_groups()` | List groups |
| `account_groups.create_account_group()` | Create group |
| `account_groups.update_account_group()` | Update group |
| `account_groups.delete_account_group()` | Delete group |

### Queue
| Method | Description |
|--------|-------------|
| `queue.list_queue_slots()` | List schedules |
| `queue.create_queue_slot()` | Create schedule |
| `queue.get_next_queue_slot()` | Get next available slot |
| `queue.update_queue_slot()` | Update schedule |
| `queue.delete_queue_slot()` | Delete schedule |
| `queue.preview_queue()` | Preview upcoming slots |

### Webhooks
| Method | Description |
|--------|-------------|
| `webhooks.create_webhook_settings()` | Create webhook |
| `webhooks.get_webhook_logs()` | Get delivery logs |
| `webhooks.get_webhook_settings()` | List webhooks |
| `webhooks.update_webhook_settings()` | Update webhook |
| `webhooks.delete_webhook_settings()` | Delete webhook |
| `webhooks.test_webhook()` | Send test webhook |

### API Keys
| Method | Description |
|--------|-------------|
| `api_keys.list_api_keys()` | List keys |
| `api_keys.create_api_key()` | Create key |
| `api_keys.delete_api_key()` | Delete key |

### Media
| Method | Description |
|--------|-------------|
| `media.get_media_presigned_url()` | Get presigned upload URL |
| `media.upload()` | Upload a file from path |
| `media.upload_bytes()` | Upload file from bytes |
| `media.upload_large()` | Upload large file with multipart |
| `media.upload_large_bytes()` | Upload large file from bytes |
| `media.upload_multiple()` | Upload multiple files |

### Tools
| Method | Description |
|--------|-------------|
| `tools.get_you_tube_transcript()` | Get YouTube transcript |
| `tools.check_instagram_hashtags()` | Check IG hashtag bans |
| `tools.download_bluesky_media()` | Download Bluesky media |
| `tools.download_facebook_video()` | Download Facebook video |
| `tools.download_instagram_media()` | Download Instagram media |
| `tools.download_linked_in_video()` | Download LinkedIn video |
| `tools.download_tik_tok_video()` | Download TikTok video |
| `tools.download_twitter_media()` | Download Twitter/X media |
| `tools.download_you_tube_video()` | Download YouTube video |

### Users
| Method | Description |
|--------|-------------|
| `users.list_users()` | List users |
| `users.get_user()` | Get user |

### Usage
| Method | Description |
|--------|-------------|
| `usage.get_usage_stats()` | Get plan and usage stats |

### Logs
| Method | Description |
|--------|-------------|
| `logs.list_connection_logs()` | List connection logs |
| `logs.list_posts_logs()` | List publishing logs |
| `logs.get_post_logs()` | Get post logs |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.list_facebook_pages()` | List Facebook pages |
| `connect.list_google_business_locations()` | List GBP locations |
| `connect.list_linked_in_organizations()` | List LinkedIn orgs |
| `connect.list_pinterest_boards_for_selection()` | List Pinterest boards |
| `connect.list_snapchat_profiles()` | List Snapchat profiles |
| `connect.get_connect_url()` | Get OAuth connect URL |
| `connect.get_facebook_pages()` | List Facebook pages |
| `connect.get_gmb_locations()` | List GBP locations |
| `connect.get_linked_in_organizations()` | List LinkedIn orgs |
| `connect.get_pending_o_auth_data()` | Get pending OAuth data |
| `connect.get_pinterest_boards()` | List Pinterest boards |
| `connect.get_reddit_flairs()` | List subreddit flairs |
| `connect.get_reddit_subreddits()` | List Reddit subreddits |
| `connect.get_telegram_connect_status()` | Generate Telegram code |
| `connect.update_facebook_page()` | Update Facebook page |
| `connect.update_gmb_location()` | Update GBP location |
| `connect.update_linked_in_organization()` | Switch LinkedIn account type |
| `connect.update_pinterest_boards()` | Set default Pinterest board |
| `connect.update_reddit_subreddits()` | Set default subreddit |
| `connect.complete_telegram_connect()` | Check Telegram status |
| `connect.connect_bluesky_credentials()` | Connect Bluesky account |
| `connect.connect_whats_app_credentials()` | Connect WhatsApp via credentials |
| `connect.handle_o_auth_callback()` | Complete OAuth callback |
| `connect.initiate_telegram_connect()` | Connect Telegram directly |
| `connect.select_facebook_page()` | Select Facebook page |
| `connect.select_google_business_location()` | Select GBP location |
| `connect.select_linked_in_organization()` | Select LinkedIn org |
| `connect.select_pinterest_board()` | Select Pinterest board |
| `connect.select_snapchat_profile()` | Select Snapchat profile |

### Reddit
| Method | Description |
|--------|-------------|
| `reddit.get_reddit_feed()` | Get subreddit feed |
| `reddit.search_reddit()` | Search posts |

### Account Settings
| Method | Description |
|--------|-------------|
| `account_settings.get_instagram_ice_breakers()` | Get IG ice breakers |
| `account_settings.get_messenger_menu()` | Get FB persistent menu |
| `account_settings.get_telegram_commands()` | Get TG bot commands |
| `account_settings.delete_instagram_ice_breakers()` | Delete IG ice breakers |
| `account_settings.delete_messenger_menu()` | Delete FB persistent menu |
| `account_settings.delete_telegram_commands()` | Delete TG bot commands |
| `account_settings.set_instagram_ice_breakers()` | Set IG ice breakers |
| `account_settings.set_messenger_menu()` | Set FB persistent menu |
| `account_settings.set_telegram_commands()` | Set TG bot commands |

### Comments (Inbox)
| Method | Description |
|--------|-------------|
| `comments.list_inbox_comments()` | List commented posts |
| `comments.get_inbox_post_comments()` | Get post comments |
| `comments.delete_inbox_comment()` | Delete comment |
| `comments.hide_inbox_comment()` | Hide comment |
| `comments.like_inbox_comment()` | Like comment |
| `comments.reply_to_inbox_post()` | Reply to comment |
| `comments.send_private_reply_to_comment()` | Send private reply |
| `comments.unhide_inbox_comment()` | Unhide comment |
| `comments.unlike_inbox_comment()` | Unlike comment |

### GMB Attributes
| Method | Description |
|--------|-------------|
| `gmb_attributes.get_google_business_attributes()` | Get attributes |
| `gmb_attributes.update_google_business_attributes()` | Update attributes |

### GMB Food Menus
| Method | Description |
|--------|-------------|
| `gmb_food_menus.get_google_business_food_menus()` | Get food menus |
| `gmb_food_menus.update_google_business_food_menus()` | Update food menus |

### GMB Location Details
| Method | Description |
|--------|-------------|
| `gmb_location_details.get_google_business_location_details()` | Get location details |
| `gmb_location_details.update_google_business_location_details()` | Update location details |

### GMB Media
| Method | Description |
|--------|-------------|
| `gmb_media.list_google_business_media()` | List media |
| `gmb_media.create_google_business_media()` | Upload photo |
| `gmb_media.delete_google_business_media()` | Delete photo |

### GMB Place Actions
| Method | Description |
|--------|-------------|
| `gmb_place_actions.list_google_business_place_actions()` | List action links |
| `gmb_place_actions.create_google_business_place_action()` | Create action link |
| `gmb_place_actions.delete_google_business_place_action()` | Delete action link |

### Messages (Inbox)
| Method | Description |
|--------|-------------|
| `messages.list_inbox_conversations()` | List conversations |
| `messages.get_inbox_conversation()` | Get conversation |
| `messages.get_inbox_conversation_messages()` | List messages |
| `messages.update_inbox_conversation()` | Update conversation status |
| `messages.edit_inbox_message()` | Edit message |
| `messages.send_inbox_message()` | Send message |

### Reviews (Inbox)
| Method | Description |
|--------|-------------|
| `reviews.list_inbox_reviews()` | List reviews |
| `reviews.delete_inbox_review_reply()` | Delete review reply |
| `reviews.reply_to_inbox_review()` | Reply to review |

### Validate
| Method | Description |
|--------|-------------|
| `validate.validate_media()` | Validate media URL |
| `validate.validate_post()` | Validate post content |
| `validate.validate_post_length()` | Validate post character count |
| `validate.validate_subreddit()` | Check subreddit existence |

### WhatsApp
| Method | Description |
|--------|-------------|
| `whatsapp.bulk_delete_whats_app_contacts()` | Bulk delete contacts |
| `whatsapp.bulk_update_whats_app_contacts()` | Bulk update contacts |
| `whatsapp.create_whats_app_broadcast()` | Create broadcast |
| `whatsapp.create_whats_app_contact()` | Create contact |
| `whatsapp.create_whats_app_template()` | Create template |
| `whatsapp.get_whats_app_broadcast()` | Get broadcast |
| `whatsapp.get_whats_app_broadcast_recipients()` | List recipients |
| `whatsapp.get_whats_app_broadcasts()` | List broadcasts |
| `whatsapp.get_whats_app_business_profile()` | Get business profile |
| `whatsapp.get_whats_app_contact()` | Get contact |
| `whatsapp.get_whats_app_contacts()` | List contacts |
| `whatsapp.get_whats_app_groups()` | List contact groups |
| `whatsapp.get_whats_app_template()` | Get template |
| `whatsapp.get_whats_app_templates()` | List templates |
| `whatsapp.update_whats_app_business_profile()` | Update business profile |
| `whatsapp.update_whats_app_contact()` | Update contact |
| `whatsapp.update_whats_app_template()` | Update template |
| `whatsapp.delete_whats_app_broadcast()` | Delete broadcast |
| `whatsapp.delete_whats_app_contact()` | Delete contact |
| `whatsapp.delete_whats_app_group()` | Delete group |
| `whatsapp.delete_whats_app_template()` | Delete template |
| `whatsapp.add_whats_app_broadcast_recipients()` | Add recipients |
| `whatsapp.cancel_whats_app_broadcast_schedule()` | Cancel scheduled broadcast |
| `whatsapp.import_whats_app_contacts()` | Bulk import contacts |
| `whatsapp.remove_whats_app_broadcast_recipients()` | Remove recipients |
| `whatsapp.rename_whats_app_group()` | Rename group |
| `whatsapp.schedule_whats_app_broadcast()` | Schedule broadcast |
| `whatsapp.send_whats_app_broadcast()` | Send broadcast |
| `whatsapp.send_whats_app_bulk()` | Bulk send template messages |

### WhatsApp Phone Numbers
| Method | Description |
|--------|-------------|
| `whatsapp_phone_numbers.get_whats_app_phone_number()` | Get phone number |
| `whatsapp_phone_numbers.get_whats_app_phone_numbers()` | List phone numbers |
| `whatsapp_phone_numbers.purchase_whats_app_phone_number()` | Purchase phone number |
| `whatsapp_phone_numbers.release_whats_app_phone_number()` | Release phone number |

### Invites
| Method | Description |
|--------|-------------|
| `invites.create_invite_token()` | Create invite token |

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
