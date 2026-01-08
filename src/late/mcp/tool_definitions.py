"""
Centralized tool definitions for MCP and documentation.

This file is the SINGLE SOURCE OF TRUTH for tool parameters and descriptions.
Used by:
- MCP server (server.py) for tool definitions via @use_tool_def decorator
- Documentation generation (generate_docs.py for MDX output)

To update tool documentation, edit ONLY this file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


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
    summary: str  # Short one-line description
    description: str  # Detailed description with usage guidelines
    params: list[ParamDef] = field(default_factory=list)

    def get_docstring(self) -> str:
        """Generate docstring for MCP function."""
        lines = [self.description, ""]

        if self.params:
            lines.append("Args:")
            for param in self.params:
                req = " (required)" if param.required else ""
                default = (
                    f" Default: {param.default}."
                    if param.default is not None and not param.required
                    else ""
                )
                lines.append(f"    {param.name}: {param.description}{req}{default}")

        return "\n".join(lines)

    def to_mdx_section(self) -> str:
        """Generate MDX documentation section."""
        lines = [
            f"### `{self.name}`",
            "",
            self.summary,
            "",
            self.description,
            "",
        ]

        if self.params:
            lines.extend([
                "| Parameter | Type | Description | Required | Default |",
                "|-----------|------|-------------|----------|---------|",
            ])
            lines.extend(p.to_mdx_row() for p in self.params)
            lines.append("")

        return "\n".join(lines)


# =============================================================================
# DECORATOR FOR APPLYING TOOL DEFINITIONS
# =============================================================================


def use_tool_def(tool_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to apply tool definition docstring to a function.

    Usage:
        @mcp.tool()
        @use_tool_def("posts_create")
        def posts_create(...):
            ...  # Implementation only, no docstring needed
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        tool = TOOL_DEFINITIONS.get(tool_name)
        if tool:
            # Set docstring on the original function
            func.__doc__ = tool.get_docstring()
        # Return the function directly - no wrapper needed
        # The @mcp.tool() decorator will read __doc__ from this function
        return func

    return decorator


# =============================================================================
# ACCOUNTS TOOLS
# =============================================================================

ACCOUNTS_LIST = ToolDef(
    name="accounts_list",
    summary="List all connected social media accounts.",
    description="""List all connected social media accounts.

Returns the platform, username, and account ID for each connected account.
Use this to find account IDs needed for creating posts.""",
    params=[],
)

ACCOUNTS_GET = ToolDef(
    name="accounts_get",
    summary="Get account details for a specific platform.",
    description="""Get account details for a specific platform.

Returns username and ID for the first account matching the platform.""",
    params=[
        ParamDef(
            name="platform",
            type="str",
            description="Platform name: twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads",
            required=True,
        ),
    ],
)

# =============================================================================
# PROFILES TOOLS
# =============================================================================

PROFILES_LIST = ToolDef(
    name="profiles_list",
    summary="List all profiles.",
    description="""List all profiles.

