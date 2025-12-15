"""
Base resource class for API endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from ..client.base import BaseClient

T = TypeVar("T", bound=BaseModel)


def _to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class BaseResource(Generic[T]):
    """
    Base class for API resources.

    Provides access to the HTTP client and common patterns
    for API resource implementations.
    """

    _BASE_PATH: str = ""

    def __init__(self, client: BaseClient) -> None:
        """
        Initialize the resource.

        Args:
            client: The Late API client instance
        """
        self._client = client

    def _build_params(self, **kwargs: Any) -> dict[str, Any]:
        """
        Build query parameters, filtering out None values.
        Converts snake_case keys to camelCase.

        Args:
            **kwargs: Parameter key-value pairs

        Returns:
            Dictionary with non-None values and camelCase keys
        """
        return {_to_camel_case(k): v for k, v in kwargs.items() if v is not None}

    def _build_payload(self, **kwargs: Any) -> dict[str, Any]:
        """
        Build request payload, filtering out None values.
        Converts snake_case keys to camelCase and handles datetime serialization.

        Args:
            **kwargs: Payload key-value pairs

        Returns:
            Dictionary with non-None values, camelCase keys, and serialized datetimes
        """
        payload: dict[str, Any] = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            camel_key = _to_camel_case(key)
            if isinstance(value, datetime):
                payload[camel_key] = value.isoformat()
            else:
                payload[camel_key] = value
        return payload

    def _path(self, *parts: str) -> str:
        """Build URL path from base path and additional parts."""
        if parts:
            return f"{self._BASE_PATH}/{'/'.join(parts)}"
        return self._BASE_PATH
