"""ChatGPT plugin surface of the Zernio MCP server.

A second FastMCP instance served at /chatgpt next to the full server at /mcp.
OpenAI reviews every tool it can see (hints, justification, response contents),
so this surface is a small, hand-shaped set of publishing and analytics tools
that call the REST API directly and return only the fields a user asked for.
Everything else (inbox, ads, queue, media upload) is added tool by tool after
the listing is approved: OpenAI's continuous review picks up new tools without
a resubmission.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_access_token
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent, ToolAnnotations
from pydantic import BaseModel, Field

from late.mcp.auth import build_auth_provider

API_BASE = (
    os.getenv("ZERNIO_BASE_URL")
    or os.getenv("LATE_BASE_URL")
    or "https://zernio.com/api"
).rstrip("/")
_TIMEOUT = 60.0
_DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
_VIDEO_EXT = (".mp4", ".mov", ".avi", ".webm", ".m4v")
# Everything this surface can do fits these four; ChatGPT asks the user to
# grant every scope the discovery document advertises.
CHATGPT_SCOPES = ["posts:read", "posts:write", "accounts:read", "analytics:read"]

PostStatus = Literal["draft", "scheduled", "published", "failed"]


# ---------------------------------------------------------------------------
# Output shapes. Every structured result is one of these models, so a tool can
# never leak a field that is not declared here (userId, timestamps, metadata).
# ---------------------------------------------------------------------------


class Profile(BaseModel):
    id: str = Field(description="Stable Zernio user id for the signed-in account")
    name: str | None = None
    email: str | None = None


class SocialAccount(BaseModel):
    id: str = Field(description="Account id to pass as account_id / account_ids")
    platform: str
    username: str | None = None
    display_name: str | None = None
    status: Literal["connected", "needs_reconnection", "disconnected"]
    profile_url: str | None = None


class SocialAccountList(BaseModel):
    accounts: list[SocialAccount]


class PostTarget(BaseModel):
    platform: str
    account_id: str | None = None
    username: str | None = None
    status: str | None = Field(
        default=None, description="pending, publishing, published or failed"
    )
    post_url: str | None = Field(default=None, description="Public URL once published")
    error: str | None = None


class Post(BaseModel):
    id: str
    status: str = Field(
        description="draft, scheduled, publishing, published, failed or partial"
    )
    content: str | None = None
    title: str | None = None
    scheduled_for: str | None = Field(default=None, description="ISO 8601, UTC")
    timezone: str | None = None
    published_at: str | None = None
    media_urls: list[str] = Field(default_factory=list)
    targets: list[PostTarget]


class PostList(BaseModel):
    posts: list[Post]
    total: int


class PostResult(BaseModel):
    post: Post


class CancelResult(BaseModel):
    post_id: str
    deleted: bool
    previous_status: str


class ValidationIssue(BaseModel):
    platform: str | None = None
    severity: Literal["error", "warning"]
    message: str


class ValidationResult(BaseModel):
    valid: bool
    issues: list[ValidationIssue]


class Metrics(BaseModel):
    impressions: int = 0
    reach: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    clicks: int = 0
    views: int = 0
    engagement_rate: float | None = None


class PlatformAnalytics(BaseModel):
    platform: str
    username: str | None = None
    status: str | None = None
    post_url: str | None = None
    sync_status: str | None = Field(
        default=None, description="synced, pending or unavailable"
    )
    metrics: Metrics | None = None


class PostAnalytics(BaseModel):
    post_id: str
    content: str | None = None
    status: str | None = None
    published_at: str | None = None
    sync_status: str | None = None
    message: str | None = Field(
        default=None, description="Explains pending or unavailable data"
    )
    metrics: Metrics
    platforms: list[PlatformAnalytics]


class DailyMetrics(BaseModel):
    date: str
    post_count: int
    metrics: Metrics


class PlatformTotals(BaseModel):
    platform: str
    post_count: int
    metrics: Metrics


class AccountAnalytics(BaseModel):
    from_date: str
    to_date: str
    days: list[DailyMetrics]
    platform_totals: list[PlatformTotals]


class BestTimeSlot(BaseModel):
    day: str
    hour_utc: int
    avg_engagement: float
    post_count: int


class BestTimes(BaseModel):
    slots: list[BestTimeSlot] = Field(description="Best slots first")
    based_on_posts: int


# ---------------------------------------------------------------------------
# API access
# ---------------------------------------------------------------------------


def _bearer() -> str:
    try:
        token = get_access_token()
    except Exception:
        token = None
    if token is not None and token.token:
        return token.token
    env = os.getenv("ZERNIO_API_KEY") or os.getenv("LATE_API_KEY")
    if env:
        return env
    raise ToolError("Sign in to Zernio to use this tool.")


def _error_message(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        body = {}
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        message = error.get("message") or error.get("code")
    else:
        message = error or (body.get("message") if isinstance(body, dict) else None)
    if not message:
        message = f"Zernio API returned HTTP {response.status_code}"
    return str(message)[:500]


async def _api(
    method: str, path: str, *, params: dict[str, Any] | None = None, json: Any = None
) -> Any:
    headers = {"Authorization": f"Bearer {_bearer()}", "Accept": "application/json"}
    async with httpx.AsyncClient(base_url=API_BASE, timeout=_TIMEOUT) as client:
        response = await client.request(
            method, path, params=params, json=json, headers=headers
        )
    if response.status_code >= 400:
        raise ToolError(_error_message(response))
    return response.json() if response.content else {}


def _result(model: BaseModel, summary: str) -> ToolResult:
    return ToolResult(
        content=[TextContent(type="text", text=summary)],
        structured_content=model.model_dump(mode="json", exclude_none=True),
    )


def _annotations(
    *, read_only: bool, destructive: bool, open_world: bool, idempotent: bool
) -> ToolAnnotations:
    return ToolAnnotations(
        readOnlyHint=read_only,
        destructiveHint=destructive,
        openWorldHint=open_world,
        idempotentHint=idempotent,
    )


def _meta(*scopes: str, **extra: Any) -> dict[str, Any]:
    return {"securitySchemes": [{"type": "oauth2", "scopes": list(scopes)}], **extra}


# ---------------------------------------------------------------------------
# Shaping
# ---------------------------------------------------------------------------


def _is_posting_account(account: dict[str, Any]) -> bool:
    platform = str(account.get("platform") or "")
    return (
        bool(platform)
        and not platform.endswith("ads")
        and account.get("enabled") is not False
    )


def _account_status(
    account: dict[str, Any],
) -> Literal["connected", "needs_reconnection", "disconnected"]:
    if account.get("needsReconnection"):
        return "needs_reconnection"
    return "connected" if account.get("isActive", True) else "disconnected"


def _shape_account(account: dict[str, Any]) -> SocialAccount:
    return SocialAccount(
        id=str(account["_id"]),
        platform=str(account.get("platform")),
        username=account.get("username") or None,
        display_name=account.get("displayName") or None,
        status=_account_status(account),
        profile_url=account.get("profileUrl") or None,
    )


async def _posting_accounts() -> list[dict[str, Any]]:
    data = await _api("GET", "/v1/accounts")
    return [a for a in data.get("accounts", []) if _is_posting_account(a)]


async def _resolve_targets(account_ids: list[str]) -> list[dict[str, str]]:
    """Map the user's chosen account ids to API platform targets, rejecting unknown ids."""
    if not account_ids:
        raise ToolError(
            "account_ids is required. Call list_social_accounts and pass the ids the user chose."
        )
    by_id = {str(a["_id"]): a for a in await _posting_accounts()}
    unknown = [i for i in account_ids if i not in by_id]
    if unknown:
        raise ToolError(
            f"Unknown account id(s): {', '.join(unknown)}. Call list_social_accounts for the current ids."
        )
    return [
        {"platform": str(by_id[i]["platform"]), "accountId": i} for i in account_ids
    ]


