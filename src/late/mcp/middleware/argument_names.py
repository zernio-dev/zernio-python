"""Renames camelCase arguments to the snake_case parameters the tools take.

Agents send the names the REST API and its docs use (postId, accountId,
contentType, mediaItems); every tool takes snake_case, so pydantic rejected
several hundred calls a day from 100+ users (Axiom zernio-mcp, 2026-11).

A key the tool does not take is renamed only when, with case, underscores and
hyphens ignored, it names exactly one parameter that the call did not also
pass and no other key claims. An explicit snake_case value is never
overwritten, nested keys are left as they are (dict parameters go to the API
verbatim), and an unknown key is left for validation to reject. FastMCP runs the middleware again for the tool
call_tool dispatches, so proxied arguments are covered too.
"""

from collections import Counter
from collections.abc import Mapping
from typing import Any

from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams


def _folded(name: str) -> str:
    return name.replace("_", "").replace("-", "").lower()


def _may_need_renaming(key: str) -> bool:
    return key != key.lower() or "-" in key


class ArgumentNamesMiddleware(Middleware):
    def __init__(
        self, *, aliases: Mapping[str, Mapping[str, str]] | None = None
    ) -> None:
        # Per tool, names that do not fold to the parameter: call_tool's
        # tool_name for name, say.
        self._aliases = {tool: dict(names) for tool, names in (aliases or {}).items()}
        # Tool name -> its parameters by folded name; a folded name two
        # parameters share maps to None. Tools never change at runtime.
        self._parameters: dict[str, tuple[frozenset[str], dict[str, str | None]]] = {}

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        params = context.message
        arguments = params.arguments
        if not arguments:
            return await call_next(context)
        aliases = self._aliases.get(params.name, {})
        # Nearly every call already uses snake_case: skip the tool lookup.
        if not any(_may_need_renaming(key) or key in aliases for key in arguments):
            return await call_next(context)
        parameters = await self._tool_parameters(params.name, context)
        if parameters is None:
            return await call_next(context)
        renamed = _renamed(arguments, *parameters, aliases)
        if renamed is None:
            return await call_next(context)
        return await call_next(
            context.copy(message=params.model_copy(update={"arguments": renamed}))
        )

    async def _tool_parameters(
        self, name: str, context: MiddlewareContext[CallToolRequestParams]
    ) -> tuple[frozenset[str], dict[str, str | None]] | None:
        cached = self._parameters.get(name)
        if cached is not None:
            return cached
        ctx = context.fastmcp_context
        if ctx is None:
            return None
        try:
            tool = await ctx.fastmcp.get_tool(name)
        except Exception:
            # An unknown or hidden tool fails in call_next with its own error.
            return None
        if tool is None:
            return None
        names = frozenset((tool.parameters or {}).get("properties") or {})
        by_folded: dict[str, str | None] = {}
        for parameter in names:
            folded = _folded(parameter)
            by_folded[folded] = None if folded in by_folded else parameter
        self._parameters[name] = (names, by_folded)
        return self._parameters[name]


def _renamed(
    arguments: dict[str, Any],
    names: frozenset[str],
    by_folded: dict[str, str | None],
    aliases: dict[str, str],
) -> dict[str, Any] | None:
    """The arguments with misnamed keys renamed, or None when none were."""
    targets: dict[str, str] = {}
    for key in arguments:
        if key in names:
            continue
        target = aliases.get(key) or by_folded.get(_folded(key))
        if target and target in names and target not in arguments:
            targets[key] = target
    claims = Counter(targets.values())
    # Two keys claiming one parameter (postId and PostID): which value was
    # meant is unknowable, so both are left for validation to reject.
    targets = {key: target for key, target in targets.items() if claims[target] == 1}
    if not targets:
        return None
    return {targets.get(key, key): value for key, value in arguments.items()}
