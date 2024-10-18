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

ENV PATH="/app/bin:${PATH}"

RUN pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

COPY requirements /tmp/requirements

RUN set -x \
    && pip --no-cache-dir --disable-pip-version-check install \
    -r /tmp/requirements/requirements.txt

FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PATH="/app/bin:${PATH}"

WORKDIR /app/src

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
    bash postgresql-client-17
  # cleaning up unused files
  && apt-get remove -y \
    curl \
    gnupg \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN adduser --system --no-create-home django
COPY --chown=django:django --from=build /app/ /app/
COPY --chown=django:django config/ /app/src/config/
COPY --chown=django:django manage.py /app/src/
COPY --chown=django:django liine_cooks/ /app/src/liine_cooks/

USER django
