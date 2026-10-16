# 90 — Proposed repo layout (ADR-0007)

Canonical descriptive layout. The **executable** cross-reference — *which directive
creates which path* — is [`../../action-steps/LAYOUT.md`](../../action-steps/LAYOUT.md);
keep the two in agreement. If they drift, LAYOUT.md (the manifest the directives
execute) wins until this file is fixed.

```
kainos-logos/
├── PROJECT_OVERVIEW.md            # the source document (read-only reference)
├── SUPPLEMENTAL_IDEAS.md          # supplemental design dialogue (read-only reference;
│                                  # projection + recursive workspace — ADR-0011/0012)
├── plan/                          # the descriptive plan (why)
├── action-steps/                  # the executable runbook (how)
├── Dockerfile                     # pinned image (ADR-0010): Python, Perl, dev deps
├── .dockerignore
├── pyproject.toml                 # package kainos; scripts: kainos = kainos.cli:main
├── Makefile                       # test / lint / typecheck / image / bench
├── README.md
├── .gitignore                     # results/ (incl. var: data/*.sqlite), __pycache__ …
├── .github/workflows/ci.yml       # pytest + typecheck + lint in-container
├── specs/
│   ├── ir.schema.json             # Semantic IR JSON schema (03 / P0.05)
│   └── codex.schema.json          # CODEX assertion schema (02 / P0.02)
├── src/kainos/
│   ├── __init__.py
│   ├── cli.py                     # `kainos` CLI (04 / P0.07)
│   ├── codex/
│   │   ├── models.py              # TermRef, Assertion, Provenance, states (02)
│   │   ├── store.py               # CodexStore protocol (02)
│   │   ├── sqlite.py              # SqliteCodexStore (02)
│   │   ├── memory.py              # InMemoryCodexStore (02)
│   │   └── explain.py             # evidence-chain explain (03)
│   ├── ir/
│   │   ├── models.py              # SemanticIR + nodes (03)
│   │   └── codec.py               # validate/load/dump (03)
│   ├── lang/
│   │   ├── kernel.py              # LanguageKernel protocol (07)
│   │   ├── deterministic.py       # DeterministicKernel (07; 20Q grammar ext. in 14)
│   │   └── llm.py                 # LLMKernel stub (12) → production (17)
│   ├── regex/
│   │   ├── ir.py                  # dialect nodes (06)
│   │   ├── emitter.py             # → PCRE (06)
│   │   ├── lexicon.py             # CODEX lexicon seed (07)
│   │   ├── resolver.py            # CODEX resolution + rotation (08)
│   │   ├── testgen.py             # positive/negative generator (08)
│   │   ├── judge.py               # Perl-judge wrapper + verdict (08)
│   │   ├── pipeline.py            # end-to-end describe (08)
│   │   ├── data.py                # corpus loader (09)
│   │   ├── bench.py               # E1.1–E1.5 runners (09–12)
│   │   ├── compose.py             # compositional set generator (10)
│   │   └── baseline.py            # DirectBaseline, no CODEX (10)
│   ├── q20/
│   │   ├── oracle.py              # seeded property oracle (13)
│   │   ├── seed.py                # corpus → CODEX assertions (13)
│   │   ├── hypothesis.py          # hypothesis space (14)
│   │   ├── selector.py            # info-gain question selection (14)
│   │   ├── game.py                # game loop (14)
│   │   ├── learn.py               # consolidation + contradiction→dimension (15)
│   │   ├── baselines.py           # random / stateless (15)
│   │   └── dashboard.py           # coverage/exception growth (15)
│   ├── harness/
│   │   ├── runner.py              # Experiment protocol + run + registry (05)
│   │   ├── report.py              # results/SUMMARY.md render (05)
│   │   └── dummy.py               # registered no-op experiment (05)
│   ├── exchange/                  # (Phase 3, step 19)
│   │   ├── protocol.py            # assertion deltas + idempotent merge
│   │   └── reconciler.py          # contradiction → missing dimension
│   ├── numerics/                  # (Phase 3, step 18 — gated)
│   │   ├── base.py                # Numerics protocol + FloatNumerics default
│   │   └── phi.py                 # PhiNumerics (gated)
│   ├── multimodal/                # (Phase 3, step 20)
│   │   ├── port.py                # PerceptionPort protocol
│   │   └── synthetic_vision.py    # synthetic scene → IR
│   ├── projection/                # (Phase 3, step 21 — ADR-0011, claims X1/X2)
│   │   ├── capabilities.py        # Capability model + CODEX seed (P11)
│   │   ├── planner.py             # bounded precondition/effect search, NO VALID PLAN
│   │   ├── contract.py            # interaction-type response contracts (data)
│   │   └── creative.py            # structured stochastic traversal (temperature)
│   └── workspace/                 # (Phase 3, step 22 — ADR-0012, claim X3)
│       ├── workspace.py           # WorkSpace: recursive, lifetime, query/fork/dump
│       └── source.py              # source + versioned analysis IRs, promotion
├── tests/                         # mirrors src/kainos/ one-to-one, see exceptions below
│   ├── __init__.py
│   ├── codex/                     # test_models, test_store, test_explain + golden/dump.json
│   ├── ir/                        # test_codec + golden/minimal.json
│   ├── golden/test_golden.py      # cross-cutting exception (see below)
│   ├── cli/test_cli.py            # cross-cutting exception (see below)
│   ├── lang/  regex/  q20/  numerics/  exchange/  multimodal/
│   ├── projection/                # tests for step 21 (test_capabilities, test_planner, …)
│   └── workspace/                 # tests for step 22 (test_workspace, test_promotion, …)
├── data/                          # committed, small, reproducible corpora
│   ├── regex/
│   │   ├── seed_corpus.jsonl          # (09)
│   │   ├── compositional_set.jsonl    # (10, ground-truthed, seed 42)
│   │   ├── vague_set.jsonl            # (11)
│   │   ├── holdout_set.jsonl          # (12, final E1.5 gate)
│   │   └── open_phrasing.jsonl        # (17)
│   └── q20/
│       ├── concepts.json              # (13)
│       └── questions.json             # (13)
├── scripts/
│   ├── judge.pl                 # Perl regex judge (08, ADR-0009)
│   ├── train_baseline.py        # Model A seq2seq (12)
│   └── predict.py               # Model A inference (12)
├── benchmarks/                  # top-level: experiments, not library code
│   ├── phi/                     # E3.5 kernels (18)
│   └── topology/                # E3.2 kernels (18)
└── results/                     # COMMITTED official artifacts (pinned runs;
    │                            # the house rule: results + SUMMARY ship in
    │                            # the build commit — regenerated only on
    │                            # re-run)
    ├── dummy.md
    ├── phase-1/e1.1..e1.5.json + e1.5.md + SUMMARY.md
    ├── phase-2/e2.1..e2.5.json + growth.md + SUMMARY.md
    ├── phase-3/e3.1..e3.7.json + SUMMARY.md
    ├── phase-4/… · phase-5/… · phase-6/…        # tutor: run dirs + derived jsons
    └── scavenge/                              # **G9** — Morpho pattern-transfer
                                               # artifacts: m1.json (final M1
                                               # verdict), m1-seed-corpus.json
                                               # (interim), m3-m6-probe.json
                                               # (sweep scale probes)
```

