#!/usr/bin/env python3
"""
Auto-generates Python resource classes from OpenAPI spec.

This script parses the OpenAPI spec and generates:
- Resource classes with sync and async methods for each endpoint
- Proper type hints and docstrings
- Snake_case method names from operationIds

Usage:
    python scripts/generate_resources.py
    # or
    uv run python scripts/generate_resources.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

# Map OpenAPI tags to resource class names
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
    "GMB Reviews": "accounts",  # Group under accounts
    "LinkedIn Mentions": "accounts",  # Group under accounts
}

# Resource descriptions for docstrings
RESOURCE_DESCRIPTIONS: dict[str, str] = {
    "posts": "Create, schedule, and manage social media posts",
    "accounts": "Manage connected social media accounts",
    "profiles": "Manage workspace profiles",
    "analytics": "Get performance metrics and analytics",
    "account_groups": "Organize accounts into groups",
    "queue": "Manage posting queue and time slots",
    "webhooks": "Configure event webhooks",
    "api_keys": "Manage API keys",
    "media": "Upload and manage media files",
    "tools": "Media download and utility tools",
    "users": "User management",
    "usage": "Get usage statistics",
    "logs": "Publishing logs for debugging",
    "connect": "OAuth connection flows",
    "reddit": "Reddit search and feed",
    "invites": "Team invitations",
}


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    # Replace hyphens with underscores first
    name = name.replace("-", "_")
    # Handle acronyms like 'URL' -> 'url', 'API' -> 'api'
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    return name.lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def get_python_type(schema: dict[str, Any], required: bool = True) -> str:
    """Convert OpenAPI schema to Python type hint."""
    if not schema:
        return "Any"

    schema_type = schema.get("type")

    if schema_type == "string":
        if schema.get("format") == "date-time":
            base = "datetime | str"
        else:
            base = "str"
    elif schema_type == "integer":
        base = "int"
    elif schema_type == "number":
        base = "float"
    elif schema_type == "boolean":
        base = "bool"
    elif schema_type == "array":
        items = schema.get("items", {})
        item_type = get_python_type(items)
        base = f"list[{item_type}]"
    elif schema_type == "object":
        base = "dict[str, Any]"
    else:
        base = "Any"

    if not required:
        return f"{base} | None"
    return base


def extract_parameters(operation: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract parameters from an operation."""
    params = []

    # Query/path parameters
    for param in operation.get("parameters", []):
        # Skip $ref parameters (they reference common params we'll handle differently)
        if "$ref" in param:
            # Handle common parameters by name
            ref = param["$ref"]
            if "PageParam" in ref:
                params.append({
                    "name": "page",
                    "original_name": "page",
                    "type": "int | None",
                    "required": False,
                    "description": "Page number (1-based)",
                    "in": "query",
                    "default": 1,
                })
            elif "LimitParam" in ref:
                params.append({
                    "name": "limit",
                    "original_name": "limit",
                    "type": "int | None",
                    "required": False,
                    "description": "Page size",
                    "in": "query",
                    "default": 10,
                })
            continue

        if "name" not in param:
            continue

        params.append({
            "name": camel_to_snake(param["name"]),
            "original_name": param["name"],
            "type": get_python_type(param.get("schema", {}), param.get("required", False)),
            "required": param.get("required", False),
            "description": param.get("description", ""),
            "in": param.get("in", "query"),
            "default": param.get("schema", {}).get("default"),
        })

    # Request body parameters
    request_body = operation.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})

        # Handle properties in request body
        properties = schema.get("properties", {})
        required_props = schema.get("required", [])

        for prop_name, prop_schema in properties.items():
            params.append({
                "name": camel_to_snake(prop_name),
                "original_name": prop_name,
                "type": get_python_type(prop_schema, prop_name in required_props),
                "required": prop_name in required_props,
                "description": prop_schema.get("description", ""),
                "in": "body",
                "default": prop_schema.get("default"),
            })

    return params


def generate_method_signature(
    method_name: str,
    params: list[dict[str, Any]],
    is_async: bool = False,
) -> str:
    """Generate method signature."""
    prefix = "async " if is_async else ""
    func_name = f"a{method_name}" if is_async else method_name

    # Separate required and optional parameters
    required_params = [p for p in params if p["required"]]
    optional_params = [p for p in params if not p["required"]]

    # Build parameter list
    param_strs = ["self"]

    # Required parameters first
    for param in required_params:
        param_strs.append(f"{param['name']}: {param['type']}")

    # Then keyword-only optional parameters
    if optional_params:
        if required_params:
            param_strs.append("*")
        else:
            param_strs.append("*")

        for param in optional_params:
            default = param.get("default")
            if default is None:
                default_str = "None"
            elif isinstance(default, str):
                default_str = f'"{default}"'
            elif isinstance(default, bool):
                default_str = str(default)
            else:
                default_str = str(default)

            # Clean up type for optional params
            param_type = param["type"]
            if "| None" not in param_type:
                param_type = f"{param_type} | None"

            param_strs.append(f"{param['name']}: {param_type} = {default_str}")

    return f"{prefix}def {func_name}({', '.join(param_strs)})"


