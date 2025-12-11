"""
Posts resource for managing social media posts.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from .base import BaseResource

if TYPE_CHECKING:
    from ..client.base import BaseClient


# Type aliases for better readability
Platform = Literal[
    "twitter",
    "instagram",
    "facebook",
    "linkedin",
    "tiktok",
    "youtube",
    "pinterest",
    "reddit",
    "bluesky",
    "threads",
    "googlebusiness",
]
PostStatus = Literal["draft", "scheduled", "publishing", "published", "failed", "partial"]


class PostsResource(BaseResource[Any]):
    """
    Resource for managing posts.

    Example:
        >>> client = Late(api_key="...")
        >>> # List posts
        >>> posts = client.posts.list(status="scheduled")
        >>> # Create a post
        >>> post = client.posts.create(
        ...     content="Hello!",
        ...     platforms=[{"platform": "twitter", "accountId": "..."}],
        ...     scheduled_for=datetime.now() + timedelta(hours=1),
        ... )
        >>> # Update a post
        >>> client.posts.update(post_id, content="Updated!")
        >>> # Delete a post
        >>> client.posts.delete(post_id)
    """

    _BASE_PATH = "/v1/posts"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def list(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        status: PostStatus | None = None,
        platform: Platform | None = None,
        profile_id: str | None = None,
        created_by: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        include_hidden: bool | None = None,
    ) -> dict[str, Any]:
        """
        List posts with optional filters.

        Args:
            page: Page number (1-based)
            limit: Number of posts per page (max 100)
            status: Filter by post status (draft, scheduled, published, failed)
            platform: Filter by platform
            profile_id: Filter by profile ID
            created_by: Filter by creator user ID
            date_from: Filter posts from this date (YYYY-MM-DD)
            date_to: Filter posts until this date (YYYY-MM-DD)
            include_hidden: Include hidden posts (default: False)

        Returns:
            Dict with 'posts' and 'pagination' keys
        """
        params = self._build_params(
            page=page,
            limit=limit,
            status=status,
            platform=platform,
            profile_id=profile_id,
            created_by=created_by,
            date_from=date_from,
            date_to=date_to,
            include_hidden=include_hidden,
        )
        return self._client._get(self._BASE_PATH, params=params)

    def get(self, post_id: str) -> dict[str, Any]:
        """
        Get a single post by ID.

        Args:
            post_id: The post ID

        Returns:
            Dict with 'post' key containing the Post object
        """
        return self._client._get(self._path(post_id))

    def create(
        self,
        *,
        content: str,
        platforms: list[dict[str, Any]],
        title: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        scheduled_for: datetime | str | None = None,
        publish_now: bool = False,
        is_draft: bool = False,
        timezone: str = "UTC",
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        crossposting_enabled: bool = True,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        queued_from_profile: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new post.

        Args:
            content: Post content/text
            platforms: List of platform targets, each with 'platform' and 'accountId'.
                       Can include 'customContent', 'customMedia', 'scheduledFor',
                       and 'platformSpecificData' for per-platform overrides.
            title: Optional title (used by YouTube, Pinterest)
            media_items: Optional list of media items with 'type' and 'url'
            scheduled_for: When to publish (datetime or ISO string)
            publish_now: If True, publish immediately (default: False)
            is_draft: If True, save as draft (default: False)
            timezone: Timezone for scheduled_for (default: UTC)
            tags: Optional tags (for YouTube: max 100 chars each, 500 total)
            hashtags: Optional hashtags
            mentions: Optional mentions
            crossposting_enabled: Enable crossposting (default: True)
            metadata: Optional custom metadata
            tiktok_settings: TikTok-specific settings (required for TikTok posts)
            queued_from_profile: Profile ID if creating via queue

        Returns:
            Dict with 'message' and 'post' keys
        """
        payload = self._build_payload(
            content=content,
            platforms=platforms,
            title=title,
            media_items=media_items,
            scheduled_for=scheduled_for,
            publish_now=publish_now if publish_now else None,
            is_draft=is_draft if is_draft else None,
            timezone=timezone,
            tags=tags,
            hashtags=hashtags,
            mentions=mentions,
            crossposting_enabled=crossposting_enabled if not crossposting_enabled else None,
            metadata=metadata,
            tiktok_settings=tiktok_settings,
            queued_from_profile=queued_from_profile,
        )
        return self._client._post(self._BASE_PATH, data=payload)

    def update(
        self,
        post_id: str,
        *,
        content: str | None = None,
        title: str | None = None,
        platforms: list[dict[str, Any]] | None = None,
        media_items: list[dict[str, Any]] | None = None,
        scheduled_for: datetime | str | None = None,
        timezone: str | None = None,
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Update an existing post.

        Only draft, scheduled, failed, and partial posts can be edited.
        Published, publishing, and cancelled posts cannot be modified.

        Args:
            post_id: ID of the post to update
            content: New post content
            title: New title
            platforms: New platform targets
            media_items: New media items
            scheduled_for: New scheduled time
            timezone: New timezone
            tags: New tags
            hashtags: New hashtags
            mentions: New mentions
            metadata: New metadata
            tiktok_settings: New TikTok settings

        Returns:
            Dict with 'message' and 'post' keys
        """
        payload = self._build_payload(
            content=content,
            title=title,
            platforms=platforms,
            media_items=media_items,
            scheduled_for=scheduled_for,
            timezone=timezone,
            tags=tags,
            hashtags=hashtags,
            mentions=mentions,
            metadata=metadata,
            tiktok_settings=tiktok_settings,
        )
        return self._client._put(self._path(post_id), data=payload)

    def delete(self, post_id: str) -> dict[str, Any]:
        """
        Delete a post.

        Published posts cannot be deleted.
        When deleting a scheduled or draft post that consumed upload quota,
        the quota will be automatically refunded.

        Args:
            post_id: ID of the post to delete

        Returns:
            Dict with 'message' key
        """
        return self._client._delete(self._path(post_id))

    def retry(self, post_id: str) -> dict[str, Any]:
        """
        Retry a failed post.

        Args:
            post_id: ID of the failed post

        Returns:
            Dict with 'message' and 'post' keys
        """
        return self._client._post(self._path(post_id, "retry"))

    def bulk_upload(
        self,
        file_path: str | Path,
        *,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """
        Bulk upload posts from a CSV file.

        Args:
            file_path: Path to the CSV file
            dry_run: If True, validate without creating posts

        Returns:
            Dict with 'success', 'totalRows', 'created', 'failed', 'errors', 'posts'
        """
        path = Path(file_path)
        params = {"dryRun": "true"} if dry_run else None
        with open(path, "rb") as f:
            return self._client._post(
                self._path("bulk-upload"),
                files={"file": (path.name, f, "text/csv")},
                params=params,
            )

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        status: PostStatus | None = None,
        platform: Platform | None = None,
        profile_id: str | None = None,
        created_by: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        include_hidden: bool | None = None,
    ) -> dict[str, Any]:
        """List posts asynchronously."""
        params = self._build_params(
            page=page,
            limit=limit,
            status=status,
            platform=platform,
            profile_id=profile_id,
            created_by=created_by,
            date_from=date_from,
            date_to=date_to,
            include_hidden=include_hidden,
        )
        return await self._client._aget(self._BASE_PATH, params=params)

    async def aget(self, post_id: str) -> dict[str, Any]:
        """Get a post asynchronously."""
        return await self._client._aget(self._path(post_id))

    async def acreate(
        self,
        *,
        content: str,
        platforms: list[dict[str, Any]],
        title: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        scheduled_for: datetime | str | None = None,
        publish_now: bool = False,
        is_draft: bool = False,
        timezone: str = "UTC",
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        crossposting_enabled: bool = True,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        queued_from_profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a post asynchronously."""
        payload = self._build_payload(
            content=content,
            platforms=platforms,
            title=title,
            media_items=media_items,
            scheduled_for=scheduled_for,
            publish_now=publish_now if publish_now else None,
            is_draft=is_draft if is_draft else None,
            timezone=timezone,
            tags=tags,
            hashtags=hashtags,
            mentions=mentions,
            crossposting_enabled=crossposting_enabled if not crossposting_enabled else None,
            metadata=metadata,
            tiktok_settings=tiktok_settings,
            queued_from_profile=queued_from_profile,
        )
        return await self._client._apost(self._BASE_PATH, data=payload)

    async def aupdate(
        self,
        post_id: str,
        *,
        content: str | None = None,
        title: str | None = None,
        platforms: list[dict[str, Any]] | None = None,
        media_items: list[dict[str, Any]] | None = None,
        scheduled_for: datetime | str | None = None,
        timezone: str | None = None,
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a post asynchronously."""
        payload = self._build_payload(
            content=content,
            title=title,
            platforms=platforms,
            media_items=media_items,
            scheduled_for=scheduled_for,
            timezone=timezone,
            tags=tags,
            hashtags=hashtags,
            mentions=mentions,
            metadata=metadata,
            tiktok_settings=tiktok_settings,
        )
        return await self._client._aput(self._path(post_id), data=payload)

    async def adelete(self, post_id: str) -> dict[str, Any]:
        """Delete a post asynchronously."""
        return await self._client._adelete(self._path(post_id))

    async def aretry(self, post_id: str) -> dict[str, Any]:
        """Retry a failed post asynchronously."""
        return await self._client._apost(self._path(post_id, "retry"))
