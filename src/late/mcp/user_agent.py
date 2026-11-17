from fastmcp.server.dependencies import get_http_headers

_CLIENT_NAME_MAX = 64
# The client name lands inside an RFC 9110 comment: these would close it early
# or split it into a second field.
_COMMENT_DELIMITERS = str.maketrans("", "", "();")


def calling_client() -> str:
    """Product name of the MCP client's User-Agent ("Claude-User"), or "" off HTTP."""
    user_agent = get_http_headers().get("user-agent", "")
    return user_agent.split("/", 1)[0].strip()[:_CLIENT_NAME_MAX]


def mcp_user_agent(surface: str) -> str:
    """User-Agent product token for the API calls this server makes on a client's behalf.

    `zernio-mcp (<surface>; <client>)`, with no version: the hosted server runs
    one deployment at a time, so the deploy history already dates a request.
    """
    client = calling_client().translate(_COMMENT_DELIMITERS).strip()
    comment = f"{surface}; {client}" if client else surface
    return f"zernio-mcp ({comment})"
