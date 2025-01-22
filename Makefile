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
	pip install -r requirements.in

.PHONY: uv-setup
uv-setup:
	uv pip install --system -r requirements.in

.PHONY: functional_tests
functional_tests:  # Run functional tests locally
	pyflyte register --project flyte-conformance --domain development --version v1 dummy_tasks.py
	python functional_tests.py

.PHONY: register
register:  # Register all the workflows
	pyflyte register --project flyte-conformance --domain development workflow/integration_tests.py
	pyflyte launchplan --project flyte-conformance --domain development flyte_agent_lp --activate
	pyflyte launchplan --project flyte-conformance --domain development flyte_conformance_lp --activate
	pyflyte launchplan --project flyte-conformance --domain development flyte_plugin_lp --activate
	pyflyte launchplan --project flyte-conformance --domain development flytesnacks_lp --activate

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
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flyte-conformance-agent:nightly-async -f noop_agent/Dockerfile .

.PHONY: build_flytekit_image
build_flytekit_image: # Build and push the default image for the flyte task
	docker buildx build --push --platform linux/amd64 -t ghcr.io/unionai/flytekit:nightly -f Dockerfile .
