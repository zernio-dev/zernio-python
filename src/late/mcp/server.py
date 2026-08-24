"""
Zernio MCP Server.

Exposes Zernio API functionality through Model Context Protocol.

Usage:
    # Run directly
    uv run python -m late.mcp.server

    # Or in Claude Desktop config:
    {
        "mcpServers": {
            "zernio": {
                "command": "uvx",
                "args": ["--from", "zernio-sdk[mcp]", "zernio-mcp"],
                "env": {
                    "ZERNIO_API_KEY": "your_api_key"
                }
            }
        }
    }
"""

from __future__ import annotations

import os
import re
from contextvars import ContextVar
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.transforms.search import BM25SearchTransform
from mcp.types import ToolAnnotations

from late import Late, MediaType, PostStatus

from .auth import build_auth_provider
from .resources import register_resources
from .tool_definitions import TOOL_DEFINITIONS

if TYPE_CHECKING:
    from fastmcp.tools import Tool

# Context variable to store the Zernio API key for the current connection
_zernio_api_key: ContextVar[str | None] = ContextVar("zernio_api_key", default=None)

# Cache for documentation content
_docs_cache: dict[str, tuple[str, datetime]] = {}
_DOCS_URL = "https://docs.zernio.com/llms-full.txt"
_CACHE_TTL_HOURS = 24

# Always-visible core: the 20 hand-written ergonomic tools (guardrails +
# LLM-shaped args, preferred over their raw generated twins) plus the generated
# tools central to working on a profile — posting, the scheduling queue,
# pre-publish validation, account health, cross-platform analytics basics, and
# engagement on published posts. The remaining ~430 generated tools (messaging
# suite, ads, connect, platform-specific analytics, ...) sit behind the BM25
# tool-search transform (search_tools / call_tool), so clients see ~51 tools up
# front instead of 481 — small enough that clients which cap or truncate large
# tool lists show them all.
_PINNED_TOOLS = [
    # Hand-written ergonomic tools
    "accounts_list", "accounts_get",
    "profiles_list", "profiles_get", "profiles_create", "profiles_update", "profiles_delete",
    "posts_list", "posts_get", "posts_create", "posts_publish_now", "posts_cross_post",
    "posts_update", "posts_delete", "posts_retry", "posts_list_failed", "posts_retry_all_failed",
    "media_generate_upload_link", "media_check_upload_status",
    "docs_search",
    # Posting operations not covered by the ergonomic set
    "posts_bulk_upload_posts", "posts_unpublish_post", "posts_edit_post",
    # Scheduling queue
    "queue_list_queue_slots", "queue_create_queue_slot", "queue_update_queue_slot",
    "queue_delete_queue_slot", "queue_preview_queue", "queue_get_next_queue_slot",
    # Pre-publish validation
    "validate_post", "validate_post_length", "validate_media",
    # Account health & organisation
    "accounts_get_all_accounts_health", "accounts_get_account_health",
    "accounts_get_follower_stats", "accounts_move_account_to_profile",
    "account_groups_list_account_groups",
    # Cross-platform analytics basics
    "analytics_get_analytics", "analytics_get_best_time_to_post",
    "analytics_get_daily_metrics", "analytics_get_post_timeline",
    # Engagement on published posts
    "comments_list_inbox_comments", "comments_get_inbox_post_comments",
    "comments_reply_to_inbox_post",
    "mentions_list_inbox_mentions", "mentions_reply_to_mention",
    # Campaign tags & usage
    "tracking_tags_list_tracking_tags", "tracking_tags_get_tracking_tag_stats",
    "usage_get_usage",
]


