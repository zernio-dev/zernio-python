import logging
import os
import sys
from collections.abc import Callable
from typing import Any

import sentry_sdk
from fastmcp.exceptions import FastMCPError, NotFoundError, ToolError
from pydantic import ValidationError as PydanticValidationError
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.mcp import MCPIntegration

from late.client.exceptions import LateError
from late.mcp.axiom_sink import axiom_handler_from_env
from late.mcp.constants import SERVICE_VERSION

TOOL_TRANSACTION_OP = "mcp.tool"
_TOOL_ERROR_LOG_PREFIX = "Error calling tool"
_INVALID_ARGUMENTS_LOG_PREFIX = "Invalid arguments for tool"

tool_call_logger = logging.getLogger("late.mcp.tools")


def _tool_call_sampler(rate: float) -> Callable[[dict[str, Any]], float]:
    def sample(sampling_context: dict[str, Any]) -> float:
        is_tool_call = (
            sampling_context["transaction_context"].get("op") == TOOL_TRANSACTION_OP
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
    tool_call_logger.addHandler(handler)
    return True


def log_tool_calls_to_stdout() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    tool_call_logger.addHandler(handler)
    tool_call_logger.setLevel(logging.INFO)
    tool_call_logger.propagate = False


class ServerErrorAccessLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        *_, status_code = record.args
        return status_code >= 500


def argument_errors_without_input(detail: Any) -> str:
    # FastMCP 4 logs its own input-free summary: {"error_count", "error_types"}.
    if isinstance(detail, dict) and isinstance(detail.get("error_types"), list):
        return ", ".join(str(error_type) for error_type in detail["error_types"])
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
            record.args = (tool, argument_errors_without_input(detail))
            return True
        if not message.startswith(_TOOL_ERROR_LOG_PREFIX):
            return True
        exc = record.exc_info[1] if record.exc_info else None
        # FastMCP 4 re-raises a tool body's pydantic error from its own wrapper.
        rejection = exc if isinstance(exc, PydanticValidationError) else getattr(exc, "__cause__", None)
        if isinstance(rejection, PydanticValidationError):
            # An SDK model rejecting an API response: its traceback would log
            # the response values, so keep only where and why it failed.
            errors = rejection.errors(include_url=False, include_context=False, include_input=False)
            record.msg, record.args = "%s: %s", (message, argument_errors_without_input(errors))
            record.exc_info = None
            return True
        return isinstance(exc, Exception) and not is_expected_failure(exc)


def quiet_routine_logs() -> None:
    logging.getLogger("uvicorn.access").addFilter(ServerErrorAccessLogFilter())
    logging.getLogger("fastmcp").setLevel(logging.WARNING)
    logging.getLogger("fastmcp.server.server").addFilter(ToolFailureLogFilter())


def is_expected_failure(exc: Exception) -> bool:
    if isinstance(exc, ToolError) and exc.__cause__ is not None:
        # A generated tool re-wraps what it raised itself, e.g. the refusal
        # of a file too large to return, and FastMCP 4's call_tool re-wraps
        # the NotFoundError of a guessed name (not a FastMCPError).
        return isinstance(exc.__cause__, (LateError, FastMCPError, NotFoundError))
    return isinstance(exc, (FastMCPError, NotFoundError, LateError))
