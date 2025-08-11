FROM ghcr.io/astral-sh/uv:python3.12-alpine

ADD . /workdir

WORKDIR /workdir

RUN uv sync --locked

CMD uv run fastapi dev --host 0.0.0.0 --port 8000