class _AnnotatedBM25SearchTransform(BM25SearchTransform):
    """BM25SearchTransform whose synthetic tools carry ToolAnnotations.

    fastmcp builds search_tools/call_tool without annotations (still true in
    4.0.0b1). Clients that gate approval on hints treat an unannotated tool as
    needing confirmation, so codex-cli auto-denies both in non-interactive
    `codex exec` runs and reports "user cancelled MCP tool call".

    Wrapping the parent's Tool via model_copy instead of rebuilding it keeps
    the upstream closure by reference, so future upstream fixes to it (4.0
    adds a catalog-membership check inside call_tool) are inherited.
    """

    def _make_search_tool(self) -> Tool:
        # Pure in-memory catalog search: no external calls, no state change.
        return super()._make_search_tool().model_copy(
            update={
                "annotations": ToolAnnotations(
                    title="Search available tools",
                    readOnlyHint=True,
                    destructiveHint=False,
                    openWorldHint=False,
                )
            }
        )

    def _make_call_tool(self) -> Tool:
        # Dispatches to any hidden tool, including writes to external
        # platforms, so it must not claim to be read-only: that would bypass
        # client approval for every write reachable through the proxy.
        return super()._make_call_tool().model_copy(
            update={
                "annotations": ToolAnnotations(
                    title="Call a tool discovered via search",
                    readOnlyHint=False,
                    destructiveHint=True,
                    openWorldHint=True,
                )
            }
        )


# Initialize MCP server
mcp = FastMCP(
    "Zernio",
    instructions="""
Zernio API server for scheduling social media posts.

Available tools are prefixed by resource:
- accounts_* : Manage connected social media accounts
- profiles_* : Manage profiles (groups of accounts)
- posts_*    : Create, list, update, delete posts
- media_*    : Upload images and videos
- docs_*     : Search Zernio API documentation

MULTI-ACCOUNT WORKFLOW (agencies, multi-client setups):
When a user has more than one account on the same platform, you MUST
disambiguate before posting:

  1. Call accounts_list (or profiles_list then accounts_list with a
     profile_id filter) to discover account IDs.
  2. Pass account_id to posts_create / posts_publish_now, or account_ids
     (parallel to platforms) to posts_cross_post.

If account_id is omitted and the selection is ambiguous, the write tools
return an error containing the candidate list - read it, pick the right
account, and retry with account_id set. Never guess. The legacy behaviour
of silently picking the first matching account has been removed.
""",
    # Resource-server auth: validates the bearer against the Zernio API and
    # auto-serves RFC 9728 protected-resource discovery (see late.mcp.auth).
    auth=build_auth_provider(),
    # Collapse the ~383 generated tools behind search_tools/call_tool; the
    # pinned ergonomic tools remain always-visible.
    transforms=[_AnnotatedBM25SearchTransform(always_visible=_PINNED_TOOLS, max_results=8)],
)

register_resources(mcp)


# Hand-written tools that only read data. Everything else is treated as a
# destructive write for annotation purposes. Drives readOnlyHint/destructiveHint
# below; the Anthropic Connectors Directory requires every tool to carry one of
# those hints. (Generated tools get the same treatment from their HTTP method
# in scripts/generate_mcp_tools.py.)
_READ_ONLY_TOOLS = {
    "accounts_list",
    "accounts_get",
    "profiles_list",
    "profiles_get",
    "posts_list",
    "posts_get",
    "posts_list_failed",
    "media_check_upload_status",
    "docs_search",
}


def tool_def(name: str):
    """Register a hand-written MCP tool from its TOOL_DEFINITIONS entry.

    Pulls the docstring + parameter docs from TOOL_DEFINITIONS (the single
    source of truth) and attaches a tool annotation (human-readable title plus
    readOnlyHint/destructiveHint). Replaces the old `@mcp.tool()` +
    `@use_tool_def(...)` decorator pair so the docstring and the annotation
    stay defined in one place.
    """

    def decorator(func):
        td = TOOL_DEFINITIONS.get(name)
        if td:
            func.__doc__ = td.get_docstring()
        read_only = name in _READ_ONLY_TOOLS
        title = td.summary.rstrip(".") if td else name
        return mcp.tool(
            annotations=ToolAnnotations(
                title=title,
                readOnlyHint=read_only,
                destructiveHint=not read_only,
                # Write tools act on external social platforms; reads do not
                # change external state. Required explicitly for ChatGPT Apps.
                openWorldHint=not read_only,
            )
        )(func)

    return decorator


