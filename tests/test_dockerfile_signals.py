from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("dockerfile", ["Dockerfile", "Dockerfile.docker"])
def test_the_server_is_exec_ed_so_deploy_sigterm_reaches_it(dockerfile):
    [cmd] = [
        line
        for line in (REPO_ROOT / dockerfile).read_text().splitlines()
        if line.startswith("CMD")
    ]

    assert '"exec /app/.venv/bin/late-mcp-http ' in cmd
    assert "uv run" not in cmd
