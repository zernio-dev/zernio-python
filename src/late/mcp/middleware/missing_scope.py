"""Asks ChatGPT to re-link Zernio when a tool needs an OAuth scope the link never granted.

A ChatGPT link made before a tool's scope was advertised holds a token without
it, and the API refuses that tool with 403 insufficient_permissions. ChatGPT
shows its linking UI only for an error result carrying
_meta["mcp/www_authenticate"], so the 403 is answered with that challenge
instead of a plain error. A 403 the token's scope already covers (a team member
with the group turned off, or a write scope that includes the read) stays a
plain error: re-linking cannot fix it.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools import ToolResult
from mcp.types import CallToolRequestParams, TextContent

from late.client.exceptions import LateAPIError

_INSUFFICIENT_PERMISSIONS = "insufficient_permissions"


def _granted_scopes() -> set[str] | None:
    """The OAuth scope of the calling token, or None for an API key."""
    try:
        token = get_access_token()
    except Exception:
        return None
    scope = token.claims.get("scope") if token else None
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
            granted = _granted_scopes()
            if (
                not reaching
                or granted is None
                or granted.intersection(reaching)
                or not _refused_for_a_group(exc.__cause__)
            ):
                raise
            needed = reaching[0]
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=(
                            f"Zernio needs the '{needed}' permission for this, which this "
                            "ChatGPT connection was not granted. Reconnect Zernio to grant it."
                        ),
                    )
                ],
                meta={"mcp/www_authenticate": [self._challenge]},
                is_error=True,
            )
