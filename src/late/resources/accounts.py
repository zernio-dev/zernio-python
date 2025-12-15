"""
Accounts resource for managing connected social accounts.
"""

from __future__ import annotations

from late.models import (
    AccountGetResponse,
    AccountsListResponse,
    FollowerStatsResponse,
)

from .base import BaseResource


class AccountsResource(BaseResource[AccountsListResponse]):
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

    def get(self, account_id: str) -> AccountGetResponse:
        """
        Get an account by ID.

        Args:
            account_id: The account ID

        Returns:
            AccountGetResponse with 'account' attribute
        """
        data = self._client._get(self._path(account_id))
        return AccountGetResponse.model_validate(data)

    def get_follower_stats(
        self,
        *,
        account_ids: list[str] | None = None,
    ) -> FollowerStatsResponse:
        """
        Get follower statistics for accounts.

        Requires analytics add-on.

        Args:
            account_ids: Optional list of account IDs to filter

        Returns:
            FollowerStatsResponse with 'stats' attribute
        """
        params = None
        if account_ids:
            params = {"accountIds": ",".join(account_ids)}
        data = self._client._get(self._path("follower-stats"), params=params)
        return FollowerStatsResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self, *, profile_id: str | None = None) -> AccountsListResponse:
        """List connected accounts asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._BASE_PATH, params=params or None)
        return AccountsListResponse.model_validate(data)

    async def aget(self, account_id: str) -> AccountGetResponse:
        """Get an account by ID asynchronously."""
        data = await self._client._aget(self._path(account_id))
        return AccountGetResponse.model_validate(data)

    async def aget_follower_stats(
        self,
        *,
        account_ids: list[str] | None = None,
    ) -> FollowerStatsResponse:
        """Get follower statistics asynchronously."""
        params = None
        if account_ids:
            params = {"accountIds": ",".join(account_ids)}
        data = await self._client._aget(self._path("follower-stats"), params=params)
        return FollowerStatsResponse.model_validate(data)
