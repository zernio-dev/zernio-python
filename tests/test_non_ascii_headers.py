"""A caller-supplied header value httpx/h11 cannot send (an Idempotency-Key
holding human text, a token with a trailing newline) must fail before the
request is built with an error that names the header and says how to fix it,
not a bare UnicodeEncodeError from httpx (Sentry ZERNIO-MCP-11) or h11's
LocalProtocolError."""

from __future__ import annotations

import httpx
import pytest
import respx
import sentry_sdk
from fastmcp import Client
from sentry_sdk.transport import Transport

from late import Late, LateValidationError
from late.mcp import http_server, telemetry

API = "https://api.test.com"
ROMANIAN_KEY = "postare-ziua-de-maine-pentru-client-ț-1"
PRINTABLE_ASCII = "must contain only printable ASCII characters"


@pytest.fixture
def client() -> Late:
    return Late(api_key="test_api_key", base_url=API)


@pytest.fixture
def posts_route():
    with respx.mock:
        yield respx.post(f"{API}/v1/posts").mock(
            return_value=httpx.Response(201, json={"post": {"_id": "p_1"}})
        )


@pytest.mark.parametrize("key", ["holo-retry-3f1c9a", "a b%20c", "retry\tkey"])
def test_a_sendable_key_reaches_the_api_unchanged(client, posts_route, key) -> None:
    client.posts.create_post(content="Salut", idempotency_key=key)

    assert posts_route.calls.last.request.headers["Idempotency-Key"] == key


@pytest.mark.parametrize(
    ("key", "problem"),
    [
        (ROMANIAN_KEY, f"got a value with 'ț' at position {ROMANIAN_KEY.index('ț')}."),
        ("café", "got a value with 'é' at position 3."),
        ("line\r\nX-Injected: 1", "got a value with '\\r' at position 4."),
        ("nul\x00", "got a value with '\\x00' at position 3."),
        (" key-1", "got a value with leading whitespace."),
        ("key-1\t", "got a value with trailing whitespace."),
    ],
)
def test_an_unsendable_key_fails_before_the_request_with_a_clear_error(
    client, posts_route, key, problem
) -> None:
    with pytest.raises(LateValidationError) as caught:
        client.posts.create_post(content="Salut", idempotency_key=key)

    message = str(caught.value)
    assert message.startswith(f"Idempotency-Key header value {PRINTABLE_ASCII}")
    assert problem in message
    assert message.endswith("Use a plain ASCII key, e.g. a UUID.")
    assert key not in message
    assert caught.value.field == "Idempotency-Key"
    assert posts_route.call_count == 0


async def test_the_async_path_checks_headers_too(client, posts_route) -> None:
    with pytest.raises(LateValidationError, match="x-request-id header value"):
        await client.posts.acreate_post(content="Salut", x_request_id="cerere-ț")

    assert posts_route.call_count == 0


@respx.mock
def test_a_token_header_error_shows_neither_the_value_nor_the_character(
    client,
) -> None:
    route = respx.get(f"{API}/v1/connect/snapchat/select-profile")
    token = "ct_sëcret_value"

    with pytest.raises(LateValidationError) as caught:
        client.connect.list_snapchat_profiles(
            x_connect_token=token, profile_id="prof_1", temp_token="tmp_1"
        )

    message = str(caught.value)
    assert message.startswith(f"X-Connect-Token header value {PRINTABLE_ASCII}")
    assert "a character that cannot be sent at position 4" in message
    assert "ë" not in message and "ct_s" not in message
    assert route.call_count == 0


class _CapturingTransport(Transport):
    def __init__(self, options: dict | None = None) -> None:
        super().__init__(options)
        self.events: list = []

    def capture_envelope(self, envelope) -> None:
        self.events += [item for item in envelope.items if item.type == "event"]


@pytest.fixture
def sentry_events(monkeypatch: pytest.MonkeyPatch):
    transport = _CapturingTransport()
    real_init = sentry_sdk.init
    monkeypatch.setattr(
        telemetry.sentry_sdk,
        "init",
        lambda **options: real_init(transport=transport, **options),
    )
    monkeypatch.setenv("SENTRY_DSN", "https://key@o1.ingest.example.invalid/1")
    assert telemetry.init_sentry() is True
    yield transport.events
    real_init(dsn=None)


async def test_the_mcp_tool_returns_the_error_to_the_agent_without_a_sentry_issue(
    monkeypatch, posts_route, sentry_events
) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", API)
    arguments = {
        "content": "Spring sale",
        "scheduled_for": "2026-12-01T10:00:00Z",
        "platforms": [{"platform": "facebook", "accountId": "acc_1"}],
        "idempotency_key": ROMANIAN_KEY,
    }

    # http_server's `mcp` is the hosted one, with the telemetry middleware.
    async with Client(http_server.mcp) as mcp_client:
        result = await mcp_client.call_tool(
            "posts_create_post", arguments, raise_on_error=False
        )

    assert result.is_error
    [text] = [block.text for block in result.content]
    assert text.startswith(f"Error: Idempotency-Key header value {PRINTABLE_ASCII}")
    assert "ascii' codec" not in text
    assert posts_route.call_count == 0
    assert sentry_events == []
