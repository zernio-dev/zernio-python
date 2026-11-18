# syntax=docker/dockerfile:1
# Zernio MCP HTTP server, deployed on Railway.
#
# Three stages: a lockfile export, a builder that has uv, and a runtime image
# that holds only Python and the virtualenv, running as a non-root user.

ARG PYTHON_IMAGE=python:3.12-slim-bookworm

FROM ghcr.io/astral-sh/uv:0.13.7 AS uv

# Every spec regeneration bumps the project version in uv.lock, so installing
# straight from uv.lock would reinstall every dependency on every deploy. The
# export leaves the project out, stays byte-identical across those bumps, and
# lets the builder reuse its dependency layer.
FROM ${PYTHON_IMAGE} AS requirements
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --extra mcp --no-emit-project -o requirements.txt

FROM ${PYTHON_IMAGE} AS builder
COPY --from=uv /uv /usr/local/bin/uv
# Bytecode is compiled at build time: the runtime user cannot write .pyc files
# next to the code, and each worker would otherwise compile on every start.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/app/.venv
WORKDIR /app
COPY --from=requirements /app/requirements.txt ./
RUN uv venv /app/.venv \
    && uv pip install --python /app/.venv/bin/python --require-hashes -r requirements.txt
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
# Non-editable, so the runtime image needs the virtualenv and not src.
RUN uv sync --frozen --no-dev --extra mcp --no-editable

FROM ${PYTHON_IMAGE}

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --create-home app

COPY --from=builder /app/.venv /app/.venv

ENV MALLOC_ARENA_MAX=2
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
USER app

# Railway sets PORT; the server reads it and defaults to 8080.
EXPOSE 8080

# Exec form, no shell or `uv run`: the server is PID 1 and gets the SIGTERM a
# deploy sends, so in-flight tool calls finish. It reads PORT itself.
CMD ["late-mcp-http", "--host", "0.0.0.0"]