def generate_method_body(
    http_method: str,
    path: str,
    params: list[dict[str, Any]],
    operation_id: str,
    is_async: bool = False,
) -> list[str]:
    """Generate method body."""
    lines = []
    await_prefix = "await " if is_async else ""
    client_method = f"_a{http_method.lower()}" if is_async else f"_{http_method.lower()}"

    # Build query params
    query_params = [p for p in params if p["in"] == "query"]
    body_params = [p for p in params if p["in"] == "body"]
    path_params = [p for p in params if p["in"] == "path"]

    # Handle path parameters
    path_expr = f'"{path}"'
    if path_params:
        # Replace {param} with f-string format
        path_formatted = path
        for p in path_params:
            path_formatted = path_formatted.replace(
                "{" + p["original_name"] + "}",
                "{" + p["name"] + "}"
            )
        path_expr = f'f"{path_formatted}"'

    # Determine if we need query params based on HTTP method
    # GET and DELETE use query params; POST/PUT/PATCH typically use body
    use_query_params = http_method.upper() in ("GET", "DELETE") and query_params
    use_body_params = http_method.upper() in ("POST", "PUT", "PATCH") and body_params
    # POST can also have query params in URL
    use_query_on_post = http_method.upper() in ("POST", "PUT", "PATCH") and query_params and not body_params

    # Build params dict if needed
    if use_query_params or use_query_on_post:
        lines.append("        params = self._build_params(")
        for p in query_params:
            lines.append(f"            {p['name']}={p['name']},")
        lines.append("        )")

    # Build payload dict if needed
    if use_body_params:
        lines.append("        payload = self._build_payload(")
        for p in body_params:
            lines.append(f"            {p['name']}={p['name']},")
        lines.append("        )")

    # Make the request
    if http_method.upper() == "GET":
        if query_params:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr}, params=params)")
        else:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr})")
    elif http_method.upper() == "DELETE":
        if query_params:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr}, params=params)")
        else:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr})")
    else:  # POST, PUT, PATCH
        if body_params:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr}, data=payload)")
        elif query_params:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr}, params=params)")
        else:
            lines.append(f"        return {await_prefix}self._client.{client_method}({path_expr})")

    return lines


def generate_resource_class(
    resource_name: str,
    operations: list[dict[str, Any]],
) -> str:
    """Generate a complete resource class."""
    class_name = "".join(word.title() for word in resource_name.split("_")) + "Resource"
    description = RESOURCE_DESCRIPTIONS.get(resource_name, f"{resource_name} operations")

    # Check if any operation uses datetime type
    uses_datetime = any(
        "datetime" in p.get("type", "")
        for op in operations
        for p in op.get("params", [])
    )

    lines = [
        '"""',
        f"Auto-generated {resource_name} resource.",
        "",
        "DO NOT EDIT THIS FILE MANUALLY.",
        "Run `python scripts/generate_resources.py` to regenerate.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Any",
        "",
        "if TYPE_CHECKING:",
    ]

    # Add datetime import inside TYPE_CHECKING block if needed
    if uses_datetime:
        lines.append("    from datetime import datetime")
        lines.append("")
        lines.append("    from ..client.base import BaseClient")
    else:
        lines.append("    from ..client.base import BaseClient")

    lines.extend([
        "",
        "",
        f"class {class_name}:",
        f'    """',
        f"    {description}.",
        f'    """',
        "",
        "    def __init__(self, client: BaseClient) -> None:",
        "        self._client = client",
        "",
        "    def _build_params(self, **kwargs: Any) -> dict[str, Any]:",
        '        """Build query parameters, filtering None values."""',
        "        def to_camel(s: str) -> str:",
        '            parts = s.split("_")',
        '            return parts[0] + "".join(p.title() for p in parts[1:])',
        "        return {to_camel(k): v for k, v in kwargs.items() if v is not None}",
        "",
        "    def _build_payload(self, **kwargs: Any) -> dict[str, Any]:",
        '        """Build request payload, filtering None values."""',
        "        from datetime import datetime",
        "        def to_camel(s: str) -> str:",
        '            parts = s.split("_")',
        '            return parts[0] + "".join(p.title() for p in parts[1:])',
        "        result: dict[str, Any] = {}",
        "        for k, v in kwargs.items():",
        "            if v is None:",
        "                continue",
        "            if isinstance(v, datetime):",
        "                result[to_camel(k)] = v.isoformat()",
        "            else:",
        "                result[to_camel(k)] = v",
        "        return result",
    ])

    # Generate sync methods
    for op in operations:
        method_name = camel_to_snake(op["operation_id"])
        params = op["params"]
        http_method = op["http_method"]
        path = op["path"]
        summary = op.get("summary", "")

        lines.append("")
        sig = generate_method_signature(method_name, params, is_async=False)
        lines.append(f"    {sig} -> dict[str, Any]:")
        lines.append(f'        """{summary}"""')
        body_lines = generate_method_body(http_method, path, params, op["operation_id"], is_async=False)
        lines.extend(body_lines)

    # Generate async methods
    for op in operations:
        method_name = camel_to_snake(op["operation_id"])
        params = op["params"]
        http_method = op["http_method"]
        path = op["path"]
        summary = op.get("summary", "")

        lines.append("")
        sig = generate_method_signature(method_name, params, is_async=True)
        lines.append(f"    {sig} -> dict[str, Any]:")
        lines.append(f'        """{summary} (async)"""')
        body_lines = generate_method_body(http_method, path, params, op["operation_id"], is_async=True)
        lines.extend(body_lines)

    return "\n".join(lines) + "\n"


