"""
Users resource for managing team users.
"""

from __future__ import annotations

from late.models import UserGetResponse, UsersListResponse

from .base import BaseResource


class UsersResource(BaseResource[UsersListResponse]):
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

    def list(self) -> UsersListResponse:
        """
        List team users.

        Returns:
            UsersListResponse with 'users' attribute
        """
        data = self._client._get(self._BASE_PATH)
        return UsersListResponse.model_validate(data)

    def get(self, user_id: str) -> UserGetResponse:
        """
        Get a user by ID.

        Args:
            user_id: The user ID

        Returns:
            UserGetResponse with 'user' attribute
        """
        data = self._client._get(self._path(user_id))
        return UserGetResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self) -> UsersListResponse:
        """List team users asynchronously."""
        data = await self._client._aget(self._BASE_PATH)
        return UsersListResponse.model_validate(data)

    async def aget(self, user_id: str) -> UserGetResponse:
        """Get a user by ID asynchronously."""
        data = await self._client._aget(self._path(user_id))
        return UserGetResponse.model_validate(data)
