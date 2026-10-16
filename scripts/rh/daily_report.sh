#!/usr/bin/env bash
# Daily RH-attack work session (installed via user crontab, 07:00 local).
# Heads off a fresh headless pi session in the repo, which does the day's
# queue work and files the daily progress report
# (plan/40-prize-islands/rh-attack/day-NNN.md).
set -euo pipefail
# cron has a minimal PATH — resolve the toolchains explicitly (fixes
# 'pi: command not found', seen in cron.log Sep-09; P-0.9).
export PATH="$HOME/.local/share/pi-node/node-v22.23.1-linux-x64/bin:$HOME/.elan/bin:$PATH"
REPO=/home/jsmille/Projects/kainos-logos
cd "$REPO"

# Pin the working provider/model (cron does not inherit the interactive
# session's PI_* env; vast-ai is the ready provider, verified via `pi auth check`).
export PI_PROVIDER=vast-ai
export PI_MODEL="pi-qwen-vast:latest"

pi -p "Scheduled daily Riemann-Hypothesis attack session (kainos-logos, cwd = repo root). \
Steps: (1) read plan/40-prize-islands/rh-attack/README.md and the latest day-NNN.md there; \
(2) call wiki_recall for prior findings; (3) standing rules (owner, 2026-09-09, see day-011.md + prompts/): Python is frozen as oracle — new engine work is TypeScript in scripts/rh-ts/; no speculative long computes (build model, test later); read the milestone prompt that owns the next step (prompts/M1..M5) before acting; 
'exact next question' section (host python3 is numpy-only; mpmath runs inside the pinned \
container image kainos-dev:dev); (4) write the next day-NNN.md following the README report \
contract (work done + verdicts + interesting findings + named missing ingredient + next-day \
queue) - this file IS the daily progress report for the owner; \
(5) git add + commit ONLY the rh-attack paths (scripts/rh/ and plan/40-prize-islands/rh-attack/). \
NEVER touch the uncommitted e6.28 in-progress work: src/kainos/tutor/brainstem.py, \
tools/bandgen/reflib.py, src/kainos/tutor/e628.py, bands/spec-e6.28.json, \
results/e6.28.json, results/phase-6/e6.28-*. Honest-wall discipline: no theorem:riemann \
is ever invented; label every claim measured/theorem/conjecture/unmapped/falsified."
