"""
Late API resources.

Manual resources with Pydantic validation are used for the main resources.
Auto-generated resources are used for additional endpoints.
"""

# Manual resources (with Pydantic model validation)
from .accounts import AccountsResource
from .analytics import AnalyticsResource
from .media import MediaResource
from .posts import PostsResource
from .profiles import ProfilesResource
from .queue import QueueResource
from .tools import ToolsResource
from .users import UsersResource

# Auto-generated resources (additional endpoints)
from ._generated.account_groups import AccountGroupsResource
from ._generated.api_keys import ApiKeysResource
from ._generated.connect import ConnectResource
from ._generated.invites import InvitesResource
from ._generated.logs import LogsResource
from ._generated.reddit import RedditResource
from ._generated.usage import UsageResource
from ._generated.webhooks import WebhooksResource

__all__ = [
    # Manual resources
    "AccountsResource",
    "AnalyticsResource",
    "MediaResource",
    "PostsResource",
    "ProfilesResource",
    "QueueResource",
    "ToolsResource",
    "UsersResource",
    # Auto-generated resources
    "AccountGroupsResource",
    "ApiKeysResource",
    "ConnectResource",
    "InvitesResource",
    "LogsResource",
    "RedditResource",
    "UsageResource",
    "WebhooksResource",
]
