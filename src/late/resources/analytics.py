"""
Analytics resource for post analytics and usage statistics.

Inherits all generated analytics methods (get_analytics, get_daily_metrics,
get_best_time_to_post, etc.) and adds convenience aliases.
"""

from __future__ import annotations

from typing import Any, Literal

from ._generated.analytics import AnalyticsResource as _GeneratedAnalyticsResource

Period = Literal["7d", "30d", "90d", "all"]


class AnalyticsResource(_GeneratedAnalyticsResource):
    """
    Resource for analytics and usage statistics.

    Inherits all generated analytics methods (get_analytics, get_daily_metrics,
    get_best_time_to_post, etc.) and adds convenience aliases for backwards
    compatibility with existing SDK users.

    Example:
        >>> client = Late(api_key="...")
        >>> # Get post analytics (generated method, used by MCP tools)
        >>> analytics = client.analytics.get_analytics(period="30d")
        >>> # Get post analytics (convenience alias)
        >>> analytics = client.analytics.get(period="30d")
        >>> # Get usage statistics
        >>> usage = client.analytics.get_usage()
    """

    # Used by convenience get()/aget() methods below
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
