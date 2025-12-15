"""
Profiles resource for managing user profiles.
"""

from __future__ import annotations

from late.models import (
    ProfileCreateResponse,
    ProfileDeleteResponse,
    ProfileGetResponse,
    ProfilesListResponse,
    ProfileUpdateResponse,
)

from .base import BaseResource


class ProfilesResource(BaseResource[ProfilesListResponse]):
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

    def list(self) -> ProfilesListResponse:
        """
        List all profiles.

        Returns:
            ProfilesListResponse with 'profiles' attribute
        """
        data = self._client._get(self._BASE_PATH)
        return ProfilesListResponse.model_validate(data)

    def get(self, profile_id: str) -> ProfileGetResponse:
        """
        Get a profile by ID.

        Args:
            profile_id: The profile ID

        Returns:
            ProfileGetResponse with 'profile' attribute
        """
        data = self._client._get(self._path(profile_id))
        return ProfileGetResponse.model_validate(data)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        color: str | None = None,
    ) -> ProfileCreateResponse:
        """
        Create a new profile.

        Args:
            name: Profile name (required)
            description: Optional profile description
            color: Optional hex color (e.g., '#ffeda0')

        Returns:
            ProfileCreateResponse with 'message' and 'profile' attributes
        """
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
        )
        data = self._client._post(self._BASE_PATH, data=payload)
        return ProfileCreateResponse.model_validate(data)

    def update(
        self,
        profile_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
        is_default: bool | None = None,
    ) -> ProfileUpdateResponse:
        """
        Update a profile.

        Args:
            profile_id: ID of the profile to update
            name: New profile name
            description: New profile description
            color: New hex color (e.g., '#2196F3')
            is_default: Set as default profile

        Returns:
            ProfileUpdateResponse with 'message' and 'profile' attributes
        """
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
            is_default=is_default,
        )
        data = self._client._put(self._path(profile_id), data=payload)
        return ProfileUpdateResponse.model_validate(data)

    def delete(self, profile_id: str) -> ProfileDeleteResponse:
        """
        Delete a profile.

        Note: Profile must have no connected accounts.

        Args:
            profile_id: ID of the profile to delete

        Returns:
            ProfileDeleteResponse with 'message' attribute
        """
        data = self._client._delete(self._path(profile_id))
        return ProfileDeleteResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def alist(self) -> ProfilesListResponse:
        """List all profiles asynchronously."""
        data = await self._client._aget(self._BASE_PATH)
        return ProfilesListResponse.model_validate(data)

    async def aget(self, profile_id: str) -> ProfileGetResponse:
        """Get a profile by ID asynchronously."""
        data = await self._client._aget(self._path(profile_id))
        return ProfileGetResponse.model_validate(data)

    async def acreate(
        self,
        *,
        name: str,
        description: str | None = None,
        color: str | None = None,
    ) -> ProfileCreateResponse:
        """Create a new profile asynchronously."""
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
        )
        data = await self._client._apost(self._BASE_PATH, data=payload)
        return ProfileCreateResponse.model_validate(data)

    async def aupdate(
        self,
        profile_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
        is_default: bool | None = None,
    ) -> ProfileUpdateResponse:
        """Update a profile asynchronously."""
        payload = self._build_payload(
            name=name,
            description=description,
            color=color,
            is_default=is_default,
        )
        data = await self._client._aput(self._path(profile_id), data=payload)
        return ProfileUpdateResponse.model_validate(data)

    async def adelete(self, profile_id: str) -> ProfileDeleteResponse:
        """Delete a profile asynchronously."""
        data = await self._client._adelete(self._path(profile_id))
        return ProfileDeleteResponse.model_validate(data)
