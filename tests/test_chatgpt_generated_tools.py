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

from late.mcp.chatgpt_server import CHATGPT_SCOPES, chatgpt_mcp
from late.mcp.chatgpt_tools import CHATGPT_GENERATED_TOOLS, concise_description
from late.mcp.generated_tools import TOOL_OAUTH_SCOPES
from late.mcp.middleware.missing_scope import _granted_scopes

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_TOOLS = json.loads((FIXTURES / "chatgpt_live_tools.json").read_text())
LIVE_INSTRUCTIONS = (FIXTURES / "chatgpt_live_instructions.txt").read_text()
CONVERSATIONS = "https://api.test.com/v1/inbox/conversations"
LINK_SCOPES = {"posts:read", "posts:write", "accounts:read", "analytics:read"}
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
        hints = listed[name]["annotations"]
        assert hints["readOnlyHint"] is True, name
        assert hints["destructiveHint"] is False, name
        assert hints["openWorldHint"] is False, name
        assert listed[name]["_meta"]["securitySchemes"] == [
            {"type": "oauth2", "scopes": [TOOL_OAUTH_SCOPES[name][0]]}
        ], name


async def test_generated_descriptions_stay_short():
    listed = await _listed()

    for name in CHATGPT_GENERATED_TOOLS:
        assert len(listed[name]["description"]) < 2_500, name


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
    assert not {
        "messaging:write",
        "ads:write",
        "automations:write",
        "money:write",
    } & set(CHATGPT_SCOPES)


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
    (challenge,) = result.meta["mcp/www_authenticate"]
    assert challenge.startswith(
        'Bearer resource_metadata="https://mcp.zernio.com/.well-known/oauth-protected-resource/chatgpt"'
    )
    assert 'error="insufficient_scope"' in challenge
    assert "messaging:read" in challenge
    assert "messaging:read" in result.content[0].text


async def test_each_group_refusal_logs_whether_it_asked_to_relink(monkeypatch, caplog):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes", lambda: LINK_SCOPES
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
async def test_other_403s_stay_plain_errors(monkeypatch, granted, body):
    monkeypatch.setattr(
        "late.mcp.middleware.missing_scope._granted_scopes", lambda: granted
    )

    result = await _list_conversations(httpx.Response(403, json=body))

    assert result.is_error
    assert not (result.meta or {}).get("mcp/www_authenticate")


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
