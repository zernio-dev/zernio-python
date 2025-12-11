"""
Queue resource for managing posting schedules.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from .base import BaseResource

if TYPE_CHECKING:
    from ..client.base import BaseClient


DayOfWeek = Literal[0, 1, 2, 3, 4, 5, 6]  # 0=Sunday, 6=Saturday


class QueueResource(BaseResource[Any]):
    """
    Resource for managing the posting queue.

    The queue allows you to set up recurring time slots for automatic
    post scheduling.

    Example:
        >>> client = Late(api_key="...")
        >>> # Get queue slots
        >>> slots = client.queue.get_slots(profile_id="prof_123")
        >>> # Update queue slots
        >>> client.queue.update_slots(
        ...     profile_id="prof_123",
        ...     timezone="America/New_York",
        ...     slots=[
        ...         {"dayOfWeek": 1, "time": "09:00"},  # Monday 9am
        ...         {"dayOfWeek": 3, "time": "14:00"},  # Wednesday 2pm
        ...     ],
        ... )
    """

    _BASE_PATH = "/v1/queue"

    # -------------------------------------------------------------------------
    # Sync methods
    # -------------------------------------------------------------------------

    def get_slots(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """
        Get queue slots for a profile.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            Dict with queue schedule information
        """
        params = self._build_params(profile_id=profile_id)
        return self._client._get(self._path("slots"), params=params or None)

    def update_slots(
        self,
        *,
        profile_id: str,
        timezone: str,
        slots: list[dict[str, Any]],
        active: bool = True,
    ) -> dict[str, Any]:
        """
        Update queue slots for a profile.

        Args:
            profile_id: Profile ID to update
            timezone: IANA timezone (e.g., "America/New_York")
            slots: List of slot dicts with 'dayOfWeek' (0-6) and 'time' (HH:mm)
            active: Whether the queue is active

        Returns:
            Dict with updated queue schedule
        """
        payload = self._build_payload(
            profile_id=profile_id,
            timezone=timezone,
            slots=slots,
            active=active,
        )
        return self._client._put(self._path("slots"), data=payload)

    def delete_slots(self, *, profile_id: str) -> dict[str, Any]:
        """
        Delete all queue slots for a profile.

        Args:
            profile_id: Profile ID to clear slots for

        Returns:
            Dict with 'message' key
        """
        params = self._build_params(profile_id=profile_id)
        return self._client._delete(self._path("slots"), params=params)

    def preview(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """
        Preview the next scheduled slot times.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            Dict with preview of next scheduled times
        """
        params = self._build_params(profile_id=profile_id)
        return self._client._get(self._path("preview"), params=params or None)

    def next_slot(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """
        Get the next available queue slot.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            Dict with next available slot information
        """
        params = self._build_params(profile_id=profile_id)
        return self._client._get(self._path("next-slot"), params=params or None)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def aget_slots(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """Get queue slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        return await self._client._aget(self._path("slots"), params=params or None)

    async def aupdate_slots(
        self,
        *,
        profile_id: str,
        timezone: str,
        slots: list[dict[str, Any]],
        active: bool = True,
    ) -> dict[str, Any]:
        """Update queue slots asynchronously."""
        payload = self._build_payload(
            profile_id=profile_id,
            timezone=timezone,
            slots=slots,
            active=active,
        )
        return await self._client._aput(self._path("slots"), data=payload)

    async def adelete_slots(self, *, profile_id: str) -> dict[str, Any]:
        """Delete queue slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        return await self._client._adelete(self._path("slots"), params=params)

    async def apreview(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """Preview next scheduled slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        return await self._client._aget(self._path("preview"), params=params or None)

    async def anext_slot(self, *, profile_id: str | None = None) -> dict[str, Any]:
        """Get next available slot asynchronously."""
        params = self._build_params(profile_id=profile_id)
        return await self._client._aget(self._path("next-slot"), params=params or None)
