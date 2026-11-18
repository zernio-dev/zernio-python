import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("dockerfile", ["Dockerfile", "Dockerfile.docker"])
def test_the_server_is_pid_1_so_deploy_sigterm_reaches_it(dockerfile):
    lines = (REPO_ROOT / dockerfile).read_text().splitlines()
    [cmd] = [line for line in lines if line.startswith("CMD")]

    assert 'ENV PATH="/app/.venv/bin:$PATH"' in lines
    assert json.loads(cmd.removeprefix("CMD"))[0] == "late-mcp-http"


@pytest.mark.parametrize("dockerfile", ["Dockerfile", "Dockerfile.docker"])
def test_the_server_runs_as_a_non_root_user(dockerfile):
    lines = (REPO_ROOT / dockerfile).read_text().splitlines()
    [user] = [line for line in lines if line.startswith("USER")]

    assert user.split()[1] not in ("root", "0")
