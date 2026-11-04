import asyncio
import json
import logging
import os
import sys
import time
from collections.abc import Callable
from typing import Any

import sentry_sdk
from fastmcp.exceptions import FastMCPError, NotFoundError, ToolError
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from mcp.types import CallToolRequestParams, TextContent
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.mcp import MCPIntegration

from late.client.exceptions import LateAPIError, LateError
from late.mcp.auth import token_cache_key
from late.mcp.constants import SERVICE_VERSION

_TOOL_TRANSACTION_OP = "mcp.tool"
_REJECTED_RESULT_PREFIX = "❌"

_SENTRY_STATUS_BY_OUTCOME = {
    "ok": "ok",
    "rejected": "invalid_argument",
    "cancelled": "cancelled",
    "error": "internal_error",
}

_tool_logger = logging.getLogger("late.mcp.tools")


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


def log_tool_calls_to_stdout() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    _tool_logger.addHandler(handler)
    _tool_logger.setLevel(logging.INFO)
    _tool_logger.propagate = False


def _caller_key() -> str | None:
    try:
        token = get_access_token()
    except Exception:
        return None
    return token_cache_key(token.token)[:12] if token and token.token else None


def _is_rejected(result: Any) -> bool:
    content = getattr(result, "content", None) or []
    first = content[0] if content else None
    return isinstance(first, TextContent) and first.text.startswith(
        _REJECTED_RESULT_PREFIX
    )


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
        fields: dict[str, Any] = {"outcome": "ok"}
        started = time.perf_counter()
        with sentry_sdk.start_transaction(
            op=_TOOL_TRANSACTION_OP, name=f"tools/call {tool}"
        ) as transaction:
            transaction.set_tag("mcp.tool", tool)
            transaction.set_tag("mcp.surface", self._surface)
            try:
                result = await call_next(context)
                if _is_rejected(result):
                    fields["outcome"] = "rejected"
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
                transaction.set_tag("mcp.outcome", fields["outcome"])
                transaction.set_status(_SENTRY_STATUS_BY_OUTCOME[fields["outcome"]])
                _tool_logger.info(
                    json.dumps(
                        {
                            "event": "mcp_tool_call",
                            "surface": self._surface,
                            "tool": tool,
                            "duration_ms": round(
                                (time.perf_counter() - started) * 1000
                            ),
                            "caller": _caller_key(),
                            **fields,
                        }
                    )
                )