def _shape_post(post: dict[str, Any], usernames: dict[str, str]) -> Post:
    targets = []
    published_at: str | None = None
    for target in post.get("platforms") or []:
        # accountId comes back populated (a full account document) on some
        # reads and as a plain id on others.
        raw_account = target.get("accountId")
        account_id = (
            str(raw_account.get("_id"))
            if isinstance(raw_account, dict)
            else (str(raw_account) if raw_account else None)
        )
        username = usernames.get(account_id or "") or (
            raw_account.get("username") if isinstance(raw_account, dict) else None
        )
        targets.append(
            PostTarget(
                platform=str(target.get("platform")),
                account_id=account_id,
                username=username or None,
                status=target.get("status") or None,
                post_url=target.get("platformPostUrl") or None,
                error=target.get("errorMessage") or None,
            )
        )
        if target.get("publishedAt") and (
            published_at is None or target["publishedAt"] > published_at
        ):
            published_at = target["publishedAt"]
    return Post(
        id=str(post["_id"]),
        status=str(post.get("status") or "unknown"),
        content=post.get("content") or None,
        title=post.get("title") or None,
        scheduled_for=post.get("scheduledFor") or None,
        timezone=post.get("timezone") or None,
        published_at=published_at,
        media_urls=[m["url"] for m in post.get("mediaItems") or [] if m.get("url")],
        targets=targets,
    )


