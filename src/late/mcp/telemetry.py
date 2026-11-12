import asyncio
import json
import logging
import os
import sys
import time
from collections.abc import Callable
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

import sentry_sdk
from fastmcp.exceptions import FastMCPError, NotFoundError, ToolError
from fastmcp.server.auth import AccessToken
from fastmcp.server.dependencies import get_access_token, get_http_headers
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams, TextContent
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.mcp import MCPIntegration

from late.client.exceptions import LateAPIError, LateError
from late.mcp.auth import token_cache_key
from late.mcp.axiom_sink import axiom_handler_from_env
from late.mcp.constants import SERVICE_VERSION
from late.mcp.response_format import format_stats

_TOOL_TRANSACTION_OP = "mcp.tool"
_REJECTED_RESULT_PREFIX = "❌"
_TOOL_ERROR_LOG_PREFIX = "Error calling tool"
_INVALID_ARGUMENTS_LOG_PREFIX = "Invalid arguments for tool"

_SENTRY_STATUS_BY_OUTCOME = {
    "ok": "ok",
    "rejected": "invalid_argument",
    "cancelled": "cancelled",
    "error": "internal_error",
}

_tool_logger = logging.getLogger("late.mcp.tools")

_CALL_TOOL = "call_tool"
# Tools the in-flight call_tool dispatched. FastMCP runs the middleware again
# for the dispatched tool, which records itself with via=call_tool, so the
# wrapper records only when it failed before dispatching anything: each call
# counts once in the logs and in Sentry.
_dispatched_by_call_tool: ContextVar[list[str] | None] = ContextVar(
    "dispatched_by_call_tool", default=None
)


def _tool_call_sampler(rate: float) -> Callable[[dict[str, Any]], float]:
    def sample(sampling_context: dict[str, Any]) -> float:
        is_tool_call = (
            sampling_context["transaction_context"].get("op") == _TOOL_TRANSACTION_OP
        )
        return rate if is_tool_call else 0.0

    return sample


def init_sentry() -> bool:
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        return False
    tool_call_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE") or "1.0")
    ignore_logger("fastmcp.server.server")
    sentry_sdk.init(
        dsn=dsn,
        release=os.getenv("RAILWAY_GIT_COMMIT_SHA") or SERVICE_VERSION,
        environment=os.getenv("RAILWAY_ENVIRONMENT_NAME") or "production",
        traces_sampler=_tool_call_sampler(tool_call_sample_rate),
        send_default_pii=False,
        disabled_integrations=[MCPIntegration()],
    )
    return True


def ship_tool_calls_to_axiom() -> bool:
    handler = axiom_handler_from_env()
    if handler is None:
        return False
    _tool_logger.addHandler(handler)
    return True


def log_tool_calls_to_stdout() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    _tool_logger.addHandler(handler)
    _tool_logger.setLevel(logging.INFO)
    _tool_logger.propagate = False


class ServerErrorAccessLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        *_, status_code = record.args
        return status_code >= 500


def _argument_errors_without_input(detail: Any) -> str:
    if not isinstance(detail, list):
        return "details omitted"
    return ", ".join(
        f"{'.'.join(str(part) for part in error['loc'])}: {error['type']}"
        for error in detail
    )


class ToolFailureLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = str(record.msg)
        if message.startswith(_INVALID_ARGUMENTS_LOG_PREFIX):
            tool, detail = record.args
            record.args = (tool, _argument_errors_without_input(detail))
            return True
        if not message.startswith(_TOOL_ERROR_LOG_PREFIX):
            return True
        exc = record.exc_info[1] if record.exc_info else None
        return isinstance(exc, Exception) and not _is_expected_failure(exc)


def quiet_routine_logs() -> None:
    logging.getLogger("uvicorn.access").addFilter(ServerErrorAccessLogFilter())
    logging.getLogger("fastmcp").setLevel(logging.WARNING)
    logging.getLogger("fastmcp.server.server").addFilter(ToolFailureLogFilter())


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
    return {"auth": claims["resolved_by"], "auth_wait_ms": claims.get("waited_ms", 0)}


def _request_fields(arguments: dict[str, Any] | None) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    limit = (arguments or {}).get("limit")
    if isinstance(limit, int):
        fields["limit"] = limit
    client = get_http_headers().get("user-agent", "").split("/", 1)[0].strip()
    if client:
        fields["client"] = client[:64]
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


def _error_fields(exc: Exception) -> dict[str, Any]:
    cause = exc.__cause__ if isinstance(exc.__cause__, Exception) else exc
    fields: dict[str, Any] = {"error_type": type(cause).__name__}
    if isinstance(cause, LateAPIError):
        fields["status_code"] = cause.status_code
    return fields


def _is_expected_failure(exc: Exception) -> bool:
    if isinstance(exc, ToolError) and exc.__cause__ is not None:
        return isinstance(exc.__cause__, LateError)
    return isinstance(exc, (FastMCPError, NotFoundError, LateError))


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
        fields: dict[str, Any] = {"outcome": "ok"}
        stats: dict[str, Any] = {}
        stats_token = format_stats.set(stats)
        started = time.perf_counter()
        with sentry_sdk.start_transaction(
            op=_TOOL_TRANSACTION_OP, name=f"tools/call {tool}"
        ) as transaction:
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
                if not _is_expected_failure(exc):
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
                    _tool_logger.info(
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
                                **request,
                                **auth,
                                **fields,
                            }
                        )
                    )
