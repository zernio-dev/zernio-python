import pytest
from fastmcp import Client

from late.mcp import feedback_source
from late.mcp.server import mcp
from late.resources._generated.feedback import FeedbackResource


async def _call(name: str, arguments: dict) -> bool:
    async with Client(mcp) as client:
        result = await client.call_tool(name, arguments, raise_on_error=False)
    return result.is_error


async def test_feedback_is_listed_up_front_and_explained_in_the_instructions():
    async with Client(mcp) as client:
        listed = {t.name for t in await client.list_tools()}
        instructions = client.initialize_result.instructions

    assert "feedback_submit_feedback" in listed
    assert "feedback_submit_feedback" in instructions
    assert "Never include" in instructions


@pytest.fixture
def submitted(monkeypatch):
    calls: list[dict] = []

    def submit_feedback(_resource, **kwargs):
        calls.append(kwargs)
        return {"id": "fb_1", "status": "received", "duplicate": False}

    monkeypatch.setenv("ZERNIO_API_KEY", "sk_test")
    monkeypatch.setattr(FeedbackResource, "submit_feedback", submit_feedback)
    return calls


async def test_feedback_from_the_mcp_server_is_labelled_with_its_source(submitted):
    is_error = await _call(
        "feedback_submit_feedback", {"type": "bug", "summary": "Posting fails"}
    )

    assert not is_error
    assert submitted[0]["agent"] == {"name": "zernio-mcp"}


async def test_feedback_keeps_the_agent_it_reported_and_adds_the_source(submitted):
    await _call(
        "feedback_submit_feedback",
        {
            "type": "missing_feature",
            "summary": "No TikTok cover frame",
            "agent": {"name": "claude-code", "model": "claude-opus-5-5"},
        },
    )

    assert submitted[0]["agent"] == {
        "name": "claude-code via zernio-mcp",
        "model": "claude-opus-5-5",
    }


def test_feedback_source_names_the_client_from_its_user_agent(monkeypatch):
    monkeypatch.setattr(
        feedback_source,
        "get_http_headers",
        lambda: {"user-agent": "Cursor/1.0.0 (darwin)"},
    )

    labelled = feedback_source.with_feedback_source({"type": "bug", "summary": "x"})

    assert labelled["agent"] == {"name": "zernio-mcp (Cursor/1.0.0)"}


def test_feedback_source_fits_the_api_length_limit(monkeypatch):
    monkeypatch.setattr(feedback_source, "get_http_headers", lambda: {})

    labelled = feedback_source.with_feedback_source({"agent": {"name": "a" * 120}})

    assert len(labelled["agent"]["name"]) == 100
