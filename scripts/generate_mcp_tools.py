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
    "LinkedIn Mentions": "accounts",
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
    "createPost",
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


def get_python_type(schema: dict[str, Any], required: bool = True) -> tuple[str, str]:
    """Convert OpenAPI schema to Python type and default value."""
    if not schema:
        return "str", '""'

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
        type_str = "str"  # Accept comma-separated
        default_str = '""'
    else:
        type_str = "str"
        default_str = '""'

    if not required:
        return type_str, default_str
    return type_str, ""


def extract_parameters(operation: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract parameters from operation."""
    params = []

    for param in operation.get("parameters", []):
        if "$ref" in param:
            ref = param["$ref"]
            if "PageParam" in ref:
                params.append({
                    "name": "page",
                    "type": "int",
                    "required": False,
                    "default": "1",
                    "description": "Page number",
                    "sdk_name": "page",
                })
            elif "LimitParam" in ref:
                params.append({
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
            param.get("required", False)
        )

        params.append({
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
            type_str, default_str = get_python_type(prop_schema, is_required)

            params.append({
                "name": py_name,
                "type": type_str,
                "required": is_required,
                "default": default_str,
                "description": prop_schema.get("description", ""),
                "sdk_name": prop_name,
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

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            operation_id = operation.get("operationId")
            if not operation_id or operation_id in SKIP_OPERATIONS:
                continue

            tags = operation.get("tags", ["Other"])
            resource = TAG_TO_RESOURCE.get(tags[0], tags[0].lower())

            # Generate tool name from operationId
            sdk_method = camel_to_snake(operation_id)
            tool_name = f"{resource}_{sdk_method}"
            # Clean up redundant prefixes
            tool_name = re.sub(rf"^{resource}_{resource}_", f"{resource}_", tool_name)

            operations.append({
                "tool_name": tool_name,
                "resource": resource,
                "sdk_method": sdk_method,
                "summary": operation.get("summary", operation_id),
                "params": extract_parameters(operation),
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
        "                status = getattr(p, 'status', 'unknown')",
        '                lines.append(f"- [{status}] {content}...")',
        '            return "\\n".join(lines)',
        "        if hasattr(response, 'accounts') and response.accounts:",
        "            accs = response.accounts",
        '            lines = [f"Found {len(accs)} account(s):"]',
        "            for a in accs[:10]:",
        "                platform = getattr(a, 'platform', '?')",
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
        '            return f"Post ID: {getattr(p, \'field_id\', \'N/A\')}\\nStatus: {getattr(p, \'status\', \'N/A\')}"',
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
