"""Request bodies and query strings must carry each field under the name the
OpenAPI spec declares, not a blanket camelCase rename of the Python kwarg.

Most Zernio endpoints read camelCase, but some read snake_case
(``ice_breakers``, ``persistent_menu``, ``message_send_ttl_seconds``). The
generated resources used to camelCase every key, so those routes answered
``400 ice_breakers is required`` (ZERNIO-472, ZERNIO-1600).
"""

from __future__ import annotations

import importlib
import inspect
import json
from collections import Counter
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
import yaml
from fastmcp import Client

from late import Late

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.test.com"


@pytest.fixture
def client() -> Late:
    return Late(api_key="test_api_key", base_url=API)


def _body(route: respx.Route) -> dict[str, Any]:
    return json.loads(route.calls[0].request.content)


# --- reported endpoints, through the SDK -----------------------------------


@respx.mock
def test_instagram_ice_breakers_body_is_snake_case(client: Late) -> None:
    route = respx.put(f"{API}/v1/accounts/acc_1/instagram-ice-breakers").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    items = [{"question": "Hours?", "payload": "HOURS"}]

    client.account_settings.set_instagram_ice_breakers("acc_1", ice_breakers=items)

    assert _body(route) == {"ice_breakers": items}


@respx.mock
async def test_messenger_ice_breakers_body_is_snake_case_async(client: Late) -> None:
    route = respx.put(f"{API}/v1/accounts/acc_1/messenger-ice-breakers").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    items = [
        {
            "locale": "default",
            "call_to_actions": [{"question": "Hours?", "payload": "HOURS"}],
        }
    ]

    await client.account_settings.aset_messenger_ice_breakers(
        "acc_1", ice_breakers=items
    )

    assert _body(route) == {"ice_breakers": items}


@respx.mock
def test_messenger_menu_body_is_snake_case(client: Late) -> None:
    route = respx.put(f"{API}/v1/accounts/acc_1/messenger-menu").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    menu = [
        {
            "locale": "default",
            "call_to_actions": [
                {"type": "postback", "title": "Talk to us", "payload": "HUMAN"}
            ],
        }
    ]

    client.account_settings.set_messenger_menu("acc_1", persistent_menu=menu)

    assert _body(route) == {"persistent_menu": menu}


@respx.mock
def test_messenger_greeting_body(client: Late) -> None:
    route = respx.put(f"{API}/v1/accounts/acc_1/messenger-greeting").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    greeting = [{"locale": "default", "text": "Hi {{user_first_name}}"}]

    client.account_settings.set_messenger_greeting("acc_1", greeting=greeting)

    assert _body(route) == {"greeting": greeting}


@respx.mock
def test_whatsapp_template_ttl_only_update_by_id(client: Late) -> None:
    route = respx.patch(f"{API}/v1/whatsapp/templates/id/123").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    client.whatsapp.update_whats_app_template_by_id(
        "123", account_id="acc_1", message_send_ttl_seconds=600
    )

    assert _body(route) == {"accountId": "acc_1", "message_send_ttl_seconds": 600}


@respx.mock
def test_whatsapp_template_ttl_update_by_name(client: Late) -> None:
    route = respx.patch(f"{API}/v1/whatsapp/templates/order_update").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    client.whatsapp.update_whats_app_template(
        "order_update", account_id="acc_1", message_send_ttl_seconds=3600
    )

    assert _body(route) == {"accountId": "acc_1", "message_send_ttl_seconds": 3600}


@respx.mock
def test_whatsapp_template_create_mixes_camel_and_snake(client: Late) -> None:
    route = respx.post(f"{API}/v1/whatsapp/templates").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    client.whatsapp.create_whats_app_template(
        account_id="acc_1",
        name="otp",
        category="AUTHENTICATION",
        language="en_US",
        library_template_name="verify_code",
        message_send_ttl_seconds=300,
    )

    assert _body(route) == {
        "accountId": "acc_1",
        "name": "otp",
        "category": "AUTHENTICATION",
        "language": "en_US",
        "library_template_name": "verify_code",
        "message_send_ttl_seconds": 300,
    }


