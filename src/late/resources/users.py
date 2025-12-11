"""
Users resource for managing team users.
"""

from __future__ import annotations

from typing import Any

from .base import BaseResource


class UsersResource(BaseResource[Any]):
    """
    Resource for managing team users.

    Example:
        >>> client = Late(api_key="...")
        >>> # List team users
        >>> users = client.users.list()
        >>> # Get a specific user
        >>> user = client.users.get("user_123")
    """

    _BASE_PATH = "/v1/users"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def list(self) -> dict[str, Any]:
        """
        List team users.

        Returns:
            Dict with 'users' key containing list of User objects
        """
        return self._client._get(self._BASE_PATH)

    def get(self, user_id: str) -> dict[str, Any]:
        """
        Get a user by ID.

        Args:
            user_id: The user ID

        Returns:
            Dict with 'user' key containing the User object
        """
        return self._client._get(self._path(user_id))

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self) -> dict[str, Any]:
        """List team users asynchronously."""
        return await self._client._aget(self._BASE_PATH)

    async def aget(self, user_id: str) -> dict[str, Any]:
        """Get a user by ID asynchronously."""
        return await self._client._aget(self._path(user_id))
