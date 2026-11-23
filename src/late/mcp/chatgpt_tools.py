"""The generated tools the ChatGPT plugin lists next to its 13 hand-shaped ones.

The plugin's tools/list is reviewed by OpenAI one tool at a time: every tool a
deploy adds here is held until OpenAI's next scan clears it, then goes live
without a resubmission. So the list grows in waves, each one deploy, and stays
curated (a few dozen tools per wave, about 150 in all) rather than mirroring
the ~1,400 tools /mcp serves.
"""

from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING, Any

from late.mcp.generated_tools import TOOL_OAUTH_SCOPES, register_generated_tools

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from fastmcp import FastMCP

# Ranked by 30-day use (REST requests plus /mcp tool calls), top first: the 40
# most used reads. Each declares its group's read scope (messaging:read,
# ads:read, contacts:read where the group has one), so a link that only reads
# never grants sending or spending. Sends, writes, deletes and spend are later
# waves.
WAVE_1 = (
    "messages_get_inbox_conversation_messages",
    "comments_get_inbox_post_comments",
    "messages_list_inbox_conversations",
    "comments_list_inbox_comments",
    "comment_automations_list_comment_automation_logs",
    "accounts_get_account_health",
    "messages_get_inbox_conversation",
    "comment_automations_get_comment_automation",
    "accounts_get_google_business_reviews",
    "analytics_get_instagram_account_insights",
    "accounts_get_account_posts",
    "profiles_list_profiles",
    "accounts_get_all_accounts_health",
    "ad_accounts_get_ad_comments",
    "ad_insights_query_ad_insights",
    "whatsapp_phone_numbers_get_whats_app_number_info",
    "lead_gen_list_form_leads",
    "broadcasts_list_broadcast_recipients",
    "reviews_list_inbox_reviews",
    "ad_campaigns_get_ad_tree",
    "ad_campaigns_get_ad",
    "comment_automations_list_comment_automations",
    "instagram_get_instagram_story_insights",
    "ad_campaigns_list_ads",
    "analytics_get_tik_tok_account_insights",
    "workflows_list_workflow_executions",
    "accounts_get_google_business_location_details",
    "ad_insights_get_ad_analytics",
    "analytics_get_google_business_performance",
    "ad_campaigns_list_ad_campaigns",
    "analytics_get_you_tube_daily_views",
    "ad_accounts_list_ad_accounts",
    "analytics_get_post_timeline",
    "ad_campaigns_get_ad_set_details",
    "accounts_get_instagram_follow_status",
    "accounts_get_follower_stats",
    "analytics_get_instagram_demographics",
    "whatsapp_get_whats_app_templates",
    "analytics_get_linked_in_post_analytics",
    "contacts_list_contacts",
)

CHATGPT_GENERATED_TOOLS = WAVE_1


_SUMMARY_MAX = 400
_PARAM_MAX = 100
_ARGS_HEADING = re.compile(r"\n[ \t]*Args:\n")
_PARAM_LINE = re.compile(r"^([ \t]+)(\w+):\s*(.*)$")


def _clip(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def _argument_lines(args: str) -> list[str]:
    """The first line of each argument; continuation lines (lists, notes) are dropped."""
    matches = [m for m in map(_PARAM_LINE.match, args.splitlines()) if m]
    if not matches:
        return []
    indent = matches[0][1]
    return [
        f"    {m[2]}: {_clip(m[3], _PARAM_MAX)}".rstrip()
        for m in matches
        if m[1] == indent
    ]


def concise_description(doc: str) -> str:
    """A generated tool's docstring cut to its first paragraph and one line per argument.

    The generated docstrings carry the API reference (metric catalogues, platform
    caveats), several hundred tokens a tool; ChatGPT loads every listed tool's
    description, so here it gets the gist and reads details from the result.
    """
    narrative, *rest = _ARGS_HEADING.split(doc, maxsplit=1)
    paragraphs = [p for p in inspect.cleandoc(narrative).split("\n\n") if p.strip()]
    lines = [_clip(p, _SUMMARY_MAX) for p in paragraphs[:2]]
    arguments = _argument_lines(rest[0]) if rest else []
    if arguments:
        lines += ["Args:", *arguments]
    return "\n\n".join(lines[:2]) + ("\n\n" + "\n".join(lines[2:]) if arguments else "")


def oauth_scopes_of(tools: Iterable[str]) -> list[str]:
    """The scopes these generated tools declare, deduplicated in first-use order."""
    return list(dict.fromkeys(TOOL_OAUTH_SCOPES[tool][0] for tool in tools))


class _ListedToolsOnly:
    """Stands in for the server in register_generated_tools: registers only the
    listed tools, each declaring its OAuth scope (securitySchemes)."""

    def __init__(self, server: FastMCP, listed: Iterable[str]) -> None:
        self._server = server
        self._listed = set(listed)

    def tool(self, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def register(fn: Callable[..., Any]) -> Callable[..., Any]:
            if fn.__name__ not in self._listed:
                return fn
            scopes = [TOOL_OAUTH_SCOPES[fn.__name__][0]]
            meta = {"securitySchemes": [{"type": "oauth2", "scopes": scopes}]}
            description = concise_description(fn.__doc__ or fn.__name__)
            self._server.tool(meta=meta, description=description, **kwargs)(fn)
            return fn

        return register


def register_chatgpt_generated_tools(
    server: FastMCP, get_client: Callable[[], Any]
) -> None:
    register_generated_tools(
        _ListedToolsOnly(server, CHATGPT_GENERATED_TOOLS), get_client
    )
