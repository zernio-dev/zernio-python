"""
End-to-end smoke test for the Streamable HTTP transport.

Boots the HTTP server in-process with auth verification stubbed out, then
drives it with the official MCP Python client over Streamable HTTP. Covers:

  1. /mcp routing reaches our auth wrapper (no 307, no signature mismatch)
  2. Streamable HTTP protocol handshake (initialize)
  3. tools/list returns the registered tool catalog
  4. ContextVar API-key propagation: a tool that reads the key sees it
  5. SSE legacy transport endpoint still responds (no regression)
"""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager

import httpx
import uvicorn

# --- Stub token verification BEFORE the server starts: ZernioTokenVerifier
# looks verify_late_api_key up on the module at call time. ---
import late.mcp.auth as auth_module


async def _always_valid(api_key: str, *, client=None) -> auth_module.Verification:
    """Stub: accept any key. Bypasses the network call to zernio.com."""
    return auth_module.Verification.VALID


auth_module.verify_late_api_key = _always_valid

import httpx2  # noqa: E402
from mcp import ClientSession  # noqa: E402
from mcp.client.streamable_http import streamable_http_client  # noqa: E402

from late.mcp.http_server import build_app  # noqa: E402

PORT = 8766
BASE = f"http://127.0.0.1:{PORT}"
FAKE_KEY = "test_key_smoke"


@contextmanager
def run_server() -> Iterator[None]:
    """Start uvicorn in a daemon thread; yield once it's accepting connections."""
    app = build_app()
    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for the server to come up.
    for _ in range(50):
        try:
            r = httpx.get(f"{BASE}/health", timeout=0.5)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.1)
    else:
        raise RuntimeError("server failed to start")

    try:
        yield
    finally:
        server.should_exit = True
        thread.join(timeout=5)


async def run_streamable_http_checks() -> None:
    """Drive the server with the real MCP client over Streamable HTTP."""
    headers = {"Authorization": f"Bearer {FAKE_KEY}"}
    url = f"{BASE}/mcp"

    print(f"[client] connecting to {url} via streamable_http_client")
    async with (
        httpx2.AsyncClient(headers=headers) as http_client,
        streamable_http_client(url, http_client=http_client) as (read, write),
        ClientSession(read, write) as session,
    ):
        print("[client] initialize()")
        init = await session.initialize()
        assert init.server_info.name == "Zernio", init.server_info
        print(f"[ok]    initialize -> serverInfo.name={init.server_info.name!r}")

        print("[client] list_tools()")
        tools = await session.list_tools()
        names = [t.name for t in tools.tools]
        assert names, "expected non-empty tool list"
        assert any(n.startswith("posts_") for n in names), names
        print(f"[ok]    list_tools -> {len(names)} tools (sample: {names[:5]})")

        # fastmcp builds the synthetic search/call tools without
        # annotations; clients that gate approval on hints then auto-deny
        # them (codex-cli in non-interactive runs). Assert over the wire,
        # not just in-process, so a serialization regression is caught too.
        by_name = {t.name: t for t in tools.tools}
        for synthetic in ("search_tools", "call_tool"):
            assert synthetic in by_name, f"{synthetic} missing from tools/list"
            assert by_name[synthetic].annotations is not None, (
                f"{synthetic} has no annotations - approval-gating clients will deny it"
            )
        assert by_name["search_tools"].annotations.read_only_hint is True
        assert by_name["call_tool"].annotations.destructive_hint is True
        print("[ok]    synthetic search/call tools carry annotations")

        # The real ContextVar test: invoke a tool and observe the error.
        # - If plumbing is BROKEN: tool errors with "API key is required"
        #   (the ValueError raised by _get_client when ContextVar is unset).
        # - If plumbing WORKS: the key reaches the Late client, which then
        #   makes a real call to zernio.com that fails with 401/auth error
        #   because our fake key isn't real. Either of those proves the
        #   key is being propagated through anyio's task group context.
        print("[client] call_tool('accounts_list') to verify API-key propagation")
        result = await session.call_tool("accounts_list", {})
        text_content = " ".join(getattr(c, "text", "") for c in result.content)
        print(f"[debug] tool response (truncated): {text_content[:200]!r}")

        broken_marker = "Zernio API key is required"
        assert broken_marker not in text_content, (
            f"ContextVar propagation FAILED — tool could not see the API key.\n"
            f"Full response: {text_content}"
        )
        print("[ok]    API key reached the tool (no 'API key required' error)")


def check_no_redirect() -> None:
    """Verify POST /mcp does not 307 to /mcp/ — the bug we fixed."""
    print("[raw]   POST /mcp without auth")
    r = httpx.post(
        f"{BASE}/mcp",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        },
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        follow_redirects=False,
    )
    assert r.status_code == 401, f"expected 401, got {r.status_code}: {r.text}"
    assert "resource_metadata" in r.headers.get("www-authenticate", ""), r.headers
    print(f"[ok]    no-auth -> 401 (no 307 redirect)")


def check_sse_still_works() -> None:
    """Verify the legacy SSE endpoint still gates auth (no regression)."""
    print("[raw]   GET /sse without auth")
    r = httpx.get(f"{BASE}/sse", timeout=5.0)
    assert r.status_code == 401, f"expected 401, got {r.status_code}"
    print(f"[ok]    /sse no-auth -> 401")


def check_root_advertises_both() -> None:
    print("[raw]   GET / (root info)")
    r = httpx.get(f"{BASE}/")
    body = r.json()
    assert "mcp" in body["endpoints"], body["endpoints"]
    assert "sse" in body["endpoints"], body["endpoints"]
    assert body["transport"] == "sse+streamable-http", body
    print(f"[ok]    root advertises both transports: {body['transport']}")


def main() -> None:
    with run_server():
        check_no_redirect()
        check_sse_still_works()
        check_root_advertises_both()
        asyncio.run(run_streamable_http_checks())
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
