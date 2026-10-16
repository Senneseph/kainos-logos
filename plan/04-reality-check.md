# 04 — Reality Check (pre-development)

Honest audit of what's actually true before we write code. Corrected 2026-08-19 for
hardware, toolchain, and scope decisions from the project owner.

## 1. Environment reality (verified 2026-08-19)

| Fact | Status | Consequence |
|------|--------|-------------|
| Host | **AMD Strix Halo** — Gmktec EVO-X2, Ryzen AI MAX+ 395, 128 GB DDR5 @ 8000 MT/s (unified memory) | no CUDA anywhere; GPU compute = Vulkan or experimental ROCm |
| GPU | Radeon RDNA 3.5 iGPU (40 CU) sharing the 128 GB | ideal for large local GGUFs; offload via **Vulkan** (ROCm on Strix Halo is still experimental) |
| **Thermal** | historically EC-gated hard power-off under heavy load; owner now runs **low-power mode — not a current constraint** | no special benchmark throttling for now |
| Python | 3.12.3 ✓ (host), venv available but PEP 668 managed | **run in Docker** (ADR-0010), don't pollute the host |
| Perl | present (system) | the regex judge lives in Perl (ADR-0009) |
| dev deps | pytest/mypy/ruff/hypothesis **missing** on host | installed inside the pinned Docker image, not the host |
| git | repo initialized, identity configured | keep committing as we go |
| local LLM | `llama-server` + GGUF models (Qwen3.6-27B, GLM-4.7-Flash, DeepSeek-V4-Flash, …) | E1.5 baseline runs fully offline |
| prior-art stance | owner: "prior art is to borrow from; our approach is new; overfit, so be it" | see §2 |

## 2. Scope: where our effort actually goes

Owner's ruling settles it: **we don't gate on prior art.** Prior art is a *library* —
we borrow datasets (e.g. `NL-RX-Synth`, `regel`) and the conventional-model baseline
where it saves time, and we don't spend cycles defending novelty.

What that ruling means for focus: the claims worth proving are the ones a compiler or
a frozen LLM **cannot** do — because those are the only ones that distinguish us and
the only ones worth our time:

1. **C2 — persistent learning without retraining** (teach → restart → still know).
2. **C3 — honest uncertainty** ("I don't know, but here's how to find out").
3. **A5 — contradiction expands the ontology** (new dimension, not averaged weights).
4. **A1 — active information-gain question selection** (20Q).

The E1.5 A/B still runs (we need a fair *conventional* comparator to claim "B > A"),
but that's borrowing a baseline, not seeking validation.

## 3. Regex engine (decided — ADR-0009)

Perl's regex engine is the judge. It's the canonical, ubiquitous regex host and a
superset of PCRE. Python's `re` (non-PCRE, Unicode `\d`) is **not** used for judging.
The emitter targets the Perl/PCRE-compatible construct set we emit; the judge is a
small Perl script the harness calls.

## 4. Kill criteria (null hypotheses we commit to before building)

- **K1:** If the teach→restart→reuse loop (C2) does not survive a restart with frozen
  kernel, the "knowledge separated from weights" claim is dead. **Stop or redesign.**
- **K2:** If, on the *novel* claims (C2/C3/A5), the CODEX adds no measurable benefit
  over a plain `dict` + compiler of equivalent complexity, the architecture is
  overhead. **Stop.**
- **K3:** If contradiction→dimension (A5) produces garbage terms that a human can't
  sign off on after one canonical conflict, the "self-expanding ontology" claim is
  unfalsifiable. **Constrain it or drop it.**
- **K4 (gated):** φ/Fibonacci numerics/topology must win a benchmark with a margin or
  be recorded **reject**. Already encoded in ADR-0006.

## 5. Decisions locked (with the owner's direction applied)

| Decision | Locked |
|----------|--------|
| Toolchain | Idempotent Docker image; every dependency pinned as data (ADR-0010) |
| Regex judge | Perl (ADR-0009) |
| Prototype language | Python, **inside Docker** only (ADR-0001) |
| Long-term language | Rust — port proven core, translate/copy crates (ADR-0001) |
| E1.5 LLM runtime | ~~local `llama-server` + one pinned small GGUF; offline~~ **superseded (owner, 2026-08-20): owner's local Ollama server on the LAN (`OLLAMA_ENDPOINT`/`OLLAMA_MODEL` from the project `.env`), offline; the pinned snapshot is recorded in experiment configs. Notes: use the NATIVE `/api/chat` (the server's custom `/v1` proxy is flaky) with `think: false` (thinking model) + `format: "json"`. E1.5 itself is LLM-free: Model A is an in-repo torch baseline, Model B the deterministic pipeline.** |
| E1.5 tensor library | `torch==2.13.0+cpu` (CPU index, hash-pinned in `requirements.lock`) — owner-approved 2026-08-20 ("as long as dependencies are pinned, we're good") |
| E1.5 timing | deferred until C2/C3/A5 are green |
| GPU | defer; CPU-only in-container for Phases 0–2 |

## 6. The cheap pre-dev spike (do this before Phase 0 scaffolding)

A ~2-hour throwaway, run inside the Docker image, to validate the two riskiest
assumptions:

1. 5 sentences hand-pumped through `parse → IR → emit → (Perl judge)`.
2. A 20-line CODEX: teach one term → serialize → reload → resolve (proves C2's
   mechanism end-to-end before building the full store).

Keep it CPU-only and short — for fast iteration, not a thermal constraint. If the spike succeeds, Phase 0 is
de-risked; if persistence surprises us, fix the schema before committing to
`SqliteCodexStore`.

## 7. Immediate next actions (ordered)

1. Author `Dockerfile` + pinned lockfile (Python, Perl, dev deps, llama.cpp if needed).
2. Build the image; confirm `pytest`/`perl` run inside it.
3. Run the §6 spike inside the container.
4. Commit; then start `action-steps/01-scaffold.md`.