Profiles group multiple social accounts together for easier management.""",
    params=[],
)

PROFILES_GET = ToolDef(
    name="profiles_get",
    summary="Get details of a specific profile.",
    description="Get details of a specific profile including name, description, and color.",
    params=[
        ParamDef(
            name="profile_id",
            type="str",
            description="The profile ID",
            required=True,
        ),
    ],
)

PROFILES_CREATE = ToolDef(
    name="profiles_create",
    summary="Create a new profile.",
    description="Create a new profile for grouping social accounts.",
    params=[
        ParamDef(
            name="name",
            type="str",
            description="Profile name",
            required=True,
        ),
        ParamDef(
            name="description",
            type="str",
            description="Optional description",
            required=False,
            default="",
        ),
        ParamDef(
            name="color",
            type="str",
            description="Optional hex color (e.g., '#4CAF50')",
            required=False,
            default="",
        ),
    ],
)

PROFILES_UPDATE = ToolDef(
    name="profiles_update",
    summary="Update an existing profile.",
    description="Update an existing profile. Only provided fields will be changed.",
    params=[
        ParamDef(
            name="profile_id",
            type="str",
            description="The profile ID to update",
            required=True,
        ),
        ParamDef(
            name="name",
            type="str",
            description="New name (leave empty to keep current)",
            required=False,
            default="",
        ),
        ParamDef(
            name="description",
            type="str",
            description="New description (leave empty to keep current)",
            required=False,
            default="",
        ),
        ParamDef(
            name="color",
            type="str",
            description="New hex color (leave empty to keep current)",
            required=False,
            default="",
        ),
        ParamDef(
            name="is_default",
            type="bool",
            description="Set as default profile",
            required=False,
            default=False,
        ),
    ],
)

PROFILES_DELETE = ToolDef(
    name="profiles_delete",
    summary="Delete a profile.",
    description="Delete a profile. The profile must have no connected accounts.",
    params=[
        ParamDef(
            name="profile_id",
            type="str",
            description="The profile ID to delete",
            required=True,
        ),
    ],
)

# =============================================================================
# POSTS TOOLS
# =============================================================================

POSTS_LIST = ToolDef(
    name="posts_list",
    summary="List posts with optional filtering.",
    description="""List posts with optional filtering by status.

Status options: draft, scheduled, published, failed""",
    params=[
        ParamDef(
            name="status",
            type="str",
            description="Filter by status: draft, scheduled, published, failed. Leave empty for all posts",
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
    ],
)

POSTS_GET = ToolDef(
    name="posts_get",
    summary="Get details of a specific post.",
    description="Get full details of a specific post including content, status, and scheduling info.",
    params=[
        ParamDef(
            name="post_id",
            type="str",
            description="The post ID to retrieve",
            required=True,
        ),
    ],
)

POSTS_CREATE = ToolDef(
    name="posts_create",
    summary="Create a social media post (draft, scheduled, or immediate).",
    description="""Create a social media post. Can be saved as DRAFT, SCHEDULED, or PUBLISHED immediately.

⚠️ IMPORTANT - Choose the correct mode based on user intent:

**DRAFT MODE (is_draft=True)**
Use when user says: "draft", "borrador", "save for later", "don't publish", "save it", "guardar"
→ Post is saved but NOT published and NOT scheduled. User can edit it later.

**IMMEDIATE MODE (publish_now=True)**
Use when user says: "publish now", "post now", "publica ya", "immediately", "right now", "ahora"
→ Post goes live IMMEDIATELY.

**SCHEDULED MODE (default)**
Use when user says: "schedule", "programar", "in X minutes/hours", "at 3pm", "tomorrow"
→ Post is scheduled for future publication. Use schedule_minutes to set the delay.

Examples:
- "Create a draft tweet" → is_draft=True
- "Post this to Twitter now" → publish_now=True
- "Schedule a LinkedIn post for 2 hours from now" → schedule_minutes=120""",
    params=[
        ParamDef(
            name="content",
            type="str",
            description="The post text/content",
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
            description="Set to True to save as DRAFT (not published, not scheduled). Use when user wants to save without publishing",
            required=False,
            default=False,
        ),
        ParamDef(
            name="publish_now",
            type="bool",
            description="Set to True to publish IMMEDIATELY. Post goes live right now",
            required=False,
            default=False,
        ),
        ParamDef(
            name="schedule_minutes",
            type="int",
            description="Minutes from now to schedule. Only used when is_draft=False AND publish_now=False",
            required=False,
            default=60,
        ),
        ParamDef(
            name="media_urls",
            type="str",
            description="Comma-separated URLs of media files to attach (images, videos)",
            required=False,
            default="",
        ),
        ParamDef(
            name="title",
            type="str",
            description="Post title (required for YouTube, recommended for Pinterest)",
            required=False,
            default="",
        ),
    ],
)

POSTS_PUBLISH_NOW = ToolDef(
    name="posts_publish_now",
    summary="Publish a post immediately.",
    description="""Publish a post immediately to a platform. The post goes live right away.

