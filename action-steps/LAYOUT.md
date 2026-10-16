# LAYOUT — Durable directory structure (action-step → artifact manifest)

> Optional reference. Maps every directive in this folder to the **durable paths** it
> creates or writes, so the repo grows deterministically as steps are executed. The
> canonical descriptive layout is `plan/90-appendices/repo-layout.md` (ADR-0007); this
> file is the *executable* cross-reference: **who writes what, and where it must live
> forever.**

## The three durability rules

1. **Committed = durable.** `src/`, `tests/`, `specs/`, `data/`, `plan/`,
   `benchmarks/`, `scripts/`, and the phase `results.md` files are committed and are
   the project's permanent record.
2. **`results/` = regenerable, gitignored.** Every `results/*.json|.md` is an
   experiment *output*, reproducible via `kainos experiment run …` from committed
   `data/` + `src/`. It must never be the only home of a finding — the finding's
   committed home is the phase `plan/30-phases/*/results.md` sign-off.
3. **Tests mirror `src/kainos/` one-to-one**, with two cross-cutting exceptions:
   `tests/golden/` (byte-stable serialization snapshots) and `tests/cli/` (mirrors the
   single `cli.py`, not a submodule).

## Canonical tree (annotated with the creating directive)

```
kainos-logos/
├── PROJECT_OVERVIEW.md                      # read-only source (pre-existing)
├── plan/                                    # descriptive plan (why) — pre-existing
│   └── 30-phases/*/results.md               # phase sign-off (05, 12, 16, 20 write these)
├── action-steps/                            # this runbook (how)
├── Dockerfile                               # ← 01
├── .dockerignore                            # ← 01
├── pyproject.toml                           # ← 01 (scripts entry: kainos = kainos.cli:main)
├── Makefile                                 # ← 01 (test/lint/typecheck/image/bench)
├── README.md                                # ← 01
├── .gitignore                               # ← 01
├── .github/workflows/ci.yml                 # ← 05
├── specs/
│   ├── ir.schema.json                       # ← 03
│   └── codex.schema.json                    # ← 02 (G1 resolved: schema ⇄ dataclass parity)
├── src/kainos/
│   ├── __init__.py                          # ← 01
│   ├── cli.py                               # ← 04
│   ├── codex/
│   │   ├── models.py                        # ← 02
│   │   ├── store.py                         # ← 02
│   │   ├── sqlite.py                        # ← 02
│   │   ├── memory.py                        # ← 02
│   │   └── explain.py                       # ← 03
│   ├── ir/
│   │   ├── models.py                        # ← 03
│   │   └── codec.py                         # ← 03
│   ├── lang/
│   │   ├── kernel.py                        # ← 07 (protocol)
│   │   ├── deterministic.py                 # ← 07 (+20Q grammar ext. in 14)
│   │   └── llm.py                           # ← 12 (stub) / 17 (production)
│   ├── regex/
│   │   ├── ir.py                            # ← 06
│   │   ├── emitter.py                       # ← 06
│   │   ├── lexicon.py                       # ← 07
│   │   ├── resolver.py                      # ← 08
│   │   ├── testgen.py                       # ← 08
│   │   ├── judge.py                         # ← 08
│   │   ├── pipeline.py                      # ← 08
│   │   ├── data.py                          # ← 09 (corpus loader)
│   │   ├── bench.py                         # ← 09 (E1.1) + runners 10–12
│   │   ├── compose.py                       # ← 10
│   │   └── baseline.py                      # ← 10
│   ├── q20/
│   │   ├── oracle.py                        # ← 13
│   │   ├── seed.py                          # ← 13
│   │   ├── hypothesis.py                    # ← 14
│   │   ├── selector.py                      # ← 14
│   │   ├── game.py                          # ← 14
│   │   ├── learn.py                         # ← 15
│   │   ├── baselines.py                     # ← 15
│   │   └── dashboard.py                     # ← 15
│   ├── exchange/
│   │   ├── protocol.py                      # ← 19
│   │   └── reconciler.py                    # ← 19
│   ├── numerics/
│   │   ├── base.py                          # ← 18
│   │   └── phi.py                           # ← 18
│   ├── multimodal/
│   │   ├── port.py                          # ← 20
│   │   └── synthetic_vision.py              # ← 20
│   ├── projection/                          # ← 21 (ADR-0011, X1/X2)
│   │   ├── capabilities.py                  # Capability model + CODEX seed
│   │   ├── planner.py                       # bounded search; NO VALID PLAN
│   │   ├── contract.py                      # response contracts (data)
│   │   └── creative.py                      # temperature traversal
│   ├── workspace/                           # ← 22 (ADR-0012, X3)
│   │   ├── workspace.py                     # recursive WorkSpace
│   │   ├── source.py                        # sources + versioned analyses
│   │   └── promote.py                       # explicit promotion + lapse
│   │   # (no reasoner/ package — G3: resolution = regex/resolver.py, consolidation =
│   │   #  q20/learn.py, reconciliation = exchange/reconciler.py; a shared seam + ADR
│   │   #  only when a second genuine consumer appears)
│   └── harness/
│       ├── runner.py                        # ← 05
│       ├── report.py                        # ← 05
│       └── dummy.py                         # ← 05
├── tests/                                   # mirrors src/kainos/ one-to-one
│   ├── __init__.py                          # ← 01
│   ├── codex/                               # ← 02, 03
│   │   ├── test_models.py, test_store.py    # ← 02
│   │   ├── test_explain.py                  # ← 03
│   │   └── golden/dump.json                 # ← 04
│   ├── ir/
│   │   ├── test_codec.py                    # ← 03
│   │   └── golden/minimal.json              # ← 03
│   ├── golden/test_golden.py                # ← 04 (cross-cutting)
│   ├── cli/test_cli.py                      # ← 04 (cross-cutting)
│   ├── regex/                               # ← 06, 07, 08, 09, 11
│   ├── lang/test_deterministic.py           # ← 07
│   ├── q20/                                 # ← 13, 14, 15
│   ├── exchange/                            # ← 19
│   ├── numerics/                            # ← 18 (explicit, G8: test_base, test_phi,
│   │                                        #    test_seam_neutral)
│   ├── projection/                          # ← 21 (test_capabilities, test_planner,
│   │                                        #    test_contracts, test_creative)
│   ├── workspace/                           # ← 22 (test_workspace, test_promotion,
│   │                                        #    test_source)
│   └── multimodal/test_synthetic_vision.py  # ← 20
├── data/                                    # committed, small, reproducible
│   ├── codex.sqlite                         # runtime-only CLI default (gitignored; G4)
│   ├── regex/
│   │   ├── seed_corpus.jsonl                # ← 09
│   │   ├── compositional_set.jsonl          # ← 10 (G2: committed, seed 42, ground-truthed)
│   │   ├── vague_set.jsonl                  # ← 11
│   │   ├── holdout_set.jsonl                # ← 12 (G2: E1.5 gate input)
│   │   └── open_phrasing.jsonl              # ← 17
│   └── q20/
│       ├── concepts.json                    # ← 13
│       └── questions.json                   # ← 13
├── scripts/
│   ├── judge.pl                             # ← 08 (Perl judge, ADR-0009)
│   ├── train_baseline.py                    # ← 12 (Model A)
│   └── predict.py                           # ← 12
├── benchmarks/
│   ├── phi/                                 # ← 18 (E3.5 kernels)
│   └── topology/                            # ← 18 (E3.2 kernels)
└── results/                                 # gitignored, regenerable
    ├── dummy.md                             # ← 05
    ├── phase-1/e1.1..e1.5.json + e1.5.md + SUMMARY.md   # ← 09,10,11,12 (SUMMARY: 12)
    ├── phase-2/e2.1..e2.5.json + growth.md + SUMMARY.md  # ← 15, 16
    └── phase-3/e3.1..e3.7.json + SUMMARY.md            # ← 17,18,19,21,22 (SUMMARY: 20)
```

