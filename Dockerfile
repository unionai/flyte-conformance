FROM ghcr.io/unionai/flyte-conformance-agent:latest

MAINTAINER Flyte Team <users@flyte.org>

RUN pip install flytekitplugins-kftensorflow
RUN pip install flytekitplugins-kfpytorch
RUN pip install flytekitplugins-ray
RUN pip install flytekitplugins-pandera
RUN pip install flytekitplugins-envd
RUN pip install flytekitplugins-mlflow
RUN pip install flytekitplugins-spark