## Layout rules

- **Package `kainos` only**; phases add submodules, never sibling packages
  (ADR-0007).
- **`tests/` mirrors `src/kainos/` one-to-one**, with exactly two documented
  cross-cutting exceptions: `tests/golden/` (byte-stable serialization snapshots)
  and `tests/cli/` (mirrors the single `cli.py`, not a submodule).
- **No `src/kainos/reasoner/` package yet.** Resolution lives in
  `regex/resolver.py`, consolidation in `q20/learn.py`, reconciliation in
  `exchange/reconciler.py`. A shared reasoner seam is created (with an ADR) only
  when a genuinely shared second consumer appears — never as an empty module.
  (See `../10-architecture/reasoner.md` for its *intended* contract.)
- **`data/` is committed corpus data.** `data/codex.sqlite` is the CLI's *runtime*
  default DB — gitignored (`data/*.sqlite`), never committed, not part of the
  substrate.
- **`data/regex/compositional_set.jsonl`** is materialized by step 10 (deterministic,
  seed 42, judge-verified ground truth) and is the input step 12 holds out as
  `holdout_set.jsonl` — both are committed files so "measure, don't argue" is
  auditable.
- **`data/codex.sqlite` stays inside `data/`** (documented runtime-only) rather than
  a new `var/` directory — keeps the CLI default simple at this project's scale.
- **`benchmarks/` and `scripts/` are top-level** by design: they are experiments,
  not library code.
- **`results/` naming is exact and stable**: `results/phase-{N}/{eX.Y}.json`
  (plus the two narrative exceptions `e1.5.md`, `growth.md`, per-phase
  `SUMMARY.md`, and phase-6's per-run directories `e6.N-run{1,2}/` with their
  `codeX/session` dumps). Never renumber. **G9** `results/scavenge/`
  (SCAVENGE_MORPHO.md; ADR-0013) holds the pattern-transfer benchmark
  artifacts on the same committed-artifact rule.
