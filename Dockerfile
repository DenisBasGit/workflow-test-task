FROM python:3.11 AS compile-image
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update \
    \
    && apt install -y \
    autoconf \
    curl \
    g++ \
    gcc \
    libgmp3-dev \
    libjpeg-dev \
    libffi-dev \
    libsecp256k1-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libpq-dev \
    tcl-dev \
    tk-dev \
    libsodium-dev \
    gettext

COPY ./requirements requirements
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# local or production
ARG ENV=local
RUN pip install -U pip && pip install wheel && pip install --no-cache-dir -r requirements/$ENV.txt
FROM python:3.11 AS build-image
RUN apt update \
    \
    && apt install -y \
    curl \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libsodium-dev \
    libtiff-dev \
    vim \
    libgmp3-dev \
    libsecp256k1-dev \
    gettext \
    git
RUN groupadd -r -g 1001 app && useradd -r -u 1001 -g app app
USER app
COPY --chown=app:app --from=compile-image /opt/venv /opt/venv
COPY --chown=app:app . /app

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
