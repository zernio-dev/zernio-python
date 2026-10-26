"""Required header params and raw-bytes bodies must reach the API from both
the SDK and the generated MCP tools."""

from __future__ import annotations

import base64
import binascii
import importlib
from pathlib import Path

import httpx
import pytest
import respx

from late import Late


@pytest.fixture
def client() -> Late:
    return Late(api_key="test_api_key", base_url="https://api.test.com")


@pytest.fixture
def mcp_generator(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("generate_mcp_tools")


@respx.mock
def test_kyc_upload_sends_raw_bytes_and_filename(client: Late) -> None:
    route = respx.post(
        "https://api.test.com/v1/phone-numbers/kyc/upload-document"
    ).mock(return_value=httpx.Response(200, json={"documentId": "doc_1"}))

    result = client.phone_numbers.upload_phone_number_kyc_document(
        x_filename="id%20card.pdf", content=b"%PDF-1.4 bytes"
    )

    request = route.calls[0].request
    assert request.content == b"%PDF-1.4 bytes"
    assert request.headers["Content-Type"] == "application/octet-stream"
    assert request.headers["X-Filename"] == "id%20card.pdf"
    assert result == {"documentId": "doc_1"}


@respx.mock
async def test_async_kyc_upload_sends_raw_bytes_and_filename(client: Late) -> None:
    route = respx.post(
        "https://api.test.com/v1/whatsapp/phone-numbers/kyc/upload-document"
    ).mock(return_value=httpx.Response(200, json={"documentId": "doc_1"}))

    await client.whatsapp_phone_numbers.aupload_whats_app_number_kyc_document(
        x_filename="id.png", content=b"\x89PNG"
    )

    request = route.calls[0].request
    assert request.content == b"\x89PNG"
    assert request.headers["Content-Type"] == "application/octet-stream"
    assert request.headers["X-Filename"] == "id.png"


@respx.mock
def test_connect_list_snapchat_profiles_sends_connect_token(client: Late) -> None:
    route = respx.get("https://api.test.com/v1/connect/snapchat/select-profile").mock(
        return_value=httpx.Response(200, json={"publicProfiles": []})
    )

    client.connect.list_snapchat_profiles(
        x_connect_token="ct_1", profile_id="prof_1", temp_token="tmp_1"
    )

    request = route.calls[0].request
    assert request.headers["X-Connect-Token"] == "ct_1"
    assert "profileId=prof_1" in str(request.url)


def test_mcp_generator_exposes_only_required_headers(mcp_generator) -> None:
    operation = {
        "parameters": [
            {"name": "X-Connect-Token", "in": "header", "required": True},
            {"name": "Idempotency-Key", "in": "header", "required": False},
            {"name": "profileId", "in": "query", "required": True},
        ]
    }

    names = [p["name"] for p in mcp_generator.extract_parameters(operation, {})]

    assert names == ["x_connect_token", "profile_id"]


def test_mcp_generator_maps_octet_stream_body_to_base64(mcp_generator) -> None:
    operation = {
        "requestBody": {
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        }
    }

    (param,) = mcp_generator.extract_parameters(operation, {})

    assert param["name"] == "content_base64"
    assert param["required"] is True
    assert param["sdk_name"] == "content"
    assert param["sdk_value"] == "_decode_base64(content_base64)"


def test_decode_base64_accepts_plain_and_data_url() -> None:
    from late.mcp.generated_tools import _decode_base64

    raw = b"%PDF-1.4 bytes"
    encoded = base64.b64encode(raw).decode()

    assert _decode_base64(encoded) == raw
    assert _decode_base64(f"data:application/pdf;base64,{encoded}") == raw


def test_decode_base64_rejects_invalid_input() -> None:
    from late.mcp.generated_tools import _decode_base64

    with pytest.raises(binascii.Error):
        _decode_base64("not base64!")
