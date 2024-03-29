FROM python:3.10-slim-buster as agent-base

MAINTAINER Flyte Team <users@flyte.org>
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

RUN apt-get update && apt-get install -y git apt-transport-https ca-certificates gnupg curl
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.asc
RUN apt-get update && apt-get install google-cloud-cli

RUN pip install prometheus_client jsonpickle grpcio-health-checking
RUN pip install apache-airflow \
                apache-airflow[slack] \
                apache-airflow[google] \
                google-cloud-orchestration-airflow==1.9.1 \
                apache-airflow-providers-amazon

From agent-base as agent

ARG FLYTEKIT_VERSION=6c917ed16265e00f8d33339b6b78235a395b99dd
ARG FLYTE_VERSION=c61d976c6f1d934d38afc3097a64f45f36b7c7ad

RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-airflow"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-openai"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-snowflake"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-bigquery"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-spark"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@542f661c0eaa10060c7798a379f0cf85b04b67d7#subdirectory=plugins/flytekit-aws-sagemaker"
RUN pip install -U "git+https://github.com/flyteorg/flyte.git@$FLYTE_VERSION#subdirectory=flyteidl"

COPY mock_agent /root/mock_agent
RUN pip install /root/mock_agent


CMD pyflyte serve agent --port 8000
