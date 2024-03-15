FROM python:3.10.12-slim-buster AS base

ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV:-development} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.0 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        bash \
        build-essential \
        curl \
        gettext \
        git \
        libpq-dev \
        wget \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry --version


WORKDIR usr/src/app

COPY . .

# Install dependencies
RUN poetry install

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