Use this when user explicitly wants to publish NOW, not schedule for later.
This is a convenience wrapper around posts_create with publish_now=True.""",
    params=[
        ParamDef(
            name="content",
            type="str",
            description="The post text/content",
            required=True,
        ),
        ParamDef(
            name="platform",
            type="str",
            description="Target platform: twitter, instagram, linkedin, tiktok, bluesky, etc.",
            required=True,
        ),
        ParamDef(
            name="media_urls",
            type="str",
            description="Comma-separated URLs of media files to attach",
            required=False,
            default="",
        ),
    ],
)

POSTS_CROSS_POST = ToolDef(
    name="posts_cross_post",
    summary="Post the same content to multiple platforms.",
    description="""Post the same content to multiple platforms at once.

⚠️ IMPORTANT - Choose the correct mode based on user intent:

**DRAFT MODE (is_draft=True)**
Use when user says: "draft", "borrador", "save for later", "don't publish"
→ Posts are saved but NOT published. User can edit them later.

**IMMEDIATE MODE (publish_now=True)**
Use when user says: "publish now", "post now", "immediately"
→ Posts go live IMMEDIATELY on all platforms.

**SCHEDULED MODE (default)**
Use when user says: "schedule", "programar", "in X hours"
→ Posts are scheduled for 1 hour from now.""",
    params=[
        ParamDef(
            name="content",
            type="str",
            description="The post text/content",
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
            description="Set to True to save as DRAFT (not published). Use when user wants to save without publishing",
            required=False,
            default=False,
        ),
        ParamDef(
            name="publish_now",
            type="bool",
            description="Set to True to publish IMMEDIATELY to all platforms",
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
    ],
)

POSTS_UPDATE = ToolDef(
    name="posts_update",
    summary="Update an existing post.",
    description="""Update an existing post.

Only draft, scheduled, and failed posts can be updated.
Published posts cannot be modified.""",
    params=[
        ParamDef(
            name="post_id",
            type="str",
            description="The post ID to update",
            required=True,
        ),
        ParamDef(
            name="content",
            type="str",
            description="New content (leave empty to keep current)",
            required=False,
            default="",
        ),
        ParamDef(
            name="scheduled_for",
            type="str",
            description="New schedule time as ISO string (leave empty to keep current)",
            required=False,
            default="",
        ),
        ParamDef(
            name="title",
            type="str",
            description="New title (leave empty to keep current)",
            required=False,
            default="",
        ),
    ],
)

POSTS_DELETE = ToolDef(
    name="posts_delete",
    summary="Delete a post.",
    description="""Delete a post by ID.

Published posts cannot be deleted.""",
    params=[
        ParamDef(
            name="post_id",
            type="str",
            description="The post ID to delete",
            required=True,
        ),
    ],
)

POSTS_RETRY = ToolDef(
    name="posts_retry",
    summary="Retry a failed post.",
    description="Retry publishing a failed post. Only works on posts with 'failed' status.",
    params=[
        ParamDef(
            name="post_id",
            type="str",
            description="The ID of the failed post to retry",
            required=True,
        ),
    ],
)

POSTS_LIST_FAILED = ToolDef(
    name="posts_list_failed",
    summary="List all failed posts.",
    description="List all failed posts that can be retried.",
    params=[
        ParamDef(
            name="limit",
            type="int",
            description="Maximum number of posts to return",
            required=False,
            default=10,
        ),
    ],
)

POSTS_RETRY_ALL_FAILED = ToolDef(
    name="posts_retry_all_failed",
    summary="Retry all failed posts.",
    description="Retry all failed posts at once.",
    params=[],
)

# =============================================================================
# DOCS TOOLS
# =============================================================================

DOCS_SEARCH = ToolDef(
    name="docs_search",
    summary="Search the Late API documentation.",
    description="""Search across the Late API documentation to find relevant information, code examples, API references, and guides.

Use this tool when you need to answer questions about Late, find specific documentation, understand how features work, or locate implementation details.

