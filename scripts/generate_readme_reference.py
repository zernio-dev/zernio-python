#!/usr/bin/env python3
"""
Generate SDK Reference section for README.md from the actual SDK code.

This script introspects the Late SDK resource classes and generates
markdown tables documenting all available methods.
"""

import inspect
import re
import sys
from pathlib import Path

# Add src to path so we can import late
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from late.resources import (
    PostsResource,
    AccountsResource,
    ProfilesResource,
    AnalyticsResource,
    AccountGroupsResource,
    QueueResource,
    WebhooksResource,
    ApiKeysResource,
    MediaResource,
    ToolsResource,
    UsersResource,
    UsageResource,
    LogsResource,
    ConnectResource,
    RedditResource,
    InvitesResource,
)

# Resource configuration: (class, resource_name, display_name)
RESOURCES = [
    (PostsResource, "posts", "Posts"),
    (AccountsResource, "accounts", "Accounts"),
    (ProfilesResource, "profiles", "Profiles"),
    (AnalyticsResource, "analytics", "Analytics"),
    (AccountGroupsResource, "account_groups", "Account Groups"),
    (QueueResource, "queue", "Queue"),
    (WebhooksResource, "webhooks", "Webhooks"),
    (ApiKeysResource, "api_keys", "API Keys"),
    (MediaResource, "media", "Media"),
    (ToolsResource, "tools", "Tools"),
    (UsersResource, "users", "Users"),
    (UsageResource, "usage", "Usage"),
    (LogsResource, "logs", "Logs"),
    (ConnectResource, "connect", "Connect (OAuth)"),
    (RedditResource, "reddit", "Reddit"),
    (InvitesResource, "invites", "Invites"),
]

# Method descriptions (can be extracted from docstrings or OpenAPI spec)
METHOD_DESCRIPTIONS = {
    # Posts
    "posts.list": "List all posts",
    "posts.create": "Create and schedule a post",
    "posts.get": "Get a specific post",
    "posts.update": "Update a scheduled post",
    "posts.delete": "Delete a post",
    "posts.retry": "Retry a failed post",
    "posts.bulk_upload": "Upload multiple posts at once",
    # Accounts
    "accounts.list": "List connected social accounts",
    "accounts.get": "Get a specific account",
    "accounts.get_follower_stats": "Get follower growth data",
    # Profiles
    "profiles.list": "List workspace profiles",
    "profiles.create": "Create a new profile",
    "profiles.get": "Get a specific profile",
    "profiles.update": "Update a profile",
    "profiles.delete": "Delete a profile",
    # Analytics
    "analytics.get": "Get post performance metrics",
    "analytics.get_usage": "Get API usage statistics",
    # Account Groups
    "account_groups.list_account_groups": "List account groups",
    "account_groups.create_account_group": "Create an account group",
    "account_groups.update_account_group": "Update an account group",
    "account_groups.delete_account_group": "Delete an account group",
    # Queue
    "queue.get_slots": "List queue time slots",
    "queue.update_slots": "Update queue slots",
    "queue.delete_slots": "Delete queue slots",
    "queue.preview": "Preview upcoming queued posts",
    "queue.next_slot": "Get next available slot",
    # Webhooks
    "webhooks.get_webhook_settings": "Get webhook configuration",
    "webhooks.create_webhook_settings": "Create webhook settings",
    "webhooks.update_webhook_settings": "Update webhook settings",
    "webhooks.delete_webhook_settings": "Delete webhook settings",
    "webhooks.test_webhook": "Send a test webhook",
    "webhooks.get_webhook_logs": "Get webhook delivery logs",
    # API Keys
    "api_keys.list_api_keys": "List API keys",
    "api_keys.create_api_key": "Create a new API key",
    "api_keys.delete_api_key": "Delete an API key",
    # Media
    "media.generate_upload_token": "Generate upload token for browser uploads",
    "media.check_upload_token": "Check upload token status",
    "media.upload": "Upload a file from path",
    "media.upload_bytes": "Upload file from bytes",
    "media.upload_large": "Upload large file with multipart",
    "media.upload_large_bytes": "Upload large file from bytes",
    "media.upload_multiple": "Upload multiple files",
    # Tools
    "tools.youtube_download": "Download YouTube video",
    "tools.youtube_transcript": "Get YouTube video transcript",
    "tools.instagram_download": "Download Instagram media",
    "tools.instagram_hashtag_check": "Check if hashtags are banned",
    "tools.tiktok_download": "Download TikTok video",
    "tools.twitter_download": "Download Twitter/X media",
    "tools.facebook_download": "Download Facebook video",
    "tools.linkedin_download": "Download LinkedIn video",
    "tools.bluesky_download": "Download Bluesky media",
    "tools.generate_caption": "Generate caption using AI",
    # Users
    "users.list": "List team users",
    "users.get": "Get a specific user",
    # Usage
    "usage.get_usage_stats": "Get API usage statistics",
    # Logs
    "logs.list_logs": "List publishing logs",
    "logs.get_log": "Get a specific log entry",
    "logs.get_post_logs": "Get logs for a specific post",
    # Connect
    "connect.get_connect_url": "Get OAuth URL for a platform",
    "connect.handle_o_auth_callback": "Handle OAuth callback",
    "connect.list_facebook_pages": "List Facebook pages",
    "connect.select_facebook_page": "Select a Facebook page",
    "connect.update_facebook_page": "Update Facebook page settings",
    "connect.list_google_business_locations": "List Google Business locations",
    "connect.select_google_business_location": "Select a Google Business location",
    "connect.list_linked_in_organizations": "List LinkedIn organizations",
    "connect.select_linked_in_organization": "Select a LinkedIn organization",
    "connect.get_linked_in_organizations": "Get LinkedIn organizations",
    "connect.update_linked_in_organization": "Update LinkedIn organization",
    "connect.list_pinterest_boards_for_selection": "List Pinterest boards",
    "connect.select_pinterest_board": "Select a Pinterest board",
    "connect.get_pinterest_boards": "Get Pinterest boards",
    "connect.update_pinterest_boards": "Update Pinterest boards",
    "connect.list_snapchat_profiles": "List Snapchat profiles",
    "connect.select_snapchat_profile": "Select a Snapchat profile",
    "connect.connect_bluesky_credentials": "Connect Bluesky with credentials",
    "connect.get_telegram_connect_status": "Get Telegram connection status",
    "connect.initiate_telegram_connect": "Start Telegram connection",
    "connect.complete_telegram_connect": "Complete Telegram connection",
    "connect.get_reddit_subreddits": "Get Reddit subreddits",
    "connect.update_reddit_subreddits": "Update Reddit subreddits",
    # Reddit
    "reddit.search_reddit": "Search Reddit",
    "reddit.get_reddit_feed": "Get Reddit feed",
    # Invites
    "invites.create_invite_token": "Create an invite token",
    "invites.list_platform_invites": "List platform invites",
    "invites.create_platform_invite": "Create a platform invite",
    "invites.delete_platform_invite": "Delete a platform invite",
}


