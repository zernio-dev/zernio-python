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
import re
from datetime import datetime, timedelta
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

from late import Late, MediaType, PostStatus

from .tool_definitions import use_tool_def

# Cache for documentation content
_docs_cache: dict[str, tuple[str, datetime]] = {}
_DOCS_URL = "https://docs.getlate.dev/llms-full.txt"
_CACHE_TTL_HOURS = 24

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
- docs_*     : Search Late API documentation
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
@use_tool_def("accounts_list")
def accounts_list() -> str:
    client = _get_client()
    response = client.accounts.list()
    accounts = response.accounts or []

    if not accounts:
        return "No accounts connected. Connect accounts at https://getlate.dev"

    lines = [f"Found {len(accounts)} connected account(s):\n"]
    for acc in accounts:
        username = acc.username or acc.displayName or acc.field_id
        lines.append(f"- {acc.platform}: {username} (ID: {acc.field_id})")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("accounts_get")
def accounts_get(platform: str) -> str:
    client = _get_client()
    response = client.accounts.list()
    accounts = response.accounts or []

    matching = [a for a in accounts if a.platform and a.platform.lower() == platform.lower()]

    if not matching:
        available = list({a.platform for a in accounts if a.platform})
        return f"No {platform} account found. Available: {', '.join(available)}"

    acc = matching[0]
    return f"Platform: {acc.platform}\nUsername: {acc.username or 'N/A'}\nID: {acc.field_id}"


# ============================================================================
# PROFILES
# ============================================================================


@mcp.tool()
@use_tool_def("profiles_list")
def profiles_list() -> str:
    client = _get_client()
    response = client.profiles.list()
    profiles = response.profiles or []

    if not profiles:
        return "No profiles found."

    lines = [f"Found {len(profiles)} profile(s):\n"]
    for profile in profiles:
        default = " (default)" if profile.isDefault else ""
        color = f" [{profile.color}]" if profile.color else ""
        lines.append(f"- {profile.name}{default}{color} (ID: {profile.field_id})")
        if profile.description:
            lines.append(f"  Description: {profile.description}")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("profiles_get")
def profiles_get(profile_id: str) -> str:
    client = _get_client()
    response = client.profiles.get(profile_id)
    profile = response.profile
    if not profile:
        return f"Profile {profile_id} not found."

    lines = [
        f"Name: {profile.name}",
        f"ID: {profile.field_id}",
        f"Default: {'Yes' if profile.isDefault else 'No'}",
    ]
    if profile.description:
        lines.append(f"Description: {profile.description}")
    if profile.color:
        lines.append(f"Color: {profile.color}")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("profiles_create")
def profiles_create(name: str, description: str = "", color: str = "") -> str:
    client = _get_client()

    params: dict[str, str] = {"name": name}
    if description:
        params["description"] = description
    if color:
        params["color"] = color

    response = client.profiles.create(**params)
    profile = response.profile

    return f"✅ Profile created!\nName: {profile.name if profile else 'N/A'}\nID: {profile.field_id if profile else 'N/A'}"


@mcp.tool()
@use_tool_def("profiles_update")
def profiles_update(
    profile_id: str,
    name: str = "",
    description: str = "",
    color: str = "",
    is_default: bool = False,
) -> str:
    client = _get_client()

    params: dict[str, str | bool] = {}
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
    profile = response.profile

    return f"✅ Profile updated!\nName: {profile.name if profile else 'N/A'}\nID: {profile.field_id if profile else 'N/A'}"


@mcp.tool()
@use_tool_def("profiles_delete")
def profiles_delete(profile_id: str) -> str:
    client = _get_client()
    client.profiles.delete(profile_id)
    return f"✅ Profile {profile_id} deleted"


# ============================================================================
# POSTS
# ============================================================================


