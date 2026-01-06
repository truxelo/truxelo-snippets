# -*- mode: makefile -*-

# tools configuration
SHELL := /bin/bash

.PHONY: init
init: ## Initialise local environment
	@ uv sync --all-groups

.PHONY: format
format: ## Format the codebase
	@ uv run black src tests
	@ uv run isort src tests

.PHONY: lint
lint: format ## Lint the codebase
	@ uv run black --check src tests
	@ uv run isort --check src tests
	@ uv run flake8 src tests
	@ uv run mypy src tests
	@ uv run pylint src tests

.PHONY: tests
tests: ## Run unit tests and code coverage
	@ uv run pytest --doctest-modules --cov=src --cov-report=html --cov-report=term src tests

.PHONY: build
build: ## Build python wheel
	@ uv build

.DEFAULT_GOAL := help
.PHONY: help
help: # See <https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html> for explanation.
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
