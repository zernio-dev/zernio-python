"""MCP Apps: the interactive views Claude and ChatGPT render for tool results.

A trial, off unless ZERNIO_MCP_APPS=1, kept in this package so it can be
removed in one go: delete it and the apps lines in server.py.

Each view is one self-contained HTML document under ``ui://zernio/``, built
from a template in this package plus the shared runtime.js (the host bridge)
and base.css (host theme tokens with zernio.com fallbacks). Inline scripts
and styles only, so the host can review the whole document and no CDN sits
in the render path. The show_* tools in tools.py are the views' entry points.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from fastmcp.apps import UI_MIME_TYPE, AppConfig, ResourceCSP, app_config_to_meta_dict
from fastmcp.resources import TextResource
from fastmcp.tools import ToolResult
from mcp.types import ToolAnnotations

from .tools import register_tools

if TYPE_CHECKING:
    from fastmcp import FastMCP

_DIR = Path(__file__).parent

# Hosts cache ui:// resources aggressively: bump on a change an old cached view
# could not handle (a new data shape, a renamed tool it calls).
_VERSION = "v1"

# Images in post previews come from Zernio media storage; Claude serves its
# host fonts from assets.claude.ai. Nothing else is fetched, and views reach
# the API only through the host (tools/call), so connectDomains stays empty.
_CSP = ResourceCSP(
    resource_domains=["https://media.zernio.com", "https://assets.claude.ai"],
)

VIEWS = {
    "overview": "Zernio overview card",
    "post-preview": "Post preview",
    "failed-posts": "Failed posts",
    "analytics": "Analytics",
    "account-health": "Account health",
    "ads-alerts": "Ads alerts",
    "automation-approvals": "Automation approvals",
}

# Listed up front while the trial is on. The ui_* tools are app-only: listed
# so the host lets the views call them, hidden from the model by the host.
APP_TOOLS = [
    "zernio_open_app",
    "show_post_preview",
    "show_failed_posts",
    "show_analytics",
    "show_account_health",
    "show_ads_alerts",
    "show_automation_approvals",
    "ui_dismiss_ads_alert",
    "ui_decide_automation_approval",
]


def apps_enabled() -> bool:
    return os.getenv("ZERNIO_MCP_APPS", "").lower() in ("1", "true", "yes")


def view_uri(name: str) -> str:
    return f"ui://zernio/{_VERSION}/{name}.html"


def _html(name: str) -> str:
    def read(file: str) -> str:
        return (_DIR / file).read_text(encoding="utf-8")

    return (
        read(f"{name}.html")
        .replace("/*ZERNIO_CSS*/", read("base.css"))
        .replace("/*ZERNIO_RUNTIME*/", read("runtime.js"))
    )


def register_apps(mcp: FastMCP) -> None:
    """Serve every view and register the tools that render them."""
    for name, title in VIEWS.items():
        mcp.add_resource(
            TextResource(
                uri=view_uri(name),
                name=title,
                mime_type=UI_MIME_TYPE,
                text=_html(name),
                meta={"ui": app_config_to_meta_dict(AppConfig(csp=_CSP))},
            )
        )
    register_tools(mcp, view_uri)
    _replace_overview(mcp)
    _register_app(mcp)


# The routed app, built from apps-src/ (Vite + TypeScript + the ext-apps SDK)
# into bundle/app.html, committed so the Python image needs no Node. It loads
# its own data through the server's tools, so the opening tool only says which
# screen to show.
APP_URI = f"ui://zernio/{_VERSION}/app.html"


def _register_app(mcp: FastMCP) -> None:
    mcp.add_resource(
        TextResource(
            uri=APP_URI,
            name="Zernio",
            mime_type=UI_MIME_TYPE,
            text=(_DIR / "bundle" / "app.html").read_text(encoding="utf-8"),
            # The app draws its own frame.
            meta={"ui": app_config_to_meta_dict(AppConfig(csp=_CSP, prefers_border=False))},
        )
    )

    @mcp.tool(
        name="zernio_open_app",
        title="Open Zernio",
        description=(
            "Open the Zernio app in the chat: the workspace at a glance (connected "
            "accounts, the ones that need attention, failed posts), with a button to "
            "open it full screen. Use it when the user wants to see their Zernio "
            "workspace or check on their accounts."
        ),
        annotations=ToolAnnotations(
            title="Open Zernio", readOnlyHint=True, destructiveHint=False, openWorldHint=False
        ),
        app=AppConfig(resource_uri=APP_URI),
        # Lists the app on Claude's Artifacts page, where people open and pin it
        # without asking Claude (custom and Verified connectors only).
        meta={"openai/ui": {"entrypoints": [{"type": "global"}]}},
    )
    def zernio_open_app() -> ToolResult:
        return ToolResult(
            content="Opened the Zernio app. The user sees it and can act there; do not repeat its contents as text.",
            structured_content={"view": "home"},
        )


def _replace_overview(mcp: FastMCP) -> None:
    # resources.py's zernio_overview points at the old static card; swap it
    # for the same tool on this view, which keeps its text answer.
    from late.mcp.resources import _OVERVIEW

    mcp.local_provider.remove_tool("zernio_overview")

    @mcp.tool(
        name="zernio_overview",
        description="Show an overview of what this Zernio MCP server can do (accounts, posts, analytics, ads, inbox) and how to find the right tool.",
        annotations=ToolAnnotations(
            title="Zernio server overview",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
        app=AppConfig(resource_uri=view_uri("overview"), visibility=["model"]),
    )
    def zernio_overview() -> str:
        return _OVERVIEW
