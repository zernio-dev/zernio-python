from __future__ import annotations

import json

import httpx
import pytest
import respx
from fastmcp import Client

from late.mcp.server import mcp

API = "https://api.test.com"
DRIVE_URL = "https://drive.google.com/file/d/abc/view?usp=sharing"
POST_RESPONSE = {
    "post": {"_id": "post_1", "content": "hi", "status": "draft", "platforms": []},
    "message": "ok",
}


@pytest.fixture(autouse=True)
def _api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


@respx.mock
@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        (
            "posts_create",
            {"platform": "twitter", "account_id": "acc_1"},
        ),
        (
            "posts_cross_post",
            {"platforms": "twitter", "account_ids": "acc_1"},
        ),
    ],
)
async def test_media_urls_are_typed_only_when_the_extension_proves_it(
    tool: str, arguments: dict
) -> None:
    create = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json=POST_RESPONSE)
    )
    media_urls = f"https://x.com/a.mp4,https://x.com/a.jpg,{DRIVE_URL}"

    async with Client(mcp) as client:
        await client.call_tool(
            tool,
            {"content": "hi", "is_draft": True, "media_urls": media_urls, **arguments},
        )

    items = json.loads(create.calls.last.request.content)["mediaItems"]
    assert items == [
        {"type": "video", "url": "https://x.com/a.mp4"},
        {"type": "image", "url": "https://x.com/a.jpg"},
        {"url": DRIVE_URL},
    ]
