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
    from mcp.types import ToolAnnotations

# Ranked by 30-day use (REST requests plus /mcp tool calls), top first: the 40
# most used reads. Each declares its group's read scope (messaging:read,
# ads:read, contacts:read where the group has one), so a link that only reads
# never grants sending or spending.
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

# The next 70 reads by the same ranking, keeping to the scopes wave 1 already
# asks for (so a link that re-linked for wave 1 needs nothing new). Left out
# on review: X search (bills per tweet read), the Reddit feed (disabled
# platform), deprecated aliases and legacy analytics replaced by metrics,
# the raw request logs, a report reader whose creator is a write, and
# LinkedIn reactors (third-party personal data).
WAVE_2 = (
    "lead_gen_list_leads",
    "broadcasts_get_broadcast",
    "lead_gen_count_leads",
    "workflows_get_workflow",
    "ad_campaigns_get_ad_campaign_details",
    "instagram_list_instagram_stories",
    "analytics_get_facebook_page_insights",
    "ad_campaigns_get_ads_timeline",
    "analytics_get_instagram_follower_history",
    "profiles_get_profile",
    "instagram_get_instagram_publishing_limit",
    "analytics_get_you_tube_video_retention",
    "mentions_list_inbox_mentions",
    "accounts_get_tik_tok_creator_info",
    "analytics_get_you_tube_channel_insights",
    "queue_list_queue_slots",
    "ad_creatives_get_ad_creative",
    "phone_numbers_list_phone_numbers",
    "ad_accounts_get_ad_account_live_entities",
    "lead_gen_list_lead_forms",
    "ad_accounts_get_ad_account_finance",
    "ad_insights_get_campaign_analytics",
    "analytics_get_you_tube_demographics",
    "instagram_get_instagram_business_discovery",
    "ad_targeting_search_ad_targeting",
    "ad_creatives_list_ad_creatives",
    "email_list_email_messages",
    "messages_search_inbox_conversations",
    "workflows_list_workflows",
    "ad_campaigns_list_ad_sets",
    "analytics_get_analytics_dashboard",
    "analytics_get_linked_in_org_aggregate_analytics",
    "contacts_get_contact",
    "voice_list_voice_calls",
    "ad_accounts_get_ads_activity_log",
    "ad_audiences_list_ad_audiences",
    "analytics_get_linked_in_aggregate_analytics",
    "ad_accounts_list_ads_instagram_accounts",
    "inbox_analytics_get_inbox_volume",
    "tracking_tags_list_tracking_tags",
    "broadcasts_list_broadcasts",
    "ad_campaigns_list_ad_keywords",
    "ad_accounts_list_ads_instagram_posts",
    "analytics_get_google_business_search_keywords",
    "ad_creatives_list_ad_videos",
    "whatsapp_get_whats_app_template_by_id",
    "inbox_analytics_get_inbox_response_time",
    "accounts_get_account",
    "ad_campaigns_get_ad_review",
    "tracking_tags_get_tracking_tag_stats",
    "account_groups_list_account_groups",
    "ad_creatives_list_ad_images",
    "lead_gen_get_lead_form",
    "whatsapp_get_whats_app_business_profile",
    "email_get_email_thread",
    "inbox_analytics_get_inbox_source_breakdown",
    "tracking_tags_get_tracking_tag",
    "tracking_tags_get_ad_tracking_tags",
    "gmb_verifications_get_google_business_verifications",
    "whatsapp_list_whats_app_account_events",
    "instagram_get_instagram_mentioned_comment",
    "ad_accounts_list_high_demand_periods",
    "gmb_services_get_google_business_services",
    "ad_library_search_ad_library",
    "inbox_analytics_get_inbox_heatmap",
    "whatsapp_get_whats_app_template",
    "accounts_list_tik_tok_commercial_music",
    "instagram_search_instagram_audio",
    "email_get_email_message",
    "whatsapp_list_whats_app_group_chats",
)

# What a write does, as the hints ChatGPT reads to decide how to confirm it:
# destructiveHint when it overwrites what is there, openWorldHint when it
# reaches people outside the account (a DM, a public reply, an automation that
# answers commenters). The generator marks every write destructive and
# open-world; these are the per-tool truths.
_ADDS = {"destructive_hint": False, "open_world_hint": False}
_REACHES_OUT = {"destructive_hint": False, "open_world_hint": True}
_OVERWRITES = {"destructive_hint": True, "open_world_hint": False}
_OVERWRITES_IN_PUBLIC = {"destructive_hint": True, "open_world_hint": True}

