FROM python:3.9-slim-buster

MAINTAINER Flyte Team <users@flyte.org>
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

RUN apt-get update && apt-get install -y git apt-transport-https ca-certificates gnupg curl

RUN pip install prometheus_client
RUN pip install flytekitplugins-airflow
RUN pip install "git+https://github.com/flyteorg/flytekit.git@87845e8bbe6064af8487d2c7088d7d333843363f#subdirectory=plugins/flytekit-airflow"
RUN pip install "git+https://github.com/flyteorg/flytekit.git@87845e8bbe6064af8487d2c7088d7d333843363f"
RUN pip install "git+https://github.com/flyteorg/flyte.git@a46196d42e80f055efc9a013cb95c20342c72622#subdirectory=flyteidl"


COPY mock_agent_server /root/mock_agent_server
RUN pip install /root/mock_agent_server


CMD pyflyte serve agent --port 8000
