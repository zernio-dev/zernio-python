"""
Pipeline for cross-posting content across multiple platforms.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client.late_client import Late


@dataclass
class PlatformConfig:
    """Configuration for a single platform."""

    platform: str
    account_id: str
    custom_content: str | None = None
    delay_minutes: int = 0


@dataclass
class CrossPostResult:
    """Result of cross-posting to a single platform."""

    platform: str
    success: bool
    post_id: str | None = None
    error: str | None = None


class CrossPosterPipeline:
    """
    Pipeline for cross-posting content across multiple platforms.

    Features:
    - Automatic content adaptation per platform character limits
    - Staggered posting to avoid rate limits
    - Platform-specific customizations

    Example:
        >>> client = Late(api_key="...")
        >>> cross_poster = CrossPosterPipeline(client)
        >>>
        >>> results = await cross_poster.post(
        ...     content="Exciting news! Our new feature is live.",
        ...     platforms=[
        ...         PlatformConfig("twitter", "tw_123"),
        ...         PlatformConfig("linkedin", "li_456"),
        ...         PlatformConfig("instagram", "ig_789"),
        ...     ],
        ... )
    """

    CHAR_LIMITS = {
        "twitter": 280,
        "threads": 500,
        "linkedin": 3000,
        "instagram": 2200,
        "facebook": 63206,
        "tiktok": 2200,
        "bluesky": 300,
    }

    def __init__(
        self,
        client: Late,
        *,
        default_stagger: int = 5,  # minutes between posts
    ) -> None:
        self._client = client
        self.default_stagger = default_stagger

    def _adapt_content(self, content: str, platform: str) -> str:
        """Adapt content to platform character limit."""
        limit = self.CHAR_LIMITS.get(platform, 5000)
        if len(content) <= limit:
            return content
        return content[: limit - 3] + "..."

    async def post(
        self,
        content: str,
        platforms: list[PlatformConfig],
        *,
        title: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        tags: list[str] | None = None,
        base_time: datetime | None = None,
        adapt_content: bool = True,
    ) -> list[CrossPostResult]:
        """
        Cross-post content to multiple platforms.

        Args:
            content: Base content to post
            platforms: List of platform configurations
            title: Optional title
            media_items: Optional media items
            tags: Optional tags
            base_time: Base scheduled time (None for now)
            adapt_content: Adapt content per platform limits

        Returns:
            List of results per platform
        """
        results: list[CrossPostResult] = []
        current_time = base_time or datetime.now()

        for i, config in enumerate(platforms):
            try:
                # Calculate scheduled time
                delay = config.delay_minutes or (i * self.default_stagger)
                scheduled_for = current_time + timedelta(minutes=delay)

                # Prepare content
                post_content = config.custom_content or content
                if adapt_content:
                    post_content = self._adapt_content(post_content, config.platform)

                # Create post
                payload: dict[str, Any] = {
                    "content": post_content,
                    "platforms": [
                        {"platform": config.platform, "accountId": config.account_id}
                    ],
                    "scheduled_for": scheduled_for,
                }
                if title:
                    payload["title"] = title
                if media_items:
                    payload["media_items"] = media_items
                if tags:
                    payload["tags"] = tags

                response = await self._client.posts.acreate(**payload)
                post_id = response.get("post", {}).get("_id")

                results.append(
                    CrossPostResult(
                        platform=config.platform, success=True, post_id=post_id
                    )
                )

            except Exception as e:
                results.append(
                    CrossPostResult(
                        platform=config.platform, success=False, error=str(e)
                    )
                )

        return results

    def post_sync(
        self,
        content: str,
        platforms: list[PlatformConfig],
        **kwargs: Any,
    ) -> list[CrossPostResult]:
        """Synchronous version of cross-posting."""
        results: list[CrossPostResult] = []
        current_time = kwargs.get("base_time") or datetime.now()
        adapt = kwargs.get("adapt_content", True)

        for i, config in enumerate(platforms):
            try:
                delay = config.delay_minutes or (i * self.default_stagger)
                scheduled_for = current_time + timedelta(minutes=delay)

                post_content = config.custom_content or content
                if adapt:
                    post_content = self._adapt_content(post_content, config.platform)

                payload: dict[str, Any] = {
                    "content": post_content,
                    "platforms": [
                        {"platform": config.platform, "accountId": config.account_id}
                    ],
                    "scheduled_for": scheduled_for,
                }
                if kwargs.get("title"):
                    payload["title"] = kwargs["title"]
                if kwargs.get("media_items"):
                    payload["media_items"] = kwargs["media_items"]

                response = self._client.posts.create(**payload)
                post_id = response.get("post", {}).get("_id")

                results.append(
                    CrossPostResult(
                        platform=config.platform, success=True, post_id=post_id
                    )
                )

            except Exception as e:
                results.append(
                    CrossPostResult(
                        platform=config.platform, success=False, error=str(e)
                    )
                )

        return results
