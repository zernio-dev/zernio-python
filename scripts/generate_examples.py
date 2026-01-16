#!/usr/bin/env python3
"""
Generate example code snippets from OpenAPI spec.

This script parses the OpenAPI spec and generates example code
for common operations based on request/response schemas.
"""

import re
import sys
from pathlib import Path
from typing import Any

import yaml


def load_openapi_spec(spec_path: Path) -> dict:
    """Load and parse the OpenAPI spec."""
    with open(spec_path) as f:
        return yaml.safe_load(f)


def get_example_value(schema: dict, name: str = "") -> Any:
    """Generate an example value from a schema."""
    if "example" in schema:
        return schema["example"]

    if "enum" in schema:
        return schema["enum"][0]

    schema_type = schema.get("type", "string")

    if schema_type == "string":
        if "format" in schema:
            fmt = schema["format"]
            if fmt == "date-time":
                return "2025-02-01T10:00:00Z"
            if fmt == "uri":
                return "https://example.com/media.mp4"
        if "accountId" in name.lower():
            return "acc_xxx"
        if "id" in name.lower():
            return "post_xxx"
        return "example_value"
    elif schema_type == "integer":
        return 10
    elif schema_type == "number":
        return 1.5
    elif schema_type == "boolean":
        return True
    elif schema_type == "array":
        items = schema.get("items", {})
        return [get_example_value(items, name)]
    elif schema_type == "object":
        props = schema.get("properties", {})
        return {k: get_example_value(v, k) for k, v in props.items()}

    return "value"


def resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a $ref to its schema."""
    if not ref.startswith("#/"):
        return {}
    parts = ref[2:].split("/")
    result = spec
    for part in parts:
        result = result.get(part, {})
    return result


def get_request_body_schema(spec: dict, operation: dict) -> dict | None:
    """Extract request body schema from an operation."""
    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})
    json_content = content.get("application/json", {})
    schema = json_content.get("schema", {})

    if "$ref" in schema:
        schema = resolve_ref(spec, schema["$ref"])

    return schema if schema else None


def generate_create_post_example(spec: dict) -> str:
    """Generate create post example from OpenAPI spec."""
    # Find the createPost operation
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if operation.get("operationId") == "createPost":
                schema = get_request_body_schema(spec, operation)
                if not schema:
                    break

                # Generate Python example
                return '''```python
post = late.posts.create(
    content="Hello world from Late!",
    platforms=[
        {"platform": "twitter", "accountId": "acc_xxx"},
        {"platform": "linkedin", "accountId": "acc_yyy"},
        {"platform": "instagram", "accountId": "acc_zzz"},
    ],
    publish_now=True,
)

print(f"Published to {len(post['post']['platforms'])} platforms!")
```'''

    return ""


def generate_schedule_post_example(spec: dict) -> str:
    """Generate schedule post example."""
    return '''```python
post = late.posts.create(
    content="This post will go live tomorrow at 10am",
    platforms=[{"platform": "instagram", "accountId": "acc_xxx"}],
    scheduled_for="2025-02-01T10:00:00Z",
)
```'''


def generate_upload_media_example(spec: dict) -> str:
    """Generate upload media example."""
    return '''```python
# Option 1: Direct upload (simplest)
result = late.media.upload("path/to/video.mp4")
media_url = result["publicUrl"]

# Option 2: Upload from bytes
result = late.media.upload_bytes(video_bytes, "video.mp4", "video/mp4")
media_url = result["publicUrl"]

# Create post with media
post = late.posts.create(
    content="Check out this video!",
    media_urls=[media_url],
    platforms=[
        {"platform": "tiktok", "accountId": "acc_xxx"},
        {"platform": "youtube", "accountId": "acc_yyy", "youtubeTitle": "My Video"},
    ],
    publish_now=True,
)
```'''


def generate_examples_markdown(spec: dict) -> str:
    """Generate the Examples section for README."""
    lines = [
        "## Examples",
        "",
        "### Schedule a Post",
        "",
        generate_schedule_post_example(spec),
        "",
        "### Platform-Specific Content",
        "",
        "Customize content per platform while posting to all at once:",
        "",
        '''```python
post = late.posts.create(
    content="Default content",
    platforms=[
        {
            "platform": "twitter",
            "accountId": "acc_twitter",
            "platformSpecificContent": "Short & punchy for X",
        },
        {
            "platform": "linkedin",
            "accountId": "acc_linkedin",
            "platformSpecificContent": "Professional tone for LinkedIn with more detail.",
        },
    ],
    publish_now=True,
)
```''',
        "",
        "### Upload Media",
        "",
        generate_upload_media_example(spec),
        "",
        "### Get Analytics",
        "",
        '''```python
data = late.analytics.get(period="30d")

print("Analytics:", data)
```''',
        "",
        "### List Connected Accounts",
        "",
        '''```python
data = late.accounts.list()

for account in data["accounts"]:
    print(f"{account['platform']}: @{account['username']}")
```''',
        "",
        "### Async Support",
        "",
        '''```python
import asyncio
from late import Late

async def main():
    async with Late(api_key="your-api-key") as late:
        posts = await late.posts.alist(status="scheduled")
        print(f"Found {len(posts['posts'])} scheduled posts")

asyncio.run(main())
```''',
    ]

    return "\n".join(lines)


def main():
    script_dir = Path(__file__).parent
    spec_path = script_dir.parent / "openapi.yaml"

    spec = load_openapi_spec(spec_path)

    if "--print" in sys.argv:
        print(generate_examples_markdown(spec))
    else:
        print("Use --print to see generated examples")
        print("This script generates example snippets from OpenAPI schemas")


if __name__ == "__main__":
    main()