@respx.mock
def test_snake_case_query_param_keeps_its_name(client: Late) -> None:
    route = respx.get(f"{API}/v1/connect/twitter").mock(
        return_value=httpx.Response(200, json={"authUrl": "https://x"})
    )

    client.connect.get_connect_url(
        "twitter", profile_id="prof_1", redirect_url="https://app.test/done"
    )

    params = route.calls[0].request.url.params
    assert params["profileId"] == "prof_1"
    assert params["redirect_url"] == "https://app.test/done"
    assert "redirectUrl" not in params


# --- camelCase endpoints are unchanged --------------------------------------


@respx.mock
def test_generated_create_post_stays_camel_case(client: Late) -> None:
    route = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json={"post": {"_id": "p1"}})
    )

    client.posts.create_post(
        content="Hello",
        scheduled_for="2026-12-01T10:00:00Z",
        platforms=[{"platform": "twitter", "accountId": "acc_1"}],
        timezone="UTC",
    )

    body = _body(route)
    assert (
        body.items()
        >= {
            "content": "Hello",
            "scheduledFor": "2026-12-01T10:00:00Z",
            "platforms": [{"platform": "twitter", "accountId": "acc_1"}],
            "timezone": "UTC",
        }.items()
    )
    # Spec defaults (publishNow, isDraft, ...) ride along, all camelCase.
    assert not [k for k in body if "_" in k]


@respx.mock
def test_hand_written_create_stays_camel_case(client: Late) -> None:
    route = respx.post(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json={"post": {"_id": "p1"}})
    )

    client.posts.create(
        content="Hello",
        platforms=[{"platform": "twitter", "accountId": "acc_1"}],
        publish_now=True,
    )

    body = _body(route)
    assert body["content"] == "Hello"
    assert body["publishNow"] is True
    assert "publish_now" not in body


@respx.mock
def test_hand_written_list_query_stays_camel_case(client: Late) -> None:
    route = respx.get(f"{API}/v1/posts").mock(
        return_value=httpx.Response(200, json={"posts": []})
    )

    client.posts.list(profile_id="prof_1", limit=5)

    params = route.calls[0].request.url.params
    assert params["profileId"] == "prof_1"
    assert params["limit"] == "5"


# --- every generated operation, against the spec ----------------------------


class RecordingClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def _record(self, path: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append({"path": path, **kwargs})
        return {}

    _get = _post = _put = _patch = _delete = _record


def _operations() -> list[tuple[str, str, str, list[dict[str, Any]]]]:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    gen = importlib.import_module("generate_resources")
    spec = yaml.safe_load((ROOT / "openapi.yaml").read_text())

    ops = []
    for item in spec["paths"].values():
        for method, op in item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            if "operationId" not in op:
                continue
            tag = op.get("tags", ["Other"])[0]
            resource = gen.TAG_TO_RESOURCE.get(tag, tag.lower().replace(" ", "_"))
            name = gen.camel_to_snake(op["operationId"])
            ops.append((resource, name, method, gen.extract_parameters(op, spec)))
    # Two operations whose ids snake_case alike in one resource: only the last
    # definition survives in the class, so this check cannot target the first.
    counts = Counter((r, n) for r, n, *_ in ops)
    return [o for o in ops if counts[(o[0], o[1])] == 1]


OPERATIONS = _operations()


def test_spec_has_snake_case_fields_to_check() -> None:
    names = {
        p["original_name"]
        for *_, params in OPERATIONS
        for p in params
        if p["in"] in ("query", "body")
    }
    assert {"ice_breakers", "persistent_menu", "message_send_ttl_seconds"} <= names


@pytest.mark.parametrize(
    ("resource", "method_name", "http_method", "params"),
    OPERATIONS,
    ids=[f"{r}.{n}" for r, n, *_ in OPERATIONS],
)
def test_generated_method_sends_spec_names(
    resource: str,
    method_name: str,
    http_method: str,
    params: list[dict[str, Any]],
) -> None:
    module = importlib.import_module(f"late.resources._generated.{resource}")
    cls = next(
        v
        for k, v in vars(module).items()
        if k.endswith("Resource") and inspect.isclass(v)
    )
    recorder = RecordingClient()
    method = getattr(cls(recorder), method_name)

    kwargs = {
        name: b"x" if name == "content" and p.annotation == "bytes" else "x"
        for name, p in inspect.signature(method).parameters.items()
    }
    method(**kwargs)

    sent_query = recorder.calls[0].get("params") or {}
    sent_body = recorder.calls[0].get("data")
    expected_query = {p["original_name"] for p in params if p["in"] == "query"}
    body_fields = [p for p in params if p["in"] == "body"]

    if expected_query:
        assert set(sent_query) == expected_query
    if body_fields and http_method != "get":
        assert set(sent_body) == {p["original_name"] for p in body_fields}


# --- end to end through the MCP server ---------------------------------------


@pytest.fixture
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)


