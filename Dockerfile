FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml .
RUN uv sync
COPY . .
RUN uv pip install -e .
CMD ["uv", "run", "parallax"]