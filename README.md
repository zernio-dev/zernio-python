<p align="center">
  <a href="https://zernio.com">
    <img src="https://zernio.com/brand/icon-primary.png" alt="Zernio" width="60">
  </a>
</p>

<h1 align="center">Zernio Python SDK</h1>

<p align="center">
  <a href="https://pypi.org/project/zernio-sdk/"><img src="https://img.shields.io/pypi/v/zernio-sdk.svg" alt="PyPI version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  <strong>One API to post everywhere. 14 platforms, zero headaches.</strong>
</p>

The official Python SDK for the [Zernio API](https://zernio.com) — schedule and publish social media posts across Instagram, TikTok, YouTube, LinkedIn, X/Twitter, Facebook, Pinterest, Threads, Bluesky, Reddit, Snapchat, Telegram, WhatsApp, and Google Business Profile with a single integration.

## Installation

```bash
pip install zernio-sdk
```

## Quick Start

```python
from zernio import Zernio

# Reads ZERNIO_API_KEY from environment (or pass explicitly)
client = Zernio()

# Publish to multiple platforms with one call
post = client.posts.create(
    content="Hello world from Zernio!",
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
client = Zernio(
    api_key="your-api-key",  # Or set ZERNIO_API_KEY env var
    base_url="https://zernio.com/api",  # Optional, this is the default
    timeout=30.0,  # Optional, request timeout in seconds
)
```

## Examples

### Schedule a Post

```python
post = client.posts.create(
    content="This post will go live tomorrow at 10am",
    platforms=[{"platform": "instagram", "accountId": "acc_xxx"}],
    scheduled_for="2025-02-01T10:00:00Z",
)
```

### Platform-Specific Content

Customize content per platform while posting to all at once:

```python
post = client.posts.create(
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
result = client.media.upload("path/to/video.mp4")
media_url = result["publicUrl"]

# Option 2: Upload from bytes
result = client.media.upload_bytes(video_bytes, "video.mp4", "video/mp4")
media_url = result["publicUrl"]

# Create post with media
post = client.posts.create(
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
data = client.analytics.get(period="30d")

print("Analytics:", data)
```

### List Connected Accounts

```python
data = client.accounts.list()

for account in data["accounts"]:
    print(f"{account['platform']}: @{account['username']}")
```

### Async Support

```python
import asyncio
from zernio import Zernio

async def main():
    async with Zernio(api_key="your-api-key") as client:
        posts = await client.posts.alist(status="scheduled")
        print(f"Found {len(posts['posts'])} scheduled posts")

asyncio.run(main())
```

## Error Handling

```python
from zernio import Zernio, ZernioAPIError, ZernioRateLimitError, ZernioValidationError

client = Zernio(api_key="your-api-key")

try:
    client.posts.create(content="Hello!", platforms=[...])
except ZernioRateLimitError as e:
    print(f"Rate limited: {e}")
except ZernioValidationError as e:
    print(f"Invalid request: {e}")
except ZernioAPIError as e:
    print(f"API error: {e}")
```

## Migration from Late

All old names continue to work. No code changes are required:

```python
# Old style (still works)
from late import Late, LateAPIError
client = Late(api_key="...")

# New style
from zernio import Zernio, ZernioAPIError
client = Zernio()  # reads ZERNIO_API_KEY env var
```

Both `from zernio import ...` and `from late import ...` work identically. The `LATE_API_KEY` environment variable is also still supported as a fallback when `ZERNIO_API_KEY` is not set.

## SDK Reference

### Posts
| Method | Description |
|--------|-------------|
| `posts.list_posts()` | List posts |
| `posts.bulk_upload_posts()` | Bulk upload from CSV |
| `posts.create_post()` | Create post |
| `posts.get_post()` | Get post |
| `posts.update_post()` | Update post |
| `posts.update_post_metadata()` | Update post metadata |
| `posts.delete_post()` | Delete post |
| `posts.edit_post()` | Edit published post |
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
| `accounts.get_tik_tok_creator_info()` | Get TikTok creator info |
| `accounts.update_account()` | Update account |
| `accounts.delete_account()` | Disconnect account |
| `accounts.delete_google_business_review_reply()` | Delete a review reply |
| `accounts.batch_get_google_business_reviews()` | Batch get reviews |
| `accounts.move_account_to_profile()` | Move account to a different profile |
| `accounts.reply_to_google_business_review()` | Reply to a review |

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
| `analytics.get_facebook_page_insights()` | Get Facebook Page insights |
| `analytics.get_google_business_performance()` | Get GBP performance metrics |
| `analytics.get_google_business_search_keywords()` | Get GBP search keywords |
| `analytics.get_instagram_account_insights()` | Get Instagram insights |
| `analytics.get_instagram_demographics()` | Get Instagram demographics |
| `analytics.get_instagram_follower_history()` | Get Instagram follower history |
| `analytics.get_linked_in_aggregate_analytics()` | Get LinkedIn aggregate stats |
| `analytics.get_linked_in_org_aggregate_analytics()` | Get LinkedIn organization page aggregate analytics |
| `analytics.get_linked_in_post_analytics()` | Get LinkedIn post stats |
| `analytics.get_linked_in_post_reactions()` | Get LinkedIn post reactions |
| `analytics.get_post_timeline()` | Get post analytics timeline |
| `analytics.get_posting_frequency()` | Get frequency vs engagement |
| `analytics.get_tik_tok_account_insights()` | Get TikTok account-level insights |
| `analytics.get_you_tube_channel_insights()` | Get YouTube channel-level insights |
| `analytics.get_you_tube_daily_views()` | Get YouTube daily views |
| `analytics.get_you_tube_demographics()` | Get YouTube demographics |

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
| `webhooks.get_webhook_logs()` | List webhook delivery logs |
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
| `media.get_media_presigned_url()` | Get upload URL |
| `media.upload()` | Upload a file from path |
| `media.upload_bytes()` | Upload file from bytes |
| `media.upload_large()` | Upload large file with multipart |
| `media.upload_large_bytes()` | Upload large file from bytes |
| `media.upload_multiple()` | Upload multiple files |

### Users
| Method | Description |
|--------|-------------|
| `users.list_users()` | List users |
| `users.get_user()` | Get user |

### Usage
| Method | Description |
|--------|-------------|
| `usage.get_usage_stats()` | Get plan and usage stats |
| `usage.get_x_api_pricing()` | Get X/Twitter API pricing table |

### Logs
| Method | Description |
|--------|-------------|
| `logs.list_logs()` | List activity logs |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.list_facebook_pages()` | List Facebook pages |
| `connect.list_google_business_locations()` | List GBP locations |
| `connect.list_linked_in_organizations()` | List LinkedIn orgs |
| `connect.list_pinterest_boards_for_selection()` | List Pinterest boards |
| `connect.list_snapchat_profiles()` | List Snapchat profiles |
| `connect.list_whats_app_phone_numbers()` | List WhatsApp phone numbers for selection |
| `connect.get_connect_url()` | Get OAuth connect URL |
| `connect.get_facebook_pages()` | List Facebook pages |
| `connect.get_gmb_locations()` | List GBP locations |
| `connect.get_linked_in_organizations()` | List LinkedIn orgs |
| `connect.get_pending_o_auth_data()` | Get pending OAuth data |
| `connect.get_pinterest_boards()` | List Pinterest boards |
| `connect.get_reddit_flairs()` | List subreddit flairs |
| `connect.get_reddit_subreddits()` | List Reddit subreddits |
| `connect.get_telegram_connect_status()` | Generate Telegram code |
| `connect.get_youtube_playlists()` | List YouTube playlists |
| `connect.update_facebook_page()` | Update Facebook page |
| `connect.update_gmb_location()` | Update GBP location |
| `connect.update_linked_in_organization()` | Switch LinkedIn account type |
| `connect.update_pinterest_boards()` | Set default Pinterest board |
| `connect.update_reddit_subreddits()` | Set default subreddit |
| `connect.update_youtube_default_playlist()` | Set default YouTube playlist |
| `connect.complete_telegram_connect()` | Check Telegram status |
| `connect.complete_whats_app_phone_selection()` | Complete WhatsApp phone number selection |
| `connect.configure_tik_tok_ads_brand_identity()` | Configure TikTok Ads Brand Identity |
| `connect.connect_ads()` | Connect ads for a platform |
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

### Ad Audiences
| Method | Description |
|--------|-------------|
| `ad_audiences.list_ad_audiences()` | List custom audiences |
| `ad_audiences.create_ad_audience()` | Create custom audience |
| `ad_audiences.get_ad_audience()` | Get audience details |
| `ad_audiences.delete_ad_audience()` | Delete custom audience |
| `ad_audiences.add_users_to_ad_audience()` | Add users to audience |

### Ad Campaigns
| Method | Description |
|--------|-------------|
| `ad_campaigns.list_ad_campaigns()` | List campaigns |
| `ad_campaigns.bulk_update_ad_campaign_status()` | Pause or resume many campaigns |
| `ad_campaigns.get_ad_tree()` | Get campaign tree |
| `ad_campaigns.get_ads_timeline()` | Get daily aggregate ad metrics for an account |
| `ad_campaigns.update_ad_campaign()` | Update a campaign (budget and/or bid strategy) |
| `ad_campaigns.update_ad_campaign_status()` | Pause or resume a campaign |
| `ad_campaigns.update_ad_set()` | Update an ad set (budget, status, and/or bid strategy) |
| `ad_campaigns.update_ad_set_status()` | Pause or resume a single ad set |
| `ad_campaigns.delete_ad_campaign()` | Delete a campaign |
| `ad_campaigns.duplicate_ad_campaign()` | Duplicate a campaign |

### Ads
| Method | Description |
|--------|-------------|
| `ads.list_ad_accounts()` | List ad accounts |
| `ads.list_ad_catalog_product_sets()` | List a catalog's product sets |
| `ads.list_ad_catalogs()` | List Meta product catalogs |
| `ads.list_ads()` | List ads |
| `ads.list_ads_business_centers()` | List TikTok Business Centers |
| `ads.list_conversion_associations()` | List campaigns associated with a conversion destination |
| `ads.list_conversion_destinations()` | List destinations for the Conversions API |
| `ads.list_form_leads()` | List leads for a single form |
| `ads.list_lead_forms()` | List Lead Gen (Instant) forms |
| `ads.list_leads()` | List submitted leads (cross-form CRM view) |
| `ads.create_conversion_destination()` | Create a conversion destination (LinkedIn) |
| `ads.create_ctwa_ad()` | Create Click-to-WhatsApp ad(s) |
| `ads.create_lead_form()` | Create a Lead Gen (Instant) form |
| `ads.create_standalone_ad()` | Create standalone ad |
| `ads.create_test_lead()` | Create a synthetic test lead |
| `ads.get_ad()` | Get ad details |
| `ads.get_ad_analytics()` | Get ad analytics |
| `ads.get_ad_comments()` | List comments on an ad |
| `ads.get_ad_tracking_tags()` | Read an ad's click-URL tracking tags |
| `ads.get_conversion_destination()` | Fetch a single conversion destination |
| `ads.get_conversion_metrics()` | Fetch attribution metrics for a conversion destination |
| `ads.get_conversions_quality()` | Read Event Match Quality + coverage for a Meta pixel |
| `ads.get_lead_form()` | Get a single Lead Gen form |
| `ads.update_ad()` | Update ad |
| `ads.update_ad_tracking_tags()` | Set/update an ad's click-URL tracking tags |
| `ads.update_conversion_destination()` | Update a conversion destination |
| `ads.delete_ad()` | Cancel an ad |
| `ads.delete_conversion_destination()` | Soft-delete a conversion destination |
| `ads.add_conversion_associations()` | Associate campaigns with a conversion destination |
| `ads.adjust_conversions()` | Adjust already-uploaded conversions (Google only) |
| `ads.archive_lead_form()` | Archive a Lead Gen form |
| `ads.boost_post()` | Boost post as ad |
| `ads.estimate_ad_reach()` | Estimate audience reach |
| `ads.remove_conversion_associations()` | Remove campaign↔conversion associations |
| `ads.search_ad_interests()` | Search targeting interests (deprecated) |
| `ads.search_ad_targeting()` | Search targeting options |
| `ads.send_conversions()` | Send conversion events to an ad platform |

### Broadcasts
| Method | Description |
|--------|-------------|
| `broadcasts.list_broadcast_recipients()` | List broadcast recipients |
| `broadcasts.list_broadcasts()` | List broadcasts |
| `broadcasts.create_broadcast()` | Create broadcast draft |
| `broadcasts.get_broadcast()` | Get broadcast details |
| `broadcasts.update_broadcast()` | Update broadcast |
| `broadcasts.delete_broadcast()` | Delete broadcast |
| `broadcasts.add_broadcast_recipients()` | Add recipients to a broadcast |
| `broadcasts.cancel_broadcast()` | Cancel broadcast |
| `broadcasts.schedule_broadcast()` | Schedule broadcast for later |
| `broadcasts.send_broadcast()` | Send broadcast now |

### Comment Automations
| Method | Description |
|--------|-------------|
| `comment_automations.list_comment_automation_logs()` | List automation logs |
| `comment_automations.list_comment_automations()` | List comment-to-DM automations |
| `comment_automations.create_comment_automation()` | Create comment-to-DM automation |
| `comment_automations.get_comment_automation()` | Get automation details |
| `comment_automations.update_comment_automation()` | Update automation settings |
| `comment_automations.delete_comment_automation()` | Delete automation |

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

### Contacts
| Method | Description |
|--------|-------------|
| `contacts.list_contacts()` | List contacts |
| `contacts.bulk_create_contacts()` | Bulk create contacts |
| `contacts.create_contact()` | Create contact |
| `contacts.get_contact()` | Get contact |
| `contacts.get_contact_channels()` | List channels for a contact |
| `contacts.update_contact()` | Update contact |
| `contacts.delete_contact()` | Delete contact |

### Custom Fields
| Method | Description |
|--------|-------------|
| `custom_fields.list_custom_fields()` | List custom field definitions |
| `custom_fields.create_custom_field()` | Create custom field |
| `custom_fields.update_custom_field()` | Update custom field |
| `custom_fields.delete_custom_field()` | Delete custom field |
| `custom_fields.clear_contact_field_value()` | Clear custom field value |
| `custom_fields.set_contact_field_value()` | Set custom field value |

### Discord
| Method | Description |
|--------|-------------|
| `discord.list_discord_guild_members()` | List Discord guild members |
| `discord.list_discord_guild_roles()` | List Discord guild roles |
| `discord.list_discord_pinned_messages()` | List pinned messages in a Discord channel |
| `discord.list_discord_scheduled_events()` | List Discord scheduled events |
| `discord.create_discord_scheduled_event()` | Create a Discord scheduled event |
| `discord.get_discord_channels()` | List Discord guild channels |
| `discord.get_discord_scheduled_event()` | Get a Discord scheduled event |
| `discord.get_discord_settings()` | Get Discord account settings |
| `discord.update_discord_scheduled_event()` | Update a Discord scheduled event |
| `discord.update_discord_settings()` | Update Discord settings |
| `discord.delete_discord_scheduled_event()` | Delete a Discord scheduled event |
| `discord.add_discord_member_role()` | Assign a role to a guild member |
| `discord.pin_discord_message()` | Pin a Discord message |
| `discord.remove_discord_member_role()` | Remove a role from a guild member |
| `discord.send_discord_direct_message()` | Send a Discord Direct Message |
| `discord.unpin_discord_message()` | Unpin a Discord message |

### GMB Attributes
| Method | Description |
|--------|-------------|
| `gmb_attributes.get_gmb_attribute_metadata()` | Get attribute metadata |
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
| `gmb_place_actions.update_google_business_place_action()` | Update action link |
| `gmb_place_actions.delete_google_business_place_action()` | Delete action link |

### GMB Services
| Method | Description |
|--------|-------------|
| `gmb_services.get_google_business_services()` | Get services |
| `gmb_services.update_google_business_services()` | Replace services |

### GMB Verifications
| Method | Description |
|--------|-------------|
| `gmb_verifications.get_google_business_verifications()` | Get verification state |
| `gmb_verifications.complete_google_business_verification()` | Complete a verification |
| `gmb_verifications.fetch_google_business_verification_options()` | Fetch verification options |
| `gmb_verifications.start_google_business_verification()` | Start a verification |

### Inbox Analytics
| Method | Description |
|--------|-------------|
| `inbox_analytics.list_inbox_conversation_analytics()` | List conversations with inbox analytics |
| `inbox_analytics.get_inbox_conversation_analytics()` | Get analytics for a single conversation |
| `inbox_analytics.get_inbox_heatmap()` | Get inbox day-of-week × hour-of-day heatmap |
| `inbox_analytics.get_inbox_response_time()` | Get inbox response-time stats |
| `inbox_analytics.get_inbox_source_breakdown()` | Get inbox source breakdown |
| `inbox_analytics.get_inbox_top_accounts()` | Get top accounts by inbox volume |
| `inbox_analytics.get_inbox_volume()` | Get inbox messaging volume |

### Instagram
| Method | Description |
|--------|-------------|
| `instagram.list_instagram_stories()` | List active Instagram stories |
| `instagram.get_instagram_story_insights()` | Get Instagram story insights |

### Messages (Inbox)
| Method | Description |
|--------|-------------|
| `messages.list_inbox_conversations()` | List conversations |
| `messages.create_inbox_conversation()` | Create conversation (send a WhatsApp template) |
| `messages.get_inbox_conversation()` | Get conversation |
| `messages.get_inbox_conversation_messages()` | List messages |
| `messages.update_inbox_conversation()` | Update conversation status |
| `messages.delete_inbox_message()` | Delete message |
| `messages.add_message_reaction()` | Add reaction |
| `messages.edit_inbox_message()` | Edit message |
| `messages.mark_conversation_read()` | Mark a conversation as read |
| `messages.remove_message_reaction()` | Remove reaction |
| `messages.send_inbox_message()` | Send message |
| `messages.send_typing_indicator()` | Send typing indicator |
| `messages.upload_media_direct()` | Upload media file |

### Reviews (Inbox)
| Method | Description |
|--------|-------------|
| `reviews.list_inbox_reviews()` | List reviews |
| `reviews.delete_inbox_review_reply()` | Delete review reply |
| `reviews.reply_to_inbox_review()` | Reply to review |

### Sequences
| Method | Description |
|--------|-------------|
| `sequences.list_sequence_enrollments()` | List enrollments for a sequence |
| `sequences.list_sequences()` | List sequences |
| `sequences.create_sequence()` | Create sequence |
| `sequences.get_sequence()` | Get sequence with steps |
| `sequences.update_sequence()` | Update sequence |
| `sequences.delete_sequence()` | Delete sequence |
| `sequences.activate_sequence()` | Activate sequence |
| `sequences.enroll_contacts()` | Enroll contacts in a sequence |
| `sequences.pause_sequence()` | Pause sequence |
| `sequences.unenroll_contact()` | Unenroll contact |

### Tracking Tags
| Method | Description |
|--------|-------------|
| `tracking_tags.list_tracking_tag_shared_accounts()` | List ad accounts a tracking tag is shared with |
| `tracking_tags.list_tracking_tags()` | List tracking tags (Meta Pixels) |
| `tracking_tags.create_tracking_tag()` | Create a tracking tag (Meta Pixel) |
| `tracking_tags.get_tracking_tag()` | Fetch a single tracking tag (Meta Pixel) |
| `tracking_tags.get_tracking_tag_stats()` | Aggregated event stats for a tracking tag (Meta Pixel) |
| `tracking_tags.update_tracking_tag()` | Update a tracking tag (Meta Pixel) |
| `tracking_tags.add_tracking_tag_shared_account()` | Share a tracking tag with an ad account |
| `tracking_tags.remove_tracking_tag_shared_account()` | Stop sharing a tracking tag with an ad account |

### Twitter Engagement
| Method | Description |
|--------|-------------|
| `twitter_engagement.bookmark_post()` | Bookmark a tweet |
| `twitter_engagement.follow_user()` | Follow a user |
| `twitter_engagement.remove_bookmark()` | Remove bookmark |
| `twitter_engagement.retweet_post()` | Retweet a post |
| `twitter_engagement.undo_retweet()` | Undo retweet |
| `twitter_engagement.unfollow_user()` | Unfollow a user |

### Validate
| Method | Description |
|--------|-------------|
| `validate.validate_media()` | Validate media URL |
| `validate.validate_post()` | Validate post content |
| `validate.validate_post_length()` | Validate character count |
| `validate.validate_subreddit()` | Check subreddit existence |

### WhatsApp
| Method | Description |
|--------|-------------|
| `whatsapp.list_whats_app_conversions()` | List recent WhatsApp conversion events |
| `whatsapp.list_whats_app_group_chats()` | List active groups |
| `whatsapp.list_whats_app_group_join_requests()` | List join requests |
| `whatsapp.create_whats_app_dataset()` | Provision CTWA conversions dataset |
| `whatsapp.create_whats_app_group_chat()` | Create group |
| `whatsapp.create_whats_app_group_invite_link()` | Create invite link |
| `whatsapp.create_whats_app_template()` | Create template |
| `whatsapp.get_whats_app_business_profile()` | Get business profile |
| `whatsapp.get_whats_app_dataset()` | Get CTWA conversions dataset |
| `whatsapp.get_whats_app_display_name()` | Get display name status |
| `whatsapp.get_whats_app_group_chat()` | Get group info |
| `whatsapp.get_whats_app_template()` | Get template |
| `whatsapp.get_whats_app_templates()` | List templates |
| `whatsapp.update_whats_app_business_profile()` | Update business profile |
| `whatsapp.update_whats_app_display_name()` | Request display name change |
| `whatsapp.update_whats_app_group_chat()` | Update group settings |
| `whatsapp.update_whats_app_template()` | Update template |
| `whatsapp.delete_whats_app_group_chat()` | Delete group |
| `whatsapp.delete_whats_app_template()` | Delete template |
| `whatsapp.add_whats_app_group_participants()` | Add participants |
| `whatsapp.approve_whats_app_group_join_requests()` | Approve join requests |
| `whatsapp.reject_whats_app_group_join_requests()` | Reject join requests |
| `whatsapp.remove_whats_app_group_participants()` | Remove participants |
| `whatsapp.send_whats_app_conversion()` | Send WhatsApp conversion event |
| `whatsapp.upload_whats_app_profile_photo()` | Upload profile picture |

### WhatsApp Calling
| Method | Description |
|--------|-------------|
| `whatsapp_calling.list_whats_app_calls()` | List call history for an account |
| `whatsapp_calling.get_whats_app_call()` | Get a single call |
| `whatsapp_calling.get_whats_app_call_estimate()` | Estimate per-minute cost for a destination |
| `whatsapp_calling.get_whats_app_call_permissions()` | Check call permission for a consumer |
| `whatsapp_calling.get_whats_app_calling_config()` | Get calling config for an account |
| `whatsapp_calling.update_whats_app_calling()` | Update calling config |
| `whatsapp_calling.disable_whats_app_calling()` | Disable calling on a number |
| `whatsapp_calling.enable_whats_app_calling()` | Enable calling on a number |
| `whatsapp_calling.initiate_whats_app_call()` | Initiate outbound call |

### WhatsApp Flows
| Method | Description |
|--------|-------------|
| `whatsapp_flows.list_whats_app_flow_responses()` | List flow responses |
| `whatsapp_flows.list_whats_app_flow_versions()` | List flow versions |
| `whatsapp_flows.list_whats_app_flows()` | List flows |
| `whatsapp_flows.create_whats_app_flow()` | Create flow |
| `whatsapp_flows.get_whats_app_flow()` | Get flow |
| `whatsapp_flows.get_whats_app_flow_json()` | Get flow JSON asset |
| `whatsapp_flows.get_whats_app_flow_preview()` | Get flow preview URL |
| `whatsapp_flows.update_whats_app_flow()` | Update flow |
| `whatsapp_flows.delete_whats_app_flow()` | Delete flow |
| `whatsapp_flows.deprecate_whats_app_flow()` | Deprecate flow |
| `whatsapp_flows.publish_whats_app_flow()` | Publish flow |
| `whatsapp_flows.send_whats_app_flow_message()` | Send flow message |
| `whatsapp_flows.upload_whats_app_flow_json()` | Upload flow JSON |

### WhatsApp Phone Numbers
| Method | Description |
|--------|-------------|
| `whatsapp_phone_numbers.list_whats_app_number_countries()` | List offerable number countries |
| `whatsapp_phone_numbers.get_whats_app_number_info()` | Get number status |
| `whatsapp_phone_numbers.get_whats_app_number_kyc_form()` | Get regulated-number KYC form spec |
| `whatsapp_phone_numbers.get_whats_app_number_remediation()` | Get the declined requirements to fix |
| `whatsapp_phone_numbers.get_whats_app_phone_number()` | Get phone number |
| `whatsapp_phone_numbers.get_whats_app_phone_numbers()` | List phone numbers |
| `whatsapp_phone_numbers.check_whats_app_number_availability()` | Check a country's availability + address constraint |
| `whatsapp_phone_numbers.purchase_whats_app_phone_number()` | Purchase phone number |
| `whatsapp_phone_numbers.release_whats_app_phone_number()` | Release phone number |
| `whatsapp_phone_numbers.remediate_whats_app_number()` | Fix a declined number and re-submit |
| `whatsapp_phone_numbers.search_available_whats_app_numbers()` | Search available numbers to purchase |
| `whatsapp_phone_numbers.submit_whats_app_number_kyc()` | Submit regulated-number KYC |
| `whatsapp_phone_numbers.upload_whats_app_number_kyc_document()` | Upload a single regulated-number KYC document |
| `whatsapp_phone_numbers.validate_whats_app_number_kyc_address()` | Pre-validate a regulated-number KYC address (Tier 4) |

### WhatsApp Sandbox
| Method | Description |
|--------|-------------|
| `whatsapp_sandbox.list_whats_app_sandbox_sessions()` | List your sandbox sessions |
| `whatsapp_sandbox.create_whats_app_sandbox_session()` | Start a sandbox activation for a phone |
| `whatsapp_sandbox.delete_whats_app_sandbox_session()` | Revoke a sandbox session |

### WhatsApp Templates
| Method | Description |
|--------|-------------|
| `whatsapp_templates.get_whats_app_library_template()` | Look up a library template |

### Workflows
| Method | Description |
|--------|-------------|
| `workflows.list_workflow_execution_events()` | Get an execution's timeline |
| `workflows.list_workflow_executions()` | List workflow runs |
| `workflows.list_workflow_versions()` | List a workflow's version history |
| `workflows.list_workflows()` | List workflows |
| `workflows.create_workflow()` | Create workflow |
| `workflows.get_workflow()` | Get workflow with graph |
| `workflows.get_workflow_version()` | Get a specific workflow version |
| `workflows.update_workflow()` | Update workflow |
| `workflows.delete_workflow()` | Delete workflow |
| `workflows.activate_workflow()` | Activate workflow |
| `workflows.duplicate_workflow()` | Duplicate a workflow |
| `workflows.pause_workflow()` | Pause workflow |
| `workflows.restore_workflow_version()` | Restore a previous workflow version |
| `workflows.trigger_workflow()` | Manually start a workflow run |

### Invites
| Method | Description |
|--------|-------------|
| `invites.create_invite_token()` | Create invite token |

## MCP Server (Claude Desktop)

The SDK includes a Model Context Protocol (MCP) server for integration with Claude Desktop. See [MCP documentation](https://docs.zernio.com/resources/mcp) for setup instructions.

```bash
pip install zernio-sdk[mcp]
```

## Requirements

- Python 3.10+
- [Zernio API key](https://zernio.com) (free tier available)

## Links

- [Documentation](https://docs.zernio.com)
- [Dashboard](https://zernio.com/dashboard)
- [Changelog](https://docs.zernio.com/changelog)

## License

Apache-2.0
