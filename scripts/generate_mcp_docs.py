#!/usr/bin/env python3
"""
Generate MCP documentation from tool definitions.

Usage:
    python scripts/generate_mcp_docs.py

This script generates MDX documentation from the centralized tool definitions
in src/late/mcp/tool_definitions.py

The generated output can be copied into the docs site.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from late.mcp.tool_definitions import TOOL_DEFINITIONS, generate_mdx_tools_reference


def main() -> None:
    """Generate and print MDX documentation."""
    print("=" * 60)
    print("MCP Tool Documentation (generated from tool_definitions.py)")
    print("=" * 60)
    print()
    print(generate_mdx_tools_reference())
    print()
    print("=" * 60)
    print(f"Total tools: {len(TOOL_DEFINITIONS)}")
    print("Copy the above into claude-mcp.mdx under '## Tool Reference'")
    print("=" * 60)


if __name__ == "__main__":
    main()