def set_late_api_key(api_key: str) -> None:
    """
    Set the Zernio API key for the current async context.

    In HTTP mode the key now flows through FastMCP's AccessToken (see
    _get_client); this setter remains for tests and embedding use.

    Args:
        api_key: The Zernio API key to use for this connection.
    """
    _zernio_api_key.set(api_key)


def _get_client() -> Late:
    """
    Get Zernio client with API key from context or environment.

    For HTTP connections, uses the bearer validated by the FastMCP auth layer.
    For STDIO connections (Claude Desktop), falls back to env vars.
    Priority: ZERNIO_API_KEY > LATE_API_KEY (legacy).

    Returns:
        Late client instance.

    Raises:
        ValueError: If no API key is available.
    """
    # HTTP mode: the FastMCP auth layer validated the bearer and exposes it as
    # the current request's AccessToken. get_access_token() returns None off
    # HTTP (STDIO) or when unauthenticated.
    api_key = ""
    try:
        token = get_access_token()
    except Exception:
        token = None
    if token is not None:
        api_key = token.token or ""

    # Fall back to the per-request ContextVar (kept for tests) then env vars
    # (STDIO mode for Claude Desktop).
    if not api_key:
        api_key = _zernio_api_key.get() or ""
    if not api_key:
        api_key = os.getenv("ZERNIO_API_KEY") or os.getenv("LATE_API_KEY", "")

    if not api_key:
        raise ValueError(
            "Zernio API key is required. "
            "For HTTP: provide via Authorization: Bearer header. "
            "For STDIO: set ZERNIO_API_KEY environment variable."
        )

    base_url = os.getenv("ZERNIO_BASE_URL") or os.getenv("LATE_BASE_URL", None)
    return Late(api_key=api_key, base_url=base_url)


# ============================================================================
# HELPERS
# ============================================================================


def _platform_str(value: Any) -> str:
    """Extract string value from a platform enum or return as-is if already a string.

    The auto-generated models use plain Enum classes (Platform5, Platform6, etc.)
    whose instances don't have .lower() and whose str() returns 'Platform5.TWITTER'
    instead of 'twitter'. This helper normalises any platform value to a clean
    lowercase string regardless of the underlying type.
    """
    if value is None:
        return ""
    # Platform(str, Enum) from enums.py is already a str, so this branch
    # handles both plain strings and StrEnum instances.
    if isinstance(value, str):
        return value.lower()
    # Plain Enum from generated models: extract .value
    if hasattr(value, "value"):
        return str(value.value).lower()
    return str(value).lower()


