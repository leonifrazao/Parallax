FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .
RUN uv pip install -e .

CMD ["uv", "run", "uvicorn", "parallax.services.render_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]