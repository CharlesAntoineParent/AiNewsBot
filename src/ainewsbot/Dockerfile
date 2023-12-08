ARG PYTHON_VERSION=3.9.18
FROM python:3.9.18-slim AS base 

# Install Poetry.
ENV POETRY_VERSION 1.6.1
RUN --mount=type=cache,target=/root/.cache/pip/ \
    pip install poetry~=$POETRY_VERSION

#Create non-root user and switch to it
ARG UID=1000
ARG GID=$UID
RUN groupadd --gid $GID user && \
    useradd --create-home --gid $GID --uid $UID user --no-log-init && \
    chown user /opt/
USER user

# Create and activate a virtual environment.
RUN python -m venv /opt/ainewsbot-env
ENV PATH /opt/ainewsbot-env/bin:$PATH
ENV VIRTUAL_ENV /opt/ainewsbot-env

# Set the working directory.
WORKDIR /workspaces/ainewsbot/

# Install the run time Python dependencies in the virtual environment.
COPY --chown=user:user poetry.lock* pyproject.toml /workspaces/ainewsbot/
RUN mkdir -p /home/user/.cache/pypoetry/ && mkdir -p /home/user/.config/pypoetry/ && \
    mkdir -p src/ainewsbot/ && touch src/ainewsbot/__init__.py && touch README.md
RUN --mount=type=cache,uid=$UID,gid=$GID,target=/home/user/.cache/pypoetry/ \
    poetry install --no-dev

COPY --chown=user:user ./src/ainewsbot ./src/ainewsbot

EXPOSE 8000

ENTRYPOINT ["uvicorn", "ainewsbot:app", "--host", "0.0.0.0"]
CMD ["--port", "8000"]