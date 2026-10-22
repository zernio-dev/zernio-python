import importlib
import inspect
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from late.resources._generated.account_settings import AccountSettingsResource
from late.resources._generated.ad_audiences import AdAudiencesResource
from late.resources._generated.connect import ConnectResource
from late.resources._generated.messaging_ads import MessagingAdsResource
from late.resources._generated.sms import SmsResource
from late.resources.posts import PostsResource

REPO_ROOT = Path(__file__).resolve().parents[1]


class RecordingClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.headers: dict[str, str] | None = None

    def _post(self, path: str, data: Any = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
        self.calls.append((path, data))
        self.headers = headers
        return {}

    def _put(self, path: str, data: Any = None) -> dict[str, Any]:
        self.calls.append((path, data))
        return {}

    async def _aput(self, path: str, data: Any = None) -> dict[str, Any]:
        self.calls.append((path, data))
        return {}

    def _get(self, path: str, params: Any = None) -> dict[str, Any]:
        self.calls.append((path, params))
        return {}


def test_create_ad_audience_requires_and_sends_raw_body() -> None:
    client = RecordingClient()
    body = {
        "accountId": "acc_1",
        "adAccountId": "act_1",
        "type": "website",
        "name": "Site visitors 30d",
    }

    AdAudiencesResource(client).create_ad_audience(body)

    assert client.calls == [("/v1/ads/audiences", body)]


def test_create_ad_audience_body_is_mandatory() -> None:
    parameters = inspect.signature(AdAudiencesResource.create_ad_audience).parameters
    assert parameters["body"].default is inspect.Parameter.empty


def test_messaging_ad_creators_expose_flattened_body_fields() -> None:
    for method in (
        MessagingAdsResource.create_messaging_ad,
        MessagingAdsResource.create_call_ad,
        MessagingAdsResource.create_ctwa_ad,
    ):
        parameters = inspect.signature(method).parameters
        for field in ("account_id", "ad_account_id", "name"):
            assert field in parameters, f"{method.__name__} lost body field {field}"


def test_create_messaging_ad_sends_camel_cased_payload() -> None:
    client = RecordingClient()

    MessagingAdsResource(client).create_messaging_ad(
        account_id="acc_1",
        ad_account_id="act_1",
        name="WhatsApp test",
        destination="whatsapp",
        headline="Talk to us",
        budget_amount=20,
    )

    path, payload = client.calls[0]
    assert path == "/v1/ads/messaging"
    assert payload["accountId"] == "acc_1"
    assert payload["adAccountId"] == "act_1"
    assert payload["destination"] == "whatsapp"
    assert payload["budgetAmount"] == 20
    assert "video" not in payload


def test_request_fields_keep_their_snake_case_openapi_names() -> None:
    client = RecordingClient()
    resource = AccountSettingsResource(client)

    resource.set_messenger_menu("acc_1", persistent_menu=[{"locale": "default"}])
    resource.set_instagram_ice_breakers("acc_1", ice_breakers=[{"question": "q"}])

    assert client.calls == [
        ("/v1/accounts/acc_1/messenger-menu", {"persistent_menu": [{"locale": "default"}]}),
        ("/v1/accounts/acc_1/instagram-ice-breakers", {"ice_breakers": [{"question": "q"}]}),
    ]


async def test_async_request_fields_keep_their_snake_case_openapi_names() -> None:
    client = RecordingClient()

    await AccountSettingsResource(client).aset_messenger_ice_breakers("acc_1", ice_breakers=[{"q": 1}])

    assert client.calls == [("/v1/accounts/acc_1/messenger-ice-breakers", {"ice_breakers": [{"q": 1}]})]


def test_query_params_keep_their_snake_case_openapi_names() -> None:
    client = RecordingClient()

    ConnectResource(client).get_connect_url(
        "instagram", "prof_1", redirect_url="https://example.com/done"
    )

    _, params = client.calls[0]
    assert params["redirect_url"] == "https://example.com/done"
    assert params["profileId"] == "prof_1"
    assert "redirectUrl" not in params


def test_python_keyword_field_is_sent_under_its_spec_name_with_idempotency_header() -> None:
    client = RecordingClient()

    SmsResource(client).send_sms(from_="+15550001", to="+15550002", idempotency_key="idem-1")

    _, payload = client.calls[0]
    assert payload["from"] == "+15550001"
    assert "from_" not in payload
    assert client.headers == {"Idempotency-Key": "idem-1"}


def test_hand_written_resources_drop_empty_string_query_values() -> None:
    params = PostsResource(RecordingClient())._build_params(platform="", status="failed")  # type: ignore[arg-type]

    assert params == {"status": "failed"}


def _emitted_wire_keys(lines: list[str], helper: str) -> set[str] | None:
    start = f"        {'params' if helper == '_wire_params' else 'payload'} = self.{helper}({{"
    if start not in lines:
        return None
    block = lines[lines.index(start) + 1 :]
    block = block[: block.index("        })")]
    return {re.match(r'\s+"(.+)": ', line).group(1) for line in block}  # type: ignore[union-attr]


def test_every_generated_operation_emits_the_spec_names_as_wire_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.syspath_prepend(str(REPO_ROOT / "scripts"))
    generator = importlib.import_module("generate_resources")
    openapi_body = importlib.import_module("openapi_body")
    spec = yaml.safe_load((REPO_ROOT / "openapi.yaml").read_text())

    checked = 0
    for path, path_item in spec["paths"].items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete") or "operationId" not in operation:
                continue
            resolved = [openapi_body.resolve_parameter_ref(p, spec) for p in operation.get("parameters", [])]
            expected_query = {p["name"] for p in resolved if p.get("in") == "query"}
            schema = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            flattened = openapi_body.flatten_request_body_schema(schema, spec) if schema else None
            expected_body = set(flattened["properties"]) if flattened and method != "get" else set()

            params = generator.extract_parameters(operation, spec)
            lines = generator.generate_method_body(method, path, params, operation["operationId"])

            assert (_emitted_wire_keys(lines, "_wire_params") or set()) == expected_query, operation["operationId"]
            assert (_emitted_wire_keys(lines, "_wire_payload") or set()) == expected_body, operation["operationId"]
            checked += 1

    assert checked > 100
