ARG PYTHON_VERSION=3.11.0
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

ENV PYTHONPATH .

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev|| echo "Poetry install failed"

COPY . .