FROM python:3.10-slim-buster as agent-base

ENV CLOUDSDK_PYTHON=/usr/local/bin/python

RUN apt-get update && apt-get install -y git apt-transport-https ca-certificates gnupg curl apt-utils
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get -f install google-cloud-sdk -y

RUN pip install prometheus_client jsonpickle grpcio-health-checking

# https://github.com/apache/airflow/issues/39437
RUN pip install apache-airflow==2.9.1 \
                apache-airflow[slack] \
                apache-airflow[google] \
                google-cloud-orchestration-airflow==1.9.1 \
                apache-airflow-providers-amazon==8.20.0 \
                anyscale

From agent-base as agent

ARG FLYTEKIT_VERSION=f03cec8af903f7553a4118865693f80d1f9c760a
ARG FLYTE_VERSION=8fc1a30cfd28e6bc813522800adb2c82eb26757d

RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-airflow"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-openai"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-snowflake"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-bigquery"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-spark"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-aws-sagemaker"
RUN pip install -U "git+https://github.com/flyteorg/flytekit.git@$FLYTEKIT_VERSION#subdirectory=plugins/flytekit-ray"
RUN pip install -U "git+https://github.com/flyteorg/flyte.git@$FLYTE_VERSION#subdirectory=flyteidl"

COPY noop_agent /root/noop_agent
RUN pip install /root/noop_agent
RUN pip install "numpy<2.0.0" "tenacity<=8.3.0" "protobuf<5.0.0"

ENV FLYTE_SDK_LOGGING_LEVEL 20

CMD pyflyte serve agent --port 8000
