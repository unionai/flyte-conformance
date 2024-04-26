export FLYTEKIT_VERSION=v1.12.0b6

.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: fmt
fmt:
	pre-commit run ruff --all-files || true
	pre-commit run ruff-format --all-files || true

.PHONY: setup
setup:
	pip install uv
	uv pip install -U pip apache-airflow[google]==2.7.3 pre-commit matplotlib \
 		tensorflow tensorboardX tensorflow_datasets "numpy<2.0.0" \
		torch torchvision \
		flytekitplugins-spark==$(FLYTEKIT_VERSION) flytekitplugins-kftensorflow==$(FLYTEKIT_VERSION) \
		flytekitplugins-kfpytorch==$(FLYTEKIT_VERSION) flytekitplugins-ray==$(FLYTEKIT_VERSION) \
		flytekitplugins-bigquery==$(FLYTEKIT_VERSION) flytekitplugins-envd==$(FLYTEKIT_VERSION) \
		flytekitplugins-pod==$(FLYTEKIT_VERSION) flytekitplugins-airflow==$(FLYTEKIT_VERSION) \
		flytekitplugins-mlflow==$(FLYTEKIT_VERSION) flytekitplugins-pandera==$(FLYTEKIT_VERSION) \
		flytekit==$(FLYTEKIT_VERSION)
	uv pip install -e dummy_agent

.PHONY: functional_tests
functional_tests:  # Run flytesnacks example locally
	python functional_tests.py

.PHONY: flytesnacks
flytesnacks:  # Run flytesnacks example locally
	pyflyte run integration_tests.py flytesnacks_wf

.PHONY: build_agent_image
build_agent_image:  # Build and push the image for the agent
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flyte-conformance-agent:nightly -f dummy_agent/Dockerfile .


.PHONY: build_ci_image
build_ci_image: # Build and push the image for the agent
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flyte-conformance-ci:latest -f Dockerfile .