def _resolve_account(
    client: Late,
    platform: str,
    account_id: str = "",
    profile_id: str = "",
) -> Any:
    """Resolve a single account for a given platform without silent guessing.

    Resolution order:
      1. account_id  -> verify it exists and matches the requested platform.
      2. profile_id  -> list accounts in that profile, filter by platform.
      3. neither     -> list all accounts, filter by platform.

    Raises ValueError with an LLM-readable message when the selection is
    ambiguous (>= 2 candidates) or empty. This is the load-bearing piece of
    the multi-account fix: previously the MCP silently picked matching[0],
    which routed agency posts to the wrong client account.
    """
    platform_l = platform.lower()

    # Path 1: explicit account_id. We still cross-check the platform so the
    # LLM can't accidentally publish a tweet to a LinkedIn account.
    if account_id:
        accounts = (client.accounts.list().accounts or [])
        acc = next((a for a in accounts if a.field_id == account_id), None)
        if not acc:
            raise ValueError(
                f"Account {account_id} not found or not accessible with this API key."
            )
        if _platform_str(acc.platform) != platform_l:
            raise ValueError(
                f"Account {account_id} is a {_platform_str(acc.platform)} "
                f"account, not {platform_l}."
            )
        return acc

    # Path 2 & 3: list (optionally scoped to a profile) then filter by platform.
    pool = (
        client.accounts.list(profile_id=profile_id).accounts
        if profile_id else client.accounts.list().accounts
    ) or []

    matching = [
        a for a in pool
        if a.platform and _platform_str(a.platform) == platform_l
    ]

    if not matching:
        scope = f" in profile {profile_id}" if profile_id else ""
        available = sorted({_platform_str(a.platform) for a in pool if a.platform})
        raise ValueError(
            f"No {platform_l} account found{scope}. "
            f"Available platforms: {', '.join(available) or '(none)'}."
        )

    if len(matching) > 1:
        listing = "\n".join(
            f"  - {a.username or a.displayName or a.field_id} (account_id: {a.field_id})"
            for a in matching
        )
        raise ValueError(
            f"Multiple {platform_l} accounts available. Pass account_id "
            f"(or profile_id to scope) and retry:\n{listing}"
        )

    return matching[0]


# ============================================================================
# ACCOUNTS
# ============================================================================


@tool_def("accounts_list")
def accounts_list() -> str:
    client = _get_client()
    response = client.accounts.list()
    accounts = response.accounts or []

    if not accounts:
        return "No accounts connected. Connect accounts at https://zernio.com"

    lines = [f"Found {len(accounts)} connected account(s):\n"]
    for acc in accounts:
        username = acc.username or acc.displayName or acc.field_id
        lines.append(f"- {_platform_str(acc.platform)}: {username} (ID: {acc.field_id})")

    return "\n".join(lines)


@tool_def("accounts_get")
def accounts_get(platform: str) -> str:
    client = _get_client()
    try:
        acc = _resolve_account(client, platform)
    except ValueError as e:
        # Surface ambiguity / missing-account errors to the LLM so it can
        # call accounts_list and retry with a specific ID. Previously this
        # path silently returned matching[0].
        return str(e)
    return (
        f"Platform: {_platform_str(acc.platform)}\n"
        f"Username: {acc.username or 'N/A'}\n"
        f"ID: {acc.field_id}"
    )


# ============================================================================
# PROFILES
# ============================================================================


@tool_def("profiles_list")
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


@tool_def("profiles_get")
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


@tool_def("profiles_create")
def profiles_create(name: str, description: str = "", color: str = "") -> str:
    client = _get_client()

    params: dict[str, str] = {"name": name}
    if description:
        params["description"] = description
    if color:
        params["color"] = color

    response = client.profiles.create(**params)
    profile = response.profile

    return f"\u2705 Profile created!\nName: {profile.name if profile else 'N/A'}\nID: {profile.field_id if profile else 'N/A'}"


@tool_def("profiles_update")
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
        return "\u26a0\ufe0f No changes specified. Provide at least one field to update."

    response = client.profiles.update(profile_id, **params)
    profile = response.profile

    return f"\u2705 Profile updated!\nName: {profile.name if profile else 'N/A'}\nID: {profile.field_id if profile else 'N/A'}"


@tool_def("profiles_delete")
def profiles_delete(profile_id: str) -> str:
    client = _get_client()
    client.profiles.delete(profile_id)
    return f"\u2705 Profile {profile_id} deleted"


# ============================================================================
# POSTS
# ============================================================================