async def _usernames() -> dict[str, str]:
    return {
        str(a["_id"]): a.get("username") or a.get("displayName") or ""
        for a in await _posting_accounts()
    }


def _media_items(media_urls: list[str] | None) -> list[dict[str, str]]:
    items = []
    for url in media_urls or []:
        lower = url.lower().split("?")[0]
        if lower.endswith(_VIDEO_EXT):
            media_type = "video"
        elif lower.endswith(".gif"):
            media_type = "gif"
        elif lower.endswith(".pdf"):
            media_type = "document"
        else:
            media_type = "image"
        items.append({"type": media_type, "url": url})
    return items


def _schedule_fields(scheduled_for: str, tz: str | None) -> dict[str, str]:
    """Turn the model's ISO 8601 time into the API's scheduledFor + timezone pair.

    A time with a UTC offset is normalised to UTC. A naive time needs the
    user's IANA timezone, otherwise the post would silently land on the
    server's clock.
    """
    try:
        parsed = datetime.fromisoformat(scheduled_for.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ToolError(
            f"scheduled_for must be ISO 8601, for example 2026-10-01T09:00:00+02:00: {exc}"
        ) from exc
    if parsed.tzinfo is not None:
        parsed_utc = parsed.astimezone(timezone.utc)
        if parsed_utc <= datetime.now(timezone.utc):
            raise ToolError(
                "scheduled_for is in the past. Use publish_post_now to publish immediately."
            )
        return {
            "scheduledFor": parsed_utc.isoformat().replace("+00:00", "Z"),
            "timezone": "UTC",
        }
    if not tz:
        raise ToolError(
            "scheduled_for has no UTC offset. Add the offset (2026-10-01T09:00:00+02:00) or pass the "
            "user's IANA timezone, for example Europe/Madrid."
        )
    return {"scheduledFor": parsed.isoformat(), "timezone": tz}


def _shape_metrics(raw: dict[str, Any] | None) -> Metrics:
    raw = raw or {}
    return Metrics(
        impressions=int(raw.get("impressions") or 0),
        reach=int(raw.get("reach") or 0),
        likes=int(raw.get("likes") or 0),
        comments=int(raw.get("comments") or 0),
        shares=int(raw.get("shares") or 0),
        saves=int(raw.get("saves") or 0),
        clicks=int(raw.get("clicks") or 0),
        views=int(raw.get("views") or 0),
        engagement_rate=raw.get("engagementRate"),
    )


def _describe_post(post: Post, verb: str) -> str:
    where = ", ".join(
        f"{t.platform}{' @' + t.username if t.username else ''}" for t in post.targets
    )
    when = (
        f" for {post.scheduled_for}"
        if post.scheduled_for and post.status == "scheduled"
        else ""
    )
    urls = [t.post_url for t in post.targets if t.post_url]
    tail = f" Links: {', '.join(urls)}" if urls else ""
    return f"{verb} post {post.id} ({post.status}) to {where}{when}.{tail}"


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

INSTRUCTIONS = (
    "Zernio schedules and publishes posts to the user's own connected social media accounts and "
    "reports how those posts perform. Every tool acts only inside the signed-in user's Zernio "
    "workspace. Before creating a post, call list_social_accounts and pass the exact account_ids "
    "the user chose; if it is unclear which account they mean, ask. publish_post_now makes content "
    "public right away, so confirm the final text with the user before calling it. Times are ISO "
    "8601; when a time has no UTC offset, pass the user's IANA timezone. When the user asks whether "
    "a text or media can go out on a platform, or whether it fits, call validate_post and report "
    "its result rather than answering from general knowledge: platform rules (required media, "
    "titles, character limits) are enforced by Zernio, not guessed."
)

chatgpt_mcp = FastMCP(
    "Zernio",
    instructions=INSTRUCTIONS,
    version="1.0.0",
    website_url="https://zernio.com",
    auth=build_auth_provider(scopes=CHATGPT_SCOPES),
)


@chatgpt_mcp.tool(
    name="get_profile",
    title="Get signed-in Zernio profile",
    description=(
        "Use this to identify which Zernio account is connected, for example when the user has "
        "several Zernio accounts or asks who they are signed in as. Returns the stable account id "
        "plus name and email when available. Do not use it to look up other people."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("accounts:read", **{"openai/profile": True}),
    output_schema=Profile.model_json_schema(),
)
async def get_profile() -> ToolResult:
    data = await _api("GET", "/v1/auth/verify")
    profile = Profile(
        id=str(data["userId"]),
        name=data.get("name") or None,
        email=data.get("email") or None,
    )
    who = profile.email or profile.name or profile.id
    return _result(profile, f"Signed in to Zernio as {who}.")


@chatgpt_mcp.tool(
    name="list_social_accounts",
    title="List connected social accounts",
    description=(
        "Use this when the user wants to see which social media accounts are connected to Zernio, "
        "or before scheduling or publishing so you can pass the right account_ids. Returns each "
        "account's id, platform, username and connection status. Optionally filter by platform "
        "(instagram, tiktok, youtube, twitter, linkedin, facebook, threads, pinterest, reddit, "
        "bluesky, googlebusiness, telegram, snapchat, discord, slack)."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("accounts:read"),
    output_schema=SocialAccountList.model_json_schema(),
)
async def list_social_accounts(
    platform: str | None = Field(
        default=None, description="Only return accounts on this platform"
    ),
) -> ToolResult:
    accounts = [_shape_account(a) for a in await _posting_accounts()]
    if platform:
        accounts = [a for a in accounts if a.platform == platform.lower()]
    listing = SocialAccountList(accounts=accounts)
    if not accounts:
        return _result(
            listing,
            "No connected social accounts match. Accounts are connected at zernio.com.",
        )
    lines = [
        f"- {a.platform} @{a.username or a.display_name or a.id} ({a.status}, id {a.id})"
        for a in accounts
    ]
    return _result(
        listing, f"{len(accounts)} connected account(s):\n" + "\n".join(lines)
    )


@chatgpt_mcp.tool(
    name="list_posts",
    title="List posts",
    description=(
        "Use this when the user wants to review their scheduled, draft, published or failed posts, "
        "for example 'what is scheduled this week' or 'which posts failed'. Returns each post's id, "
        "status, text, scheduled time and per-platform status. Newest first. For one post's full "
        "details use get_post; for performance numbers use get_post_analytics."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("posts:read"),
    output_schema=PostList.model_json_schema(),
)
async def list_posts(
    status: PostStatus | None = Field(
        default=None, description="Only posts in this status"
    ),
    account_id: str | None = Field(
        default=None, description="Only posts targeting this social account"
    ),
    limit: int = Field(default=20, ge=1, le=50, description="Maximum posts to return"),
) -> ToolResult:
    params: dict[str, Any] = {"limit": limit, "page": 1, "sortBy": "scheduled-desc"}
    if status:
        params["status"] = status
    if account_id:
        params["accountId"] = account_id
    data = await _api("GET", "/v1/posts", params=params)
    usernames = await _usernames()
    posts = [_shape_post(p, usernames) for p in data.get("posts", [])]
    total = int((data.get("pagination") or {}).get("total") or len(posts))
    listing = PostList(posts=posts, total=total)
    if not posts:
        return _result(listing, f"No {status or ''} posts found.".replace("  ", " "))
    lines = [
        f"- {p.id} [{p.status}] {(p.content or p.title or '')[:80]!r}"
        + (f" scheduled {p.scheduled_for}" if p.scheduled_for else "")
        + " -> "
        + ", ".join(t.platform for t in p.targets)
        for p in posts
    ]
    return _result(listing, f"{len(posts)} of {total} post(s):\n" + "\n".join(lines))


@chatgpt_mcp.tool(
    name="get_post",
    title="Get post details",
    description=(
        "Use this when the user asks about one specific post: its full text, media, schedule, "
        "per-platform status, public links or failure reason. Requires the post id from list_posts "
        "or from an earlier create result."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("posts:read"),
    output_schema=PostResult.model_json_schema(),
)
async def get_post(post_id: str = Field(description="Zernio post id")) -> ToolResult:
    data = await _api("GET", f"/v1/posts/{post_id}")
    post = _shape_post(data["post"], await _usernames())
    return _result(PostResult(post=post), _describe_post(post, "Found"))


@chatgpt_mcp.tool(
    name="validate_post",
    title="Check a post against platform rules",
    description=(
        "Use this whenever the user asks whether a text or media can go out, fits, or is allowed on "
        "a chosen platform, for example character limits or required media, and before scheduling "
        "when in doubt. Use it instead of answering from general knowledge: the rules are enforced "
        "by Zernio. Nothing is created. Returns valid true/false plus each error or warning with "
        "the platform it applies to."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("posts:read", "accounts:read"),
    output_schema=ValidationResult.model_json_schema(),
)
async def validate_post(
    content: str = Field(description="Post text to check"),
    account_ids: list[str] = Field(
        description="Target social account ids from list_social_accounts"
    ),
    media_urls: list[str] | None = Field(
        default=None, description="Public image, video or PDF URLs to attach"
    ),
) -> ToolResult:
    body: dict[str, Any] = {
        "content": content,
        "platforms": await _resolve_targets(account_ids),
    }
    items = _media_items(media_urls)
    if items:
        body["mediaItems"] = items
    data = await _api("POST", "/v1/tools/validate/post", json=body)
    issues = [
        ValidationIssue(
            platform=e.get("platform"),
            severity="error",
            message=str(e.get("error") or e),
        )
        for e in data.get("errors") or []
    ] + [
        ValidationIssue(
            platform=w.get("platform"),
            severity="warning",
            message=str(w.get("warning") or w),
        )
        for w in data.get("warnings") or []
    ]
    result = ValidationResult(valid=bool(data.get("valid")), issues=issues)
    if not issues:
        return _result(result, "The post passes every platform check.")
    lines = [
        f"- {i.severity}{' (' + i.platform + ')' if i.platform else ''}: {i.message}"
        for i in issues
    ]
    return _result(
        result,
        ("Valid with warnings:\n" if result.valid else "Not valid:\n")
        + "\n".join(lines),
    )


@chatgpt_mcp.tool(
    name="schedule_post",
    title="Schedule a post",
    description=(
        "Use this when the user wants a post published later at a specific time on one or more of "
        "their connected accounts. The post stays editable and cancellable until that time. "
        "Requires the text, the account_ids from list_social_accounts and the time. Media is "
        "attached from public URLs. For publishing right now use publish_post_now instead; for a "
        "text-only check use validate_post."
    ),
    annotations=_annotations(
        read_only=False, destructive=False, open_world=True, idempotent=False
    ),
    meta=_meta("posts:write", "accounts:read"),
    output_schema=PostResult.model_json_schema(),
)
async def schedule_post(
    content: str = Field(
        description="Post text. Platform limits apply, for example 280 characters on X"
    ),
    account_ids: list[str] = Field(
        description="Target social account ids from list_social_accounts"
    ),
    scheduled_for: str = Field(
        description="When to publish, ISO 8601 such as 2026-10-01T09:00:00+02:00"
    ),
    timezone: str | None = Field(
        default=None,
        description="IANA timezone, needed only when scheduled_for has no UTC offset",
    ),
    media_urls: list[str] | None = Field(
        default=None, description="Public image, video or PDF URLs to attach"
    ),
    title: str | None = Field(
        default=None, description="Title for YouTube or Pinterest"
    ),
) -> ToolResult:
    body: dict[str, Any] = {
        "content": content,
        "platforms": await _resolve_targets(account_ids),
        **_schedule_fields(scheduled_for, timezone),
    }
    items = _media_items(media_urls)
    if items:
        body["mediaItems"] = items
    if title:
        body["title"] = title
    data = await _api("POST", "/v1/posts", json=body)
    post = _shape_post(data["post"], await _usernames())
    return _result(PostResult(post=post), _describe_post(post, "Scheduled"))


@chatgpt_mcp.tool(
    name="publish_post_now",
    title="Publish a post immediately",
    description=(
        "Use this only when the user explicitly wants the post live right now on one or more of "
        "their connected accounts. The content becomes public on those platforms immediately and "
        "this cannot be undone from ChatGPT, so confirm the final text and accounts with the user "
        "first. Calling it twice publishes twice. Returns the post with its public links. To "
        "publish later use schedule_post."
    ),
    annotations=_annotations(
        read_only=False, destructive=True, open_world=True, idempotent=False
    ),
    meta=_meta("posts:write", "accounts:read"),
    output_schema=PostResult.model_json_schema(),
)
async def publish_post_now(
    content: str = Field(
        description="Post text. Platform limits apply, for example 280 characters on X"
    ),
    account_ids: list[str] = Field(
        description="Target social account ids from list_social_accounts"
    ),
    media_urls: list[str] | None = Field(
        default=None, description="Public image, video or PDF URLs to attach"
    ),
    title: str | None = Field(
        default=None, description="Title for YouTube or Pinterest"
    ),
) -> ToolResult:
    body: dict[str, Any] = {
        "content": content,
        "platforms": await _resolve_targets(account_ids),
        "publishNow": True,
    }
    items = _media_items(media_urls)
    if items:
        body["mediaItems"] = items
    if title:
        body["title"] = title
    data = await _api("POST", "/v1/posts", json=body)
    post = _shape_post(data["post"], await _usernames())
    return _result(PostResult(post=post), _describe_post(post, "Published"))


async def _unpublished_post(post_id: str, action: str) -> dict[str, Any]:
    data = await _api("GET", f"/v1/posts/{post_id}")
    post = data["post"]
    if post.get("status") in ("published", "publishing", "partial"):
        raise ToolError(
            f"Post {post_id} is {post['status']} and cannot be {action} from ChatGPT. "
            "Only draft, scheduled and failed posts can be changed."
        )
    return post


@chatgpt_mcp.tool(
    name="update_scheduled_post",
    title="Edit a scheduled post",
    description=(
        "Use this when the user wants to change the text, media, title or publish time of a post "
        "that has not been published yet (draft, scheduled or failed). Only the fields given are "
        "changed; new media_urls replace the existing media. Published posts cannot be edited here. "
        "Requires the post id from list_posts."
    ),
    annotations=_annotations(
        read_only=False, destructive=True, open_world=False, idempotent=True
    ),
    meta=_meta("posts:write"),
    output_schema=PostResult.model_json_schema(),
)
async def update_scheduled_post(
    post_id: str = Field(description="Zernio post id"),
    content: str | None = Field(default=None, description="New post text"),
    scheduled_for: str | None = Field(
        default=None, description="New publish time, ISO 8601"
    ),
    timezone: str | None = Field(
        default=None,
        description="IANA timezone, needed only when scheduled_for has no UTC offset",
    ),
    media_urls: list[str] | None = Field(
        default=None, description="Replacement media URLs; an empty list removes media"
    ),
    title: str | None = Field(
        default=None, description="New title for YouTube or Pinterest"
    ),
) -> ToolResult:
    await _unpublished_post(post_id, "edited")
    body: dict[str, Any] = {}
    if content is not None:
        body["content"] = content
    if scheduled_for is not None:
        body.update(_schedule_fields(scheduled_for, timezone))
    if media_urls is not None:
        body["mediaItems"] = _media_items(media_urls)
    if title is not None:
        body["title"] = title
    if not body:
        raise ToolError(
            "Nothing to change: pass content, scheduled_for, media_urls or title."
        )
    data = await _api("PUT", f"/v1/posts/{post_id}", json=body)
    post = _shape_post(data["post"], await _usernames())
    return _result(PostResult(post=post), _describe_post(post, "Updated"))


@chatgpt_mcp.tool(
    name="cancel_scheduled_post",
    title="Cancel a scheduled post",
    description=(
        "Use this when the user wants to delete a draft, scheduled or failed post so it will not "
        "be published. This removes the post from Zernio and cannot be undone. Posts that are "
        "already published are left untouched and this tool reports that. Requires the post id "
        "from list_posts."
    ),
    annotations=_annotations(
        read_only=False, destructive=True, open_world=False, idempotent=True
    ),
    meta=_meta("posts:write"),
    output_schema=CancelResult.model_json_schema(),
)
async def cancel_scheduled_post(
    post_id: str = Field(description="Zernio post id"),
) -> ToolResult:
    post = await _unpublished_post(post_id, "deleted")
    await _api("DELETE", f"/v1/posts/{post_id}")
    result = CancelResult(
        post_id=post_id, deleted=True, previous_status=str(post.get("status"))
    )
    return _result(
        result,
        f"Deleted post {post_id} (was {result.previous_status}). It will not be published.",
    )


@chatgpt_mcp.tool(
    name="retry_failed_post",
    title="Retry a failed post",
    description=(
        "Use this when a post shows status failed and the user wants Zernio to try publishing it "
        "again on the platforms that failed. This publishes the same content publicly on retry, so "
        "confirm with the user first. Requires the post id from list_posts. Read the failure reason "
        "with get_post before retrying; a reconnect or content fix may be needed first."
    ),
    annotations=_annotations(
        read_only=False, destructive=True, open_world=True, idempotent=False
    ),
    meta=_meta("posts:write"),
    output_schema=PostResult.model_json_schema(),
)
async def retry_failed_post(
    post_id: str = Field(description="Zernio post id of a failed post"),
) -> ToolResult:
    data = await _api("POST", f"/v1/posts/{post_id}/retry")
    post = _shape_post(data["post"], await _usernames())
    return _result(PostResult(post=post), _describe_post(post, "Retried"))


@chatgpt_mcp.tool(
    name="get_post_analytics",
    title="Get analytics for one post",
    description=(
        "Use this when the user asks how a specific published post performed: impressions, reach, "
        "likes, comments, shares, saves, clicks, views and engagement rate, per platform. Numbers "
        "sync from the platforms periodically, so a just-published post may report pending data. "
        "Requires the post id from list_posts."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("analytics:read"),
    output_schema=PostAnalytics.model_json_schema(),
)
async def get_post_analytics(
    post_id: str = Field(description="Zernio post id of a published post"),
) -> ToolResult:
    data = await _api("GET", "/v1/analytics", params={"postId": post_id})
    platforms = [
        PlatformAnalytics(
            platform=str(p.get("platform")),
            username=p.get("accountUsername") or None,
            status=p.get("status") or None,
            post_url=p.get("platformPostUrl") or None,
            sync_status=p.get("syncStatus") or None,
            metrics=_shape_metrics(p.get("analytics")) if p.get("analytics") else None,
        )
        for p in data.get("platformAnalytics") or []
    ]
    analytics = PostAnalytics(
        post_id=str(data.get("latePostId") or data.get("postId") or post_id),
        content=data.get("content") or None,
        status=data.get("status") or None,
        published_at=data.get("publishedAt") or None,
        sync_status=data.get("syncStatus") or None,
        message=data.get("message") or None,
        metrics=_shape_metrics(data.get("analytics")),
        platforms=platforms,
    )
    m = analytics.metrics
    summary = (
        f"Post {analytics.post_id}: {m.impressions} impressions, {m.likes} likes, {m.comments} comments, "
        f"{m.shares} shares, {m.views} views"
        + (
            f", engagement rate {m.engagement_rate}%"
            if m.engagement_rate is not None
            else ""
        )
        + (f". {analytics.message}" if analytics.message else ".")
    )
    return _result(analytics, summary)


@chatgpt_mcp.tool(
    name="get_account_analytics",
    title="Get daily analytics across accounts",
    description=(
        "Use this when the user asks how their accounts or platforms performed over a period, for "
        "example 'how did Instagram do last month'. Returns daily totals (impressions, reach, likes, "
        "comments, shares, saves, clicks, views) and per-platform totals for the date range, "
        "defaulting to the last 30 days. Filter by account_id or platform. For a single post use "
        "get_post_analytics."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("analytics:read"),
    output_schema=AccountAnalytics.model_json_schema(),
)
async def get_account_analytics(
    account_id: str | None = Field(
        default=None, description="Only this social account"
    ),
    platform: str | None = Field(
        default=None, description="Only this platform, for example instagram"
    ),
    from_date: str | None = Field(
        default=None, description="Start date YYYY-MM-DD, default 30 days ago"
    ),
    to_date: str | None = Field(
        default=None, description="End date YYYY-MM-DD, default today"
    ),
) -> ToolResult:
    today = datetime.now(timezone.utc).date()
    start = from_date or (today - timedelta(days=30)).isoformat()
    end = to_date or today.isoformat()
    params: dict[str, Any] = {"fromDate": start, "toDate": end}
    if account_id:
        params["accountId"] = account_id
    if platform:
        params["platform"] = platform.lower()
    data = await _api("GET", "/v1/analytics/daily-metrics", params=params)
    days = [
        DailyMetrics(
            date=str(d.get("date")),
            post_count=int(d.get("postCount") or 0),
            metrics=_shape_metrics(d.get("metrics")),
        )
        for d in data.get("dailyData") or []
    ]
    totals = [
        PlatformTotals(
            platform=str(p.get("platform")),
            post_count=int(p.get("postCount") or 0),
            metrics=_shape_metrics(p),
        )
        for p in data.get("platformBreakdown") or []
    ]
    analytics = AccountAnalytics(
        from_date=start, to_date=end, days=days, platform_totals=totals
    )
    if not totals:
        return _result(analytics, f"No analytics between {start} and {end}.")
    lines = [
        f"- {t.platform}: {t.post_count} posts, {t.metrics.impressions} impressions, {t.metrics.likes} likes, "
        f"{t.metrics.comments} comments"
        for t in totals
    ]
    return _result(analytics, f"Totals {start} to {end}:\n" + "\n".join(lines))


@chatgpt_mcp.tool(
    name="get_best_time_to_post",
    title="Get best times to post",
    description=(
        "Use this when the user asks when they should post for the most engagement. Computed from "
        "the engagement history of the user's own published posts, as weekday and hour in UTC, best "
        "first. Filter by account_id or platform. Returns nothing useful until the account has "
        "published posts with synced analytics."
    ),
    annotations=_annotations(
        read_only=True, destructive=False, open_world=False, idempotent=True
    ),
    meta=_meta("analytics:read"),
    output_schema=BestTimes.model_json_schema(),
)
async def get_best_time_to_post(
    account_id: str | None = Field(
        default=None, description="Only this social account"
    ),
    platform: str | None = Field(
        default=None, description="Only this platform, for example instagram"
    ),
) -> ToolResult:
    params: dict[str, Any] = {}
    if account_id:
        params["accountId"] = account_id
    if platform:
        params["platform"] = platform.lower()
    data = await _api("GET", "/v1/analytics/best-time", params=params)
    raw_slots = sorted(
        data.get("slots") or [],
        key=lambda s: float(s.get("avg_engagement") or 0),
        reverse=True,
    )
    slots = [
        BestTimeSlot(
            day=_DAY_NAMES[int(s.get("day_of_week") or 0) % 7],
            hour_utc=int(s.get("hour") or 0),
            avg_engagement=round(float(s.get("avg_engagement") or 0), 2),
            post_count=int(s.get("post_count") or 0),
        )
        for s in raw_slots[:10]
    ]
    best = BestTimes(
        slots=slots,
        based_on_posts=sum(int(s.get("post_count") or 0) for s in raw_slots),
    )
    if not slots:
        return _result(
            best, "Not enough published posts with analytics to suggest a time yet."
        )
    lines = [
        f"- {s.day} {s.hour_utc:02d}:00 UTC (avg engagement {s.avg_engagement}, {s.post_count} posts)"
        for s in slots[:5]
    ]
    return _result(best, "Best times to post (UTC):\n" + "\n".join(lines))
