"""The generated tools the ChatGPT plugin lists next to its 13 hand-shaped ones.

OpenAI publishes a plugin's tools one by one after a scan, and keeps serving
the definitions it approved: the 13 live tools must not change shape, every
added tool must carry explicit hints and its OAuth scope, and a link made
before a scope existed must be asked to re-link rather than fail.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx
from fastmcp import Client
from fastmcp.server.auth import AccessToken
from mcp.types import ToolAnnotations

from late.mcp.chatgpt_server import CHATGPT_SCOPES, chatgpt_mcp
from late.mcp.chatgpt_tools import (
    CHATGPT_GENERATED_TOOLS,
    DESCRIPTION_LEADS,
    WAVE_1,
    WAVE_2,
    WAVE_3,
    WRITE_EFFECTS,
    _hints_for,
    concise_description,
)
from late.mcp.generated_tools import TOOL_OAUTH_SCOPES
from late.mcp.middleware.missing_scope import _granted_scopes

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_TOOLS = json.loads((FIXTURES / "chatgpt_live_tools.json").read_text())
LIVE_INSTRUCTIONS = (FIXTURES / "chatgpt_live_instructions.txt").read_text()
CONVERSATIONS = "https://api.test.com/v1/inbox/conversations"
LINK_SCOPES = {"posts:read", "posts:write", "accounts:read", "analytics:read"}
OPEN_WORLD_READS = {
    "accounts_list_tik_tok_commercial_music",
    "ad_library_search_ad_library",
    "ad_targeting_search_ad_targeting",
    "instagram_get_instagram_business_discovery",
    "instagram_search_instagram_audio",
}
GROUP_DENIED = {
    "error": "This connector token has the 'messages' resource group disabled.",
    "code": "insufficient_permissions",
    "required_group": "messages",
}


@pytest.fixture(autouse=True)
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


async def _listed() -> dict[str, dict]:
    async with Client(chatgpt_mcp) as client:
        result = await client.session.list_tools()
    return {
        t.name: t.model_dump(mode="json", by_alias=True, exclude_none=True)
        for t in result.tools
    }


async def test_the_live_tools_keep_the_definitions_openai_approved():
    listed = await _listed()

    for live in LIVE_TOOLS:
        assert listed[live["name"]] == live, live["name"]


async def test_the_server_instructions_keep_their_published_text():
    async with Client(chatgpt_mcp) as client:
        assert client.instructions == LIVE_INSTRUCTIONS


async def test_lists_the_live_tools_and_the_wave_and_no_tool_search_proxy():
    listed = await _listed()

    assert set(listed) == {t["name"] for t in LIVE_TOOLS} | set(CHATGPT_GENERATED_TOOLS)
    assert "search_tools" not in listed
    assert "call_tool" not in listed


async def test_every_generated_tool_has_explicit_hints_and_its_oauth_scope():
    listed = await _listed()

    for name in CHATGPT_GENERATED_TOOLS:
        assert listed[name]["_meta"]["securitySchemes"] == [
            {"type": "oauth2", "scopes": [TOOL_OAUTH_SCOPES[name][0]]}
        ], name
    for name in WAVE_1 + WAVE_2:
        hints = listed[name]["annotations"]
        assert hints["readOnlyHint"] is True, name
        assert hints["destructiveHint"] is False, name
        # Reads of public catalogs and other accounts' content are open-world.
        assert hints["openWorldHint"] is (name in OPEN_WORLD_READS), name


@pytest.mark.parametrize(
    ("name", "destructive", "open_world"),
    [
        ("messages_send_inbox_message", False, True),
        ("comments_reply_to_inbox_post", False, True),
        ("comment_automations_create_comment_automation", False, True),
        ("broadcasts_create_broadcast", False, False),
        ("profiles_create_profile", False, False),
        ("comments_pin_inbox_comment", True, True),
        ("workflows_trigger_api_call_workflow", True, True),
        ("posts_edit_post", True, True),
        ("accounts_reply_to_google_business_review", True, True),
    ],
)
async def test_a_write_says_whether_it_overwrites_and_whether_it_reaches_out(
    name, destructive, open_world
):
    hints = (await _listed())[name]["annotations"]

    assert hints["readOnlyHint"] is False
    assert hints["destructiveHint"] is destructive
    assert hints["openWorldHint"] is open_world


async def test_every_listed_write_has_its_effects_spelled_out():
    listed = await _listed()

    writes = {
        name
        for name in CHATGPT_GENERATED_TOOLS
        if not listed[name]["annotations"]["readOnlyHint"]
    }

    assert writes == set(WAVE_3)
    for name in writes:
        hints = listed[name]["annotations"]
        effects = WRITE_EFFECTS[name]
        assert hints["destructiveHint"] is effects["destructive_hint"], name
        assert hints["openWorldHint"] is effects["open_world_hint"], name


async def test_generated_descriptions_stay_short():
    listed = await _listed()

    for name in CHATGPT_GENERATED_TOOLS:
        arguments = len(listed[name]["inputSchema"].get("properties", {}))
        assert len(listed[name]["description"]) < 1_000 + 110 * arguments, name


def test_advertises_exactly_the_scopes_the_listed_tools_need():
    needed = {TOOL_OAUTH_SCOPES[name][0] for name in CHATGPT_GENERATED_TOOLS}

    assert CHATGPT_SCOPES[:4] == [
        "posts:read",
        "posts:write",
        "accounts:read",
        "analytics:read",
    ]
    assert set(CHATGPT_SCOPES) == LINK_SCOPES | needed
    assert {"messaging:read", "ads:read", "contacts:read"} <= set(CHATGPT_SCOPES)
    assert {"messaging:write", "accounts:write"} <= set(CHATGPT_SCOPES)
    # automations:write also opens webhooks; ads:write and money:write spend.
    assert not {
        "automations:write",
        "ads:write",
        "money:write",
        "commerce:write",
    } & set(CHATGPT_SCOPES)


async def test_a_held_write_says_who_it_reaches_right_after_its_title():
    listed = await _listed()

    title, lead, *_ = listed["broadcasts_create_broadcast"]["description"].split("\n\n")

    assert title == "Create broadcast draft"
    assert lead.startswith("Creates a draft only: nothing is sent")
    assert DESCRIPTION_LEADS.keys() <= set(CHATGPT_GENERATED_TOOLS)


def test_a_write_listed_without_its_effects_is_refused():
    generated = ToolAnnotations(readOnlyHint=False, destructiveHint=True)

    with pytest.raises(LookupError, match="WRITE_EFFECTS"):
        _hints_for("fake_write", generated)


async def test_the_whole_listing_stays_within_budget():
    listed = await _listed()

    assert len(json.dumps(list(listed.values()))) < 300_000


def test_a_description_keeps_its_first_paragraph_and_one_line_per_argument():
    doc = """List conversations

    Fetch conversations from every connected account.

    ### X limitation

    X hides encrypted chats.

    Args:
        platform: Filter by platform
        folder: `requests` lists message requests.