## Per-directive manifest

| Step | Directive | Creates (committed) | Writes (gitignored `results/`) |
|------|-----------|---------------------|--------------------------------|
| 01 | scaffold | Dockerfile, .dockerignore, pyproject.toml, src/kainos/\_\_init\_\_.py, tests/\_\_init\_\_.py, .gitignore, Makefile, README.md | — |
| 02 | codex model+store | src/kainos/codex/{models,store,sqlite,memory}.py, specs/codex.schema.json, tests/codex/{test_models,test_store}.py | — |
| 03 | explain + IR codec | src/kainos/codex/explain.py, src/kainos/ir/{models,codec}.py, specs/ir.schema.json, tests/codex/test_explain.py, tests/ir/{test_codec.py, golden/minimal.json} | — |
| 04 | golden + CLI | src/kainos/cli.py, tests/codex/golden/dump.json, tests/golden/test_golden.py, tests/cli/test_cli.py | — |
| 05 | harness + CI | src/kainos/harness/{runner,report,dummy}.py, .github/workflows/ci.yml, plan/…/phase-0-foundation/results.md | results/dummy.md |
| 06 | regex IR + emitter | src/kainos/regex/{ir,emitter}.py, tests/regex/{test_ir,test_emitter}.py | — |
| 07 | kernel + lexicon | src/kainos/lang/{kernel,deterministic}.py, src/kainos/regex/lexicon.py, tests/lang/test_deterministic.py, tests/regex/test_codex_seed.py | — |
| 08 | resolver/judge/pipeline | src/kainos/regex/{resolver,testgen,judge,pipeline}.py, scripts/judge.pl, tests/regex/{test_resolver,test_testgen,test_pipeline}.py | — |
| 09 | seed corpus + E1.1 | src/kainos/regex/{data,bench}.py, data/regex/seed_corpus.jsonl | results/phase-1/e1.1.json |
| 10 | compositionality + E1.2 | src/kainos/regex/{compose,baseline}.py, data/regex/compositional_set.jsonl | results/phase-1/e1.2.json |
| 11 | persistence + uncertainty | data/regex/vague_set.jsonl, tests/regex/test_persistence.py | results/phase-1/{e1.3,e1.4}.json |
| 12 | LLM A/B + E1.5 | src/kainos/lang/llm.py (stub), scripts/{train_baseline,predict}.py, data/regex/holdout_set.jsonl, plan/…/phase-1-regex/results.md | results/phase-1/{e1.5.json, e1.5.md} |
| 13 | 20Q corpus + oracle | data/q20/{concepts,questions}.json, src/kainos/q20/{oracle,seed}.py, tests/q20/{test_oracle,test_seed}.py | — |
| 14 | hypothesis/selector/game | src/kainos/q20/{hypothesis,selector,game}.py (+ kernel 20Q grammar), tests/q20/{test_question_parse,test_hypothesis,test_selector,test_game}.py | — |
| 15 | learning + dashboard | src/kainos/q20/{learn,baselines,dashboard}.py, tests/q20/{test_learn,test_baselines,test_dashboard}.py | results/phase-2/growth.md |
| 16 | E2.1–E2.5 sign-off | plan/…/phase-2-20questions/results.md | results/phase-2/e2.{1,2,3,4,5}.json + SUMMARY.md |
| 17 | production LLM kernel | data/regex/open_phrasing.jsonl (+ extends lang/llm.py) | results/phase-3/e3.1.json |
| 18 | φ numerics + topology | src/kainos/numerics/{base,phi}.py, benchmarks/{phi,topology}/, tests/numerics/{test_base,test_phi,test_seam_neutral}.py | results/phase-3/{e3.5,e3.2}.json |
| 19 | distributed CODEX | src/kainos/exchange/{protocol,reconciler}.py, tests/exchange/{test_merge,test_reconciler}.py | results/phase-3/e3.3.json |
| 20 | multimodal + consolidation | src/kainos/multimodal/{port,synthetic_vision}.py, tests/multimodal/test_synthetic_vision.py, plan/…/phase-3-generalization/results.md, updates plan/20-roadmap.md + plan/03-adr.md | results/phase-3/e3.4.json + SUMMARY.md |
| 21 | projection (P3.12–P3.14) | src/kainos/projection/{capabilities,planner,contract,creative}.py, tests/projection/{test_capabilities,test_planner,test_contracts,test_creative}.py | results/phase-3/e3.6.json |
| 22 | workspace memory (P3.15–P3.17) | src/kainos/workspace/{workspace,source,promote}.py, tests/workspace/{test_workspace,test_promotion,test_source}.py | results/phase-3/e3.7.json |

