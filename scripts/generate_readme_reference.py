#!/usr/bin/env python3
"""
Generate SDK Reference section for README.md from the OpenAPI spec.

This script parses the OpenAPI spec and generates markdown tables
documenting all available methods with descriptions from the spec.

New tags added to the OpenAPI spec are auto-discovered and included
in the README. Only special cases need explicit configuration below.
"""

import re
import sys
from pathlib import Path

import yaml

# Tags that should be merged into another resource instead of getting their own section
TAG_MERGE: dict[str, str] = {
    "GMB Reviews": "accounts",
    "LinkedIn Mentions": "accounts",
}

# Tags to skip entirely (no SDK methods)
SKIP_TAGS: set[str] = {
    "Inbox Access",
}

# Override display names (tag -> display name). Unmatched tags use the tag name as-is.
DISPLAY_NAME_OVERRIDES: dict[str, str] = {
    "Connect": "Connect (OAuth)",
    "Reddit Search": "Reddit",
    "Messages": "Messages (Inbox)",
    "Comments": "Comments (Inbox)",
    "Reviews": "Reviews (Inbox)",
}

# Override resource key names (tag -> snake_case key). Unmatched tags are auto-converted.
RESOURCE_KEY_OVERRIDES: dict[str, str] = {
    "Account Groups": "account_groups",
    "API Keys": "api_keys",
    "Reddit Search": "reddit",
}

# Preferred ordering for known resources. Auto-discovered resources appear after these.
PREFERRED_ORDER: list[str] = [
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
]

# Resources that should always appear last, in this order
LAST_RESOURCES: list[str] = [
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


def tag_to_resource_key(tag: str) -> str:
    """Convert a tag name to a snake_case resource key.

    e.g. "Account Groups" -> "account_groups", "Messages" -> "messages"
    """
    if tag in RESOURCE_KEY_OVERRIDES:
        return RESOURCE_KEY_OVERRIDES[tag]
    return tag.lower().replace(" ", "_")


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


def extract_methods_from_spec(
    spec: dict,
) -> tuple[dict[str, list[tuple[str, str]]], list[str], dict[str, str]]:
    """
    Extract methods and descriptions from OpenAPI spec.

    Returns (resources, resource_order, display_names).
    """
    resources: dict[str, list[tuple[str, str]]] = {}
    display_names: dict[str, str] = {}
    discovered: set[str] = set()

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            tags = operation.get("tags", [])
            if not tags:
                continue

            tag = tags[0]
            if tag in SKIP_TAGS:
                continue

            operation_id = operation.get("operationId", "")
            if not operation_id:
                continue

            # Resolve the resource key: merged tags go to their parent, others auto-generate
            resource_name = TAG_MERGE.get(tag) or tag_to_resource_key(tag)
            discovered.add(resource_name)

            # Track display name (non-merged tags only)
            if tag not in TAG_MERGE:
                display_names[resource_name] = DISPLAY_NAME_OVERRIDES.get(tag, tag)

            if resource_name not in resources:
                resources[resource_name] = []

            # Convert operationId to snake_case method name
            method_name = camel_to_snake(operation_id)

            # Use summary as description, or generate from method name
            summary = operation.get("summary", "")
            description = summary if summary else method_name.replace("_", " ").title()

            resources[resource_name].append((method_name, description))

    # Add SDK-only methods
    for resource_name, methods in SDK_ONLY_METHODS.items():
        if resource_name in resources:
            resources[resource_name].extend(methods)

    # Build final order: preferred first, then auto-discovered, then last resources
    preferred_set = set(PREFERRED_ORDER)
    last_set = set(LAST_RESOURCES)
    auto_discovered = sorted(
        r for r in discovered if r not in preferred_set and r not in last_set
    )

    resource_order = [
        *[r for r in PREFERRED_ORDER if r in discovered],
        *auto_discovered,
        *[r for r in LAST_RESOURCES if r in discovered],
    ]

    # Sort methods within each resource
    for resource_name in resource_order:
        if resource_name in resources:
            resources[resource_name] = sorted(
                resources[resource_name], key=lambda x: get_method_sort_key(x[0])
            )

    return resources, resource_order, display_names


def generate_reference_section(
    resources: dict[str, list[tuple[str, str]]],
    resource_order: list[str],
    display_names: dict[str, str],
) -> str:
    """Generate the SDK Reference section markdown."""
    lines = ["## SDK Reference", ""]

    for resource_name in resource_order:
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
    resources, resource_order, display_names = extract_methods_from_spec(spec)
    reference_section = generate_reference_section(resources, resource_order, display_names)

    if "--print" in sys.argv:
        print(reference_section)
    else:
        update_readme(readme_path, reference_section)


if __name__ == "__main__":
    main()
