import inspect
from typing import Any

from late.resources._generated.ad_audiences import AdAudiencesResource
from late.resources._generated.messaging_ads import MessagingAdsResource


class RecordingClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    def _post(self, path: str, data: Any = None) -> dict[str, Any]:
        self.calls.append((path, data))
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