def _platform_errors(post: Any) -> list[str]:
    """One "Error (platform): message" line per platform that did not publish.

    A post holds one entry in post.platforms[] per target platform, and each
    entry tracks its own status and errorMessage. The API never populates
    post.metadata["error"], so that is where the real text lives.

    An entry that published can still carry an errorMessage left over from an
    earlier attempt, so the entry's own status decides whether it counts, not
    whether it has a message.

    Two statuses count, the two that mean "this platform is done and did not
    publish": failed and cancelled. Cancelled matters because
    account-disconnect cleanup writes the only actionable reason onto that
    entry ('Account "X" was disconnected'), so a failed post targeting one
    platform that got cancelled would otherwise read "Unknown error".

    The in-progress statuses (pending, processing, uploading) are excluded:
    every reset path clears errorMessage, so anything still on one is stale.
    """
    errors = []
    for target in post.platforms or []:
        if target.status not in ("failed", "cancelled"):
            continue
        message = (target.errorMessage or "").strip()
        if message:
            errors.append(f"Error ({target.platform or '?'}): {message}")
    return errors


@tool_def("posts_list")
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
        lines.extend(f"  {error}" for error in _platform_errors(post))

    return "\n".join(lines)


@tool_def("posts_get")
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

    lines.extend(_platform_errors(post))

    return "\n".join(lines)


