"""Tells an agent how long a rate limit lasts, so it waits instead of retrying into it.

429s were 84% of tool errors in production (433,000 in the week to Nov 18), and
agents called again at once: the message said "Rate limit exceeded" and dropped
the API's Retry-After, its explanation, and whether the quota was Zernio's or a
platform's (Meta, Google, Reddit), where an early retry cannot succeed.
"""

import math
from typing import Any

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams

from late.client.exceptions import LateAPIError, LateRateLimitError


def wait_hint(
    retry_after: float | None, *, platform: str | None = None, resets_at: str | None = None
) -> str:
    """What to do next, for an agent that just hit a rate limit."""
    if retry_after is not None:
        return (
            f"Wait {math.ceil(retry_after)} seconds before calling this again; "
            "an earlier call fails the same way."
        )
    if platform:
        until = f" until {resets_at}" if resets_at else ""
        return (
            f"This is the connected account's {platform} quota, not a Zernio limit: "
            f"calls fail{until}. Do not retry it now."
        )
    if resets_at:
        return f"Wait until {resets_at} before calling this again."
    return "Wait before calling this again; an immediate retry fails the same way."


def rate_limit_message(error: LateRateLimitError) -> str:
    details = error.details.get("details")
    resets_at = details.get("resetsAt") if isinstance(details, dict) else None
    if resets_at is None and error.reset_time and not error.details.get("platform"):
        resets_at = error.reset_time.isoformat()
    hint = wait_hint(
        error.retry_after, platform=error.details.get("platform"), resets_at=resets_at
    )
    # LateAPIError's form keeps the API's message and code without the
    # retry suffix, which the hint states for the agent.
    return f"Error: {LateAPIError.__str__(error).rstrip('.')}. {hint}"


class RateLimitGuidanceMiddleware(Middleware):
    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        try:
            return await call_next(context)
        except ToolError as exc:
            limit = exc.__cause__
            if not isinstance(limit, LateRateLimitError):
                raise
            raise ToolError(rate_limit_message(limit)) from limit
