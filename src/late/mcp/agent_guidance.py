"""Middleware that turns common agent mistakes into calls or errors an agent can act on.

Agents reach most tools through search_tools and call_tool. Two mistakes cost
about 150 failed calls a day before this: wrapping search_tools in call_tool,
which FastMCP refuses, and guessing tool names, which returned a bare
"Unknown tool" with nothing to retry with.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from fastmcp.exceptions import NotFoundError, ToolError
from fastmcp.server.context import Context
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

FEEDBACK_TOOL = "feedback_submit_feedback"
_FEEDBACK_SOURCE = "zernio-mcp"
# POST /v1/feedback rejects an agent.name longer than this.
_AGENT_NAME_MAX = 100
_CLIENT_NAME_MAX = 40

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


class FeedbackSourceMiddleware(Middleware):
    """Labels every feedback report filed through this server with its channel and client."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        if context.message.name == FEEDBACK_TOOL:
            labelled = context.message.model_copy(
                update={
                    "arguments": with_feedback_source(context.message.arguments or {})
                }
            )
            context = context.copy(message=labelled)
        return await call_next(context)


def with_feedback_source(arguments: dict[str, Any]) -> dict[str, Any]:
    client = get_http_headers().get("user-agent", "").split(" ")[0][:_CLIENT_NAME_MAX]
    source = f"{_FEEDBACK_SOURCE} ({client})" if client else _FEEDBACK_SOURCE
    agent = dict(arguments.get("agent") or {})
    reported = agent.get("name")
    agent["name"] = (f"{reported} via {source}" if reported else source)[
        :_AGENT_NAME_MAX
    ]
    return {**arguments, "agent": agent}
