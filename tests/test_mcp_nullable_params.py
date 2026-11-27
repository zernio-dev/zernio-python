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


TIME_INCREMENT = {
    "anyOf": [
        {"type": "string", "enum": ["monthly", "all_days"]},
        {"type": "integer", "minimum": 1, "maximum": 90},
    ]
}


def test_integer_or_string_enum_union_is_int_or_literal(generator):
    # A JSON body is not coerced by the API, so `str` sent days as "7".
    assert generator.get_python_type(TIME_INCREMENT, required=False, spec=SPEC) == (
        "int | Literal['monthly', 'all_days'] | None",
        "None",
    )
    one_of = {"oneOf": list(reversed(TIME_INCREMENT["anyOf"])) + [{"type": "null"}]}
    assert generator.get_python_type(one_of, required=True, spec=SPEC) == ("int | Literal['monthly', 'all_days']", "")


@pytest.mark.parametrize(
    "branches",
    [
        [{"type": "string"}, {"type": "integer"}],
        [{"type": "string", "enum": ["monthly"]}, {"type": "number"}],
        [{"type": "string", "enum": ["monthly"]}, {"type": "integer"}, {"type": "boolean"}],
        [{"type": "string", "enum": ["monthly"]}, {"type": "integer"}, {"type": "integer"}],
    ],
)
def test_other_mixed_unions_keep_the_str_fallback(generator, branches):
    assert generator.get_python_type({"anyOf": branches}, required=False, spec=SPEC)[0] == "str | None"


@pytest.mark.parametrize(
    ("branches", "expected"),
    [
        # advantageAudience: the API takes true/false or 0/1.
        ([{"type": "integer", "enum": [0, 1]}, {"type": "boolean"}], "bool | Literal[0, 1] | None"),
        ([{"type": "boolean"}, {"type": "integer"}, {"type": "null"}], "bool | int | None"),
        # flow_json / mailerContact: a JSON object or a string.
        ([{"type": "object"}, {"type": "string"}], "dict[str, Any] | str | None"),
        ([{"type": "string"}, {"type": "object"}, {"type": "null"}], "dict[str, Any] | str | None"),
    ],
)
def test_bool_int_and_object_string_unions_keep_both_types(generator, branches, expected):
    assert generator.get_python_type({"oneOf": branches}, required=False, spec=SPEC) == (expected, "None")


@pytest.mark.parametrize(
    "branches",
    [
        [{"type": "boolean"}, {"type": "integer"}, {"type": "string"}],
        [{"type": "boolean"}, {"type": "number"}],
        [{"type": "object"}, {"type": "string", "enum": ["a"]}],
        [{"type": "object"}, {"type": "array", "items": {"type": "string"}}],
        [{"type": "object"}, {"type": "string"}, {"type": "string"}],
    ],
)
def test_neighbouring_mixed_unions_keep_the_str_fallback(generator, branches):
    assert generator.get_python_type({"anyOf": branches}, required=False, spec=SPEC)[0] == "str | None"
