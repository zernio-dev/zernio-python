"""
Main Late API client.
"""

from __future__ import annotations

from ..resources import (
    AccountGroupsResource,
    AccountsResource,
    AnalyticsResource,
    ApiKeysResource,
    ConnectResource,
    InvitesResource,
    LogsResource,
    MediaResource,
    PostsResource,
    ProfilesResource,
    QueueResource,
    RedditResource,
    ToolsResource,
    UsageResource,
    UsersResource,
    WebhooksResource,
)
from .base import BaseClient


class Late(BaseClient):
    """
    Late API client for scheduling social media posts.

    Example:
        >>> from late import Late, Platform
        >>>
        >>> # Initialize client
        >>> client = Late(api_key="your_api_key")
        >>>
        >>> # List profiles
        >>> profiles = client.profiles.list()
        >>>
        >>> # Create a post
        >>> post = client.posts.create(
        ...     content="Hello world!",
        ...     platforms=[{"platform": Platform.TWITTER, "accountId": "..."}],
        ...     scheduled_for="2024-12-25T10:00:00Z",
        ... )
        >>>
        >>> # Async usage
        >>> async with Late(api_key="...") as client:
        ...     posts = await client.posts.alist()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the Late client.

        Args:
            api_key: Late API key
            base_url: Base URL (default: https://getlate.dev/api)
            timeout: Request timeout in seconds
            max_retries: Maximum retries for failed requests
        """
        super().__init__(
            api_key, base_url=base_url, timeout=timeout, max_retries=max_retries
        )

        # Core resources (manual with Pydantic validation)
        self.posts = PostsResource(self)
        self.profiles = ProfilesResource(self)
        self.accounts = AccountsResource(self)
        self.users = UsersResource(self)
        self.media = MediaResource(self)
        self.analytics = AnalyticsResource(self)
        self.tools = ToolsResource(self)
        self.queue = QueueResource(self)

        # Additional resources (auto-generated)
        self.webhooks = WebhooksResource(self)
        self.logs = LogsResource(self)
        self.connect = ConnectResource(self)
        self.invites = InvitesResource(self)
        self.api_keys = ApiKeysResource(self)
        self.account_groups = AccountGroupsResource(self)
        self.usage = UsageResource(self)
        self.reddit = RedditResource(self)

    async def __aenter__(self) -> Late:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        """Async context manager exit."""
        pass
