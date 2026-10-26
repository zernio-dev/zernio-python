"""Every SDK call in the generated MCP tools must bind to the real client method.

generated_tools.py and the SDK resources are regenerated together, but the
hand-written resources can shadow or hide generated methods. When they drift,
the MCP tool raises TypeError/AttributeError on every call (e.g.
accounts_get_follower_stats after limit/cursor were added). This check runs
in CI on regen PRs, so drift fails before deploy.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from late import Late

GENERATED_TOOLS = (
    Path(__file__).resolve().parents[1] / "src" / "late" / "mcp" / "generated_tools.py"
)


def _sdk_calls() -> list[tuple[str, str, str, int, list[str]]]:
    """(tool, resource, method, positional arg count, keyword names) for each
    ``client.<resource>.<method>(...)`` call, keyed by its innermost function."""
    calls = []

    def visit(node: ast.AST, func_name: str) -> None:
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Attribute)
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.value.id == "client"
        ):
            calls.append(
                (
                    func_name,
                    node.func.value.attr,
                    node.func.attr,
                    len(node.args),
                    [kw.arg for kw in node.keywords if kw.arg is not None],
                )
            )
        for child in ast.iter_child_nodes(node):
            visit(child, func_name)

    visit(ast.parse(GENERATED_TOOLS.read_text()), "<module>")
    return calls


# Known mismatches left as-is; strict=True flags an entry once it starts passing.
KNOWN_FAILURES = {
    "tools_download_tik_tok_video": "ToolsResource does not expose the generated method",
}

SDK_CALLS = _sdk_calls()


def test_sdk_calls_found() -> None:
    assert len(SDK_CALLS) > 100


@pytest.fixture(scope="module")
def client() -> Late:
    return Late(api_key="x")


@pytest.mark.parametrize(
    ("tool", "resource", "method", "n_args", "kwargs"),
    [
        pytest.param(
            *call,
            id=call[0],
            marks=(
                [pytest.mark.xfail(reason=KNOWN_FAILURES[call[0]], strict=True)]
                if call[0] in KNOWN_FAILURES
                else []
            ),
        )
        for call in SDK_CALLS
    ],
)
def test_mcp_tool_call_matches_sdk_signature(
    client: Late,
    tool: str,
    resource: str,
    method: str,
    n_args: int,
    kwargs: list[str],
) -> None:
    fn = getattr(getattr(client, resource, None), method, None)
    assert fn is not None, f"{tool}: client.{resource}.{method} does not exist"

    try:
        inspect.signature(fn).bind(*[None] * n_args, **dict.fromkeys(kwargs))
    except TypeError as e:
        pytest.fail(f"{tool}: client.{resource}.{method}(...) does not bind: {e}")
