FROM python:3.9.9-slim-bullseye as base
# FROM python:3.9.9-alpine as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder
ARG DEV
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.11

# RUN apk add --no-cache gcc libffi-dev musl-dev python3-dev g++
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export $([ -z "${DEV}" ] || echo --dev) -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final
ARG DEV

# RUN apk add --no-cache libffi libpq chromium
RUN apt-get update \
    && apt-get install -y chromium $([ -z "${DEV}" ] || echo chromium-driver) \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
ENV PATH /venv/bin:$PATH
COPY tests .
COPY docker-entrypoint.sh .
ENTRYPOINT ["sh", "docker-entrypoint.sh"]