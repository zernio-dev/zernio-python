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
