"""
Accounts resource for managing connected social accounts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import BaseResource

if TYPE_CHECKING:
    from ..client.base import BaseClient


class AccountsResource(BaseResource[Any]):
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

    def list(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """
        List connected accounts.

        Args:
            profile_id: Optional profile ID to filter accounts

        Returns:
            Dict with 'accounts' and 'hasAnalyticsAccess' keys
        """
        params = self._build_params(profile_id=profile_id)
        return self._client._get(self._BASE_PATH, params=params or None)

    def get(self, account_id: str) -> dict[str, Any]:
        """
        Get an account by ID.

        Args:
            account_id: The account ID

        Returns:
            Dict with 'account' key containing the SocialAccount object
        """
        return self._client._get(self._path(account_id))

    def get_follower_stats(
        self,
        *,
        account_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Get follower statistics for accounts.

        Requires analytics add-on.

        Args:
            account_ids: Optional list of account IDs to filter

        Returns:
            Dict with follower statistics
        """
        params = None
        if account_ids:
            params = {"accountIds": ",".join(account_ids)}
        return self._client._get(self._path("follower-stats"), params=params)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """List connected accounts asynchronously."""
        params = self._build_params(profile_id=profile_id)
        return await self._client._aget(self._BASE_PATH, params=params or None)

    async def aget(self, account_id: str) -> dict[str, Any]:
        """Get an account by ID asynchronously."""
        return await self._client._aget(self._path(account_id))

    async def aget_follower_stats(
        self,
        *,
        account_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get follower statistics asynchronously."""
        params = None
        if account_ids:
            params = {"accountIds": ",".join(account_ids)}
        return await self._client._aget(self._path("follower-stats"), params=params)
