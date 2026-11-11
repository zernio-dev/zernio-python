"""Turns the two commonest agent mistakes with search_tools/call_tool into a result or a hint.

Wrapping search_tools in call_tool, which FastMCP refuses, and guessing tool
names, which returned a bare "Unknown tool", cost about 180 failed calls a day.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from fastmcp.exceptions import NotFoundError, ToolError
from fastmcp.server.context import Context
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

ClosestTools = Callable[[str, Context | None], Awaitable[list[str]]]


class ToolGuidanceMiddleware(Middleware):
    def __init__(
        self, *, search_tool: str, call_tool: str, closest_tools: ClosestTools
    ) -> None:
        self._search_tool = search_tool
        self._call_tool = call_tool
        self._closest_tools = closest_tools

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        context = self._run_proxied_search_directly(context)
        try:
            return await call_next(context)
        except NotFoundError as exc:
            if not str(exc).startswith("Unknown tool"):
                raise
            # A ToolError reaches the model as a tool result; FastMCP re-wraps a
            # NotFoundError and would drop the suggestions.
            raise ToolError(await self._unknown_tool_message(context)) from None

    def _run_proxied_search_directly(
        self, context: MiddlewareContext[CallToolRequestParams]
    ) -> MiddlewareContext[CallToolRequestParams]:
        params = context.message
        arguments = params.arguments or {}
        if params.name != self._call_tool or arguments.get("name") != self._search_tool:
            return context
        search = params.model_copy(
            update={
                "name": self._search_tool,
                "arguments": arguments.get("arguments") or {},
            }
        )
        return context.copy(message=search)

    async def _unknown_tool_message(
        self, context: MiddlewareContext[CallToolRequestParams]
    ) -> str:
        name = context.message.name
        closest = await self._closest_tools(name, context.fastmcp_context)
        hint = f" Closest tools: {', '.join(closest)}." if closest else ""
        return (
            f"Unknown tool {name!r}.{hint} Never guess tool names: call {self._search_tool} "
            f"with what you want to do, then {self._call_tool} with the exact name it returns."
        )
