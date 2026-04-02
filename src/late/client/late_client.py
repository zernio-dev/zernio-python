"""Main Zernio API client.

Provides the primary client class for interacting with the Zernio API.
The ``Late`` alias is kept for backwards compatibility.
"""

from __future__ import annotations

import os

from ..resources import (
    AccountGroupsResource,
    AccountSettingsResource,
    AccountsResource,
    AdAudiencesResource,
    AdCampaignsResource,
    AdsResource,
    AnalyticsResource,
    ApiKeysResource,
    BroadcastsResource,
    CommentAutomationsResource,
    CommentsResource,
    ConnectResource,
    ContactsResource,
    CustomFieldsResource,
    InvitesResource,
    LogsResource,
    MediaResource,
    MessagesResource,
    PostsResource,
    ProfilesResource,
    QueueResource,
    RedditResource,
    ReviewsResource,
    SequencesResource,
    ToolsResource,
    TwitterEngagementResource,
    UsageResource,
    UsersResource,
    ValidateResource,
    WebhooksResource,
    WhatsappResource,
    WhatsappPhoneNumbersResource,
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
        >>> # Inbox: list comments, conversations, reviews
        >>> comments = client.comments.list_inbox_comments()
        >>> conversations = client.inbox.list_inbox_conversations()
        >>> reviews = client.reviews.list_inbox_reviews()
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

        # --- auto-registered resources (do not edit) ---
        self.account_groups = AccountGroupsResource(self)
        self.account_settings = AccountSettingsResource(self)
        self.accounts = AccountsResource(self)
        self.ad_audiences = AdAudiencesResource(self)
        self.ad_campaigns = AdCampaignsResource(self)
        self.ads = AdsResource(self)
        self.analytics = AnalyticsResource(self)
        self.api_keys = ApiKeysResource(self)
        self.broadcasts = BroadcastsResource(self)
        self.comment_automations = CommentAutomationsResource(self)
        self.comments = CommentsResource(self)
        self.connect = ConnectResource(self)
        self.contacts = ContactsResource(self)
        self.custom_fields = CustomFieldsResource(self)
        self.invites = InvitesResource(self)
        self.logs = LogsResource(self)
        self.media = MediaResource(self)
        self.messages = MessagesResource(self)
        self.posts = PostsResource(self)
        self.profiles = ProfilesResource(self)
        self.queue = QueueResource(self)
        self.reddit = RedditResource(self)
        self.reviews = ReviewsResource(self)
        self.sequences = SequencesResource(self)
        self.tools = ToolsResource(self)
        self.twitter_engagement = TwitterEngagementResource(self)
        self.usage = UsageResource(self)
        self.users = UsersResource(self)
        self.validate = ValidateResource(self)
        self.webhooks = WebhooksResource(self)
        self.whatsapp = WhatsappResource(self)
        self.whatsapp_phone_numbers = WhatsappPhoneNumbersResource(self)
        # --- end auto-registered resources ---

    async def __aenter__(self) -> Zernio:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        """Async context manager exit."""
        pass


# Backwards-compatible alias so ``from late import Late`` keeps working
Late = Zernio
