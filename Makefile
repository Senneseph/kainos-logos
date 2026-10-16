# Kainos-Logos — stable commands (action-step 01: "set them once, never change them")
#
# All quality gates run INSIDE the pinned Docker image (ADR-0010); the host is
# never modified. Build the image once with `make image` (or let test/lint/
# typecheck depend on it), then run targets freely.

DOCKER_IMAGE ?= kainos-dev:dev
# Host-side commit id, injected into containers (no git in the image) so experiment
# result configs carry a real commit instead of "unknown".
GIT_COMMIT ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo unknown)

.DEFAULT_GOAL := help

.PHONY: help image test lint typecheck bench

help: ## Show available targets
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

image: ## Build the pinned developer image (ADR-0010)
	docker build -t $(DOCKER_IMAGE) .

test: image ## Run the test suite in-container (pytest)
	docker run --rm -v $$(pwd):/work -w /work $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe '.[dev]' && python -c 'import kainos; print(kainos.__version__)' && python -m pytest -q"

lint: image ## Lint (ruff) in-container
	docker run --rm -v $$(pwd):/work -w /work $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe . && python -m ruff check src tests"

typecheck: image ## Type check (mypy) in-container
	docker run --rm -v $$(pwd):/work -w /work $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe . && python -m mypy src"

bench: image ## Run every registered experiment — equivalent to `kainos experiment run --all`
	docker run --rm -v $$(pwd):/work -w /work -e KAINOS_GIT_COMMIT=$(GIT_COMMIT) $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe . && python -m kainos.harness.runner --all"

# --- bandgen — the band compiler (v0.1: validate/compute/control) ---
#
# `band-validate NAME=e6.17`: spec schema + structural checks only (fast, no runtime).
# `band-dryrun NAME=e6.17`: the full control — seed checks, computed beds, the
# labeled dry-run (x2 for the twin) + carry, mastery, totals, discipline.
# Exit 0 = CLEAN (ready to freeze); 1 = the mechanism disagrees with the spec.
band-validate: image ## Validate a band spec (schema + structural, no runtime)
	docker run --rm -v $$(pwd):/work -w /work $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe . && python -m tools.bandgen validate bands/spec-$(NAME).json"

band-dryrun: image ## Run the bandgen control (dry-run + frozen-shape table)
	docker run --rm -v $$(pwd):/work -w /work $(DOCKER_IMAGE) \
	  bash -c "pip install --no-build-isolation -qe . && python -m tools.bandgen dryrun bands/spec-$(NAME).json --md /work/bandgen-$(NAME)-report.md"
