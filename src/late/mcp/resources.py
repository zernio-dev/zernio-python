"""Static MCP resources: orientation docs an agent can read before (or
without) authenticating. Content is bundled, not fetched, so resources/read
never depends on the Zernio API being reachable."""

from fastmcp import FastMCP

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
        "zernio://docs/rate-limits",
        name="Rate limits",
        description="Request throughput limits per plan tier and the response headers that report them.",
        mime_type="text/markdown",
    )
    def rate_limits() -> str:
        return _RATE_LIMITS