MCP_CASES = [
    (
        "account_settings_set_instagram_ice_breakers",
        "PUT",
        "/v1/accounts/acc_1/instagram-ice-breakers",
        {"ice_breakers": [{"question": "Hours?", "payload": "HOURS"}]},
        {"ice_breakers": [{"question": "Hours?", "payload": "HOURS"}]},
    ),
    (
        "account_settings_set_messenger_ice_breakers",
        "PUT",
        "/v1/accounts/acc_1/messenger-ice-breakers",
        {
            "ice_breakers": [
                {
                    "locale": "default",
                    "call_to_actions": [{"question": "Hours?", "payload": "H"}],
                }
            ]
        },
        {
            "ice_breakers": [
                {
                    "locale": "default",
                    "call_to_actions": [{"question": "Hours?", "payload": "H"}],
                }
            ]
        },
    ),
    (
        "account_settings_set_messenger_menu",
        "PUT",
        "/v1/accounts/acc_1/messenger-menu",
        {
            "persistent_menu": [
                {
                    "locale": "default",
                    "call_to_actions": [
                        {"type": "postback", "title": "Help", "payload": "HELP"}
                    ],
                }
            ]
        },
        {
            "persistent_menu": [
                {
                    "locale": "default",
                    "call_to_actions": [
                        {"type": "postback", "title": "Help", "payload": "HELP"}
                    ],
                }
            ]
        },
    ),
    (
        "account_settings_set_messenger_greeting",
        "PUT",
        "/v1/accounts/acc_1/messenger-greeting",
        {"greeting": [{"locale": "default", "text": "Hi!"}]},
        {"greeting": [{"locale": "default", "text": "Hi!"}]},
    ),
    (
        "whatsapp_update_whats_app_template_by_id",
        "PATCH",
        "/v1/whatsapp/templates/id/123",
        {"template_id": "123", "message_send_ttl_seconds": 600},
        {"accountId": "acc_1", "message_send_ttl_seconds": 600},
    ),
    (
        "whatsapp_update_whats_app_template",
        "PATCH",
        "/v1/whatsapp/templates/order_update",
        {"template_name": "order_update", "message_send_ttl_seconds": 600},
        {"accountId": "acc_1", "message_send_ttl_seconds": 600},
    ),
    (
        "posts_create_post",
        "POST",
        "/v1/posts",
        {
            "content": "Hello",
            "scheduled_for": "2026-12-01T10:00:00Z",
            "platforms": [{"platform": "twitter", "accountId": "acc_1"}],
        },
        {
            "content": "Hello",
            "scheduledFor": "2026-12-01T10:00:00Z",
            "platforms": [{"platform": "twitter", "accountId": "acc_1"}],
        },
    ),
]


@pytest.mark.usefixtures("api_env")
@pytest.mark.parametrize(
    ("tool", "http_method", "path", "arguments", "expected_body"),
    MCP_CASES,
    ids=[c[0] for c in MCP_CASES],
)
@respx.mock
async def test_mcp_tool_sends_spec_names(
    tool: str,
    http_method: str,
    path: str,
    arguments: dict[str, Any],
    expected_body: dict[str, Any],
) -> None:
    from late.mcp.server import mcp

    route = respx.route(method=http_method, url=f"{API}{path}").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    if not tool.startswith("posts_"):
        arguments = {"account_id": "acc_1", **arguments}

    async with Client(mcp) as mcp_client:
        result = await mcp_client.call_tool(
            "call_tool", {"name": tool, "arguments": arguments}, raise_on_error=False
        )

    assert not result.is_error, result.content[0].text
    assert route.call_count == 1
    body = _body(route)
    if tool == "posts_create_post":
        # Spec defaults (publishNow, isDraft, ...) ride along, all camelCase.
        assert body.items() >= expected_body.items()
        assert not [k for k in body if "_" in k]
    else:
        assert body == expected_body