The search returns contextual content with section titles and relevant snippets.""",
    params=[
        ParamDef(
            name="query",
            type="str",
            description="Search query (e.g., 'webhooks', 'create post', 'authentication')",
            required=True,
        ),
    ],
)

# =============================================================================
# MEDIA TOOLS
# =============================================================================

MEDIA_GENERATE_UPLOAD_LINK = ToolDef(
    name="media_generate_upload_link",
    summary="Generate an upload URL for media files.",
    description="""Generate a unique upload URL for the user to upload files via browser.

Use this when the user wants to include images or videos in their post.
The flow is:
1. Call this tool to get an upload URL
2. Ask the user to open the URL in their browser
3. User uploads files through the web interface
4. Call media_check_upload_status to get the uploaded file URLs
5. Use those URLs when creating the post with posts_create""",
    params=[],
)

MEDIA_CHECK_UPLOAD_STATUS = ToolDef(
    name="media_check_upload_status",
    summary="Check upload status and get file URLs.",
    description="""Check the status of an upload token and get uploaded file URLs.

Use this after the user has uploaded files through the browser upload page.
Returns: pending (waiting for upload), completed (files ready), or expired (token expired).""",
    params=[
        ParamDef(
            name="token",
            type="str",
            description="The upload token from media_generate_upload_link",
            required=True,
        ),
    ],
)


# =============================================================================
# ALL TOOL DEFINITIONS REGISTRY
# =============================================================================

TOOL_DEFINITIONS: dict[str, ToolDef] = {
    # Accounts
    "accounts_list": ACCOUNTS_LIST,
    "accounts_get": ACCOUNTS_GET,
    # Profiles
    "profiles_list": PROFILES_LIST,
    "profiles_get": PROFILES_GET,
    "profiles_create": PROFILES_CREATE,
    "profiles_update": PROFILES_UPDATE,
    "profiles_delete": PROFILES_DELETE,
    # Posts
    "posts_list": POSTS_LIST,
    "posts_get": POSTS_GET,
    "posts_create": POSTS_CREATE,
    "posts_publish_now": POSTS_PUBLISH_NOW,
    "posts_cross_post": POSTS_CROSS_POST,
    "posts_update": POSTS_UPDATE,
    "posts_delete": POSTS_DELETE,
    "posts_retry": POSTS_RETRY,
    "posts_list_failed": POSTS_LIST_FAILED,
    "posts_retry_all_failed": POSTS_RETRY_ALL_FAILED,
    # Media
    "media_generate_upload_link": MEDIA_GENERATE_UPLOAD_LINK,
    "media_check_upload_status": MEDIA_CHECK_UPLOAD_STATUS,
    # Docs
    "docs_search": DOCS_SEARCH,
}


# =============================================================================
# DOCUMENTATION GENERATION
# =============================================================================


def generate_mdx_tools_reference() -> str:
    """Generate MDX documentation for all tools."""
    sections = [
        "## Tool Reference",
        "",
        "Detailed parameters for each MCP tool.",
        "",
    ]

    # Group by category
    categories = {
        "Accounts": ["accounts_list", "accounts_get"],
        "Profiles": [
            "profiles_list",
            "profiles_get",
            "profiles_create",
            "profiles_update",
            "profiles_delete",
        ],
        "Posts": [
            "posts_create",
            "posts_publish_now",
            "posts_cross_post",
            "posts_list",
            "posts_get",
            "posts_update",
            "posts_delete",
            "posts_retry",
            "posts_list_failed",
            "posts_retry_all_failed",
        ],
        "Media": ["media_generate_upload_link", "media_check_upload_status"],
        "Docs": ["docs_search"],
    }

    for category, tool_names in categories.items():
        sections.append(f"### {category}")
        sections.append("")
        for name in tool_names:
            tool = TOOL_DEFINITIONS.get(name)
            if tool:
                sections.append(tool.to_mdx_section())
        sections.append("")

    return "\n".join(sections)


def get_tool_docstring(tool_name: str) -> str:
    """Get the docstring for a tool, formatted for MCP."""
    tool = TOOL_DEFINITIONS.get(tool_name)
    if not tool:
        return ""
    return tool.get_docstring()
