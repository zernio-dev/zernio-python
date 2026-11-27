"""Turns the two commonest agent mistakes with search_tools/call_tool into a result or a hint.

Wrapping search_tools in call_tool, which FastMCP refuses, and guessing tool
names, which returned a bare "Unknown tool", cost about 180 failed calls a day.
Wrapping call_tool in itself is refused too, but with the call to make instead.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from fastmcp.exceptions import NotFoundError, ToolError
from fastmcp.server.context import Context
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

from late.mcp.telemetry import is_synthetic_tool_refusal

ClosestTools = Callable[[str, Context | None], Awaitable[list[str]]]

# How many call_tool wrappers to look through for the tool the agent meant.
_MAX_NESTING = 10


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
            if not _is_unknown_tool(exc):
                raise
            # A ToolError reaches the model as a tool result; FastMCP re-wraps a
            # NotFoundError and would drop the suggestions.
            raise ToolError(await self._unknown_tool_message(context.message.name, context)) from None
        except ToolError as exc:
            if context.message.name != self._call_tool:
                raise
            arguments = context.message.arguments or {}
            if is_synthetic_tool_refusal(exc):
                raise ToolError(self._nested_call_tool_message(arguments)) from None
            # call_tool checks the name itself and wraps its NotFoundError.
            if not _is_unknown_tool(exc.__cause__):
                raise
            raise ToolError(await self._unknown_tool_message(arguments.get("name"), context)) from None

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

    def _nested_call_tool_message(self, arguments: dict[str, Any]) -> str:
        inner = _wrapped_tool_name(arguments, self._call_tool)
        refusal = f"{self._call_tool} runs other tools; don't wrap {self._call_tool} in itself."
        if inner == self._search_tool:
            return f"{refusal} Call {self._search_tool} directly with its arguments."
        if inner:
            return f"{refusal} Call {self._call_tool} with name={inner!r} and its arguments directly."
        return (
            f"{refusal} Call {self._search_tool} with what you want to do, "
            f"then {self._call_tool} with the exact name it returns."
        )

    async def _unknown_tool_message(
        self, name: str, context: MiddlewareContext[CallToolRequestParams]
    ) -> str:
        closest = await self._closest_tools(name, context.fastmcp_context)
        hint = f" Closest tools: {', '.join(closest)}." if closest else ""
        return (
            f"Unknown tool {name!r}.{hint} Never guess tool names: call {self._search_tool} "
            f"with what you want to do, then {self._call_tool} with the exact name it returns."
        )


def _wrapped_tool_name(arguments: dict[str, Any], call_tool: str) -> str | None:
    """The tool inside call_tool(name=call_tool, arguments=...), through nested wrappers."""
    for _ in range(_MAX_NESTING):
        if arguments.get("name") != call_tool:
            break
        inner = arguments.get("arguments")
        if not isinstance(inner, dict):
            return None
        arguments = inner
    name = arguments.get("name")
    if not isinstance(name, str) or not name.strip() or name == call_tool:
        return None
    return name.strip()


def _is_unknown_tool(exc: BaseException | None) -> bool:
    return isinstance(exc, NotFoundError) and str(exc).startswith("Unknown tool")
