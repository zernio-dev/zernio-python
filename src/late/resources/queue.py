"""
Queue resource for managing posting schedules.
"""

from __future__ import annotations

from typing import Any

from late.models import (
    QueueDeleteResponse,
    QueueNextSlotResponse,
    QueuePreviewResponse,
    QueueSlotsResponse,
    QueueUpdateResponse,
)

from .base import BaseResource


class QueueResource(BaseResource[QueueSlotsResponse]):
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

    def get_slots(self, *, profile_id: str | None = None) -> QueueSlotsResponse:
        """
        Get queue slots for a profile.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            QueueSlotsResponse with queue schedule information
        """
        params = self._build_params(profile_id=profile_id)
        data = self._client._get(self._path("slots"), params=params or None)
        return QueueSlotsResponse.model_validate(data)

    def update_slots(
        self,
        *,
        profile_id: str,
        timezone: str,
        slots: list[dict[str, Any]],
        active: bool = True,
    ) -> QueueUpdateResponse:
        """
        Update queue slots for a profile.

        Args:
            profile_id: Profile ID to update
            timezone: IANA timezone (e.g., "America/New_York")
            slots: List of slot dicts with 'dayOfWeek' (0-6) and 'time' (HH:mm)
            active: Whether the queue is active

        Returns:
            QueueUpdateResponse with updated queue schedule
        """
        payload = self._build_payload(
            profile_id=profile_id,
            timezone=timezone,
            slots=slots,
            active=active,
        )
        data = self._client._put(self._path("slots"), data=payload)
        return QueueUpdateResponse.model_validate(data)

    def delete_slots(self, *, profile_id: str) -> QueueDeleteResponse:
        """
        Delete all queue slots for a profile.

        Args:
            profile_id: Profile ID to clear slots for

        Returns:
            QueueDeleteResponse with 'message' attribute
        """
        params = self._build_params(profile_id=profile_id)
        data = self._client._delete(self._path("slots"), params=params)
        return QueueDeleteResponse.model_validate(data)

    def preview(self, *, profile_id: str | None = None) -> QueuePreviewResponse:
        """
        Preview the next scheduled slot times.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            QueuePreviewResponse with preview of next scheduled times
        """
        params = self._build_params(profile_id=profile_id)
        data = self._client._get(self._path("preview"), params=params or None)
        return QueuePreviewResponse.model_validate(data)

    def next_slot(self, *, profile_id: str | None = None) -> QueueNextSlotResponse:
        """
        Get the next available queue slot.

        Args:
            profile_id: Optional profile ID to filter

        Returns:
            QueueNextSlotResponse with next available slot information
        """
        params = self._build_params(profile_id=profile_id)
        data = self._client._get(self._path("next-slot"), params=params or None)
        return QueueNextSlotResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def aget_slots(self, *, profile_id: str | None = None) -> QueueSlotsResponse:
        """Get queue slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._path("slots"), params=params or None)
        return QueueSlotsResponse.model_validate(data)

    async def aupdate_slots(
        self,
        *,
        profile_id: str,
        timezone: str,
        slots: list[dict[str, Any]],
        active: bool = True,
    ) -> QueueUpdateResponse:
        """Update queue slots asynchronously."""
        payload = self._build_payload(
            profile_id=profile_id,
            timezone=timezone,
            slots=slots,
            active=active,
        )
        data = await self._client._aput(self._path("slots"), data=payload)
        return QueueUpdateResponse.model_validate(data)

    async def adelete_slots(self, *, profile_id: str) -> QueueDeleteResponse:
        """Delete queue slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._adelete(self._path("slots"), params=params)
        return QueueDeleteResponse.model_validate(data)

    async def apreview(self, *, profile_id: str | None = None) -> QueuePreviewResponse:
        """Preview next scheduled slots asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._path("preview"), params=params or None)
        return QueuePreviewResponse.model_validate(data)

    async def anext_slot(
        self, *, profile_id: str | None = None
    ) -> QueueNextSlotResponse:
        """Get next available slot asynchronously."""
        params = self._build_params(profile_id=profile_id)
        data = await self._client._aget(self._path("next-slot"), params=params or None)
        return QueueNextSlotResponse.model_validate(data)
