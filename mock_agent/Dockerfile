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

ARG FLYTEKIT_VERSION=b475c87b73b8f765804562f2e38266833cf67882
ARG FLYTE_VERSION=c61d976c6f1d934d38afc3097a64f45f36b7c7ad

RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-airflow"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-openai"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-snowflake"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-bigquery"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-spark"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-aws-sagemaker"
RUN pip install -U "git+https://github.com/flyteorg/flyte.git@$FLYTE_VERSION#subdirectory=flyteidl"

COPY mock_agent /root/mock_agent
RUN pip install /root/mock_agent

ENV FLYTE_SDK_LOGGING_LEVEL 30

CMD pyflyte serve agent --port 8000
