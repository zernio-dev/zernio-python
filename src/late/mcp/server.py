"""
Late MCP Server.

Exposes Late API functionality through Model Context Protocol.

Usage:
    # Run directly
    uv run python -m late.mcp.server

    # Or in Claude Desktop config:
    {
        "mcpServers": {
            "late": {
                "command": "uvx",
                "args": ["--from", "late-sdk[mcp]", "late-mcp"],
                "env": {
                    "LATE_API_KEY": "your_api_key"
                }
            }
        }
    }
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP

from late import Late, MediaType, PostStatus

# Initialize MCP server
mcp = FastMCP(
    "Late",
    instructions="""
Late API server for scheduling social media posts.

Available tools are prefixed by resource:
- accounts_* : Manage connected social media accounts
- profiles_* : Manage profiles (groups of accounts)
- posts_*    : Create, list, update, delete posts
- media_*    : Upload images and videos
""",
)


def _get_client() -> Late:
    """Get Late client with API key from environment."""
    api_key = os.getenv("LATE_API_KEY", "")
    if not api_key:
        raise ValueError("LATE_API_KEY environment variable is required")

    base_url = os.getenv("LATE_BASE_URL", None)
    return Late(api_key=api_key, base_url=base_url)


# ============================================================================
# ACCOUNTS
# ============================================================================


@mcp.tool()
def accounts_list() -> str:
    """
    List all connected social media accounts.

    Returns the platform, username, and account ID for each connected account.
    """
    client = _get_client()
    response = client.accounts.list()
    accounts = response.get("accounts", [])

    if not accounts:
        return "No accounts connected. Connect accounts at https://getlate.dev"

    lines = [f"Found {len(accounts)} connected account(s):\n"]
    for acc in accounts:
        username = acc.get("username") or acc.get("name") or acc["_id"]
        lines.append(f"- {acc['platform']}: {username} (ID: {acc['_id']})")

    return "\n".join(lines)


@mcp.tool()
def accounts_get(platform: str) -> str:
    """
    Get account details for a specific platform.

    Args:
        platform: Platform name (twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads)
    """
    client = _get_client()
    response = client.accounts.list()
    accounts = response.get("accounts", [])

    matching = [a for a in accounts if a["platform"].lower() == platform.lower()]

    if not matching:
        available = list({a["platform"] for a in accounts})
        return f"No {platform} account found. Available: {', '.join(available)}"

    acc = matching[0]
    return f"Platform: {acc['platform']}\nUsername: {acc.get('username', 'N/A')}\nID: {acc['_id']}"


# ============================================================================
# PROFILES
# ============================================================================


@mcp.tool()
def profiles_list() -> str:
    """
    List all profiles.

    Profiles group multiple social accounts together for easier management.
    """
    client = _get_client()
    response = client.profiles.list()
    profiles = response.get("profiles", [])

    if not profiles:
        return "No profiles found."

    lines = [f"Found {len(profiles)} profile(s):\n"]
    for profile in profiles:
        default = " (default)" if profile.get("isDefault") else ""
        color = f" [{profile.get('color', '')}]" if profile.get("color") else ""
        lines.append(f"- {profile['name']}{default}{color} (ID: {profile['_id']})")
        if profile.get("description"):
            lines.append(f"  Description: {profile['description']}")

    return "\n".join(lines)


@mcp.tool()
def profiles_get(profile_id: str) -> str:
    """
    Get details of a specific profile.

    Args:
        profile_id: The profile ID
    """
    client = _get_client()
    response = client.profiles.get(profile_id)
    profile = response.get("profile", response)

    lines = [
        f"Name: {profile['name']}",
        f"ID: {profile['_id']}",
        f"Default: {'Yes' if profile.get('isDefault') else 'No'}",
    ]
    if profile.get("description"):
        lines.append(f"Description: {profile['description']}")
    if profile.get("color"):
        lines.append(f"Color: {profile['color']}")

    return "\n".join(lines)


@mcp.tool()
def profiles_create(name: str, description: str = "", color: str = "") -> str:
    """
    Create a new profile.

    Args:
        name: Profile name (required)
        description: Optional description
        color: Optional hex color (e.g., '#4CAF50')
    """
    client = _get_client()

    params = {"name": name}
    if description:
        params["description"] = description
    if color:
        params["color"] = color

    response = client.profiles.create(**params)
    profile = response.get("profile", {})

    return f"✅ Profile created!\nName: {profile.get('name')}\nID: {profile.get('_id')}"


@mcp.tool()
def profiles_update(
    profile_id: str,
    name: str = "",
    description: str = "",
    color: str = "",
    is_default: bool = False,
) -> str:
    """
    Update an existing profile.

    Args:
        profile_id: The profile ID to update
        name: New name (leave empty to keep current)
        description: New description (leave empty to keep current)
        color: New hex color (leave empty to keep current)
        is_default: Set as default profile
    """
    client = _get_client()

    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description
    if color:
        params["color"] = color
    if is_default:
        params["is_default"] = True

    if not params:
        return "⚠️ No changes specified. Provide at least one field to update."

    response = client.profiles.update(profile_id, **params)
    profile = response.get("profile", {})

    return f"✅ Profile updated!\nName: {profile.get('name')}\nID: {profile.get('_id')}"


@mcp.tool()
def profiles_delete(profile_id: str) -> str:
    """
    Delete a profile.

    Note: Profile must have no connected accounts.

    Args:
        profile_id: The profile ID to delete
    """
    client = _get_client()
    client.profiles.delete(profile_id)
    return f"✅ Profile {profile_id} deleted"


# ============================================================================
# POSTS
# ============================================================================


@mcp.tool()
def posts_list(status: str = "", limit: int = 10) -> str:
    """
    List posts with optional filtering.

    Args:
        status: Filter by status (scheduled, published, failed, draft). Empty for all.
        limit: Maximum number of posts to return (default 10)
    """
    client = _get_client()
    params = {"limit": limit}
    if status:
        params["status"] = status

    response = client.posts.list(**params)
    posts = response.get("posts", [])

    if not posts:
        return f"No posts found{f' with status {status}' if status else ''}."

    lines = [f"Found {len(posts)} post(s):\n"]
    for post in posts:
        content_preview = (
            post["content"][:60] + "..."
            if len(post["content"]) > 60
            else post["content"]
        )
        platforms = ", ".join(t.get("platform", "?") for t in post.get("platforms", []))
        lines.append(f"- [{post['status']}] {content_preview}")
        lines.append(f"  Platforms: {platforms} | ID: {post['_id']}")

    return "\n".join(lines)


@mcp.tool()
def posts_get(post_id: str) -> str:
    """
    Get details of a specific post by ID.

    Args:
        post_id: The post ID to retrieve
    """
    client = _get_client()
    response = client.posts.get(post_id)
    post = response.get("post", response)

    content_preview = (
        post["content"][:100] + "..." if len(post["content"]) > 100 else post["content"]
    )
    platforms = ", ".join(t.get("platform", "?") for t in post.get("platforms", []))

    lines = [
        f"Post ID: {post['_id']}",
        f"Status: {post['status']}",
        f"Platforms: {platforms}",
        f"Content: {content_preview}",
    ]

    if post.get("scheduledFor"):
        lines.append(f"Scheduled for: {post['scheduledFor']}")

    if post.get("publishedAt"):
        lines.append(f"Published at: {post['publishedAt']}")

    if post.get("error"):
        lines.append(f"Error: {post['error']}")

    return "\n".join(lines)


@mcp.tool()
def posts_create(
    content: str,
    platform: str,
    is_draft: bool = False,
    publish_now: bool = False,
    schedule_minutes: int = 0,
    media_urls: str = "",
    title: str = "",
) -> str:
    """
    Create a new social media post, optionally with media.

    Scheduling behavior:
    - is_draft=True: Save as draft (no scheduling, can edit later)
    - publish_now=True: Publish immediately
    - Neither: Schedule for schedule_minutes from now (default: 60 min)

    Args:
        content: The post content/text
        platform: Target platform (twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads)
        is_draft: Save as draft without scheduling. Draft posts can be edited and scheduled later (default: False)
        publish_now: Publish immediately instead of scheduling (default: False)
        schedule_minutes: Minutes from now to schedule (ignored if publish_now=True or is_draft=True). Default 60 min.
        media_urls: Comma-separated URLs of media files to attach. Optional.
        title: Optional title (required for YouTube, recommended for Pinterest)
    """
    client = _get_client()

    # Find account for platform
    accounts = client.accounts.list().get("accounts", [])
    matching = [a for a in accounts if a["platform"].lower() == platform.lower()]

    if not matching:
        available = list({a["platform"] for a in accounts})
        return f"No {platform} account connected. Available platforms: {', '.join(available)}"

    account = matching[0]

    # Build request
    params = {
        "content": content,
        "platforms": [
            {
                "platform": account["platform"],
                "accountId": account["_id"],
            }
        ],
    }

    if title:
        params["title"] = title

    # Add media items if provided
    if media_urls:
        urls = [u.strip() for u in media_urls.split(",") if u.strip()]
        media_items = []
        for url in urls:
            media_type: MediaType | str = MediaType.IMAGE
            if any(
                ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]
            ):
                media_type = MediaType.VIDEO
            elif any(ext in url.lower() for ext in [".gif"]):
                media_type = MediaType.GIF
            media_items.append({"type": media_type, "url": url})
        params["media_items"] = media_items

    if is_draft:
        params["is_draft"] = True
    elif publish_now:
        params["publish_now"] = True
    else:
        minutes = schedule_minutes if schedule_minutes > 0 else 60
        params["scheduled_for"] = datetime.now() + timedelta(minutes=minutes)

    response = client.posts.create(**params)
    post = response.get("post", {})

    username = account.get("username") or account.get("name") or account["_id"]
    media_info = (
        f" with {len(params.get('media_items', []))} media file(s)"
        if params.get("media_items")
        else ""
    )

    if is_draft:
        return f"📝 Draft saved for {platform} (@{username}){media_info}\nPost ID: {post.get('_id', 'N/A')}\nStatus: draft"
    elif publish_now:
        return f"✅ Published to {platform} (@{username}){media_info}\nPost ID: {post.get('_id', 'N/A')}"
    else:
        scheduled = params["scheduled_for"].strftime("%Y-%m-%d %H:%M")
        return f"✅ Scheduled for {platform} (@{username}){media_info}\nPost ID: {post.get('_id', 'N/A')}\nScheduled: {scheduled}"


@mcp.tool()
def posts_publish_now(content: str, platform: str, media_urls: str = "") -> str:
    """
    Publish a post immediately to a platform.

    Args:
        content: The post content/text
        platform: Target platform (twitter, instagram, linkedin, tiktok, bluesky, etc.)
        media_urls: Comma-separated URLs of media files to attach. Optional.
    """
    return posts_create(
        content=content, platform=platform, publish_now=True, media_urls=media_urls
    )


@mcp.tool()
def posts_cross_post(
    content: str,
    platforms: str,
    is_draft: bool = False,
    publish_now: bool = False,
    media_urls: str = "",
) -> str:
    """
    Post the same content to multiple platforms at once.

    Scheduling behavior:
    - is_draft=True: Save as draft (no scheduling, can edit later)
    - publish_now=True: Publish immediately
    - Neither: Schedule for 1 hour from now

    Args:
        content: The post content/text
        platforms: Comma-separated list of platforms (e.g., "twitter,linkedin,bluesky")
        is_draft: Save as draft without scheduling (default: False)
        publish_now: Publish immediately instead of scheduling (default: False)
        media_urls: Comma-separated URLs of media files to attach. Optional.
    """
    client = _get_client()

    target_platforms = [p.strip().lower() for p in platforms.split(",")]
    accounts = client.accounts.list().get("accounts", [])

    platform_targets = []
    not_found = []

    for platform in target_platforms:
        matching = [a for a in accounts if a["platform"].lower() == platform]
        if matching:
            platform_targets.append(
                {
                    "platform": matching[0]["platform"],
                    "accountId": matching[0]["_id"],
                }
            )
        else:
            not_found.append(platform)

    if not platform_targets:
        available = list({a["platform"] for a in accounts})
        return f"No matching accounts found. Available: {', '.join(available)}"

    params = {
        "content": content,
        "platforms": platform_targets,
    }

    if media_urls:
        urls = [u.strip() for u in media_urls.split(",") if u.strip()]
        media_items = []
        for url in urls:
            media_type: MediaType | str = MediaType.IMAGE
            if any(
                ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]
            ):
                media_type = MediaType.VIDEO
            elif any(ext in url.lower() for ext in [".gif"]):
                media_type = MediaType.GIF
            media_items.append({"type": media_type, "url": url})
        params["media_items"] = media_items

    if is_draft:
        params["is_draft"] = True
    elif publish_now:
        params["publish_now"] = True
    else:
        params["scheduled_for"] = datetime.now() + timedelta(hours=1)

    response = client.posts.create(**params)
    post = response.get("post", {})

    posted_to = [t["platform"] for t in platform_targets]
    media_info = (
        f" with {len(params.get('media_items', []))} media file(s)"
        if params.get("media_items")
        else ""
    )

    if is_draft:
        result = f"📝 Draft saved for: {', '.join(posted_to)}{media_info}\nPost ID: {post.get('_id', 'N/A')}\nStatus: draft"
    else:
        result = f"✅ {'Published' if publish_now else 'Scheduled'} to: {', '.join(posted_to)}{media_info}\nPost ID: {post.get('_id', 'N/A')}"

    if not_found:
        result += f"\n⚠️ Accounts not found for: {', '.join(not_found)}"

    return result


@mcp.tool()
def posts_update(
    post_id: str,
    content: str = "",
    scheduled_for: str = "",
    title: str = "",
) -> str:
    """
    Update an existing post.

    Only draft, scheduled, and failed posts can be updated.

    Args:
        post_id: The post ID to update
        content: New content (leave empty to keep current)
        scheduled_for: New schedule time as ISO string (leave empty to keep current)
        title: New title (leave empty to keep current)
    """
    client = _get_client()

    params = {}
    if content:
        params["content"] = content
    if scheduled_for:
        params["scheduled_for"] = scheduled_for
    if title:
        params["title"] = title

    if not params:
        return "⚠️ No changes specified. Provide at least one field to update."

    response = client.posts.update(post_id, **params)
    post = response.get("post", {})

    return f"✅ Post updated!\nID: {post.get('_id')}\nStatus: {post.get('status')}"


@mcp.tool()
def posts_delete(post_id: str) -> str:
    """
    Delete a post by ID.

    Published posts cannot be deleted.

    Args:
        post_id: The post ID to delete
    """
    client = _get_client()
    client.posts.delete(post_id)
    return f"✅ Post {post_id} deleted"


@mcp.tool()
def posts_retry(post_id: str) -> str:
    """
    Retry a failed post.

    Args:
        post_id: The ID of the failed post to retry
    """
    client = _get_client()

    try:
        post_response = client.posts.get(post_id)
        post = post_response.get("post", post_response)
        if post.get("status") != PostStatus.FAILED:
            return f"⚠️ Post {post_id} is not in failed status (current: {post.get('status')})"
    except Exception as e:
        return f"❌ Could not find post {post_id}: {e}"

    try:
        client.posts.retry(post_id)
        return f"✅ Post {post_id} has been queued for retry"
    except Exception as e:
        return f"❌ Failed to retry post: {e}"


@mcp.tool()
def posts_list_failed(limit: int = 10) -> str:
    """
    List all failed posts that can be retried.

    Args:
        limit: Maximum number of posts to return (default 10)
    """
    client = _get_client()
    response = client.posts.list(status=PostStatus.FAILED, limit=limit)
    posts = response.get("posts", [])

    if not posts:
        return "No failed posts found."

    lines = [f"Found {len(posts)} failed post(s):\n"]
    for post in posts:
        content_preview = (
            post["content"][:50] + "..."
            if len(post["content"]) > 50
            else post["content"]
        )
        platforms = ", ".join(t.get("platform", "?") for t in post.get("platforms", []))
        error = post.get("error", "Unknown error")
        lines.append(f"- {content_preview}")
        lines.append(f"  Platforms: {platforms} | ID: {post['_id']}")
        lines.append(f"  Error: {error}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
def posts_retry_all_failed() -> str:
    """
    Retry all failed posts.
    """
    client = _get_client()
    response = client.posts.list(status=PostStatus.FAILED, limit=50)
    posts = response.get("posts", [])

    if not posts:
        return "No failed posts to retry."

    results = []
    success_count = 0
    fail_count = 0

    for post in posts:
        try:
            client.posts.retry(post["_id"])
            success_count += 1
        except Exception as e:
            fail_count += 1
            results.append(f"❌ {post['_id']}: {e}")

    summary = f"✅ Retried {success_count} post(s)"
    if fail_count > 0:
        summary += f"\n❌ Failed to retry {fail_count} post(s)"
        summary += "\n" + "\n".join(results)

    return summary


# ============================================================================
# MEDIA UPLOAD
# ============================================================================


@mcp.tool()
def media_generate_upload_link() -> str:
    """
    Generate a unique upload URL for the user to upload files via browser.

    Use this when the user wants to include images or videos in their post.
    The flow is:
    1. Call this tool to get an upload URL
    2. Ask the user to open the URL in their browser
    3. User uploads files through the web interface
    4. Call media_check_upload_status to get the uploaded file URLs
    5. Use those URLs when creating the post with posts_create

    Returns:
        Upload URL and token for the user to open in browser
    """
    client = _get_client()

    try:
        response = client.media.generate_upload_token()

        upload_url = response.get("uploadUrl", "")
        token = response.get("token", "")
        expires_at = response.get("expiresAt", "")

        return f"""📤 Upload link generated!

