"""Keeps every tool result encodable as UTF-8.

API text cut by UTF-16 index can end in half of an emoji (a lone surrogate).
`json` keeps it as-is, and the streamable HTTP writer then fails to encode the
response, so the client never receives it while the call looks successful.
FastMCP 4 serializes a tool's return value inside the tool, before middleware
runs, and fails the call on it: WellFormedOutputTransform repairs the value
first, WellFormedOutputMiddleware repairs error messages and other results.
"""

import functools
import inspect
from collections.abc import Callable
from typing import Any

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.server.transforms import GetToolNext, Transform
from fastmcp.tools import Tool, ToolResult
from fastmcp.tools.function_tool import FunctionTool
from fastmcp.utilities.versions import VersionSpec
from mcp.types import CallToolRequestParams


def well_formed(text: str) -> str:
    """Rejoins split surrogate pairs and replaces lone surrogates with U+FFFD."""
    if text.isascii():
        return text
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return text.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
    return text


def _well_formed_value(value: Any) -> Any:
    if isinstance(value, str):
        return well_formed(value)
    if isinstance(value, list):
        return [_well_formed_value(item) for item in value]
    if isinstance(value, dict):
        return {
            _well_formed_value(key): _well_formed_value(item)
            for key, item in value.items()
        }
    return value


def _well_formed_result(result: ToolResult) -> ToolResult:
    content = [
        block.model_copy(update={"text": well_formed(block.text)})
        if isinstance(getattr(block, "text", None), str)
        else block
        for block in result.content
    ]
    return result.model_copy(
        update={
            "content": content,
            "structured_content": _well_formed_value(result.structured_content),
        }
    )


class WellFormedOutputMiddleware(Middleware):
    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        try:
            result = await call_next(context)
        except ToolError as exc:
            message = str(exc)
            if well_formed(message) == message:
                raise
            raise ToolError(well_formed(message)) from exc.__cause__
        if isinstance(result, ToolResult):
            return _well_formed_result(result)
        return result


def _returning_well_formed(fn: Callable[..., Any]) -> Callable[..., Any]:
    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return _well_formed_value(await fn(*args, **kwargs))

        return async_wrapper

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return _well_formed_value(fn(*args, **kwargs))

    return wrapper


class WellFormedOutputTransform(Transform):
    """Serves each function tool with a body whose return value is well formed.

    Only the tool that runs is wrapped; listings and schemas are untouched.
    """

    def __init__(self) -> None:
        super().__init__()
        # One wrapped copy per tool name, kept while FastMCP serves the same tool.
        self._served: dict[str, tuple[FunctionTool, FunctionTool]] = {}

    async def get_tool(
        self, name: str, call_next: GetToolNext, *, version: VersionSpec | None = None
    ) -> Tool | None:
        tool = await call_next(name, version=version)
        if not isinstance(tool, FunctionTool):
            return tool
        served = self._served.get(tool.name)
        if served is None or served[0] is not tool:
            wrapped = tool.model_copy(update={"fn": _returning_well_formed(tool.fn)})
            served = self._served[tool.name] = (tool, wrapped)
        return served[1]
