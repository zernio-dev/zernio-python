"""
Profiles resource for managing user profiles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import BaseResource

if TYPE_CHECKING:
    from ..client.base import BaseClient


class ProfilesResource(BaseResource[Any]):
    """
    Resource for managing profiles.

    Profiles are containers that group social media accounts together.
    Think of them as "brands" or "projects".

    Example:
        >>> client = Late(api_key="...")
        >>> # List all profiles
        >>> profiles = client.profiles.list()
        >>> # Create a new profile
        >>> profile = client.profiles.create(name="My Brand", color="#4CAF50")
        >>> # Update a profile
        >>> client.profiles.update(profile_id, name="New Name")
        >>> # Delete a profile
        >>> client.profiles.delete(profile_id)
    """

    _BASE_PATH = "/v1/profiles"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def list(self) -> dict[str, Any]:
        """
        List all profiles.

        Returns:
            Dict with 'profiles' key containing list of Profile objects
        """
        return self._client._get(self._BASE_PATH)

    def get(self, profile_id: str) -> dict[str, Any]:
        """
        Get a profile by ID.

        Args:
            profile_id: The profile ID

        Returns:
            Dict with 'profile' key containing the Profile object
        """
        return self._client._get(self._path(profile_id))

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new profile.

        Args:
            name: Profile name (required)
            description: Optional profile description
            color: Optional hex color (e.g., '#ffeda0')

        Returns:
            Dict with 'message' and 'profile' keys
        """
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
        )
        return self._client._post(self._BASE_PATH, data=payload)

    def update(
        self,
        profile_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
        is_default: bool | None = None,
    ) -> dict[str, Any]:
        """
        Update a profile.

        Args:
            profile_id: ID of the profile to update
            name: New profile name
            description: New profile description
            color: New hex color (e.g., '#2196F3')
            is_default: Set as default profile

        Returns:
            Dict with 'message' and 'profile' keys
        """
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
            is_default=is_default,
        )
        return self._client._put(self._path(profile_id), data=payload)

    def delete(self, profile_id: str) -> dict[str, Any]:
        """
        Delete a profile.

        Note: Profile must have no connected accounts.

        Args:
            profile_id: ID of the profile to delete

        Returns:
            Dict with 'message' key
        """
        return self._client._delete(self._path(profile_id))

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self) -> dict[str, Any]:
        """List all profiles asynchronously."""
        return await self._client._aget(self._BASE_PATH)

    async def aget(self, profile_id: str) -> dict[str, Any]:
        """Get a profile by ID asynchronously."""
        return await self._client._aget(self._path(profile_id))

    async def acreate(
        self,
        *,
        name: str,
        description: str | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Create a new profile asynchronously."""
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
        )
        return await self._client._apost(self._BASE_PATH, data=payload)

    async def aupdate(
        self,
        profile_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
        is_default: bool | None = None,
    ) -> dict[str, Any]:
        """Update a profile asynchronously."""
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
            is_default=is_default,
        )
        return await self._client._aput(self._path(profile_id), data=payload)

    async def adelete(self, profile_id: str) -> dict[str, Any]:
        """Delete a profile asynchronously."""
        return await self._client._adelete(self._path(profile_id))