**Open this link in your browser to upload files:**
{upload_url}

Token: {token}
Expires: {expires_at}

Once you've uploaded your files, let me know and I'll check the status to get the URLs."""

    except Exception as e:
        return f"❌ Failed to generate upload link: {e}"


@mcp.tool()
def media_check_upload_status(token: str) -> str:
    """
    Check the status of an upload token and get uploaded file URLs.

    Use this after the user has uploaded files through the browser upload page.

    Args:
        token: The upload token from media_generate_upload_link

    Returns:
        Status and uploaded file URLs if completed
    """
    client = _get_client()

    try:
        response = client.media.check_upload_token(token)

        status = response.get("status", "unknown")
        files = response.get("files", [])

        if status == "pending":
            return f"""⏳ Upload pending

The user hasn't uploaded files yet. Please wait for them to complete the upload in their browser.

Token: {token}"""

        elif status == "expired":
            return """⏰ Upload link expired

The upload link has expired. Use media_generate_upload_link to create a new one."""

        elif status == "completed":
            if not files:
                return "✅ Upload completed but no files were found."

            lines = [f"✅ Upload completed! {len(files)} file(s) uploaded:\n"]
            media_urls = []

            for f in files:
                url = f.get("url", "")
                media_urls.append(url)
                lines.append(f"- {f.get('filename', 'unknown')}")
                lines.append(f"  Type: {f.get('type', 'N/A')}")
                lines.append(f"  URL: {url}")
                lines.append(f"  Size: {f.get('size', 0) / 1024:.1f} KB")
                lines.append("")

            lines.append(
                "\n📝 You can now create a post with these media URLs using posts_create with the media_urls parameter."
            )
            lines.append(f"\nMedia URLs: {','.join(media_urls)}")

            return "\n".join(lines)

        else:
            return f"Unknown status: {status}"

    except Exception as e:
        return f"❌ Failed to check upload status: {e}"


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    mcp.run()
