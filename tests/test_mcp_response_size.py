from __future__ import annotations

import json
import logging
import re

import httpx
import pytest
import respx
from fastmcp import Client, FastMCP

from late.mcp import response_format
from late.mcp.response_format import MAX_RESULT_CHARS, fit_to_size, format_payload
from late.mcp.server import mcp
from late.mcp.telemetry import ToolTelemetryMiddleware

API = "https://api.test.com"


@pytest.fixture(autouse=True)
def _api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


def _item(index: int, size: int = 2_000) -> dict:
    return {"_id": f"item_{index}", "body": "x" * size}


def _ids(document: dict, key: str) -> list[str]:
    return [item["_id"] for item in document[key]]


def test_output_is_compact_json_that_keeps_unicode_and_drops_only_nulls() -> None:
    text = format_payload(
        {
            "name": "Campanya d'estiu 🌞",
            "spend": 0,
            "isExternal": False,
            "rejectionReason": None,
            "ads": [],
            "actions": {},
            "note": "",
        }
    )

    assert (
        text
        == '{"name":"Campanya d\'estiu 🌞","spend":0,"isExternal":false,"ads":[],"actions":{},"note":""}'
    )


def test_a_response_under_the_cap_is_never_truncated() -> None:
    document = {
        "ads": [_item(i) for i in range(10)],
        "pagination": {"page": 1, "limit": 10, "total": 10},
    }

    assert json.loads(format_payload(document)) == document


def _page_api(items: list[dict], page: int, limit: int) -> dict:
    start = (page - 1) * limit
    return {
        "ads": items[start : start + limit],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(items),
            "pages": -(-len(items) // limit),
        },
    }


@pytest.mark.parametrize(
    ("limit", "start_page"), [(100, 1), (100, 2), (50, 3), (20, 1), (7, 4)]
)
def test_following_the_page_instructions_reads_every_item_once(
    limit: int, start_page: int
) -> None:
    items = [_item(i, size=3_000) for i in range(300)]
    first_index = (start_page - 1) * limit
    seen: list[str] = []
    page = start_page
    for _ in range(200):
        text = format_payload(_page_api(items, page, limit))
        assert len(text) <= MAX_RESULT_CHARS
        document = json.loads(text)
        seen.extend(_ids(document, "ads"))
        notes = " ".join(document.get("_truncated", []))
        resumed = re.search(r"limit=(\d+) and page=(\d+)", notes)
        if resumed:
            limit, page = int(resumed.group(1)), int(resumed.group(2))
        elif (page - 1) * limit + len(document["ads"]) < len(items):
            page += 1
        else:
            break

    assert seen == [f"item_{i}" for i in range(first_index, 300)]


def test_a_trimmed_page_drops_counts_that_would_skip_items() -> None:
    document = json.loads(
        format_payload(_page_api([_item(i, 3_000) for i in range(100)], 1, 100))
    )

    assert "pages" not in document["pagination"]
    assert len(document["ads"]) < 100


def test_a_trimmed_cursor_page_drops_its_next_cursor_and_says_how_to_continue() -> None:
    document = json.loads(
        format_payload(
            {
                "comments": [_item(i, 3_000) for i in range(100)],
                "pagination": {"hasMore": True, "nextCursor": "c_after_100"},
            }
        )
    )

    kept = len(document["comments"])
    assert "nextCursor" not in document["pagination"]
    assert "hasMore" not in document["pagination"]
    assert f"same cursor and limit={kept}" in document["_truncated"][0]


def test_a_page_with_neither_page_number_nor_cursor_asks_to_narrow_the_request() -> (
    None
):
    document = json.loads(
        format_payload(
            {
                "conversations": [_item(i, 3_000) for i in range(100)],
                "pagination": {"hasMore": True, "nextCursor": None},
            }
        )
    )

    assert "Narrow the request" in document["_truncated"][0]
    assert "cursor" not in document["_truncated"][0]


def test_the_largest_list_is_trimmed_first_so_the_page_stays_whole() -> None:
    document = json.loads(
        format_payload(
            {
                "posts": [_item(i, 1_000) for i in range(20)],
                "pagination": {"page": 1, "limit": 20, "total": 20},
                "accounts": [_item(i, 500) for i in range(1_000)],
            }
        )
    )

    assert len(document["posts"]) == 20
    assert len(document["accounts"]) < 1_000
    assert document["_truncated"][0].startswith("`accounts` shows")


