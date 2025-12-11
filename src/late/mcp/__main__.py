"""Allow running MCP server with: python -m late.mcp"""

from late.mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
