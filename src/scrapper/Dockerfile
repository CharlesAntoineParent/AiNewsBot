# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.9.18
FROM python:3.9.18-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install Poetry.
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.6.1
RUN --mount=type=cache,target=/root/.cache/pip/ \
    pip install poetry~=$POETRY_VERSION

WORKDIR /app
COPY ./README.md /app/
COPY ./poetry.lock* /app/
COPY ./pyproject.toml /app/
COPY ./src/scrapper /app/src/scrapper
RUN touch /app/src/__init__.py

RUN poetry install --only main,scrapper --no-interaction --no-root && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000
WORKDIR /app/src
ENTRYPOINT ["poetry", "run", "uvicorn", "scrapper:app" ,"--host", "0.0.0.0"]