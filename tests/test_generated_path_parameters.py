"""Referenced path parameters must reach generated signatures and URLs."""

import importlib
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest


@pytest.mark.parametrize("is_async", [False, True])
async def test_referenced_account_parameter_is_sent(monkeypatch, is_async):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    generator = importlib.import_module("generate_resources")
    spec = {
        "components": {
            "parameters": {
                "AccountId": {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            }
        }
    }
    operation = {
        "parameters": [
            {"$ref": "#/components/parameters/AccountId"},
            {
                "name": "entryId",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
    }
    source = generator.generate_resource_class(
        "probe",
        [
            {
                "operation_id": "removeEntry",
                "http_method": "delete",
                "path": "/v1/accounts/{accountId}/entries/{entryId}",
                "summary": "Remove entry",
                "description": "",
                "params": generator.extract_parameters(operation, spec),
            }
        ],
    )
    namespace = {}
    exec(compile(source, "<generated-probe>", "exec"), namespace)
    client = Mock()
    client._adelete = AsyncMock(return_value={})
    resource = namespace["ProbeResource"](client)
    if is_async:
        await resource.aremove_entry(account_id="acc_123", entry_id="entry_456")
        client._adelete.assert_awaited_once_with(
            "/v1/accounts/acc_123/entries/entry_456"
        )
    else:
        resource.remove_entry(account_id="acc_123", entry_id="entry_456")
        client._delete.assert_called_once_with("/v1/accounts/acc_123/entries/entry_456")


DELETE_WITH_BODY = {
    "parameters": [
        {"name": "groupId", "in": "path", "required": True, "schema": {"type": "string"}},
        {"name": "accountId", "in": "query", "required": True, "schema": {"type": "string"}},
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["participants"],
                    "properties": {"participants": {"type": "array", "items": {"type": "string"}}},
                }
            }
        },
    },
}


@pytest.mark.parametrize("is_async", [False, True])
async def test_delete_operation_with_a_request_body_sends_it_as_json(monkeypatch, is_async):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    generator = importlib.import_module("generate_resources")
    source = generator.generate_resource_class(
        "probe",
        [
            {
                "operation_id": "removeParticipants",
                "http_method": "delete",
                "path": "/v1/groups/{groupId}/participants",
                "summary": "Remove participants",
                "description": "",
                "params": generator.extract_parameters(DELETE_WITH_BODY, {}),
            }
        ],
    )
    namespace = {}
    exec(compile(source, "<generated-probe>", "exec"), namespace)
    client = Mock()
    client._adelete = AsyncMock(return_value={})
    resource = namespace["ProbeResource"](client)
    expected = (
        ("/v1/groups/g1/participants",),
        {"params": {"accountId": "acc_1"}, "data": {"participants": ["123"]}},
    )
    if is_async:
        await resource.aremove_participants(group_id="g1", account_id="acc_1", participants=["123"])
        assert client._adelete.await_args == expected
    else:
        resource.remove_participants(group_id="g1", account_id="acc_1", participants=["123"])
        assert client._delete.call_args == expected


def test_base_client_delete_puts_data_in_the_json_body(monkeypatch):
    import httpx

    from late.client import base as client_base
    from late.client.base import BaseClient

    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"removed": True})

    real_client = httpx.Client
    monkeypatch.setattr(
        client_base.httpx,
        "Client",
        lambda **kwargs: real_client(**{**kwargs, "transport": httpx.MockTransport(handler)}),
    )

    BaseClient(api_key="k")._delete("/v1/x", params={"a": "1"}, data={"ids": ["1", "2"]})

    assert seen[0].method == "DELETE"
    assert seen[0].url.params["a"] == "1"
    assert seen[0].read() == b'{"ids":["1","2"]}'
