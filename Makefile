export REPOSITORY=flytekit

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
	pip install pre-commit
	pip install flytekitplugins-spark flytekitplugins-ray flytekitplugins-bigquery
	pip install -U flytekit


# Build and push the image for the agent
.PHONY: build_agent
build_agent:
	docker build --push --platform linux/amd64 -t ghcr.io/unionai/flyte-conformance-agent:nightly -f mock_agent/Dockerfile .