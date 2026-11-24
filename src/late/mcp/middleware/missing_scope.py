"""Asks ChatGPT to re-link Zernio when a tool needs an OAuth scope the link never granted.

A ChatGPT link made before a tool's scope was advertised holds a token without
it, and the API refuses that tool with 403 insufficient_permissions. ChatGPT
shows its linking UI only for an error result carrying
_meta["mcp/www_authenticate"], so the 403 is answered with that challenge
instead of a plain error. A 403 the token's scope already covers (a team member
with the group turned off, or a write scope that includes the read) stays a
plain error: re-linking cannot fix it.
"""

import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools import ToolResult
from mcp.types import CallToolRequestParams, TextContent

from late.client.exceptions import LateAPIError
from late.mcp.telemetry import tool_call_logger

_INSUFFICIENT_PERMISSIONS = "insufficient_permissions"

_SCOPE_PURPOSE = {
    "messaging:read": "read your inbox, comments and messages",
    "ads:read": "read your ad accounts, campaigns and results",
    "contacts:read": "read your contacts and leads",
    "messaging:write": "send messages, replies and broadcasts for you",
    "automations:write": "change your contacts and automations",
    "accounts:write": "create workflows, profiles and WhatsApp templates",
}


def relink_instructions(needed: str) -> str:
    """What the model tells the user when ChatGPT does not show its re-link prompt."""
    purpose = _SCOPE_PURPOSE.get(needed, f"use this ({needed})")
    return (
        f"Zernio needs one more permission to {purpose} ('{needed}'); this ChatGPT "
        "connection was set up before Zernio asked for it. Nothing was sent or changed. "
        "Tell the user, in these steps: open ChatGPT Settings > Plugins (Apps in some "
        "versions) > Zernio, click ... next to the connected Zernio account, choose "
        "Reconnect, approve the new permission, then ask again."
    )


def _token_claims() -> dict[str, Any]:
    try:
        token = get_access_token()
    except Exception:
        return {}
    return token.claims if token else {}


def _granted_scopes() -> set[str] | None:
    """The OAuth scope of the calling token, or None for an API key."""
    scope = _token_claims().get("scope")
    return set(scope.split()) if isinstance(scope, str) else None


def _refused_for_a_group(cause: BaseException | None) -> bool:
    return (
        isinstance(cause, LateAPIError)
        and cause.status_code == 403
        and cause.details.get("code") == _INSUFFICIENT_PERMISSIONS
        and bool(cause.details.get("required_group"))
    )


class MissingScopeChallengeMiddleware(Middleware):
    def __init__(
        self,
        *,
        scopes_by_tool: Mapping[str, Sequence[str]],
        resource_metadata_url: str,
        scopes: Sequence[str],
    ) -> None:
        self._scopes_by_tool = scopes_by_tool
        self._challenge = (
            f'Bearer resource_metadata="{resource_metadata_url}", '
            f'error="insufficient_scope", scope="{" ".join(scopes)}", '
            'error_description="Reconnect Zernio to grant the permission this needs"'
        )

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        try:
            return await call_next(context)
        except ToolError as exc:
            reaching = self._scopes_by_tool.get(context.message.name)
            if not reaching or not _refused_for_a_group(exc.__cause__):
                raise
            granted = _granted_scopes()
            relink_helps = granted is not None and not granted.intersection(reaching)
            _log_group_refusal(
                tool=context.message.name,
                needed=reaching[0],
                granted=granted,
                challenged=relink_helps,
            )
            if not relink_helps:
                raise
            needed = reaching[0]
            return ToolResult(
                content=[TextContent(type="text", text=relink_instructions(needed))],
                meta={"mcp/www_authenticate": [self._challenge]},
                is_error=True,
            )


def _log_group_refusal(
    *, tool: str, needed: str, granted: set[str] | None, challenged: bool
) -> None:
    """One line per group 403 on a scoped tool, so a missing re-link prompt shows in Axiom."""
    tool_call_logger.info(
        json.dumps(
            {
                "event": "mcp_scope_challenge",
                "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                "surface": "chatgpt",
                "tool": tool,
                "needed_scope": needed,
                "token_scope": " ".join(sorted(granted))
                if granted is not None
                else None,
                "challenged": challenged,
                "user_id": _token_claims().get("user_id"),
            }
        )
    )
