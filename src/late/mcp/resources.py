"""Static MCP resources: orientation docs an agent can read before (or
without) authenticating. Content is bundled, not fetched, so resources/read
never depends on the Zernio API being reachable."""

from fastmcp import FastMCP
from fastmcp.apps import AppConfig, ResourceCSP
from mcp.types import ToolAnnotations

_OVERVIEW = """\
# Zernio — social media and messaging API

Zernio lets you publish and schedule posts to 16 platforms (TikTok, Instagram,
WhatsApp, Facebook, YouTube, LinkedIn, X/Twitter, Threads, Reddit, Pinterest,
Bluesky, Google Business, Telegram, Snapchat, Discord, Slack), send and receive
messages through a unified inbox (WhatsApp Cloud API, Instagram DMs, Messenger,
Telegram, X DMs), read cross-platform analytics, and run paid ads on 7 ad
networks (Meta, Google, TikTok, LinkedIn, Pinterest, X, OpenAI Ads).

## When to use this server

- Publish or schedule a post to one or many social accounts in one call.
- List connected accounts and profiles, check post status, read analytics.
- Send WhatsApp/Instagram/Messenger/Telegram messages programmatically.
- Create and manage ad campaigns.

Tools are named by resource: `accounts_*`, `profiles_*`, `posts_*`, `media_*`,
`docs_*`. The long tail of endpoints is reachable through `search_tools` +
`call_tool`.

## Links

- Docs: https://docs.zernio.com
- OpenAPI spec: https://zernio.com/openapi.json (also /openapi.yaml)
- LLM summary: https://zernio.com/llms.txt
- Status: https://status.zernio.com
"""

_AUTHENTICATION = """\
# Authenticating to the Zernio MCP server

Discovery (initialize, tools/list, resources) works without credentials.
Calling tools requires one of:

1. **OAuth 2.0** (interactive clients: Claude, ChatGPT, Cursor): connect to
   `https://mcp.zernio.com/mcp` and complete the flow the 401 challenge
   advertises. Dynamic client registration is open; PKCE is required.
2. **API key** (headless/CI): send `Authorization: Bearer YOUR_API_KEY`.
   Create a key at https://zernio.com/dashboard (free for up to 2 connected
   social accounts, no credit card).

Scopes: posts:read, posts:write, accounts:read, accounts:write,
analytics:read, ads:write, messaging:write, automations:write.
"""

_RATE_LIMITS = """\
# Rate limits

API throughput is limited per minute on a sliding window, scaling with the
team's connected social accounts:

- 0-2 accounts (free tier): 60 requests/minute
- 3-2,000 accounts: 600 requests/minute
- 2,001+ accounts: 1,200 requests/minute

Responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining`,
`X-RateLimit-Reset`, and 429s include `Retry-After`. Posting volume itself is
not metered by these limits; per-platform daily publish caps apply separately.
Details: https://docs.zernio.com/guides/rate-limits
"""


_OVERVIEW_VIEW_HTML = """\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src https://mcp.zernio.com; form-action https://zernio.com; frame-ancestors https://chatgpt.com https://claude.ai https://claude.com https://web.chatgpt.com">
<title>Zernio</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; padding: 16px; color: #1a1a1a; background: #fff; }
  h1 { font-size: 18px; margin: 0 0 4px; }
  p { margin: 4px 0; font-size: 13px; color: #444; }
  ul { margin: 8px 0 0; padding-left: 18px; font-size: 13px; }
  li { margin: 2px 0; }
  @media (prefers-color-scheme: dark) {
    body { color: #eee; background: #111; }
    p { color: #bbb; }
  }
</style>
</head>
<body>
  <h1>Zernio</h1>
  <p>Social media and messaging API: publish, schedule, and analyze across 16 platforms, plus unified inbox and ads on 7 networks.</p>
  <ul>
    <li>Post or schedule with <code>posts_create</code> / <code>posts_cross_post</code></li>
    <li>Discover accounts with <code>accounts_list</code> and <code>profiles_list</code></li>
    <li>Read metrics with <code>analytics_get_analytics</code></li>
    <li>Find the long tail of tools with <code>search_tools</code></li>
  </ul>
</body>
</html>
"""


def register_resources(mcp: FastMCP) -> None:
    """Attach the static discovery resources to the server."""

    @mcp.resource(
        "zernio://docs/overview",
        name="Zernio overview and when to use it",
        description="What the Zernio API does, when an agent should reach for it, and where the full docs live.",
        mime_type="text/markdown",
    )
    def overview() -> str:
        return _OVERVIEW

    @mcp.resource(
        "zernio://docs/authentication",
        name="Authentication guide",
        description="How to authenticate tool calls: OAuth flow for interactive clients, API keys for headless use.",
        mime_type="text/markdown",
    )
    def authentication() -> str:
        return _AUTHENTICATION

    @mcp.resource(
        "ui://zernio/overview.html",
        name="Zernio overview card",
        description="Self-contained MCP App view summarizing what this server does. No external origins.",
        app=AppConfig(csp=ResourceCSP(connect_domains=["https://mcp.zernio.com"], resource_domains=[])),
    )
    def overview_view() -> str:
        return _OVERVIEW_VIEW_HTML

    @mcp.tool(
        name="zernio_overview",
        description="Show an overview of what this Zernio MCP server can do (accounts, posts, analytics, ads, inbox) and how to find the right tool.",
        annotations=ToolAnnotations(
            title="Zernio server overview",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
        app=AppConfig(resource_uri="ui://zernio/overview.html", visibility=["model"]),
    )
    def zernio_overview() -> str:
        return _OVERVIEW

    @mcp.resource(
        "zernio://docs/rate-limits",
        name="Rate limits",
        description="Request throughput limits per plan tier and the response headers that report them.",
        mime_type="text/markdown",
    )
    def rate_limits() -> str:
        return _RATE_LIMITS
