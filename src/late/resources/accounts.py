"""
Accounts resource for managing connected social accounts.
"""

from __future__ import annotations

from typing import Any

from late.models import (
    AccountsListResponse,
    FollowerStatsResponse,
)

from ._generated.accounts import AccountsResource as _GeneratedAccountsResource
from .base import BaseResource


# Inherit from the auto-generated resource first so all OpenAPI-derived
# methods (list_accounts, get_account_health, update_account, the
# google_business_* suite, etc.) remain callable on client.accounts. The
# hand-written methods below override the generated list/get/get_follower_stats
# with pydantic-typed return values; everything else falls through to the
# generated implementation. Without this, MCP tools generated from the
# OpenAPI spec (e.g. accounts_list_accounts) crash with AttributeError
# because the hand-written class used to hide the generated methods.
class AccountsResource(_GeneratedAccountsResource, BaseResource[AccountsListResponse]):
    """
    Resource for managing connected social media accounts.

    Accounts are your connected social media accounts (Twitter, Instagram, etc.).
    They belong to profiles.

    Example:
        >>> client = Late(api_key="...")
        >>> # List all accounts
        >>> accounts = client.accounts.list()
        >>> # List accounts for a specific profile
        >>> accounts = client.accounts.list(profile_id="prof_123")
        >>> # Get a specific account
        >>> account = client.accounts.get("acc_456")
    """

    _BASE_PATH = "/v1/accounts"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def list(self, *, profile_id: str | None = None) -> AccountsListResponse:
        """
        List connected accounts.

        Args:
            profile_id: Optional profile ID to filter accounts

        Returns:
            AccountsListResponse with 'accounts' and 'hasAnalyticsAccess' attributes
        """
        params = self._build_params(profile_id=profile_id)
        data = self._client._get(self._BASE_PATH, params=params or None)
        return AccountsListResponse.model_validate(data)

    # Overrides the generated method only to return a typed FollowerStatsResponse
    # (SDK users read resp.stats; the MCP formatter keys off accounts/stats) and
    # to accept a list for account_ids. Everything else goes through **kwargs so
    # params added to the spec on regen reach the generated method; a copied
    # signature silently dropped them before.
    def get_follower_stats(
        self,
        *,
        account_ids: str | list[str] | None = None,
        **kwargs: Any,
    ) -> FollowerStatsResponse:
        """
        Get follower statistics for accounts. Requires analytics add-on.

        Args:
            account_ids: Account IDs to filter, as a comma-separated string or a
                list of IDs (optional, defaults to all)
            **kwargs: Forwarded to the generated method (profile_id, from_date,
                to_date, granularity, limit, cursor, ...)

        Returns:
            FollowerStatsResponse with 'accounts', 'stats', 'dateRange',
            'granularity' and 'pagination'
        """
        if isinstance(account_ids, list):
            account_ids = ",".join(account_ids)
        data = super().get_follower_stats(account_ids=account_ids, **kwargs)
        return FollowerStatsResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self, *, profile_id: str | None = None) -> AccountsListResponse:
        """List connected accounts asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._BASE_PATH, params=params or None)
        return AccountsListResponse.model_validate(data)

    # See get_follower_stats.
    async def aget_follower_stats(
        self,
        *,
        account_ids: str | list[str] | None = None,
        **kwargs: Any,
    ) -> FollowerStatsResponse:
        """Get follower statistics asynchronously. Same arguments as
        get_follower_stats."""
        if isinstance(account_ids, list):
            account_ids = ",".join(account_ids)
        data = await super().aget_follower_stats(account_ids=account_ids, **kwargs)
        return FollowerStatsResponse.model_validate(data)
