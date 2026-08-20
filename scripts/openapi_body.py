"""Shared request-body flattening for the SDK and MCP code generators."""

from __future__ import annotations

from typing import Any


def resolve_local_ref(ref: str, spec: dict[str, Any]) -> dict[str, Any]:
    node: Any = spec
    for part in ref.lstrip("#/").split("/"):
        if not isinstance(node, dict):
            return {}
        node = node.get(part, {})
    return node if isinstance(node, dict) else {}


def flatten_request_body_schema(
    schema: dict[str, Any], spec: dict[str, Any]
) -> dict[str, Any] | None:
    """Flatten a JSON request-body schema into {"properties", "required"}.

    Resolves $ref and merges allOf branches. Returns None for oneOf/anyOf
    unions: their variants cannot share one kwargs signature, so callers must
    fall back to a raw body parameter instead of dropping the body entirely.
    """
    if not isinstance(schema, dict) or not schema:
        return {"properties": {}, "required": []}
    if "$ref" in schema:
        return flatten_request_body_schema(
            resolve_local_ref(schema["$ref"], spec), spec
        )
    if "oneOf" in schema or "anyOf" in schema:
        return None
    if "allOf" in schema:
        properties: dict[str, Any] = {}
        required: list[str] = []
        for branch in schema["allOf"]:
            flattened_branch = flatten_request_body_schema(branch, spec)
            if flattened_branch is None:
                return None
            properties.update(flattened_branch["properties"])
            required.extend(flattened_branch["required"])
        properties.update(schema.get("properties", {}))
        required.extend(schema.get("required", []))
        return {"properties": properties, "required": required}
    return {
        "properties": schema.get("properties", {}),
        "required": schema.get("required", []),
    }
