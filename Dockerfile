# Kainos-Logos — pinned developer image (ADR-0010: idempotent build; every
# dependency is pinned data). Phases 0–2 are CPU-only (no GPU pass-through).
#
#   Base image  : pinned by digest (no :latest)
#   Python      : 3.12.14 (from base; satisfies ">=3.11")
#   Perl        : 5.40 (perl-base from base; the regex judge, ADR-0009 —
#                 verified: captures, /g, full-match all work)
#   Python deps : requirements.lock (full transitive closure, sha256-pinned)
#
# No apt-get: the base digest pins everything the OS layer provides, so the
# build never touches a moving apt index. If a recipe ever needs a system
# package, pin its exact version here AND record it in the lockfile header.

FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.lock /tmp/requirements.lock
RUN pip install --require-hashes -r /tmp/requirements.lock \
    && rm /tmp/requirements.lock

# The repository is bind-mounted over this directory at `docker run` time.
WORKDIR /work