# The most used sends and writes by the same ranking, each declaring its
# group's write scope. Sends can be billed per message (SMS, RCS and X
# broadcasts, managed messaging). Held back: creating and activating a
# workflow (the API checks a workflow's sending nodes against API keys only,
# so an OAuth link without messaging:write could install them) and updating a
# contact (its only scope, automations:write, also opens webhooks). Deletes and
# ad spend are a later wave.
WAVE_3_EFFECTS = {
    "messages_send_inbox_message": _REACHES_OUT,
    "comments_send_private_reply_to_comment": _REACHES_OUT,
    "comments_reply_to_inbox_post": _REACHES_OUT,
    "posts_edit_post": _OVERWRITES_IN_PUBLIC,
    "broadcasts_send_broadcast": _REACHES_OUT,
    "messages_create_inbox_conversation": _REACHES_OUT,
    "broadcasts_create_broadcast": _ADDS,
    "broadcasts_add_broadcast_recipients": _ADDS,
    "comment_automations_update_comment_automation": _OVERWRITES_IN_PUBLIC,
    "comment_automations_create_comment_automation": _REACHES_OUT,
    "comments_pin_inbox_comment": _OVERWRITES_IN_PUBLIC,
    "comments_like_inbox_comment": _REACHES_OUT,
    "messages_add_message_reaction": _REACHES_OUT,
    "profiles_create_profile": _ADDS,
    "posts_update_post_metadata": _OVERWRITES_IN_PUBLIC,
    "whatsapp_create_whats_app_template": _ADDS,
    "workflows_trigger_api_call_workflow": _OVERWRITES_IN_PUBLIC,
    "accounts_reply_to_google_business_review": _OVERWRITES_IN_PUBLIC,
}
WAVE_3 = tuple(WAVE_3_EFFECTS)

CHATGPT_GENERATED_TOOLS = WAVE_1 + WAVE_2 + WAVE_3
WRITE_EFFECTS = WAVE_3_EFFECTS


_SUMMARY_MAX = 400
_PARAM_MAX = 100
_ARGS_HEADING = re.compile(r"\n[ \t]*Args:\n")
_PARAM_LINE = re.compile(r"^([ \t]+)(\w+)(?::[ \t]*(.*))?$")


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
        f"    {m[2]}: {_clip(m[3] or '', _PARAM_MAX)}".rstrip(": ")
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
    sections = [_clip(p, _SUMMARY_MAX) for p in paragraphs[:2]]
    arguments = _argument_lines(rest[0]) if rest else []
    if arguments:
        sections.append("\n".join(["Args:", *arguments]))
    return "\n\n".join(sections)


def oauth_scopes_of(tools: Iterable[str]) -> list[str]:
    """The scopes these generated tools declare, deduplicated in first-use order."""
    return list(
        dict.fromkeys(s for tool in tools for s in TOOL_OAUTH_SCOPES.get(tool, ())[:1])
    )


def _hints_for(name: str, generated: ToolAnnotations) -> ToolAnnotations:
    """The generated hints, or for a write its effects from WRITE_EFFECTS."""
    if generated.read_only_hint:
        return generated
    if name not in WRITE_EFFECTS:
        raise LookupError(
            f"{name} is a write listed for ChatGPT without WRITE_EFFECTS: say "
            "whether it overwrites and whether it reaches people outside the account"
        )
    return generated.model_copy(update=WRITE_EFFECTS[name])


class _ListedToolsOnly:
    """Stands in for the server in register_generated_tools: registers only the
    listed tools, each declaring its OAuth scope (securitySchemes) and, for a
    write, the hints of what it does."""

    def __init__(self, server: FastMCP, listed: Iterable[str]) -> None:
        self._server = server
        self._listed = set(listed)

    def tool(self, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def register(fn: Callable[..., Any]) -> Callable[..., Any]:
            if fn.__name__ not in self._listed:
                return fn
            scopes = list(TOOL_OAUTH_SCOPES.get(fn.__name__, ()))[:1]
            if not scopes:
                raise LookupError(
                    f"{fn.__name__} is listed for ChatGPT but the spec gives it no "
                    "x-oauth-scopes; regenerate from a spec that has them"
                )
            meta = {"securitySchemes": [{"type": "oauth2", "scopes": scopes}]}
            description = concise_description(fn.__doc__ or fn.__name__)
            annotations = _hints_for(fn.__name__, kwargs.pop("annotations"))
            self._server.tool(
                meta=meta, description=description, annotations=annotations, **kwargs
            )(fn)
            return fn

        return register


def register_chatgpt_generated_tools(
    server: FastMCP, get_client: Callable[[], Any]
) -> None:
    register_generated_tools(
        _ListedToolsOnly(server, CHATGPT_GENERATED_TOOLS), get_client
    )
