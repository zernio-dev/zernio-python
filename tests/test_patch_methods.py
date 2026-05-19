"""Regression tests for PATCH methods on BaseClient.

The SDK used to call ``self._client._patch(...)`` from 13 generated PATCH
endpoints, but ``_patch`` (and the async ``_apatch``) were never defined on
``BaseClient`` — every PATCH call raised
``AttributeError: 'Zernio' object has no attribute '_patch'``.

These tests lock in two things:
1. The methods exist on ``BaseClient``.
2. End-to-end through the resource layer: an SDK call like
   ``client.contacts.update_contact(...)`` actually issues a real PATCH
   request with the right method, path, and body. We mock the HTTP layer
   so we can assert on what went on the wire.
"""

from __future__ import annotations

import pytest
import respx

from late import Zernio
from late.client.base import BaseClient


class TestPatchMethodsExist:
    """``_patch`` and ``_apatch`` must be defined on ``BaseClient``."""

    def test_sync_patch_exists(self) -> None:
        assert hasattr(BaseClient, "_patch")
        assert callable(BaseClient._patch)

    def test_async_apatch_exists(self) -> None:
        assert hasattr(BaseClient, "_apatch")
        assert callable(BaseClient._apatch)


class TestPatchEndToEnd:
    """End-to-end: SDK resource method -> HTTP PATCH on the wire."""

    def test_update_contact_sends_patch_with_body(self, api_key: str) -> None:
        # Soma's exact failing case: update_contact with tags.
        contact_id = "6a09a6adb798eb3335fb6377"
        with respx.mock(base_url="https://zernio.com/api") as mock:
            route = mock.patch(f"/v1/contacts/{contact_id}").respond(
                200, json={"success": True, "contact": {"id": contact_id, "tags": ["Scam"]}}
            )

            client = Zernio(api_key=api_key)
            result = client.contacts.update_contact(contact_id, tags=["Scam"])

        assert route.called
        sent = route.calls.last.request
        assert sent.method == "PATCH"
        assert sent.url.path == f"/api/v1/contacts/{contact_id}"
        assert sent.content.decode() == '{"tags":["Scam"]}'
        assert result == {"success": True, "contact": {"id": contact_id, "tags": ["Scam"]}}

    def test_complete_telegram_connect_sends_patch_with_query(self, api_key: str) -> None:
        # The one PATCH endpoint that uses query params, not a body.
        # Must work without a body — _patch has to accept params= kwarg.
        with respx.mock(base_url="https://zernio.com/api") as mock:
            route = mock.patch("/v1/connect/telegram").respond(
                200, json={"status": "connected"}
            )

            client = Zernio(api_key=api_key)
            result = client.connect.complete_telegram_connect(code="abc123")

        assert route.called
        sent = route.calls.last.request
        assert sent.method == "PATCH"
        assert sent.url.query.decode() == "code=abc123"
        assert result == {"status": "connected"}

    @pytest.mark.asyncio
    async def test_aupdate_contact_sends_patch_with_body(self, api_key: str) -> None:
        contact_id = "abc123"
        with respx.mock(base_url="https://zernio.com/api") as mock:
            route = mock.patch(f"/v1/contacts/{contact_id}").respond(
                200, json={"success": True}
            )

            async with Zernio(api_key=api_key) as client:
                result = await client.contacts.aupdate_contact(contact_id, tags=["Async"])

        assert route.called
        sent = route.calls.last.request
        assert sent.method == "PATCH"
        assert sent.content.decode() == '{"tags":["Async"]}'
        assert result == {"success": True}