def test_nested_lists_are_trimmed_with_their_path_named() -> None:
    tree = {
        "campaigns": [
            {
                "_id": "c1",
                "adSets": [
                    {"_id": f"s{i}", "ads": [_item(j, 400) for j in range(100)]}
                    for i in range(5)
                ],
            }
        ]
    }

    document = json.loads(format_payload(tree))

    assert any(
        note.startswith("`campaigns[0].adSets") for note in document["_truncated"]
    )


def test_one_huge_string_is_cut_and_the_output_stays_valid_json() -> None:
    thread = {
        "messages": [
            {"_id": "m1", "html": "<p>" + "a" * 10_000_000 + "</p>", "text": "short"}
        ]
    }

    text = format_payload(thread)
    document = json.loads(text)

    assert len(text) <= MAX_RESULT_CHARS
    assert document["messages"][0]["text"] == "short"
    assert document["messages"][0]["html"].endswith("…[cut]")
    assert "keeps its first" in document["_truncated"][0]


def test_a_top_level_list_is_wrapped_so_the_note_has_somewhere_to_go() -> None:
    document = json.loads(fit_to_size([_item(i, 3_000) for i in range(100)], 50_000))

    assert len(document["items"]) < 100
    assert document["_truncated"]


def test_every_shape_fits_the_cap() -> None:
    shapes = [
        {
            "data": [
                {"actions": [{"type": f"t{j}", "value": "9" * 50} for j in range(300)]}
                for _ in range(200)
            ]
        },
        {"a": [_item(i, 50_000) for i in range(5)], "b": ["y" * 200_000]},
        {"rows": [[f"cell{i}{j}" for j in range(50)] for i in range(2_000)]},
    ]

    for shape in shapes:
        text = format_payload(shape)
        assert len(text) <= MAX_RESULT_CHARS
        json.loads(text)


def test_stats_record_the_untruncated_size() -> None:
    stats: dict = {}
    token = response_format.format_stats.set(stats)
    try:
        format_payload({"ads": [_item(i, 3_000) for i in range(100)]})
    finally:
        response_format.format_stats.reset(token)

    assert stats["raw_chars"] > MAX_RESULT_CHARS
    assert stats["truncated"] is True


async def _call(name: str, arguments: dict) -> str:
    async with Client(mcp) as client:
        result = await client.call_tool(
            "call_tool", {"name": name, "arguments": arguments}
        )
    return result.content[0].text


@respx.mock
async def test_list_ad_sets_asks_for_twenty_by_default_and_never_more_than_forty() -> (
    None
):
    route = respx.get(f"{API}/v1/ads/ad-sets").mock(
        return_value=httpx.Response(
            200, json={"adSets": [], "pagination": {"page": 1, "limit": 20}}
        )
    )

    await _call("ad_campaigns_list_ad_sets", {})
    await _call("ad_campaigns_list_ad_sets", {"limit": 500})

    assert [call.request.url.params["limit"] for call in route.calls] == ["20", "40"]


@respx.mock
async def test_list_ads_caps_the_page_an_agent_asks_for() -> None:
    route = respx.get(f"{API}/v1/ads").mock(
        return_value=httpx.Response(
            200,
            json={
                "ads": [_item(i, 9_000) for i in range(20)],
                "pagination": {"page": 1, "limit": 20, "total": 40},
            },
        )
    )

    text = await _call("ad_campaigns_list_ads", {"limit": 100})

    assert route.calls.last.request.url.params["limit"] == "20"
    assert len(text) <= MAX_RESULT_CHARS
    assert "limit=" in json.loads(text)["_truncated"][0]


async def test_the_tool_log_records_the_limit_asked_and_the_size_before_truncation(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO, logger="late.mcp.tools")
    server = FastMCP("t")

    @server.tool
    def list_things(limit: int = 10) -> str:
        return format_payload({"things": [_item(i, 9_000) for i in range(limit)]})

    server.add_middleware(ToolTelemetryMiddleware("mcp"))
    async with Client(server) as client:
        await client.call_tool("list_things", {"limit": 30})

    [line] = [
        json.loads(r.getMessage()) for r in caplog.records if r.name == "late.mcp.tools"
    ]
    assert line["limit"] == 30
    assert line["truncated"] is True
    assert line["raw_chars"] > MAX_RESULT_CHARS >= line["result_chars"]