## Conventions to keep the tree stable

- **Experiment IDs** (`e1.1`…`e3.5`) are stable. Result files are named `results/phase-{1|2|3}/{id}.json` **exactly** — never renumber, never rename (matches the "never renumber Action IDs" rule).
- **Per-phase summary**: the harness `report` command renders `results/phase-N/SUMMARY.md` (see `plan/40-testing/harness.md`). Narrative reports are the exception, not the rule — only `e1.5.md` (A/B write-up) and `growth.md` (curve) carry prose; everything else is a `.json` + the phase `results.md`.
- **Data split**: `data/regex/` + `data/q20/` are committed JSONL/JSON corpora. `data/codex.sqlite` is the CLI's *runtime* DB and stays gitignored (`*.sqlite`, `data/*.sqlite`).
- **`benchmarks/` + `scripts/`** are top-level by design (ADR-0007): they are experiments, not library code.

## Gaps — resolved (2026-08-19 plan review)

All eight layout gaps found in the audit are **applied to the directives** as of this
date. Kept here as a changelog so the reasoning stays discoverable.

- **G1 — `specs/codex.schema.json` (no producer). RESOLVED:** step 02 now emits it
  (`kainos/codex/1`, mirror of the `Assertion` model) with a model ⇄ schema parity
  test (ADR-0008: the no-bare-edge rule is schema-enforced too).
