FROM python:3.12-slim-bullseye as build

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    build-essential \
    ca-certificates \
    curl \
    gettext \
    gnupg \
  && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    postgresql-client-17 \
    postgresql-client-common

RUN set -x \
    && python3 -m venv /app

ENV PATH="/app:${PATH}"

RUN pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt

RUN set -x \
    && pip --no-cache-dir --disable-pip-version-check install \
    -r /tmp/requirements.txt

FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PATH="/app:${PATH}"

WORKDIR /app

RUN apt-get update \
  # psycopg2 dependencies
  && apt-get install --no-install-recommends -y \
    ca-certificates \
    curl \
    gettext \
    gnupg \
  && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    libpq5 \
    bash postgresql-client-17 \
  && apt-get remove -y \
    curl \
    gnupg \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN adduser --system --no-create-home django && addgroup django
COPY --chown=django:django --from=build /app/ /app/
COPY requirements.txt /tmp/requirements.txt
RUN set -x \
    && pip --no-cache-dir --disable-pip-version-check install \
    -r /tmp/requirements.txt

USER django
