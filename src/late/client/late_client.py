"""
Main Zernio API client.

Provides the primary client class for interacting with the Zernio API.
The ``Late`` alias is kept for backwards compatibility.
"""

from __future__ import annotations

import os

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


class Zernio(BaseClient):
    """
    Zernio API client for scheduling social media posts.

    Example:
        >>> from late import Zernio, Platform
        >>>
        >>> # Initialize client (reads ZERNIO_API_KEY or LATE_API_KEY from env)
        >>> client = Zernio()
        >>>
        >>> # Or pass the key explicitly
        >>> client = Zernio(api_key="your_api_key")
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
        >>> async with Zernio(api_key="...") as client:
        ...     posts = await client.posts.alist()
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the Zernio client.

        Args:
            api_key: Zernio API key. If not provided, reads from ZERNIO_API_KEY
                     or LATE_API_KEY environment variable (in that order).
            base_url: Base URL (default: https://zernio.com/api)
            timeout: Request timeout in seconds
            max_retries: Maximum retries for failed requests

        Raises:
            ValueError: If no API key is provided and neither ZERNIO_API_KEY
                        nor LATE_API_KEY environment variable is set.
        """
        # Resolve API key: explicit arg > ZERNIO_API_KEY env > LATE_API_KEY env
        resolved_key = api_key or os.environ.get("ZERNIO_API_KEY") or os.environ.get("LATE_API_KEY")
        if not resolved_key:
            raise ValueError(
                "API key is required. Pass api_key= or set the ZERNIO_API_KEY "
                "(or LATE_API_KEY) environment variable."
            )

        super().__init__(
            resolved_key, base_url=base_url, timeout=timeout, max_retries=max_retries
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

    async def __aenter__(self) -> Zernio:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        """Async context manager exit."""
        pass


# Backwards-compatible alias so ``from late import Late`` keeps working
Late = Zernio