@tool_def("posts_create")
def posts_create(
    content: str,
    platform: str,
    account_id: str = "",
    profile_id: str = "",
    is_draft: bool = False,
    publish_now: bool = False,
    schedule_minutes: int = 0,
    media_urls: str = "",
    title: str = "",
) -> str:
    client = _get_client()

    # Resolve the target account. _resolve_account raises ValueError with a
    # helpful candidate list when the user has multiple accounts and no
    # account_id was passed - we surface that string back to the LLM so it
    # can retry. Previously this silently picked accounts[0].
    try:
        account = _resolve_account(client, platform, account_id, profile_id)
    except ValueError as e:
        return f"❌ {e}"

    # Build request
    params: dict[str, Any] = {
        "content": content,
        "platforms": [
            {
                "platform": _platform_str(account.platform),
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
        return f"\u2705 Published to {platform} (@{username}){media_info}\nPost ID: {post_id}"
    else:
        scheduled = params["scheduled_for"].strftime("%Y-%m-%d %H:%M")
        return f"\u2705 Scheduled for {platform} (@{username}){media_info}\nPost ID: {post_id}\nScheduled: {scheduled}"


@tool_def("posts_publish_now")
def posts_publish_now(
    content: str,
    platform: str,
    account_id: str = "",
    profile_id: str = "",
    media_urls: str = "",
) -> str:
    return posts_create(
        content=content,
        platform=platform,
        account_id=account_id,
        profile_id=profile_id,
        publish_now=True,
        media_urls=media_urls,
    )


@tool_def("posts_cross_post")
def posts_cross_post(
    content: str,
    platforms: str,
    account_ids: str = "",
    profile_id: str = "",
    is_draft: bool = False,
    publish_now: bool = False,
    media_urls: str = "",
) -> str:
    client = _get_client()

    target_platforms = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    # account_ids is parallel to platforms (same order). Pad with empty strings
    # so positions without a specific ID fall back to profile/auto-resolution.
    ids = [i.strip() for i in account_ids.split(",")] if account_ids else []
    ids += [""] * max(0, len(target_platforms) - len(ids))

    platform_targets = []
    errors = []

    # Resolve each (platform, account_id) pair via the shared resolver so the
    # ambiguity / not-found behaviour matches posts_create exactly. Repeating
    # a platform with different account_ids is supported (e.g. agency posting
    # to two Twitter accounts in one cross_post call).
    # ids is padded to len(target_platforms) above, so strict=True is safe
    # and catches any future logic error that would silently truncate.
    for plat, acc_id in zip(target_platforms, ids, strict=True):
        try:
            acc = _resolve_account(client, plat, acc_id, profile_id)
            platform_targets.append(
                {
                    "platform": _platform_str(acc.platform),
                    "accountId": acc.field_id,
                }
            )
        except ValueError as e:
            errors.append(f"{plat}: {e}")

    if errors:
        return "❌ Could not resolve account(s):\n" + "\n".join(errors)

    if not platform_targets:
        return "❌ No platforms specified."

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
        result = f"\u2705 {'Published' if publish_now else 'Scheduled'} to: {', '.join(posted_to)}{media_info}\nPost ID: {post_id}"

    # not_found is no longer accumulated: resolution errors short-circuit
    # above. If we got here, every requested target was resolved.
    return result


@tool_def("posts_update")
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
        return "\u26a0\ufe0f No changes specified. Provide at least one field to update."

    response = client.posts.update(post_id, **params)
    post = response.post

    post_id_str = post.field_id if post else "N/A"
    status = post.status if post else "N/A"
    return f"\u2705 Post updated!\nID: {post_id_str}\nStatus: {status}"


@tool_def("posts_delete")
def posts_delete(post_id: str) -> str:
    client = _get_client()
    client.posts.delete(post_id)
    return f"\u2705 Post {post_id} deleted"


@tool_def("posts_retry")
def posts_retry(post_id: str) -> str:
    client = _get_client()

    try:
        post_response = client.posts.get(post_id)
        post = post_response.post
        if not post:
            return f"\u274c Post {post_id} not found"
        status_value = post.status.value if post.status else "unknown"
        if status_value != PostStatus.FAILED.value:
            return f"\u26a0\ufe0f Post {post_id} is not in failed status (current: {status_value})"
    except Exception as e:
        return f"\u274c Could not find post {post_id}: {e}"

    try:
        client.posts.retry(post_id)
        return f"\u2705 Post {post_id} has been queued for retry"
    except Exception as e:
        return f"\u274c Failed to retry post: {e}"


@tool_def("posts_list_failed")
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
        lines.append(f"- {content_preview}")
        lines.append(f"  Platforms: {platforms} | ID: {post.field_id}")
        # This view exists to show why posts failed, so it always carries an
        # error line even when no platform recorded a message.
        errors = _platform_errors(post) or ["Error: Unknown error"]
        lines.extend(f"  {error}" for error in errors)
        lines.append("")

    return "\n".join(lines)


@tool_def("posts_retry_all_failed")
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
            results.append(f"\u274c {post.field_id}: {e}")

    summary = f"\u2705 Retried {success_count} post(s)"
    if fail_count > 0:
        summary += f"\n\u274c Failed to retry {fail_count} post(s)"
        summary += "\n" + "\n".join(results)

    return summary


# ============================================================================
# MEDIA UPLOAD
# ============================================================================


@tool_def("media_generate_upload_link")
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
        return f"\u274c Failed to generate upload link: {e}"


@tool_def("media_check_upload_status")
def media_check_upload_status(token: str) -> str:
    client = _get_client()

    try:
        response = client.media.check_upload_token(token)

        status = response.status.value if response.status else "unknown"
        files = response.files or []

        if status == "pending":
            return f"""\u23f3 Upload pending

The user hasn't uploaded files yet. Please wait for them to complete the upload in their browser.

Token: {token}"""

        elif status == "expired":
            return """\u23f0 Upload link expired

The upload link has expired. Use media_generate_upload_link to create a new one."""

        elif status == "completed":
            if not files:
                return "\u2705 Upload completed but no files were found."

            lines = [f"\u2705 Upload completed! {len(files)} file(s) uploaded:\n"]
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
        return f"\u274c Failed to check upload status: {e}"


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


@tool_def("docs_search")
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
        return f"\u274c Failed to search documentation: {e}"


# ============================================================================
# AUTO-GENERATED TOOLS
# ============================================================================

# Import and register auto-generated tools from OpenAPI spec
# These complement the custom tools above with full API coverage
try:
    from .generated_tools import register_generated_tools
    register_generated_tools(mcp, _get_client)
except ImportError:
    # generated_tools.py not yet created - run scripts/generate_mcp_tools.py
    pass


# ============================================================================
# MAIN
# ============================================================================


def main() -> None:
    """Entry point for STDIO transport (Claude Desktop)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
