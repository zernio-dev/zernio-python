"""Spec defaults of {} or [] must not become shared mutable kwarg defaults."""

import importlib
from pathlib import Path
from unittest.mock import Mock


def test_empty_object_and_array_defaults_are_omitted(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    generator = importlib.import_module("generate_resources")
    operation = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "inputs": {"type": "object", "default": {}},
                            "targets": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                            "status": {"type": "string", "default": "paused"},
                        },
                    }
                }
            }
        }
    }
    source = generator.generate_resource_class(
        "probe",
        [
            {
                "operation_id": "installTemplate",
                "http_method": "post",
                "path": "/v1/templates/install",
                "summary": "Install template",
                "description": "",
                "params": generator.extract_parameters(operation, {}),
            }
        ],
    )

    assert "= {}," not in source
    assert "= []," not in source

    namespace = {}
    exec(compile(source, "<generated-probe>", "exec"), namespace)
    client = Mock()
    client._post = Mock(return_value={})
    namespace["ProbeResource"](client).install_template()
    client._post.assert_called_once_with(
        "/v1/templates/install", data={"status": "paused"}
    )
