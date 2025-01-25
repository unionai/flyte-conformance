import os

DEFAULT_REGISTRY = "ghcr.io/unionai"
registry = os.getenv("FLYTE_REGISTRY", DEFAULT_REGISTRY)