@mcp.tool()
@use_tool_def("posts_list")
def posts_list(status: str = "", limit: int = 10) -> str:
    client = _get_client()
    params: dict[str, str | int] = {"limit": limit}
    if status:
        params["status"] = status

    response = client.posts.list(**params)
    posts = response.posts or []

    if not posts:
        return f"No posts found{f' with status {status}' if status else ''}."

    lines = [f"Found {len(posts)} post(s):\n"]
    for post in posts:
        content = post.content or ""
        content_preview = content[:60] + "..." if len(content) > 60 else content
        platforms = ", ".join(
            t.platform or "?" for t in (post.platforms or [])
        )
        status = post.status.value if post.status else "unknown"
        lines.append(f"- [{status}] {content_preview}")
        lines.append(f"  Platforms: {platforms} | ID: {post.field_id}")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("posts_get")
def posts_get(post_id: str) -> str:
    client = _get_client()
    response = client.posts.get(post_id)
    post = response.post
    if not post:
        return f"Post {post_id} not found."

    content = post.content or ""
    content_preview = content[:100] + "..." if len(content) > 100 else content
    platforms = ", ".join(t.platform or "?" for t in (post.platforms or []))

    status = post.status.value if post.status else "unknown"
    lines = [
        f"Post ID: {post.field_id}",
        f"Status: {status}",
        f"Platforms: {platforms}",
        f"Content: {content_preview}",
    ]

    if post.scheduledFor:
        lines.append(f"Scheduled for: {post.scheduledFor}")

    if hasattr(post, "publishedAt") and post.publishedAt:
        lines.append(f"Published at: {post.publishedAt}")

    if post.metadata and post.metadata.get("error"):
        lines.append(f"Error: {post.metadata['error']}")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("posts_create")