def generate_init_file(resources: list[str]) -> str:
    """Generate __init__.py for resources."""
    lines = [
        '"""',
        "Auto-generated resource exports.",
        "",
        "DO NOT EDIT THIS FILE MANUALLY.",
        "Run `python scripts/generate_resources.py` to regenerate.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
    ]

    # Import each resource
    for resource in sorted(resources):
        class_name = "".join(word.title() for word in resource.split("_")) + "Resource"
        lines.append(f"from ._generated.{resource} import {class_name}")

    lines.append("")
    lines.append("__all__ = [")
    for resource in sorted(resources):
        class_name = "".join(word.title() for word in resource.split("_")) + "Resource"
        lines.append(f'    "{class_name}",')
    lines.append("]")

    return "\n".join(lines) + "\n"


def generate_client_resources(resources: list[str]) -> str:
    """Generate the resource initialization code for the client."""
    lines = []
    for resource in sorted(resources):
        class_name = "".join(word.title() for word in resource.split("_")) + "Resource"
        attr_name = resource
        lines.append(f"        self.{attr_name} = {class_name}(self)")
    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    openapi_path = project_root / "openapi.yaml"

    if not openapi_path.exists():
        print(f"Error: OpenAPI spec not found at {openapi_path}")
        print("Run 'curl -o openapi.yaml https://getlate.dev/openapi.yaml' first")
        return 1

    with openapi_path.open() as f:
        spec = yaml.safe_load(f)

    # Group operations by resource
    resources: dict[str, list[dict[str, Any]]] = {}

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            operation_id = operation.get("operationId")
            if not operation_id:
                print(f"Warning: No operationId for {method.upper()} {path}")
                continue

            tags = operation.get("tags", ["Other"])
            primary_tag = tags[0]
            resource_name = TAG_TO_RESOURCE.get(primary_tag, primary_tag.lower().replace(" ", "_"))

            if resource_name not in resources:
                resources[resource_name] = []

            resources[resource_name].append({
                "operation_id": operation_id,
                "http_method": method,
                "path": path,
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "params": extract_parameters(operation),
            })

    # Create output directory
    output_dir = project_root / "src" / "late" / "resources" / "_generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate each resource file
    generated_resources = []
    for resource_name, operations in resources.items():
        code = generate_resource_class(resource_name, operations)
        output_file = output_dir / f"{resource_name}.py"
        output_file.write_text(code)
        generated_resources.append(resource_name)
        print(f"Generated {output_file.name} with {len(operations)} methods")

    # Generate __init__.py for _generated
    init_content = '"""Auto-generated resources."""\n\nfrom __future__ import annotations\n\n'
    for resource in sorted(generated_resources):
        class_name = "".join(word.title() for word in resource.split("_")) + "Resource"
        init_content += f"from .{resource} import {class_name}\n"
    init_content += "\n__all__ = [\n"
    for resource in sorted(generated_resources):
        class_name = "".join(word.title() for word in resource.split("_")) + "Resource"
        init_content += f'    "{class_name}",\n'
    init_content += "]\n"

    (output_dir / "__init__.py").write_text(init_content)

    print(f"\nGenerated {len(generated_resources)} resource classes")
    print(f"Output: {output_dir}")

    # Print resource initialization code for the client
    print("\n# Add to Late client __init__:")
    print(generate_client_resources(generated_resources))

    return 0


if __name__ == "__main__":
    sys.exit(main())
