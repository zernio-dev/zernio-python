"""Records every tool call: one mcp_tool_call log line and one Sentry transaction."""

import asyncio
import json
import time
from collections.abc import Callable
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

import sentry_sdk
from fastmcp.exceptions import ValidationError as InvalidArgumentsError
from fastmcp.server.auth import AccessToken
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams, TextContent
from pydantic import ValidationError as PydanticValidationError

from late.client.exceptions import LateAPIError, LateRateLimitError
from late.mcp.auth import token_cache_key
from late.mcp.response_format import format_stats
from late.mcp.telemetry import (
    TOOL_TRANSACTION_OP,
    is_expected_failure,
    tool_call_logger,
)
from late.mcp.user_agent import calling_client, calling_user_agent

_REJECTED_RESULT_PREFIX = "❌"

_SENTRY_STATUS_BY_OUTCOME = {
    "ok": "ok",
    "rejected": "invalid_argument",
    "cancelled": "cancelled",
    "error": "internal_error",
}

_CALL_TOOL = "call_tool"
# Tools the in-flight call_tool dispatched. FastMCP runs the middleware again
# for the dispatched tool, which records itself with via=call_tool, so the
# wrapper records only when it failed before dispatching anything: each call
# counts once in the logs and in Sentry.
_dispatched_by_call_tool: ContextVar[list[str] | None] = ContextVar(
    "dispatched_by_call_tool", default=None
)


def _current_token() -> AccessToken | None:
    try:
        return get_access_token()
    except Exception:
        return None


def _caller_key() -> str | None:
    token = _current_token()
    return token_cache_key(token.token)[:12] if token and token.token else None


def _auth_fields() -> dict[str, Any]:
    token = _current_token()
    claims = token.claims if token else {}
    if "resolved_by" not in claims:
        return {}
    fields = {"auth": claims["resolved_by"], "auth_wait_ms": claims.get("waited_ms", 0)}
    if claims.get("user_id"):
        fields["user_id"] = claims["user_id"]
    return fields


def _request_fields(arguments: dict[str, Any] | None) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    limit = (arguments or {}).get("limit")
    if isinstance(limit, int):
        fields["limit"] = limit
    client = calling_client()
    if client:
        fields["client"] = client
    return fields


def _is_rejected(result: Any) -> bool:
    content = getattr(result, "content", None) or []
    first = content[0] if content else None
    return isinstance(first, TextContent) and first.text.startswith(
        _REJECTED_RESULT_PREFIX
    )


def _result_chars(result: Any) -> int:
    content = getattr(result, "content", None) or []
    return sum(len(block.text) for block in content if isinstance(block, TextContent))


def _invalid_fields(error: PydanticValidationError) -> str:
    # Field paths and error types only: argument values can carry customer content.
    return ",".join(
        f"{'.'.join(str(part) for part in detail['loc'])}:{detail['type']}"
        for detail in error.errors(include_input=False)
    )


def _pydantic_cause(exc: BaseException) -> PydanticValidationError | None:
    while exc is not None and not isinstance(exc, PydanticValidationError):
        exc = exc.__cause__
    return exc


def _error_fields(exc: Exception) -> dict[str, Any]:
    validation = _pydantic_cause(exc)
    if validation is not None:
        return {
            "error_type": "InvalidArguments"
            if isinstance(exc, InvalidArgumentsError)
            else "ValidationError",
            "invalid_fields": _invalid_fields(validation),
        }
    cause = exc.__cause__ if isinstance(exc.__cause__, Exception) else exc
    fields: dict[str, Any] = {"error_type": type(cause).__name__}
    if isinstance(cause, LateAPIError):
        fields["status_code"] = cause.status_code
    if isinstance(cause, LateRateLimitError) and cause.retry_after is not None:
        fields["retry_after_s"] = cause.retry_after
    return fields


class ToolTelemetryMiddleware(Middleware):
    def __init__(self, surface: str) -> None:
        self._surface = surface

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
    ) -> Any:
        tool = context.message.name
        if tool != _CALL_TOOL:
            dispatched = _dispatched_by_call_tool.get()
            if dispatched is not None:
                dispatched.append(tool)
            via = _CALL_TOOL if dispatched is not None else "direct"
            return await self._record(context, call_next, via=via)

        dispatched = []
        token = _dispatched_by_call_tool.set(dispatched)
        try:
            return await self._record(
                context, call_next, via="direct", silent=lambda: bool(dispatched)
            )
        finally:
            _dispatched_by_call_tool.reset(token)

    async def _record(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: CallNext[CallToolRequestParams, Any],
        *,
        via: str,
        silent: Callable[[], bool] = lambda: False,
    ) -> Any:
        tool = context.message.name
        caller = _caller_key()
        request = _request_fields(context.message.arguments)
        auth = _auth_fields()
        user_agent = calling_user_agent()
        fields: dict[str, Any] = {"outcome": "ok"}
        stats: dict[str, Any] = {}
        stats_token = format_stats.set(stats)
        started = time.perf_counter()
        with (
            sentry_sdk.new_scope() as scope,
            sentry_sdk.start_transaction(
                op=TOOL_TRANSACTION_OP, name=f"tools/call {tool}"
            ) as transaction,
        ):
            if auth.get("user_id"):
                scope.set_user({"id": auth["user_id"]})
            transaction.set_tag("mcp.tool", tool)
            transaction.set_tag("mcp.surface", self._surface)
            transaction.set_tag("mcp.via", via)
            if caller:
                transaction.set_tag("mcp.caller", caller)
            for name, value in request.items():
                transaction.set_tag(f"mcp.{name}", value)
            if auth:
                transaction.set_tag("mcp.auth", auth["auth"])
                transaction.set_data("mcp.auth.wait_ms", auth["auth_wait_ms"])
            try:
                result = await call_next(context)
                if _is_rejected(result):
                    fields["outcome"] = "rejected"
                fields["result_chars"] = _result_chars(result)
                transaction.set_data("mcp.tool.result.chars", fields["result_chars"])
                if "raw_chars" in stats:
                    fields["raw_chars"] = stats["raw_chars"]
                    fields["truncated"] = bool(stats.get("truncated"))
                    transaction.set_data(
                        "mcp.tool.result.raw_chars", stats["raw_chars"]
                    )
                    transaction.set_tag("mcp.truncated", fields["truncated"])
                return result
            except asyncio.CancelledError:
                fields = {"outcome": "cancelled"}
                raise
            except Exception as exc:
                fields = {"outcome": "error", **_error_fields(exc)}
                if not is_expected_failure(exc):
                    sentry_sdk.capture_exception(exc)
                raise
            finally:
                format_stats.reset(stats_token)
                transaction.set_tag("mcp.outcome", fields["outcome"])
                transaction.set_status(_SENTRY_STATUS_BY_OUTCOME[fields["outcome"]])
                if silent():
                    # The tool call_tool dispatched recorded itself; an
                    # unsampled transaction is dropped at finish, not sent.
                    transaction.sampled = False
                else:
                    tool_call_logger.info(
                        json.dumps(
                            {
                                "event": "mcp_tool_call",
                                "ts": datetime.now(timezone.utc).isoformat(
                                    timespec="milliseconds"
                                ),
                                "surface": self._surface,
                                "tool": tool,
                                "via": via,
                                "duration_ms": round(
                                    (time.perf_counter() - started) * 1000
                                ),
                                "caller": caller,
                                **({"user_agent": user_agent} if user_agent else {}),
                                **request,
                                **auth,
                                **fields,
                            }
                        )
                    )
