"""
Accounts resource for managing connected social accounts.
"""

from __future__ import annotations

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

    # Signature must mirror _GeneratedAccountsResource.get_follower_stats; this
    # override exists ONLY to return a typed FollowerStatsResponse instead of a
    # raw dict. Keep the params in sync on every OpenAPI regen, dropping them is
    # what caused the TypeError in GET-820. account_ids is a comma-separated
    # string (the MCP wrapper and the REST endpoint both use that shape); a list
    # is also accepted for backwards compatibility and joined into that shape.
    def get_follower_stats(
        self,
        *,
        account_ids: str | list[str] | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        granularity: str | None = None,
    ) -> FollowerStatsResponse:
        """
        Get follower statistics for accounts. Requires analytics add-on.

        Args:
            account_ids: Account IDs to filter, as a comma-separated string or a
                list of IDs (optional, defaults to all)
            profile_id: Filter by profile ID
            from_date: Start date YYYY-MM-DD (server defaults to 30 days ago)
            to_date: End date YYYY-MM-DD (server defaults to today)
            granularity: Aggregation level ('daily' | 'weekly' | 'monthly')

        Returns:
            FollowerStatsResponse with 'accounts', 'stats', 'dateRange', 'granularity'
        """
        if isinstance(account_ids, list):
            account_ids = ",".join(account_ids)
        params = self._build_params(
            account_ids=account_ids,
            profile_id=profile_id,
            from_date=from_date,
            to_date=to_date,
            granularity=granularity,
        )
        data = self._client._get(self._path("follower-stats"), params=params or None)
        return FollowerStatsResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self, *, profile_id: str | None = None) -> AccountsListResponse:
        """List connected accounts asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._BASE_PATH, params=params or None)
        return AccountsListResponse.model_validate(data)

    # Same signature/params as the sync version; only the return wrapping differs.
    # See GET-820 note on get_follower_stats above.
    async def aget_follower_stats(
        self,
        *,
        account_ids: str | list[str] | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        granularity: str | None = None,
    ) -> FollowerStatsResponse:
        """Get follower statistics asynchronously.

        Args:
            account_ids: Account IDs to filter, as a comma-separated string or a
                list of IDs (optional, defaults to all)
            profile_id: Filter by profile ID
            from_date: Start date YYYY-MM-DD
            to_date: End date YYYY-MM-DD
            granularity: Aggregation level ('daily' | 'weekly' | 'monthly')

        Returns:
            FollowerStatsResponse with 'accounts', 'stats', 'dateRange', 'granularity'
        """
        if isinstance(account_ids, list):
            account_ids = ",".join(account_ids)
        params = self._build_params(
            account_ids=account_ids,
            profile_id=profile_id,
            from_date=from_date,
            to_date=to_date,
            granularity=granularity,
        )
        data = await self._client._aget(
            self._path("follower-stats"), params=params or None
        )
        return FollowerStatsResponse.model_validate(data)
