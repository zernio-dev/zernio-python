import re

from fastmcp.server.dependencies import get_http_headers, get_http_request

from late.mcp.constants import ENDPOINT_CHATGPT

_CLIENT_NAME_MAX = 64
_USER_AGENT_MAX = 200
# The client name lands inside an RFC 9110 comment: these would close it early
# or split it into a second field.
_COMMENT_DELIMITERS = str.maketrans("", "", "();")
# Outbound header values must be printable ASCII: httpx refuses anything else,
# and Starlette decodes an inbound UTF-8 User-Agent as latin-1 ("CafÃ©").
_NOT_HEADER_SAFE = re.compile(r"[^\x20-\x7e]")


def calling_user_agent() -> str:
    """The MCP client's User-Agent ("Cursor/1.7.0 (linux)"), capped, or "" off HTTP."""
    return get_http_headers().get("user-agent", "").strip()[:_USER_AGENT_MAX]


def calling_client() -> str:
    """Product name of the MCP client's User-Agent ("Claude-User"), or "" off HTTP."""
    return calling_user_agent().split("/", 1)[0].strip()[:_CLIENT_NAME_MAX]


def _surface() -> str:
    try:
        path = get_http_request().url.path
    except RuntimeError:
        return "stdio"
    return "chatgpt" if path.startswith(ENDPOINT_CHATGPT) else "mcp"


def mcp_user_agent() -> str:
    """User-Agent product token for every request this server sends to Zernio.

    `zernio-mcp (<surface>; <client>)`, where surface is the endpoint the
    current request came in on (mcp, chatgpt) or stdio off HTTP. No version:
    the hosted server runs one deployment at a time, so the deploy history
    already dates a request.
    """
    client = _NOT_HEADER_SAFE.sub(
        "", calling_client().translate(_COMMENT_DELIMITERS)
    ).strip()
    surface = _surface()
    comment = f"{surface}; {client}" if client else surface
    return f"zernio-mcp ({comment})"
