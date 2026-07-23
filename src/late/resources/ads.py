"""
Backward-compat `ads` resource.

The `ads` API was split into capability-specific resources. This alias forwards
each call to the right resource and emits a DeprecationWarning, so existing code
keeps working. It will be removed in a future major version.

This is a hand-written (manual) resource; it overrides any auto-generated
`_generated/ads.py`. Do not replace it with a generated file.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client.base import BaseClient

# Resources the old `ads` namespace was split into, checked in this order when
# resolving a forwarded method.
_AD_RESOURCES = [
    "ad_campaigns",
    "ad_accounts",
    "ad_creatives",
    "ad_audiences",
    "ad_targeting",
    "ad_insights",
    "conversions",
    "messaging_ads",
    "reach_and_frequency",
    "lead_gen",
    "tracking_tags",
]


class AdsResource:
    """
    Deprecated. The `ads` resource was split into: ad_campaigns, ad_accounts,
    ad_creatives, ad_audiences, ad_targeting, ad_insights, conversions,
    messaging_ads, reach_and_frequency, lead_gen, tracking_tags.

    Calls still work (forwarded to the right resource) but emit a
    DeprecationWarning. Migrate to the resource named in the warning.
    """

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def __getattr__(self, name: str) -> Any:
        # __getattr__ only runs when normal lookup fails, so `_client` (set in
        # __init__) is resolved normally and never recurses here.
        for resource_name in _AD_RESOURCES:
            resource = getattr(self._client, resource_name, None)
            if resource is not None and hasattr(resource, name):
                warnings.warn(
                    f"`ads.{name}()` is deprecated: the `ads` resource was split. "
                    f"Use `{resource_name}.{name}()` instead. "
                    f"`ads` will be removed in a future major version.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return getattr(resource, name)
        raise AttributeError(f"'AdsResource' object has no attribute '{name}'")
