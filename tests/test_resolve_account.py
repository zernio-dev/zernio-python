"""Unit tests for `_resolve_account` - the multi-account disambiguation
helper that replaced silent matching[0] selection in the MCP write tools.

Coverage:
  1. account_id happy path
  2. account_id present but the account belongs to a different platform
  3. account_id not found / not accessible
  4. profile_id with exactly one matching account on the platform
  5. profile_id with no matching accounts (scoped error)
  6. ambiguous selection (>=2 accounts) without account_id raises with the
     candidate list in the error message
  7. no accounts at all raises with available platforms (empty)

These tests use a stubbed Zernio client so they run offline and don't depend
on any HTTP fixtures. The contract being tested is purely:
    inputs -> account, or inputs -> ValueError(<message>)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from late.mcp.server import _resolve_account


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------


@dataclass
class _Account:
    """Stand-in for the SDK Account model. Only exposes the fields the
    resolver actually reads (field_id, platform, username, displayName)."""

    field_id: str
    platform: str
    username: str = ""
    displayName: str = ""


@dataclass
class _ListResponse:
    accounts: list[_Account]


class _AccountsResource:
    """Stub of `client.accounts` that returns a fixed list, optionally
    scoped by profile_id (matching the real SDK signature)."""

    def __init__(self, all_accounts: list[_Account], by_profile: dict[str, list[_Account]] | None = None):
        self._all = all_accounts
        self._by_profile = by_profile or {}

    def list(self, *, profile_id: str | None = None) -> _ListResponse:
        if profile_id:
            return _ListResponse(accounts=self._by_profile.get(profile_id, []))
        return _ListResponse(accounts=self._all)


class _Client:
    def __init__(self, accounts: _AccountsResource):
        self.accounts = accounts


def _make_client(
    all_accounts: list[_Account],
    by_profile: dict[str, list[_Account]] | None = None,
) -> Any:
    return _Client(_AccountsResource(all_accounts, by_profile))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_account_id_happy_path() -> None:
    """When account_id is given and matches a real account on the requested
    platform, return that account directly."""
    accs = [
        _Account(field_id="acc_1", platform="twitter", username="acme"),
        _Account(field_id="acc_2", platform="twitter", username="beta"),
    ]
    client = _make_client(accs)

    result = _resolve_account(client, "twitter", account_id="acc_2")

    assert result.field_id == "acc_2"
    assert result.username == "beta"


def test_account_id_wrong_platform_errors() -> None:
    """If account_id resolves to a real account but for the wrong platform,
    raise ValueError so the LLM can't post to the wrong network."""
    accs = [_Account(field_id="acc_1", platform="linkedin", username="bob")]
    client = _make_client(accs)

    with pytest.raises(ValueError, match="is a linkedin account, not twitter"):
        _resolve_account(client, "twitter", account_id="acc_1")


def test_account_id_not_found_errors() -> None:
    """Unknown / inaccessible account_id raises explicitly rather than
    falling back to auto-resolution."""
    client = _make_client([_Account(field_id="acc_1", platform="twitter")])

    with pytest.raises(ValueError, match="not found or not accessible"):
        _resolve_account(client, "twitter", account_id="acc_does_not_exist")


def test_profile_id_single_match_returns_account() -> None:
    """profile_id scopes the lookup; when exactly one account in that
    profile matches the platform, return it."""
    in_profile = [_Account(field_id="acc_p1", platform="twitter", username="acme")]
    out_of_profile = [_Account(field_id="acc_o1", platform="twitter", username="other")]
    client = _make_client(
        all_accounts=in_profile + out_of_profile,
        by_profile={"prof_acme": in_profile},
    )

    result = _resolve_account(client, "twitter", profile_id="prof_acme")

    assert result.field_id == "acc_p1"


def test_profile_id_no_match_errors_with_scope() -> None:
    """When the profile exists but has no account on the requested platform,
    the error should mention the profile so the LLM knows where to look."""
    client = _make_client(
        all_accounts=[],
        by_profile={"prof_x": [_Account(field_id="acc_p", platform="linkedin")]},
    )

    with pytest.raises(ValueError, match="in profile prof_x"):
        _resolve_account(client, "twitter", profile_id="prof_x")


def test_ambiguous_selection_lists_candidates() -> None:
    """The core bug fix: when 2+ accounts match without an explicit
    account_id, raise ValueError with all candidate IDs in the message so
    the LLM can pick one and retry. Previously this silently returned
    matching[0], which routed agency posts to the wrong client."""
    accs = [
        _Account(field_id="acc_1", platform="twitter", username="acme"),
        _Account(field_id="acc_2", platform="twitter", username="beta"),
        _Account(field_id="acc_3", platform="twitter", username="gamma"),
    ]
    client = _make_client(accs)

    with pytest.raises(ValueError) as exc_info:
        _resolve_account(client, "twitter")

    msg = str(exc_info.value)
    assert "Multiple twitter accounts" in msg
    # Every candidate ID must appear so the LLM has the full menu.
    assert "acc_1" in msg
    assert "acc_2" in msg
    assert "acc_3" in msg
    # Usernames help the LLM pick by semantic name.
    assert "acme" in msg
    assert "beta" in msg


def test_no_accounts_at_all_errors() -> None:
    """When the user has no accounts, the error should still be readable
    and mention an empty available-platforms list."""
    client = _make_client([])

    with pytest.raises(ValueError, match="No twitter account found"):
        _resolve_account(client, "twitter")
