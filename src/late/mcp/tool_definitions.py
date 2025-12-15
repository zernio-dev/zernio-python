"""
Centralized tool definitions for MCP and documentation.

This file is the single source of truth for tool parameters and descriptions.
Used by:
- MCP server (server.py) for tool definitions
- Documentation generation (can be exported to MDX)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ParamDef:
    """Definition of a tool parameter."""

    name: str
    type: str
    description: str
    required: bool = False
    default: Any = None

    def to_mdx_row(self) -> str:
        """Generate MDX table row."""
        req = "Yes" if self.required else "No"
        default_str = f"`{self.default}`" if self.default is not None else "-"
        return f"| `{self.name}` | `{self.type}` | {self.description} | {req} | {default_str} |"


@dataclass
class ToolDef:
    """Definition of a tool."""

    name: str
    description: str
    params: list[ParamDef]

    def to_mdx_section(self) -> str:
        """Generate MDX documentation section."""
        lines = [
            f"### {self.name}",
            "",
            self.description,
            "",
            "| Parameter | Type | Description | Required | Default |",
            "|-----------|------|-------------|----------|---------|",
        ]
        lines.extend(p.to_mdx_row() for p in self.params)
        return "\n".join(lines)


# =============================================================================
# POSTS TOOL DEFINITIONS
# =============================================================================

POSTS_CREATE_PARAMS = [
    ParamDef(
        name="content",
        type="str",
        description="The post content/text",
        required=True,
    ),
    ParamDef(
        name="platform",
        type="str",
        description="Target platform: twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads",
        required=True,
    ),
    ParamDef(
        name="is_draft",
        type="bool",
        description="Save as draft without scheduling. Draft posts can be edited and scheduled later",
        required=False,
        default=False,
    ),
    ParamDef(
        name="publish_now",
        type="bool",
        description="Publish immediately instead of scheduling",
        required=False,
        default=False,
    ),
    ParamDef(
        name="schedule_minutes",
        type="int",
        description="Minutes from now to schedule the post. Ignored if publish_now=True or is_draft=True",
        required=False,
        default=60,
    ),
    ParamDef(
        name="media_urls",
        type="str",
        description="Comma-separated URLs of media files to attach (images, videos, GIFs)",
        required=False,
        default="",
    ),
    ParamDef(
        name="title",
        type="str",
        description="Optional title (required for YouTube, recommended for Pinterest)",
        required=False,
        default="",
    ),
]

POSTS_CREATE = ToolDef(
    name="posts_create",
    description="""Create a new social media post.

**Scheduling behavior:**
- `is_draft=True`: Save as draft (no scheduling, can edit later)
- `publish_now=True`: Publish immediately
- Neither: Schedule for `schedule_minutes` from now (default: 60 min)""",
    params=POSTS_CREATE_PARAMS,
)

POSTS_CROSS_POST_PARAMS = [
    ParamDef(
        name="content",
        type="str",
        description="The post content/text",
        required=True,
    ),
    ParamDef(
        name="platforms",
        type="str",
        description="Comma-separated list of platforms (e.g., 'twitter,linkedin,bluesky')",
        required=True,
    ),
    ParamDef(
        name="is_draft",
        type="bool",
        description="Save as draft without scheduling",
        required=False,
        default=False,
    ),
    ParamDef(
        name="publish_now",
        type="bool",
        description="Publish immediately instead of scheduling",
        required=False,
        default=False,
    ),
    ParamDef(
        name="media_urls",
        type="str",
        description="Comma-separated URLs of media files to attach",
        required=False,
        default="",
    ),
]

POSTS_CROSS_POST = ToolDef(
    name="posts_cross_post",
    description="Post the same content to multiple platforms at once.",
    params=POSTS_CROSS_POST_PARAMS,
)

POSTS_LIST_PARAMS = [
    ParamDef(
        name="status",
        type="str",
        description="Filter by status: draft, scheduled, published, failed. Empty for all",
        required=False,
        default="",
    ),
    ParamDef(
        name="limit",
        type="int",
        description="Maximum number of posts to return",
        required=False,
        default=10,
    ),
]

POSTS_LIST = ToolDef(
    name="posts_list",
    description="List posts with optional filtering by status.",
    params=POSTS_LIST_PARAMS,
)

# =============================================================================
# ALL TOOL DEFINITIONS
# =============================================================================

TOOL_DEFINITIONS = {
    "posts_create": POSTS_CREATE,
    "posts_cross_post": POSTS_CROSS_POST,
    "posts_list": POSTS_LIST,
}


def generate_mdx_docs() -> str:
    """Generate complete MDX documentation for all tools."""
    sections = [
        "## Tool Reference",
        "",
        "Detailed parameters for each MCP tool.",
        "",
    ]
    for tool in TOOL_DEFINITIONS.values():
        sections.append(tool.to_mdx_section())
        sections.append("")
    return "\n".join(sections)


def get_tool_docstring(tool_name: str) -> str:
    """Get the docstring for a tool, formatted for MCP."""
    tool = TOOL_DEFINITIONS.get(tool_name)
    if not tool:
        return ""

    lines = [tool.description, "", "Args:"]
    for param in tool.params:
        req = " (required)" if param.required else ""
        default = (
            f" (default: {param.default})"
            if param.default is not None and not param.required
            else ""
        )
        lines.append(f"    {param.name}: {param.description}{req}{default}")

    return "\n".join(lines)
