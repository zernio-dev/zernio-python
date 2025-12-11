"""
Analytics resource for post analytics and usage statistics.
"""

from __future__ import annotations

from typing import Any, Literal

from .base import BaseResource

Period = Literal["7d", "30d", "90d", "all"]


class AnalyticsResource(BaseResource[Any]):
    """
    Resource for analytics and usage statistics.

    Example:
        >>> client = Late(api_key="...")
        >>> # Get post analytics
        >>> analytics = client.analytics.get(period="30d")
        >>> # Get usage statistics
        >>> usage = client.analytics.get_usage()
    """

    _BASE_PATH = "/v1/analytics"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def get(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        period: Period | None = None,
    ) -> dict[str, Any]:
        """
        Get post analytics.

        Args:
            page: Page number (1-based)
            limit: Number of results per page
            period: Time period filter (7d, 30d, 90d, all)

        Returns:
            Dict with analytics data
        """
        params = self._build_params(page=page, limit=limit, period=period)
        return self._client._get(self._BASE_PATH, params=params)

    def get_usage(self) -> dict[str, Any]:
        """
        Get plan usage statistics.

        Returns:
            Dict with usage information including posts count, limits, etc.
        """
        return self._client._get("/v1/usage-stats")

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def aget(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        period: Period | None = None,
    ) -> dict[str, Any]:
        """Get post analytics asynchronously."""
        params = self._build_params(page=page, limit=limit, period=period)
        return await self._client._aget(self._BASE_PATH, params=params)

    async def aget_usage(self) -> dict[str, Any]:
        """Get plan usage statistics asynchronously."""
        return await self._client._aget("/v1/usage-stats")
