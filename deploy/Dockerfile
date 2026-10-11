# jwdev deployment image: upstream mcp-mealie + batch writes (mgummich/mcp-mealie#38),
# served over Streamable HTTP. Build from the repo root:
#   docker build -f deploy/Dockerfile -t gitea.jwdev.casa/jwdev/mcp-mealie:<sha> .
FROM python:3.12-slim-bookworm AS build
COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src/mealie_mcp/__init__.py ./src/mealie_mcp/__init__.py
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm
RUN useradd --system --uid 10001 --no-create-home mcp
COPY --from=build --chown=mcp:mcp /app /app
COPY --chown=mcp:mcp deploy/serve_http.py /app/serve_http.py
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 MCP_PORT=8000
USER mcp
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD ["python", "-c", "import socket; socket.create_connection(('127.0.0.1', 8000), 3).close()"]
ENTRYPOINT ["python", "/app/serve_http.py"]
