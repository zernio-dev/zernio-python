"""Keeps every tool result encodable as UTF-8.

API text cut by UTF-16 index can end in half of an emoji (a lone surrogate).
`json` keeps it as-is, and the streamable HTTP writer then fails to encode the
response, so the client never receives it while the call looks successful.
"""

from typing import Any

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.tool import ToolResult
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
