"""MCP Apps: the Zernio app Claude and ChatGPT render in the chat.

A trial, off unless ZERNIO_MCP_APPS=1, kept in this package so it can be
removed in one go: delete it, apps-src/ and the apps lines in server.py.

One app, every screen in it: apps-src/ (Vite + React + the ext-apps SDK,
drawn in the dashboard's design system v2) builds into bundle/mcp-app.html,
committed so the Python image needs no Node. The tools in tools.py each open
it on one screen (zernio_open_app on Home, show_failed_posts on Failed posts,
...) and hand it that screen's data; the app calls the same tools to switch
screens and refresh, so every screen looks and behaves alike.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from fastmcp.apps import UI_MIME_TYPE, AppConfig, ResourceCSP, app_config_to_meta_dict
from fastmcp.resources import TextResource
from mcp.types import ToolAnnotations
from starlette.responses import Response

from ..constants import MCP_PUBLIC_URL
from .tools import register_tools

if TYPE_CHECKING:
    from fastmcp import FastMCP
    from starlette.requests import Request

_DIR = Path(__file__).parent

# Hosts cache ui:// resources aggressively: bump on a change an old cached app
# could not handle (a new data shape, a renamed tool it calls).
APP_URI = "ui://zernio/v2/app.html"

# The design system's fonts, served by this server: MCP Apps take fonts only
# from origins the resource declares, never as data: URLs. The bundle names
# its origin as __ZERNIO_ORIGIN__, filled in when it is served.
_FONT_PATH = "/apps/fonts/{name}"
_FONTS = {
    name: (_DIR / "fonts" / name).read_bytes()
    for name in ("Geist-Variable.woff2", "GeistMono-Variable.woff2", "GeistPixel-Square.woff2")
}

# This server (fonts), zernio.com (platform app icons, the logo), Zernio media
# storage (post previews) and Claude's host fonts. Built from MCP_PUBLIC_URL,
# so dev and prod each name themselves: a wrong origin fails silently, as a
# blocked font. The app reaches the API only through the host (tools/call),
# so connectDomains stays empty.
_CSP = ResourceCSP(
    resource_domains=[
        MCP_PUBLIC_URL,
        "https://zernio.com",
        "https://media.zernio.com",
        "https://assets.claude.ai",
    ],
)

# Listed up front while the trial is on. The ui_* tools are app-only: listed
# so the host lets the app call them, hidden from the model by the host.
APP_TOOLS = [
    "zernio_open_app",
    "show_post_preview",
    "show_failed_posts",
    "show_analytics",
    "show_account_health",
    "show_ads_alerts",
    "show_automation_approvals",
    "ui_reconnect_account",
    "ui_dismiss_ads_alert",
    "ui_decide_automation_approval",
]


def apps_enabled() -> bool:
    return os.getenv("ZERNIO_MCP_APPS", "").lower() in ("1", "true", "yes")


async def _app_font(request: Request) -> Response:
    body = _FONTS.get(request.path_params["name"])
    if body is None:
        return Response(status_code=404)
    return Response(
        body,
        media_type="font/woff2",
        headers={
            # Claude loads it from its sandbox origin (*.claudemcpcontent.com).
            "Access-Control-Allow-Origin": "*",
            "Cross-Origin-Resource-Policy": "cross-origin",
            "Cache-Control": "public, max-age=86400",
        },
    )


def register_apps(mcp: FastMCP) -> None:
    """Serve the app and its fonts, and register the tools that open it."""
    html = (_DIR / "bundle" / "mcp-app.html").read_text(encoding="utf-8")
    mcp.add_resource(
        TextResource(
            uri=APP_URI,
            name="Zernio",
            mime_type=UI_MIME_TYPE,
            text=html.replace("__ZERNIO_ORIGIN__", MCP_PUBLIC_URL),
            meta={"ui": app_config_to_meta_dict(AppConfig(csp=_CSP))},
        )
    )
    mcp.custom_route(_FONT_PATH, methods=["GET"])(_app_font)
    register_tools(mcp, APP_URI)
    _plain_overview(mcp)


def _plain_overview(mcp: FastMCP) -> None:
    # resources.py's zernio_overview renders the old static card; while the app
    # is on, the overview is text and the app is opened by zernio_open_app.
    from late.mcp.resources import _OVERVIEW

    mcp.local_provider.remove_tool("zernio_overview")
    mcp.local_provider.remove_resource("ui://zernio/overview.html")

    @mcp.tool(
        name="zernio_overview",
        description="Show an overview of what this Zernio MCP server can do (accounts, posts, analytics, ads, inbox) and how to find the right tool.",
        annotations=ToolAnnotations(
            title="Zernio server overview",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def zernio_overview() -> str:
        return _OVERVIEW
