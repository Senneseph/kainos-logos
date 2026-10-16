# Phase 1 — Experiments (E1.1–E1.5)

Each experiment: hypothesis, metric, threshold, evidence file. All must pass.

---

## E1.1 — Parity: NL → PCRE on the seed grammar

- **Hypothesis:** The deterministic kernel + emitter correctly translate every
  description expressible in the seed grammar (spec.md) into a regex that passes the
  judge.
- **Metric:** `accuracy = correct / total` over the full seed corpus (every operator
  × representative combinations).
- **Threshold:** `accuracy == 1.0`.
- **Evidence:** `data/regex/seed_corpus.jsonl`, `tests/regex/test_emitter.py`,
  `results/phase-1/e1.1.json`.

## E1.2 — Compositional generalization (C1)

- **Hypothesis:** The pipeline solves descriptions combining abstractions that never
  co-occurred in any single training/seed example (e.g. "three digits, optionally
  followed by a hyphen and two letters" when "optional" and "three digits" were only
  seen separately).
- **Metric:** accuracy on a held-out **compositional set** (novel combos of known
  operators) vs. a **direct baseline** (no IR/CODEX; e.g. a rule/seq2seq model that
  saw the same non-compositional seed data).
- **Threshold:** pipeline accuracy ≥ baseline accuracy + a margin, and pipeline
  accuracy ≥ 0.8.
- **Evidence:** `results/phase-1/e1.2.json` (side-by-side).

## E1.3 — Persistent memory (C2)

- **Hypothesis:** A CODEX entry (`US_PHONE_NUMBER = \d{3}-\d{3}-\d{4}`) introduced in
  one session is retained and used after a full restart, with neural weights
  unchanged.
- **Metric:** before-restart and after-restart success on "an American phone number"
  (both == 1), plus the CODEX dump contains the assertion with provenance.
- **Threshold:** both == 1; assertion present post-restart.
- **Evidence:** `results/phase-1/e1.3.json`, `kainos codex explain us_phone_number`.

## E1.4 — Honest uncertainty (C3)

- **Hypothesis:** For underspecified input ("…then the dash thing…"), the system
  either resolves via CODEX rotation or escalates to a clarifying question, and
  never emits a regex it cannot justify.
- **Metric:** on a set of deliberately vague descriptions, `clarification_rate`
  (fraction escalated) and `justified_rate` (fraction of emitted regexes with a
  complete audit trace).
- **Threshold:** `clarification_rate ≥ 0.5` and `justified_rate == 1.0`.
- **Evidence:** `results/phase-1/e1.4.json`.

## E1.5 — A/B vs. conventional baseline (the big one)

- **Hypothesis:** Given the same parameter budget and the same training corpus, the
  CODEX pipeline (Model B) beats a conventional next-token model (Model A) on
  **combinations absent from training**.
- **Setup:** Train Model A (small transformer/seq2seq) on English→PCRE pairs that
  *exclude* the compositional set. Run Model B (this pipeline, same seed data loaded
  as CODEX assertions). Test both on the compositional set.
- **Metric:** accuracy (and, secondarily, abstention quality) on the compositional
  set.
- **Threshold:** B > A with statistical significance (or, at minimum, B ≥ A while B
  also abstains correctly on the vague set — C3 — which A cannot).
- **Evidence:** `results/phase-1/e1.5.json`, `results/phase-1/e1.5.md`.

> Note: E1.5 requires the `LLMKernel`/baseline path from ADR-0004. If a hosted model
> is unavailable, use a tiny local model via a standard inference backend. The
> comparison is still valid: both paths produce PCRE from the *same* seed data; only
> the architecture differs.
