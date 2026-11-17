"""Labels feedback filed through the hosted MCP server with its channel and client."""

from typing import Any

from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

FEEDBACK_TOOL = "feedback_submit_feedback"
_FEEDBACK_SOURCE = "zernio-mcp"
# POST /v1/feedback rejects an agent.name longer than this.
_AGENT_NAME_MAX = 100
_CLIENT_NAME_MAX = 40


class FeedbackSourceMiddleware(Middleware):
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
