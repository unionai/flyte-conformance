export FLYTEKIT_PLUGIN_VERSION=v1.13.5

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
	pip install uv==0.2.29
	uv pip install -U pip apache-airflow[google]==2.7.3 pre-commit matplotlib "tenacity<=8.3.0" \
 		tensorflow tensorboardX tensorflow_datasets "numpy<2.0.0" "pandera>=0.7.1,<=0.19.3" \
		torch torchvision \
		flytekitplugins-spark==$(FLYTEKIT_PLUGIN_VERSION) flytekitplugins-kftensorflow==$(FLYTEKIT_PLUGIN_VERSION) \
		flytekitplugins-kfpytorch==$(FLYTEKIT_PLUGIN_VERSION) flytekitplugins-ray==$(FLYTEKIT_PLUGIN_VERSION) \
		flytekitplugins-bigquery==$(FLYTEKIT_PLUGIN_VERSION) \
		flytekitplugins-pod==$(FLYTEKIT_PLUGIN_VERSION) flytekitplugins-airflow==$(FLYTEKIT_PLUGIN_VERSION) \
		flytekitplugins-mlflow==$(FLYTEKIT_PLUGIN_VERSION) flytekitplugins-pandera==$(FLYTEKIT_PLUGIN_VERSION) \
		flytekitplugins-openai==$(FLYTEKIT_PLUGIN_VERSION) flytekitplugins-envd==$(FLYTEKIT_PLUGIN_VERSION) \
		union flytekit==$(FLYTEKIT_PLUGIN_VERSION)
	uv pip install -e dummy_agent
	uv pip install "git+https://github.com/flyteorg/flytekit.git@a366653e697cd3adf429a05adde2ac421fbcae99"
	uv pip install "git+https://github.com/flyteorg/flyte.git@27d9746e60e2a42fc1621e47c55591c56f216d7f#subdirectory=flyteidl"

.PHONY: functional_tests
functional_tests:  # Run functional tests locally
	pyflyte register --project flyte-conformance --domain development --version v1 dummy_tasks.py
	python functional_tests.py

.PHONY: flytesnacks
flytesnacks:  # Register and run flytesnacks example
	pyflyte run --remote workflow/integration_tests.py flytesnacks_wf

.PHONY: flyteplugins
flyteplugins:  # Register and run flyte plugins example
	pyflyte run --remote workflow/integration_tests.py flyte_plugin_wf

.PHONY: flyteagents
flyteagents:  # Register and run flyte agents example
	pyflyte run --remote workflow/integration_tests.py flyte_agent_wf

.PHONY: flyte-conformance
flyte-conformance:  # Register and run flyte conformance example
	pyflyte run --remote workflow/integration_tests.py flyte_conformance_wf

.PHONY: build_agent_image
build_agent_image:  # Build and push the image for the agent
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flyte-conformance-agent:nightly -f dummy_agent/Dockerfile .


.PHONY: build_flytekit_image
build_flytekit_image: # Build and push the default image for the flyte task
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flytekit:nightly -f Dockerfile .
