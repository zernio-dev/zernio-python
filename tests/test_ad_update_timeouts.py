"""A slow ad update must wait for the result, and a timeout must not run it again."""

from __future__ import annotations

import httpx
import pytest
import respx

from late import Late
from late.client.exceptions import LateTimeoutError

API = "https://api.test.com"
SLOW_UPDATES = [
    ("PUT", "/v1/ads/ad_1"),
    ("PUT", "/v1/ads/ad-sets/set_1"),
    ("PUT", "/v1/ads/campaigns/camp_1"),
    ("PATCH", "/v1/ads/ad_1"),
]


def _read_timeout(route: respx.Route) -> float:
    return route.calls[0].request.extensions["timeout"]["read"]


def _send(client: Late, method: str, path: str, data: dict | None = None) -> dict:
    return getattr(client, f"_{method.lower()}")(path, data=data or {"name": "Spring"})


async def _asend(client: Late, method: str, path: str) -> dict:
    return await getattr(client, f"_a{method.lower()}")(path, data={"name": "Spring"})


@pytest.fixture
def client() -> Late:
    return Late(api_key="test_api_key", base_url=API)


@pytest.mark.parametrize(("method", "path"), SLOW_UPDATES)
@respx.mock
def test_ad_updates_wait_for_the_publish_timeout(
    client: Late, method: str, path: str
) -> None:
    route = respx.route(method=method, url=f"{API}{path}").mock(
        return_value=httpx.Response(200, json={})
    )

    _send(client, method, path)

    assert _read_timeout(route) == client.publish_timeout


@pytest.mark.parametrize(("method", "path"), SLOW_UPDATES)
@respx.mock
async def test_async_ad_updates_wait_for_the_publish_timeout(
    client: Late, method: str, path: str
) -> None:
    route = respx.route(method=method, url=f"{API}{path}").mock(
        return_value=httpx.Response(200, json={})
    )

    await _asend(client, method, path)

    assert _read_timeout(route) == client.publish_timeout


@pytest.mark.parametrize(("method", "path"), SLOW_UPDATES)
@respx.mock
def test_an_ad_update_that_times_out_runs_only_once(
    client: Late, method: str, path: str
) -> None:
    route = respx.route(method=method, url=f"{API}{path}").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(
        LateTimeoutError, match=f"{method} {path} timed out and was NOT retried"
    ):
        _send(client, method, path)

    assert route.call_count == 1


@pytest.mark.parametrize(("method", "path"), SLOW_UPDATES)
@respx.mock
async def test_an_async_ad_update_that_times_out_runs_only_once(
    client: Late, method: str, path: str
) -> None:
    route = respx.route(method=method, url=f"{API}{path}").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(LateTimeoutError, match="NOT retried"):
        await _asend(client, method, path)

    assert route.call_count == 1


@respx.mock
def test_a_post_update_with_publish_now_waits_and_cannot_publish_twice(
    client: Late,
) -> None:
    route = respx.put(f"{API}/v1/posts/post_1").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(LateTimeoutError, match="NOT retried"):
        _send(client, "PUT", "/v1/posts/post_1", {"publishNow": True})

    assert route.call_count == 1
    assert _read_timeout(route) == client.publish_timeout


@respx.mock
def test_other_updates_keep_the_default_timeout_and_their_retries(
    client: Late, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("late.client.base.time.sleep", lambda _seconds: None)
    route = respx.put(f"{API}/v1/profiles/prof_1").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(LateTimeoutError):
        _send(client, "PUT", "/v1/profiles/prof_1")

    assert route.call_count == client.max_retries
    assert _read_timeout(route) == client.timeout


@respx.mock
def test_deleting_an_ad_stays_retryable(
    client: Late, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("late.client.base.time.sleep", lambda _seconds: None)
    route = respx.delete(f"{API}/v1/ads/ad_1").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(LateTimeoutError):
        client._delete("/v1/ads/ad_1")

    assert route.call_count == client.max_retries


@respx.mock
def test_an_update_with_a_list_body_still_sends(client: Late) -> None:
    route = respx.put(f"{API}/v1/profiles/prof_1").mock(
        return_value=httpx.Response(200, json={})
    )

    client._put("/v1/profiles/prof_1", data=[{"name": "Spring"}])

    assert route.call_count == 1