- When Meta will not list the folder, the call answers 400.
        limit: Maximum number of conversations to return"""

    assert concise_description(doc) == (
        "List conversations\n\n"
        "Fetch conversations from every connected account.\n\n"
        "Args:\n"
        "    platform: Filter by platform\n"
        "    folder: `requests` lists message requests.\n"
        "    limit: Maximum number of conversations to return"
    )


def test_a_title_only_description_keeps_undocumented_arguments_by_name():
    doc = """Get workflow

    Args:
        workflow_id: (required)
        account_id"""

    assert concise_description(doc) == (
        "Get workflow\n\nArgs:\n    workflow_id: (required)\n    account_id"
    )


async def _list_conversations(response: httpx.Response):
    with respx.mock:
        respx.get(url__startswith=CONVERSATIONS).mock(return_value=response)
        async with Client(chatgpt_mcp) as client:
            return await client.call_tool(
                "messages_list_inbox_conversations", {}, raise_on_error=False
            )


async def test_a_link_without_the_tools_scope_is_asked_to_relink(monkeypatch):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes", lambda: LINK_SCOPES
    )

    result = await _list_conversations(httpx.Response(403, json=GROUP_DENIED))

    assert result.is_error
    text = result.content[0].text
    assert "read your inbox" in text and "'messaging:read'" in text
    assert "Settings > Plugins" in text and "Reconnect" in text


async def test_the_relink_steps_carry_no_auth_challenge_chatgpt_would_hide_them_behind(
    monkeypatch,
):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes", lambda: LINK_SCOPES
    )

    result = await _list_conversations(httpx.Response(403, json=GROUP_DENIED))

    assert "mcp/www_authenticate" not in (result.meta or {})


async def test_a_link_that_only_reads_messages_is_asked_to_relink_before_a_send(
    monkeypatch,
):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes",
        lambda: LINK_SCOPES | {"messaging:read"},
    )
    read_only = {
        "error": "This connector token can only read the 'messages' resource group.",
        "code": "insufficient_permissions",
        "required_group": "messages",
    }

    with respx.mock:
        respx.post(url__startswith="https://api.test.com/v1/broadcasts").mock(
            return_value=httpx.Response(403, json=read_only)
        )
        async with Client(chatgpt_mcp) as client:
            result = await client.call_tool(
                "broadcasts_create_broadcast",
                {
                    "profile_id": "p1",
                    "account_id": "a1",
                    "platform": "telegram",
                    "name": "Draft",
                },
                raise_on_error=False,
            )

    assert result.is_error
    text = result.content[0].text
    assert "send messages" in text and "'messaging:write'" in text


async def test_each_group_refusal_logs_whether_it_asked_to_relink(monkeypatch, caplog):
    token = AccessToken(
        token="t",
        client_id="chatgpt",
        scopes=[],
        claims={"scope": " ".join(LINK_SCOPES), "user_id": "u1"},
    )
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope.get_access_token", lambda: token
    )

    with caplog.at_level("INFO", logger="late.mcp.tools"):
        await _list_conversations(httpx.Response(403, json=GROUP_DENIED))

    (line,) = [
        json.loads(r.message)
        for r in caplog.records
        if "mcp_scope_challenge" in r.message
    ]
    assert line["tool"] == "messages_list_inbox_conversations"
    assert line["needed_scope"] == "messaging:read"
    assert line["challenged"] is True
    assert "messaging:read" not in line["token_scope"]
    assert line["user_id"] == "u1"


@pytest.mark.parametrize(
    ("granted", "body"),
    [
        # The link holds the scope: a team member with the group off, which re-linking cannot fix.
        (LINK_SCOPES | {"messaging:read"}, GROUP_DENIED),
        # A write scope reaches the read too.
        (LINK_SCOPES | {"messaging:write"}, GROUP_DENIED),
        # An API key: no OAuth link to redo.
        (None, GROUP_DENIED),
        # A 403 that is not about a resource group.
        (LINK_SCOPES, {"error": "Upgrade your plan", "code": "plan_required"}),
    ],
)
async def test_other_403s_keep_the_apis_own_error(monkeypatch, granted, body):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes", lambda: granted
    )

    result = await _list_conversations(httpx.Response(403, json=body))

    assert result.is_error
    assert "Reconnect" not in result.content[0].text
    assert body["error"] in result.content[0].text


async def test_a_generated_tool_answers_from_the_api():
    with respx.mock:
        respx.get(url__startswith=CONVERSATIONS).mock(
            return_value=httpx.Response(
                200, json={"data": [{"id": "conv_1", "participantName": "Ana"}]}
            )
        )
        async with Client(chatgpt_mcp) as client:
            result = await client.call_tool(
                "messages_list_inbox_conversations", {}, raise_on_error=False
            )

    assert not result.is_error
    assert "conv_1" in result.content[0].text


@pytest.mark.parametrize(
    ("claims", "granted"),
    [
        ({"scope": "posts:read messaging:read"}, {"posts:read", "messaging:read"}),
        ({"user_id": "u1"}, None),
    ],
)
def test_the_granted_scopes_come_from_the_verified_token(monkeypatch, claims, granted):
    token = AccessToken(token="t", client_id="zernio", scopes=[], claims=claims)
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope.get_access_token", lambda: token
    )

    assert _granted_scopes() == granted
