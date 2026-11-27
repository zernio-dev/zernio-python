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



def _body_type(generator, branches, combinator="anyOf", spec=SPEC):
    return generator.get_python_type({combinator: branches}, required=False, spec=spec, body=True)[0]


@pytest.mark.parametrize(
    ("branches", "expected"),
    [
        # timeIncrement: 1-90 days, or monthly / all_days.
        (
            [{"type": "string", "enum": ["monthly", "all_days"]}, {"type": "integer", "minimum": 1, "maximum": 90}],
            "int | Literal['monthly', 'all_days'] | None",
        ),
        # advantageAudience: the API takes true/false or 0/1.
        ([{"type": "integer", "enum": [0, 1]}, {"type": "boolean"}], "bool | Literal[0, 1] | None"),
        # flow_json / mailerContact: a JSON object or a string.
        ([{"type": "string"}, {"type": "object"}, {"type": "null"}], "dict[str, Any] | str | None"),
        # Shapes the spec does not use yet: one member per branch type.
        ([{"type": "string"}, {"type": "integer"}], "int | str | None"),
        ([{"type": "boolean"}, {"type": "integer"}, {"type": "number"}], "bool | int | float | None"),
        ([{"type": "array", "items": {"type": "string"}}, {"type": "string"}], "list[str] | str | None"),
        ([{"type": "string", "enum": ["a"]}, {"type": "string"}, {"type": "boolean"}], "bool | str | None"),
        ([{"type": "string", "enum": ["a"]}, {"type": "string", "enum": ["b"]}, {"type": "integer"}], "int | Literal['a', 'b'] | None"),
        ([{"$ref": "#/components/schemas/Media"}, {"type": "string"}], "dict[str, Any] | str | None"),
    ],
)
def test_mixed_body_union_maps_each_branch(generator, branches, expected):
    assert _body_type(generator, branches) == expected
    assert _body_type(generator, branches, combinator="oneOf") == expected


def test_union_member_order_does_not_follow_the_spec(generator):
    branches = [{"type": "string", "enum": ["monthly"]}, {"type": "null"}, {"type": "integer"}]
    assert _body_type(generator, branches) == _body_type(generator, branches[::-1]) == "int | Literal['monthly'] | None"


def test_a_required_body_union_has_no_none(generator):
    schema = {"oneOf": [{"type": "object"}, {"type": "string"}]}
    assert generator.get_python_type(schema, required=True, spec=SPEC, body=True) == ("dict[str, Any] | str", "")


@pytest.mark.parametrize(
    "branches",
    [
        [{"type": "string"}, {"type": "integer"}, {"description": "anything"}],
        [{"type": "integer"}, {"type": "boolean"}, {"anyOf": [{"type": "string"}, {"type": "object"}]}],
        [{"type": "string"}, {"type": "object"}, {"$ref": "#/components/schemas/Missing"}],
    ],
)
def test_a_branch_without_a_json_type_keeps_the_str_fallback(generator, branches):
    assert _body_type(generator, branches) == "str | None"


def test_query_and_path_unions_keep_the_str_fallback(generator):
    # The API coerces query text, and lax mode would rewrite it ("1" -> True -> "true").
    schema = {"anyOf": [{"type": "boolean"}, {"type": "integer"}]}
    assert generator.get_python_type(schema, required=False, spec=SPEC) == ("str | None", "None")
