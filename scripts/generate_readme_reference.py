#!/usr/bin/env python3
"""
Generate SDK Reference section for README.md from the OpenAPI spec.

This script parses the OpenAPI spec and generates markdown tables
documenting all available methods with descriptions from the spec.
"""

import re
import sys
from pathlib import Path

import yaml

# Map OpenAPI tags to SDK resource names and display names
TAG_TO_RESOURCE: dict[str, tuple[str, str]] = {
    "Posts": ("posts", "Posts"),
    "Accounts": ("accounts", "Accounts"),
    "Profiles": ("profiles", "Profiles"),
    "Analytics": ("analytics", "Analytics"),
    "Account Groups": ("account_groups", "Account Groups"),
    "Queue": ("queue", "Queue"),
    "Webhooks": ("webhooks", "Webhooks"),
    "API Keys": ("api_keys", "API Keys"),
    "Media": ("media", "Media"),
    "Tools": ("tools", "Tools"),
    "Users": ("users", "Users"),
    "Usage": ("usage", "Usage"),
    "Logs": ("logs", "Logs"),
    "Connect": ("connect", "Connect (OAuth)"),
    "Reddit Search": ("reddit", "Reddit"),
    "Invites": ("invites", "Invites"),
    # Group these under existing resources
    "GMB Reviews": ("accounts", "Accounts"),
    "LinkedIn Mentions": ("accounts", "Accounts"),
}

# Order of resources in the README
RESOURCE_ORDER = [
    "posts",
    "accounts",
    "profiles",
    "analytics",
    "account_groups",
    "queue",
    "webhooks",
    "api_keys",
    "media",
    "tools",
    "users",
    "usage",
    "logs",
    "connect",
    "reddit",
    "invites",
]

# Additional SDK-only methods not in OpenAPI (helper methods)
SDK_ONLY_METHODS: dict[str, list[tuple[str, str]]] = {
    "media": [
        ("upload", "Upload a file from path"),
        ("upload_bytes", "Upload file from bytes"),
        ("upload_large", "Upload large file with multipart"),
        ("upload_large_bytes", "Upload large file from bytes"),
        ("upload_multiple", "Upload multiple files"),
    ],
}


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    name = name.replace("-", "_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    return name.lower()


def get_method_sort_key(method_name: str) -> tuple:
    """
    Generate a sort key for consistent method ordering.

    Ordering rules (CRUD-style):
    1. list/get_all methods first
    2. bulk/create methods
    3. get (single) methods
    4. update methods
    5. delete methods
    6. Everything else alphabetically
    """
    name_lower = method_name.lower()

    if name_lower.startswith("list") or name_lower.startswith("get_all"):
        return (0, method_name)
    elif name_lower.startswith("bulk") or name_lower.startswith("create"):
        return (1, method_name)
    elif name_lower.startswith("get") and not name_lower.startswith("get_all"):
        return (2, method_name)
    elif name_lower.startswith("update"):
        return (3, method_name)
    elif name_lower.startswith("delete"):
        return (4, method_name)
    else:
        return (5, method_name)


def load_openapi_spec(spec_path: Path) -> dict:
    """Load and parse the OpenAPI spec."""
    with open(spec_path) as f:
        return yaml.safe_load(f)


def extract_methods_from_spec(spec: dict) -> dict[str, list[tuple[str, str]]]:
    """
    Extract methods and descriptions from OpenAPI spec.

    Returns a dict mapping resource names to list of (method_name, description) tuples.
    """
    resources: dict[str, list[tuple[str, str]]] = {name: [] for name in RESOURCE_ORDER}

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            tags = operation.get("tags", [])
            if not tags:
                continue

            tag = tags[0]
            if tag not in TAG_TO_RESOURCE:
                continue

            resource_name, _ = TAG_TO_RESOURCE[tag]
            operation_id = operation.get("operationId", "")
            summary = operation.get("summary", "")

            if not operation_id:
                continue

            # Convert operationId to snake_case method name
            method_name = camel_to_snake(operation_id)

            # Use summary as description, or generate from method name
            if summary:
                description = summary
            else:
                # Auto-generate from method name
                description = method_name.replace("_", " ").title()

            resources[resource_name].append((method_name, description))

    # Add SDK-only methods
    for resource_name, methods in SDK_ONLY_METHODS.items():
        if resource_name in resources:
            resources[resource_name].extend(methods)

    # Sort methods within each resource
    for resource_name in resources:
        resources[resource_name] = sorted(
            resources[resource_name],
            key=lambda x: get_method_sort_key(x[0])
        )

    return resources


def generate_reference_section(resources: dict[str, list[tuple[str, str]]]) -> str:
    """Generate the SDK Reference section markdown."""
    lines = ["## SDK Reference", ""]

    # Get display names
    display_names = {v[0]: v[1] for v in TAG_TO_RESOURCE.values()}

    for resource_name in RESOURCE_ORDER:
        methods = resources.get(resource_name, [])
        if not methods:
            continue

        display_name = display_names.get(resource_name, resource_name.title())

        lines.append(f"### {display_name}")
        lines.append("| Method | Description |")
        lines.append("|--------|-------------|")

        for method_name, description in methods:
            lines.append(f"| `{resource_name}.{method_name}()` | {description} |")

        lines.append("")

    return "\n".join(lines)


def update_readme(readme_path: Path, reference_section: str) -> None:
    """Update the README.md file with the new SDK Reference section."""
    content = readme_path.read_text()

    # Find the SDK Reference section and replace it
    # It starts with "## SDK Reference" and ends before "## MCP Server"
    pattern = r"## SDK Reference\n.*?(?=## MCP Server)"
    replacement = reference_section + "\n"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content != content:
        readme_path.write_text(new_content)
        print(f"Updated {readme_path}")
    else:
        print("No changes needed")


def main():
    script_dir = Path(__file__).parent
    spec_path = script_dir.parent / "openapi.yaml"
    readme_path = script_dir.parent / "README.md"

    spec = load_openapi_spec(spec_path)
    resources = extract_methods_from_spec(spec)
    reference_section = generate_reference_section(resources)

    if "--print" in sys.argv:
        print(reference_section)
    else:
        update_readme(readme_path, reference_section)


if __name__ == "__main__":
    main()