def get_method_sort_key(method_name: str) -> tuple:
    """
    Generate a sort key for consistent method ordering.

    Ordering rules (CRUD-style):
    1. list/get_all methods first
    2. create methods
    3. get (single) methods
    4. update methods
    5. delete methods
    6. Everything else alphabetically

    This ensures consistent output regardless of how methods are discovered.
    """
    name_lower = method_name.lower()

    # Priority prefixes (lower number = higher priority)
    if name_lower.startswith("list") or name_lower.startswith("get_all"):
        return (0, method_name)
    elif name_lower.startswith("create") or name_lower == "bulk_upload":
        return (1, method_name)
    elif name_lower.startswith("get") and not name_lower.startswith("get_all"):
        return (2, method_name)
    elif name_lower.startswith("update"):
        return (3, method_name)
    elif name_lower.startswith("delete"):
        return (4, method_name)
    else:
        return (5, method_name)


def get_methods(cls):
    """Get all public sync methods from a resource class."""
    methods = []
    for name in dir(cls):
        # Skip private methods and async methods (prefixed with 'a')
        if name.startswith("_"):
            continue
        if name.startswith("a") and name[1:] in dir(cls):
            # This is an async variant of a sync method, skip it
            continue

        attr = getattr(cls, name, None)
        if callable(attr) and not isinstance(attr, type):
            # Check if it's actually a method (not inherited from object)
            if name not in dir(object):
                methods.append(name)

    # Sort with CRUD-style ordering for consistency
    return sorted(methods, key=get_method_sort_key)


def generate_description(resource_name: str, method_name: str) -> str:
    """Generate a description for a method."""
    key = f"{resource_name}.{method_name}"
    if key in METHOD_DESCRIPTIONS:
        return METHOD_DESCRIPTIONS[key]

    # Auto-generate description from method name
    words = re.sub(r"_", " ", method_name).title()
    return words


def generate_reference_section() -> str:
    """Generate the SDK Reference section markdown."""
    lines = ["## SDK Reference", ""]

    for cls, resource_name, display_name in RESOURCES:
        methods = get_methods(cls)

        if not methods:
            continue

        lines.append(f"### {display_name}")
        lines.append("| Method | Description |")
        lines.append("|--------|-------------|")

        for method in methods:
            desc = generate_description(resource_name, method)
            lines.append(f"| `{resource_name}.{method}()` | {desc} |")

        lines.append("")

    return "\n".join(lines)


def parse_existing_readme(readme_path: Path) -> dict[str, list[tuple[str, str]]]:
    """Parse existing SDK Reference section from README to get current methods."""
    content = readme_path.read_text()

    # Extract SDK Reference section
    match = re.search(r"## SDK Reference\n(.*?)(?=## MCP Server)", content, re.DOTALL)
    if not match:
        return {}

    section = match.group(1)
    existing = {}
    current_resource = None

    for line in section.split("\n"):
        # Match resource headers like "### Posts"
        header_match = re.match(r"### (.+)", line)
        if header_match:
            current_resource = header_match.group(1)
            existing[current_resource] = []
            continue

        # Match method rows like "| `posts.list()` | List all posts |"
        method_match = re.match(r"\| `([^`]+)\(\)` \| (.+) \|", line)
        if method_match and current_resource:
            method = method_match.group(1)
            description = method_match.group(2)
            existing[current_resource].append((method, description))

    return existing


def update_readme(readme_path: Path, reference_section: str) -> None:
    """
    Update the README.md file, only modifying if there are actual changes.

    This approach:
    1. Parses the existing SDK Reference section
    2. Compares with newly generated content
    3. Only writes if there are real changes (new methods, removed methods, or description changes)
    """
    content = readme_path.read_text()

    # Find the SDK Reference section and replace it
    # It starts with "## SDK Reference" and ends before "## MCP Server"
    pattern = r"## SDK Reference\n.*?(?=## MCP Server)"
    replacement = reference_section + "\n"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content != content:
        readme_path.write_text(new_content)
        print(f"Updated {readme_path}")

        # Show what changed
        old_methods = parse_existing_readme(readme_path)
        # Could add detailed diff output here if needed
    else:
        print("No changes needed")


def main():
    readme_path = Path(__file__).parent.parent / "README.md"

    if "--print" in sys.argv:
        # Just print the generated section
        print(generate_reference_section())
    else:
        # Update the README
        reference_section = generate_reference_section()
        update_readme(readme_path, reference_section)


if __name__ == "__main__":
    main()
