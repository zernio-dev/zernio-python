"""Serving the hosted MCP server from several processes behind one port.

One Python process tops out at one core (the GIL), which is what saturated
mcp.zernio.com on Nov 10. WEB_CONCURRENCY (uvicorn's own convention) sets how
many worker processes uvicorn starts; unset means one, the old behaviour.
"""

import os
import tempfile
from pathlib import Path


def worker_count() -> int:
    return max(1, int(os.getenv("WEB_CONCURRENCY") or "1"))


def _ready_dir() -> Path:
    # Every worker is a child of the same uvicorn supervisor, so its pid names a
    # directory they all share and a later container never reuses.
    return Path(tempfile.gettempdir()) / f"zernio-mcp-ready-{os.getppid()}"


def mark_worker_ready() -> None:
    ready_dir = _ready_dir()
    ready_dir.mkdir(exist_ok=True)
    (ready_dir / str(os.getpid())).touch()


def all_workers_ready() -> bool:
    """Whether every worker can take connections.

    A worker that starts serving first accepts every connection opened before
    the others finish importing the tool catalog, and keep-alive pins those
    connections to it. /health reports 503 until all are up, so Railway only
    switches traffic to a new deploy once connections can spread.
    """
    workers = worker_count()
    if workers == 1:
        return True
    try:
        return sum(1 for _ in _ready_dir().iterdir()) >= workers
    except FileNotFoundError:
        return False
