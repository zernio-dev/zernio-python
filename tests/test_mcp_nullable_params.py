"""A nullable param ("send null to clear") is typed as its non-null type, not str."""

import importlib
from pathlib import Path

import pytest

SPEC = {
    "components": {
        "schemas": {
            "Media": {"type": "object", "properties": {"url": {"type": "string"}}},
        }
    }
}


@pytest.fixture
def generator(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("generate_mcp_tools")


@pytest.mark.parametrize(
    ("schema", "expected"),
    [
        ({"oneOf": [{"$ref": "#/components/schemas/Media"}, {"type": "null"}]}, "dict[str, Any] | None"),
        ({"type": ["array", "null"], "items": {"type": "string"}}, "list[str] | None"),
        ({"type": ["integer", "null"]}, "int | None"),
    ],
)
def test_nullable_param_keeps_its_type(generator, schema, expected):
    type_str, default = generator.get_python_type(schema, required=False, spec=SPEC)
    assert (type_str, default) == (expected, "None")


def test_a_real_union_still_falls_back_to_str(generator):
    schema = {"oneOf": [{"type": "string"}, {"type": "integer"}, {"type": "null"}]}
    assert generator.get_python_type(schema, required=False, spec=SPEC)[0] == "str | None"


AD_STATUS_SPEC = {
    "components": {
        "schemas": {
            "AdStatus": {
                "type": "string",
                "enum": ["active", "paused", "pending_review", "rejected", "completed", "cancelled", "error"],
            },
        }
    }
}


def test_string_union_keeps_every_branch_enum(generator):
    schema = {"anyOf": [{"$ref": "#/components/schemas/AdStatus"}, {"type": "string", "enum": ["not_deleted"]}]}
    assert generator.get_python_type(schema, required=False, spec=AD_STATUS_SPEC)[0] == (
        "Literal['active', 'paused', 'pending_review', 'rejected', 'completed', 'cancelled', 'error', 'not_deleted'] | None"
    )


def test_string_union_with_an_open_branch_is_plain_str(generator):
    schema = {"oneOf": [{"$ref": "#/components/schemas/AdStatus"}, {"type": "string"}]}
    assert generator.get_python_type(schema, required=False, spec=AD_STATUS_SPEC)[0] == "str | None"
