FROM ghcr.io/unionai/flyte-conformance-agent:latest

MAINTAINER Flyte Team <users@flyte.org>

COPY ./config.yaml /root/.flyte/config.yaml
ENV FLYTECTL_CONFIG /root/.flyte/config.yaml

RUN pip install flytekitplugins-kftensorflow
RUN pip install flytekitplugins-kfpytorch
RUN pip install flytekitplugins-ray
RUN pip install flytekitplugins-pandera
RUN pip install flytekitplugins-envd
RUN pip install flytekitplugins-mlflow
RUN pip install flytekitplugins-spark