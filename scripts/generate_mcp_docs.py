#!/usr/bin/env python3
"""
Generate MCP documentation from tool definitions.

Usage:
    python scripts/generate_mcp_docs.py

This script generates MDX documentation from the centralized tool definitions
in src/late/mcp/tool_definitions.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from late.mcp.tool_definitions import generate_mdx_docs, TOOL_DEFINITIONS


def main():
    """Generate and print MDX documentation."""
    print("=" * 60)
    print("MCP Tool Documentation (generated from tool_definitions.py)")
    print("=" * 60)
    print()
    print(generate_mdx_docs())
    print()
    print("=" * 60)
    print("Copy the above into claude-mcp.mdx under '## Tool Reference'")
    print("=" * 60)


if __name__ == "__main__":
    main()
