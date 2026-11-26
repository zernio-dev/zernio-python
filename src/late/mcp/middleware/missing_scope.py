"""The re-link steps carry no _meta["mcp/www_authenticate"]: for an account that
is already linked, ChatGPT shows no re-link prompt for that challenge and hides
the result's text from the model, so the user only heard "it failed" (tested in
a live account on 2026-11-24). A 403 the token's scope already covers (a team
member with the group turned off, or a write scope that includes the read)
stays the API's own error: re-linking cannot fix it.

The steps key on the tool's first declared scope, not on all its x-oauth-scopes:
the spec lists the :read scope on writes too, and the API now refuses a write
to a token holding only the read, so a link with accounts:read but not
accounts:write would otherwise get a bare error.
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

# The plugin's public page. ChatGPT documents no link that opens its Reconnect.
_PLUGIN_URL = (
    "https://chatgpt.com/plugins/plugin_asdk_app_6aad5ef1fadc81919260bddebb06a407"
)

_SCOPE_PURPOSE = {
    "messaging:read": "read your inbox, comments and messages",
    "ads:read": "read your ad accounts, campaigns and results",
    "contacts:read": "read your contacts and leads",
    "messaging:write": "send messages, replies and broadcasts for you",
    "ads:write": "create ads and pause or resume campaigns, which spends your ad budget",
    "accounts:write": "create, change or remove your profiles and connected accounts",
}


def relink_instructions(needed: str) -> str:
    purpose = _SCOPE_PURPOSE.get(needed, f"use this ({needed})")
    return (
        f"Zernio needs one more permission to {purpose} ('{needed}'); this ChatGPT "
        "connection was set up before Zernio asked for it. Do not retry. Nothing "
        f"changed. Tell the user: open {_PLUGIN_URL}, Settings, ... by your account, "
        "Reconnect, approve, ask again."
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


def _holds(granted: set[str], needed: str) -> bool:
    """A :write scope includes its :read."""
    return needed in granted or (
        needed.endswith(":read") and f"{needed[: -len(':read')]}:write" in granted
    )


def _refused_for_a_group(cause: BaseException | None) -> bool:
    return (
        isinstance(cause, LateAPIError)
        and cause.status_code == 403
        and cause.details.get("code") == _INSUFFICIENT_PERMISSIONS
        and bool(cause.details.get("required_group"))
    )


class MissingScopeMiddleware(Middleware):
    def __init__(self, *, scopes_by_tool: Mapping[str, Sequence[str]]) -> None:
        self._scopes_by_tool = scopes_by_tool

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
            relink_helps = granted is not None and not _holds(granted, reaching[0])
            _log_group_refusal(
                tool=context.message.name,
                needed=reaching[0],
                granted=granted,
                challenged=relink_helps,
            )
            if not relink_helps:
                raise
            return ToolResult(
                content=[
                    TextContent(type="text", text=relink_instructions(reaching[0]))
                ],
                is_error=True,
            )


def _log_group_refusal(
    *, tool: str, needed: str, granted: set[str] | None, challenged: bool
) -> None:
    """`mcp_scope_challenge` and `challenged` keep their names from before the
    challenge was dropped, so Axiom re-link tracking spans the change;
    `challenged` now means the user got the re-link steps."""
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
