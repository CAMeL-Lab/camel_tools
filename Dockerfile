# syntax = docker/dockerfile:1.3
FROM python:3.8-slim as builder
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc
COPY . /opt/service/
WORKDIR /opt/service/

FROM builder as worker
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir .
# RUN --mount=type=cache,target=/root/.cache/camel_data camel_data -i all

FROM worker as final

ENTRYPOINT ["flask", "run"]