- **G2 — compositional/holdout sets never materialized. RESOLVED:** step 10 commits
  `data/regex/compositional_set.jsonl` (deterministic, seed 42, judge-verified);
  step 12 materializes `data/regex/holdout_set.jsonl` from it as the E1.5 gate input
  (split rule recorded in the result config).
- **G3 — `src/kainos/reasoner/` (in layout, no directive). RESOLVED:** dropped from
  the layout. Resolution/consolidation/reconciliation live in the domain packages
  (08/15/19); a shared seam — and an ADR — only when a second genuine consumer
  appears. `plan/10-architecture/reasoner.md` documents its *intended* contract.
- **G4 — `data/codex.sqlite` CLI default in committed `data/`. RESOLVED:** kept as the
  default, documented as **runtime-only** (gitignored via `data/*.sqlite`); no `var/`
  directory at this project's scale.
- **G5 — `tests/golden/` + `tests/cli/` break the mirror rule. RESOLVED:** the two
  cross-cutting exceptions are codified in the “Layout rules” of
  `plan/90-appendices/repo-layout.md` (and in the durability rules above).
- **G6 — per-phase `SUMMARY.md` not emitted. RESOLVED:** steps 16 and 20 render
  `results/phase-{2,3}/SUMMARY.md` via the harness `report` command (phase 1 already
  had the convention; the harness CLI now defines `report --phase N`).
- **G7 — `make bench` placeholder. RESOLVED:** step 01 makes `bench` a succeeding
  no-op; step 05 rewires it to the real runner (`python -m kainos.harness.runner
  --all` ≡ `kainos experiment run --all`).
- **G8 — numerics tests path. RESOLVED:** step 18 writes explicit
  `tests/numerics/{test_base,test_phi,test_seam_neutral}.py`,
  mirroring `src/kainos/numerics/`; the seam-neutrality regression runs in CI.

*Process rule: any new layout gap found during execution gets a `G<n>` entry here,
the matching directive update, and a commit — the tree and the manifest never drift.*