def posts_create(
    content: str,
    platform: str,
    is_draft: bool = False,
    publish_now: bool = False,
    schedule_minutes: int = 0,
    media_urls: str = "",
    title: str = "",
) -> str:
    client = _get_client()

    # Find account for platform
    accounts_response = client.accounts.list()
    accounts = accounts_response.accounts or []
    matching = [a for a in accounts if a.platform and a.platform.lower() == platform.lower()]

    if not matching:
        available = list({a.platform for a in accounts if a.platform})
        return f"No {platform} account connected. Available platforms: {', '.join(available)}"

    account = matching[0]

    # Build request
    params: dict[str, Any] = {
        "content": content,
        "platforms": [
            {
                "platform": account.platform,
                "accountId": account.field_id,
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
    post = response.post

    username = account.username or account.displayName or account.field_id
    media_info = (
        f" with {len(params.get('media_items', []))} media file(s)"
        if params.get("media_items")
        else ""
    )

    post_id = post.field_id if post else "N/A"
    if is_draft:
        return f"📝 Draft saved for {platform} (@{username}){media_info}\nPost ID: {post_id}\nStatus: draft"
    elif publish_now:
        return f"✅ Published to {platform} (@{username}){media_info}\nPost ID: {post_id}"
    else:
        scheduled = params["scheduled_for"].strftime("%Y-%m-%d %H:%M")
        return f"✅ Scheduled for {platform} (@{username}){media_info}\nPost ID: {post_id}\nScheduled: {scheduled}"


@mcp.tool()
@use_tool_def("posts_publish_now")
def posts_publish_now(content: str, platform: str, media_urls: str = "") -> str:
    return posts_create(
        content=content, platform=platform, publish_now=True, media_urls=media_urls
    )


@mcp.tool()
@use_tool_def("posts_cross_post")
def posts_cross_post(
    content: str,
    platforms: str,
    is_draft: bool = False,
    publish_now: bool = False,
    media_urls: str = "",
) -> str:
    client = _get_client()

    target_platforms = [p.strip().lower() for p in platforms.split(",")]
    accounts_response = client.accounts.list()
    accounts = accounts_response.accounts or []

    platform_targets = []
    not_found = []

    for platform in target_platforms:
        matching = [a for a in accounts if a.platform and a.platform.lower() == platform]
        if matching:
            platform_targets.append(
                {
                    "platform": matching[0].platform,
                    "accountId": matching[0].field_id,
                }
            )
        else:
            not_found.append(platform)

    if not platform_targets:
        available = list({a.platform for a in accounts if a.platform})
        return f"No matching accounts found. Available: {', '.join(available)}"

    params: dict[str, Any] = {
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
    post = response.post

    posted_to = [t["platform"] for t in platform_targets]
    media_info = (
        f" with {len(params.get('media_items', []))} media file(s)"
        if params.get("media_items")
        else ""
    )

    post_id = post.field_id if post else "N/A"
    if is_draft:
        result = f"📝 Draft saved for: {', '.join(posted_to)}{media_info}\nPost ID: {post_id}\nStatus: draft"
    else:
        result = f"✅ {'Published' if publish_now else 'Scheduled'} to: {', '.join(posted_to)}{media_info}\nPost ID: {post_id}"

    if not_found:
        result += f"\n⚠️ Accounts not found for: {', '.join(not_found)}"

    return result


@mcp.tool()
@use_tool_def("posts_update")
def posts_update(
    post_id: str,
    content: str = "",
    scheduled_for: str = "",
    title: str = "",
) -> str:
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
    post = response.post

    post_id_str = post.field_id if post else "N/A"
    status = post.status if post else "N/A"
    return f"✅ Post updated!\nID: {post_id_str}\nStatus: {status}"


@mcp.tool()
@use_tool_def("posts_delete")
def posts_delete(post_id: str) -> str:
    client = _get_client()
    client.posts.delete(post_id)
    return f"✅ Post {post_id} deleted"


@mcp.tool()
@use_tool_def("posts_retry")
def posts_retry(post_id: str) -> str:
    client = _get_client()

    try:
        post_response = client.posts.get(post_id)
        post = post_response.post
        if not post:
            return f"❌ Post {post_id} not found"
        if post.status != PostStatus.FAILED:
            return f"⚠️ Post {post_id} is not in failed status (current: {post.status})"
    except Exception as e:
        return f"❌ Could not find post {post_id}: {e}"

    try:
        client.posts.retry(post_id)
        return f"✅ Post {post_id} has been queued for retry"
    except Exception as e:
        return f"❌ Failed to retry post: {e}"


@mcp.tool()
@use_tool_def("posts_list_failed")
def posts_list_failed(limit: int = 10) -> str:
    client = _get_client()
    response = client.posts.list(status=PostStatus.FAILED, limit=limit)
    posts = response.posts or []

    if not posts:
        return "No failed posts found."

    lines = [f"Found {len(posts)} failed post(s):\n"]
    for post in posts:
        content = post.content or ""
        content_preview = content[:50] + "..." if len(content) > 50 else content
        platforms = ", ".join(t.platform or "?" for t in (post.platforms or []))
        error = post.metadata.get("error", "Unknown error") if post.metadata else "Unknown error"
        lines.append(f"- {content_preview}")
        lines.append(f"  Platforms: {platforms} | ID: {post.field_id}")
        lines.append(f"  Error: {error}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
@use_tool_def("posts_retry_all_failed")
def posts_retry_all_failed() -> str:
    client = _get_client()
    response = client.posts.list(status=PostStatus.FAILED, limit=50)
    posts = response.posts or []

    if not posts:
        return "No failed posts to retry."

    results = []
    success_count = 0
    fail_count = 0

    for post in posts:
        try:
            client.posts.retry(post.field_id)
            success_count += 1
        except Exception as e:
            fail_count += 1
            results.append(f"❌ {post.field_id}: {e}")

    summary = f"✅ Retried {success_count} post(s)"
    if fail_count > 0:
        summary += f"\n❌ Failed to retry {fail_count} post(s)"
        summary += "\n" + "\n".join(results)

    return summary


# ============================================================================
# MEDIA UPLOAD
# ============================================================================


@mcp.tool()
@use_tool_def("media_generate_upload_link")
def media_generate_upload_link() -> str:
    client = _get_client()

    try:
        response = client.media.generate_upload_token()

        upload_url = str(response.uploadUrl) if response.uploadUrl else ""
        token = response.token or ""
        expires_at = str(response.expiresAt) if response.expiresAt else ""

        return f"""📤 Upload link generated!

**Open this link in your browser to upload files:**
{upload_url}

Token: {token}
Expires: {expires_at}

Once you've uploaded your files, let me know and I'll check the status to get the URLs."""

    except Exception as e:
        return f"❌ Failed to generate upload link: {e}"


@mcp.tool()
@use_tool_def("media_check_upload_status")
def media_check_upload_status(token: str) -> str:
    client = _get_client()

    try:
        response = client.media.check_upload_token(token)

        status = response.status.value if response.status else "unknown"
        files = response.files or []

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
                url = str(f.url) if f.url else ""
                media_urls.append(url)
                lines.append(f"- {f.filename or 'unknown'}")
                lines.append(f"  Type: {f.type.value if f.type else 'N/A'}")
                lines.append(f"  URL: {url}")
                lines.append(f"  Size: {(f.size or 0) / 1024:.1f} KB")
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
# DOCS
# ============================================================================


def _get_docs_content() -> str:
    """Fetch and cache documentation content."""
    cache_key = "docs"

    # Check cache
    if cache_key in _docs_cache:
        content, cached_at = _docs_cache[cache_key]
        if datetime.now() - cached_at < timedelta(hours=_CACHE_TTL_HOURS):
            return content

    # Fetch fresh content
    try:
        response = httpx.get(_DOCS_URL, timeout=30.0)
        response.raise_for_status()
        content = response.text
        _docs_cache[cache_key] = (content, datetime.now())
        return content
    except Exception as e:
        # Return cached content if available, even if expired
        if cache_key in _docs_cache:
            return _docs_cache[cache_key][0]
        raise RuntimeError(f"Failed to fetch documentation: {e}") from e


def _search_docs(content: str, query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Search documentation content for relevant sections."""
    results: list[dict[str, str]] = []
    query_lower = query.lower()
    query_terms = query_lower.split()

    # Split content into sections (by markdown headers)
    sections = re.split(r'\n(?=#{1,3} )', content)

    scored_sections: list[tuple[int, str, str]] = []

    for section in sections:
        if not section.strip():
            continue

        section_lower = section.lower()

        # Calculate relevance score
        score = 0

        # Exact phrase match (highest priority)
        if query_lower in section_lower:
            score += 100

        # Individual term matches
        for term in query_terms:
            if term in section_lower:
                score += 10
                # Bonus for term in header
                first_line = section.split('\n')[0].lower()
                if term in first_line:
                    score += 20

        if score > 0:
            # Extract title from first line
            lines = section.strip().split('\n')
            title = lines[0].lstrip('#').strip() if lines else "Untitled"
            scored_sections.append((score, title, section.strip()))

    # Sort by score and take top results
    scored_sections.sort(key=lambda x: x[0], reverse=True)

    for score, title, section_text in scored_sections[:max_results]:
        # Truncate long sections
        if len(section_text) > 1500:
            section_text = section_text[:1500] + "\n...(truncated)"

        results.append({
            "title": title,
            "content": section_text,
            "relevance": str(score),
        })

    return results


@mcp.tool()
@use_tool_def("docs_search")
def docs_search(query: str) -> str:
    try:
        content = _get_docs_content()
        results = _search_docs(content, query)

        if not results:
            return f"No documentation found for '{query}'. Try different search terms."

        lines = [f"Found {len(results)} relevant section(s) for '{query}':\n"]

        for i, result in enumerate(results, 1):
            lines.append(f"--- Result {i}: {result['title']} ---")
            lines.append(result["content"])
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"❌ Failed to search documentation: {e}"


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    mcp.run()
