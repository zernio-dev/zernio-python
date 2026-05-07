#!/usr/bin/env python3
"""
Auto-generates MCP tool handlers from OpenAPI spec.

This script parses the OpenAPI spec and generates complete MCP tool handlers
that wrap the SDK resources. The generated code can be imported directly
into server.py.

Usage:
    python scripts/generate_mcp_tools.py
    # or
    uv run python scripts/generate_mcp_tools.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

# Map OpenAPI tags to SDK resource names
TAG_TO_RESOURCE: dict[str, str] = {
    "Posts": "posts",
    "Accounts": "accounts",
    "Profiles": "profiles",
    "Analytics": "analytics",
    "Account Groups": "account_groups",
    "Queue": "queue",
    "Webhooks": "webhooks",
    "API Keys": "api_keys",
    "Media": "media",
    "Tools": "tools",
    "Users": "users",
    "Usage": "usage",
    "Logs": "logs",
    "Connect": "connect",
    "Reddit Search": "reddit",
    "Invites": "invites",
    "GMB Reviews": "accounts",
    "GMB Food Menus": "accounts",
    "GMB Location Details": "accounts",
    "GMB Media": "accounts",
    "GMB Attributes": "accounts",
    "GMB Place Actions": "accounts",
    "LinkedIn Mentions": "accounts",
    "Validate": "validate",
}

# Operations to SKIP (not useful for MCP)
SKIP_OPERATIONS = {
    # OAuth redirect endpoints
    "connectPlatform",
    "startBlueskyConnect",
    "completeTiktokAuth",
    "startSnapchatConnect",
    # Internal endpoints
    "deleteUser",
    "deleteTeam",
    # Already have custom implementations
    # Note: createPost is intentionally NOT skipped anymore. The simplified
    # posts_create wrapper in tool_definitions.py is friendlier for single-
    # account flows, but power users (agencies cross-posting with per-target
    # customContent / scheduledFor / platformSpecificData) need the full
    # nested-array form. Both are exposed; LLMs pick whichever fits.
    "retryPost",
    "generateMediaUploadToken",
    "checkMediaUploadToken",
}


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    name = name.replace("-", "_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    return name.lower()


def _resolve_ref(ref: str, spec: dict[str, Any]) -> dict[str, Any]:
    """Resolve a `#/components/schemas/Foo` style JSON-pointer against spec.

    Returns an empty dict if any segment is missing, so callers can keep
    walking without raising on a malformed/external ref.
    """
    parts = ref.lstrip("#/").split("/")
    node: Any = spec
    for p in parts:
        if not isinstance(node, dict):
            return {}
        node = node.get(p, {})
    return node if isinstance(node, dict) else {}


def _resolve_schema(schema: dict[str, Any], spec: dict[str, Any] | None) -> dict[str, Any]:
    """Dereference a property schema into something with a concrete `type`.

    Handles three composite forms commonly used in our OpenAPI spec:

      - `{"$ref": "..."}`        -> look up the target schema.
      - `{"allOf": [{...}, ...]}` -> return the first branch with a concrete
        `type` (we mostly see single-element allOf as a "ref + description"
        pattern, but this generalises safely).
      - `{"oneOf"|"anyOf": [...]}` -> if every branch resolves to the same
        scalar/object/array `type`, return that branch; otherwise leave the
        schema alone so the caller falls back to `str`. A deliberately
        over-broad type is worse than no type for the LLM.

    Without spec access (spec=None) the function is a no-op so unit tests
    that don't load the full spec still work.
    """
    if not schema or not isinstance(schema, dict) or spec is None:
        return schema

    if "$ref" in schema:
        return _resolve_schema(_resolve_ref(schema["$ref"], spec), spec)

    if "allOf" in schema and isinstance(schema["allOf"], list):
        for branch in schema["allOf"]:
            resolved = _resolve_schema(branch, spec)
            if resolved.get("type") in ("string", "integer", "number", "boolean", "array", "object"):
                return resolved

    for combinator in ("oneOf", "anyOf"):
        if combinator in schema and isinstance(schema[combinator], list):
            resolved_branches = [_resolve_schema(b, spec) for b in schema[combinator]]
            types = {b.get("type") for b in resolved_branches if isinstance(b, dict)}
            types.discard(None)
            if len(types) == 1:
                only = types.pop()
                for b in resolved_branches:
                    if b.get("type") == only:
                        return b

    return schema


def get_python_type(
    schema: dict[str, Any],
    required: bool = True,
    spec: dict[str, Any] | None = None,
) -> tuple[str, str]:
    """Convert OpenAPI schema to a Python type annotation and default literal.

    For scalar types (string/integer/number/boolean) we map to the obvious
    Python type with a sensible default ('', 0, 0.0, False).

    For complex types (array / object) we emit proper container types with a
    `None` default. Previously these were collapsed to `str = ""` with the
    intent that callers would pass comma-separated strings, but the
    generated wrapper never parsed them back - it forwarded the literal
    string straight into the SDK, which then sent it to the API expecting
    an array/object and got rejected with `Expected array, received string`.

    Emitting the correct container type (e.g. `list[str] | None`) means:
      - FastMCP's JSON-schema introspection now declares the right shape
        to the LLM, so the model passes a real array.
      - The SDK's `_build_payload` already filters `None` values, so leaving
        an unused param at `None` is a no-op upstream.

    Item types for arrays are inferred from `items.type`; $ref/allOf wrappers
    on either the top-level schema or the items schema are dereferenced via
    `_resolve_schema`. Unknown item types fall back to `Any`.
    """
    if not schema:
        return "str", '""'

    # Dereference $ref / allOf / single-type oneOf|anyOf so we can read the
    # underlying `type` consistently. Without this, properties like
    # `createPost.tiktokSettings` (a $ref to an object schema) would fall
    # through to the `str` branch and the wrapper would forward a string
    # where the API expects an object.
    schema = _resolve_schema(schema, spec)

    schema_type = schema.get("type")
    default = schema.get("default")

    if schema_type == "string":
        type_str = "str"
        default_str = f'"{default}"' if default else '""'
    elif schema_type == "integer":
        type_str = "int"
        default_str = str(default) if default is not None else "0"
    elif schema_type == "number":
        type_str = "float"
        default_str = str(default) if default is not None else "0.0"
    elif schema_type == "boolean":
        type_str = "bool"
        default_str = str(default) if default is not None else "False"
    elif schema_type == "array":
        # Inspect items.type so the LLM gets the right inner schema. Most
        # array fields in the spec hold strings (countries, keywords, etc.)
        # or objects (cities, interests, creatives, plus any $ref-wrapped
        # object). Items themselves may be $ref/allOf/oneOf so resolve
        # before reading the type.
        items_schema = _resolve_schema(schema.get("items", {}) or {}, spec)
        items_type = items_schema.get("type")
        if items_type == "string":
            inner = "str"
        elif items_type == "integer":
            inner = "int"
        elif items_type == "number":
            inner = "float"
        elif items_type == "boolean":
            inner = "bool"
        elif items_type == "object":
            inner = "dict[str, Any]"
        else:
            inner = "Any"
        type_str = f"list[{inner}] | None"
        default_str = "None"
    elif schema_type == "object":
        type_str = "dict[str, Any] | None"
        default_str = "None"
    else:
        type_str = "str"
        default_str = '""'

    if not required:
        return type_str, default_str
    return type_str, ""


def extract_parameters(
    operation: dict[str, Any],
    spec: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Extract parameters from operation.

    `spec` is threaded through so `get_python_type` can dereference
    `$ref`/`allOf` schemas to read the underlying type.

    Dedupes by Python name: when the same parameter appears in both the path
    and the request body (e.g. `accountId` as a path param and also in the
    body schema), Python can't accept duplicate kwargs in a function
    signature, so we keep the first occurrence (path > query > body) and
    drop subsequent ones. This prevents SyntaxErrors in generated_tools.py.
    """
    params: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    def add_param(entry: dict[str, Any]) -> None:
        if entry["name"] in seen_names:
            return
        seen_names.add(entry["name"])
        params.append(entry)

    for param in operation.get("parameters", []):
        if "$ref" in param:
            ref = param["$ref"]
            if "PageParam" in ref:
                add_param({
                    "name": "page",
                    "type": "int",
                    "required": False,
                    "default": "1",
                    "description": "Page number",
                    "sdk_name": "page",
                })
            elif "LimitParam" in ref:
                add_param({
                    "name": "limit",
                    "type": "int",
                    "required": False,
                    "default": "10",
                    "description": "Results per page",
                    "sdk_name": "limit",
                })
            continue

        if "name" not in param:
            continue

        # Skip header parameters - they're handled differently in SDK
        if param.get("in") == "header":
            continue

        py_name = camel_to_snake(param["name"])
        # SDK name must also be valid Python identifier
        sdk_name = camel_to_snake(param["name"]).replace("-", "_")
        # MCP doesn't allow params starting with underscore
        if py_name.startswith("_"):
            py_name = py_name.lstrip("_") + "_id" if py_name == "_id" else py_name.lstrip("_")

        type_str, default_str = get_python_type(
            param.get("schema", {}),
            param.get("required", False),
            spec,
        )

        add_param({
            "name": py_name,
            "type": type_str,
            "required": param.get("required", False),
            "default": default_str,
            "description": param.get("description", ""),
            "sdk_name": sdk_name,
        })

    # Request body
    request_body = operation.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        properties = schema.get("properties", {})
        required_props = schema.get("required", [])

        for prop_name, prop_schema in properties.items():
            py_name = camel_to_snake(prop_name)
            # MCP doesn't allow params starting with underscore
            if py_name.startswith("_"):
                py_name = py_name.lstrip("_")
                if not py_name:  # Was just "_"
                    continue
            is_required = prop_name in required_props
            type_str, default_str = get_python_type(prop_schema, is_required, spec)

            add_param({
                "name": py_name,
                "type": type_str,
                "required": is_required,
                "default": default_str,
                "description": prop_schema.get("description", ""),
                "sdk_name": py_name,
            })

    return params


