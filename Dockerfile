FROM python:3.10-slim-bookworm

WORKDIR /root
ENV PYTHONPATH /root
ENV FLYTE_SDK_RICH_TRACEBACKS 0

RUN apt-get update && apt-get install build-essential -y \
    && pip install uv rustfs \
    && uv pip install --system --no-cache-dir -U flytekit==1.2.3 \
        flytekitplugins-deck-standard==1.2.3 \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 flytekit \
    && chown flytekit: /root \
    && chown flytekit: /home \
    && :

USER flytekit