def generate_tool_handler(
    tool_name: str,
    resource: str,
    sdk_method: str,
    summary: str,
    params: list[dict[str, Any]],
) -> str:
    """Generate a complete tool handler function."""
    lines = []

    # Sort params: required first, then optional
    required = [p for p in params if p["required"]]
    optional = [p for p in params if not p["required"]]

    # Build function signature
    sig_params = []
    for p in required:
        sig_params.append(f"{p['name']}: {p['type']}")
    for p in optional:
        sig_params.append(f"{p['name']}: {p['type']} = {p['default']}")

    sig = ", ".join(sig_params)

    # Docstring - strip trailing whitespace from all lines
    doc_lines = [summary.rstrip()]
    if params:
        doc_lines.append("")
        doc_lines.append("Args:")
        for p in params:
            req = " (required)" if p["required"] else ""
            desc = p['description'] if p['description'] else ""
            # Strip trailing whitespace from each line of multiline descriptions
            desc = "\n".join(line.rstrip() for line in desc.split("\n"))
            # Avoid trailing whitespace when description is empty
            if desc:
                doc_lines.append(f"    {p['name']}: {desc}{req}")
            else:
                doc_lines.append(f"    {p['name']}:{req}" if req else f"    {p['name']}")

    # Strip trailing whitespace from all docstring lines
    docstring = "\n    ".join(line.rstrip() for line in doc_lines)

    lines.append("")
    lines.append("")
    lines.append("@mcp.tool()")
    lines.append(f"def {tool_name}({sig}) -> str:")
    lines.append(f'    """{docstring}"""')
    lines.append("    client = _get_client()")

    # Build SDK call - always use keyword args for clarity
    sdk_args = []
    for p in params:
        sdk_name = p.get("sdk_name", p["name"])
        sdk_args.append(f"{sdk_name}={p['name']}")

    lines.append(f"    try:")
    lines.append(f"        response = client.{resource}.{sdk_method}({', '.join(sdk_args)})")
    lines.append(f"        return _format_response(response)")
    lines.append(f"    except Exception as e:")
    lines.append(f"        return f'Error: {{e}}'")

    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    openapi_path = project_root / "openapi.yaml"

    if not openapi_path.exists():
        print(f"Error: OpenAPI spec not found at {openapi_path}")
        return 1

    with openapi_path.open() as f:
        spec = yaml.safe_load(f)

    # Collect operations
    operations = []

    # Track tool_names already emitted. Two different (path, method) pairs can
    # produce the same tool_name when their operationIds snake-case to the
    # same string, or when the spec has a duplicate operation. Either way,
    # emitting two @mcp.tool() functions with the same name causes an F811
    # redefinition lint failure, so we skip collisions with a warning.
    seen_tool_names: set[str] = set()

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            operation_id = operation.get("operationId")
            if not operation_id or operation_id in SKIP_OPERATIONS:
                continue

            tags = operation.get("tags", ["Other"])
            resource = TAG_TO_RESOURCE.get(tags[0], tags[0].lower().replace(" ", "_"))

            # Generate tool name from operationId
            sdk_method = camel_to_snake(operation_id)
            tool_name = f"{resource}_{sdk_method}"
            # Clean up redundant prefixes
            tool_name = re.sub(rf"^{resource}_{resource}_", f"{resource}_", tool_name)

            if tool_name in seen_tool_names:
                print(
                    f"Warning: duplicate MCP tool_name '{tool_name}' at "
                    f"{method.upper()} {path} (operationId={operation_id}); skipping.",
                    file=sys.stderr,
                )
                continue
            seen_tool_names.add(tool_name)

            operations.append({
                "tool_name": tool_name,
                "resource": resource,
                "sdk_method": sdk_method,
                "summary": operation.get("summary", operation_id),
                "params": extract_parameters(operation, spec),
            })

    # Generate output file
    lines = [
        '"""',
        "Auto-generated MCP tool handlers.",
        "",
        "DO NOT EDIT - Run `python scripts/generate_mcp_tools.py` to regenerate.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "",
        "def _enum_str(value: Any) -> str:",
        '    """Extract string value from an enum or return as-is if already a string.',
        "",
        '    The auto-generated models use plain Enum classes (Platform5, etc.) whose',
        "    str() returns 'Platform5.TWITTER' instead of 'twitter'. This helper",
        '    normalises any enum value to its underlying string.',
        '    """',
        "    if value is None:",
        '        return ""',
        "    if isinstance(value, str):",
        "        return value",
        "    if hasattr(value, 'value'):",
        "        return str(value.value)",
        "    return str(value)",
        "",
        "",
        "def _format_response(response: Any) -> str:",
        '    """Format SDK response for MCP output."""',
        "    if response is None:",
        '        return "Success"',
        "    if hasattr(response, '__dict__'):",
        "        # Handle response objects",
        "        if hasattr(response, 'posts') and response.posts:",
        "            posts = response.posts",
        '            lines = [f"Found {len(posts)} post(s):"]',
        "            for p in posts[:10]:",
        "                content = str(getattr(p, 'content', ''))[:50]",
        "                status = _enum_str(getattr(p, 'status', 'unknown'))",
        '                lines.append(f"- [{status}] {content}...")',
        '            return "\\n".join(lines)',
        "        if hasattr(response, 'accounts') and response.accounts:",
        "            accs = response.accounts",
        '            lines = [f"Found {len(accs)} account(s):"]',
        "            for a in accs[:10]:",
        "                platform = _enum_str(getattr(a, 'platform', '?'))",
        "                username = getattr(a, 'username', None) or getattr(a, 'displayName', '?')",
        '                lines.append(f"- {platform}: {username}")',
        '            return "\\n".join(lines)',
        "        if hasattr(response, 'profiles') and response.profiles:",
        "            profiles = response.profiles",
        '            lines = [f"Found {len(profiles)} profile(s):"]',
        "            for p in profiles[:10]:",
        "                name = getattr(p, 'name', 'Unnamed')",
        '                lines.append(f"- {name}")',
        '            return "\\n".join(lines)',
        "        if hasattr(response, 'post') and response.post:",
        "            p = response.post",
        '            return f"Post ID: {getattr(p, \'field_id\', \'N/A\')}\\nStatus: {_enum_str(getattr(p, \'status\', \'N/A\'))}"',
        "        if hasattr(response, 'profile') and response.profile:",
        "            p = response.profile",
        '            return f"Profile: {getattr(p, \'name\', \'N/A\')} (ID: {getattr(p, \'field_id\', \'N/A\')})"',
        "    return str(response)",
        "",
        "",
        "def register_generated_tools(mcp, _get_client):",
        '    """Register all auto-generated tools with the MCP server."""',
    ]

    # Group by resource for organization
    by_resource: dict[str, list] = {}
    for op in operations:
        res = op["resource"]
        if res not in by_resource:
            by_resource[res] = []
        by_resource[res].append(op)

    # Generate handlers inside register function
    for resource, ops in sorted(by_resource.items()):
        lines.append(f"")
        lines.append(f"    # {resource.upper()}")

        for op in ops:
            handler = generate_tool_handler(
                op["tool_name"],
                op["resource"],
                op["sdk_method"],
                op["summary"],
                op["params"],
            )
            # Indent for being inside register function
            handler_lines = handler.split("\n")
            for hl in handler_lines:
                if hl.strip():
                    lines.append(f"    {hl}")
                else:
                    lines.append("")

    # Output
    output_file = project_root / "src" / "late" / "mcp" / "generated_tools.py"
    output_file.write_text("\n".join(lines) + "\n")

    print(f"Generated {output_file}")
    print(f"Total tools: {len(operations)}")
    print(f"\nTo use: import and call register_generated_tools(mcp, _get_client) in server.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
