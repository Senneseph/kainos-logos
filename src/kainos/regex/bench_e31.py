"""E3.1 A/B experiment (P3.02) — LLM kernel vs deterministic kernel on open phrasing.

Hypothesis (experiments.md E3.1): an `LLMKernel` behind the SAME `LanguageKernel`
interface handles open/vague phrasing the deterministic kernel cannot, while the
CODEX/reasoner/emitter/judge path is **identical in both arms** — that is what
isolates the kernel contribution (the step-17 goal: same interface, production
parser).

Design
------
- Set: `data/regex/open_phrasing.jsonl` — 12 hand-labeled idioms/synonyms
  OUTSIDE the deterministic grammar (verified: deterministic arm fails all 12 —
  parse error or escalation). Each record carries the hand-authored expected
  generic-IR AST (`expected_ir`, the hand-label of step 17), the emitter-derived
  `expected_pcre`, and hand-picked positive/negative judge examples.
- Arms: `describe(text, codex=<one shared store>, kernel=<LLMKernel or DeterministicKernel>)`.
  One `default_codex()` instance serves BOTH arms (the directive: "assert same
  codex object reused"); the deterministic arm runs first over the whole set,
  then the LLM arm — shared-state growth is recorded in `config.codex`.
- Per-item correctness (both arms, same yardstick): the arm emits a pcre AND
  that pcre passes the record's hand-picked judge examples
  (`judge(pcre, positive, negative).ok`). Escalation and parse errors are
  failures (no correct pattern). `byte_exact` (pcre == the hand-labeled
  expected_pcre) is reported separately — structurally equivalent ASTs may emit
  spelling-equivalent but byte-different patterns, so judge-correctness, not
  byte-equality, is the pass criterion (the same PCRE-level contract E1.1 uses
  against the authored expectation).
- Threshold (directive): `llm_accuracy >= deterministic_accuracy`.

The LLM arm wraps the owner's LAN Ollama (native `/api/chat`, `think: false`,
`format: "json"`, temp 0 — `OllamaBackend`). When the backend is unreachable
the experiment reports SKIP (harness), never a silent pass or a false fail.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from kainos.harness.paths import default_phase_dir
from kainos.lang.deterministic import DeterministicKernel
from kainos.lang.llm import LLMKernel, OllamaBackend
from kainos.regex.bench import corpus_hash
from kainos.regex.emitter import UnresolvedError, emit
from kainos.regex.ir import from_ir
from kainos.regex.judge import judge
from kainos.regex.pipeline import PipelineResult, default_codex, describe

if TYPE_CHECKING:
    from kainos.codex.store import CodexStore
    from kainos.lang.kernel import LanguageKernel

__all__ = [
    "OPEN_PHRASING_REL",
    "E3_1Experiment",
    "default_open_phrasing_path",
    "load_open_phrasing",
    "run_e3_1",
]

OPEN_PHRASING_REL = Path("data/regex/open_phrasing.jsonl")


def default_open_phrasing_path() -> Path:
    """The open-phrasing set: `data/regex/open_phrasing.jsonl` (hand-labeled,
    step 17) — repo-relative via CWD or the checkout containing this package."""

    here = Path(__file__).resolve()
    candidates = (OPEN_PHRASING_REL, here.parents[3] / OPEN_PHRASING_REL)
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("open phrasing set not found (looked for data/regex/open_phrasing.jsonl)")


def load_open_phrasing(path: str | Path | None = None) -> list[dict]:
    """Load + INTEGRITY-CHECK the hand labels: each record's `expected_ir` must
    (a) validate through `from_ir`, (b) emit exactly `expected_pcre`, and
    (c) pass its own judge examples. A broken label is a loading error, not a
    silent benchmark input."""

    p = Path(path) if path is not None else default_open_phrasing_path()
    records: list[dict] = []
    for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        rec = json.loads(line)
        missing = [k for k in ("id", "description", "expected_ir", "expected_pcre", "positive", "negative") if not rec.get(k)]
        if missing:
            raise ValueError(f"open phrasing record {rec.get('id', f'line {lineno}')!r} is missing {missing}")
        node = from_ir(rec["expected_ir"])
        derived = emit(node)
        if derived != rec["expected_pcre"]:
            raise ValueError(
                f"open phrasing record {rec['id']!r}: expected_ir emits {derived!r}, "
                f"but expected_pcre is {rec['expected_pcre']!r} (stale hand label)"
            )
        verdict = judge(derived, rec["positive"], rec["negative"])
        if not verdict.ok:
            raise ValueError(
                f"open phrasing record {rec['id']!r}: the hand label fails its own judge: {verdict.summary()}"
            )
        records.append(rec)
    if not records:
        raise ValueError(f"open phrasing set {p} is empty")
    return records


def _evaluate_arm(
    kernel: LanguageKernel, rec: dict, store: CodexStore, out: dict
) -> dict:
    """Run one arm on one record; fill `out` in place. See module docstring for
    the correctness yardstick."""

    try:
        result: PipelineResult = describe(rec["description"], codex=store, kernel=kernel)
    except (ValueError, UnresolvedError) as e:
        out.update(status="parse_error", pcre=None, ok=False, byte_exact=False, note=f"{type(e).__name__}: {e}")
        return out
    pcre = result.pcre
    out["parse_score"] = result.parse_score
    if pcre is None:
        out.update(
            status="escalated",
            pcre=None,
            ok=False,
            byte_exact=False,
            candidates=(result.escalation or {}).get("candidates", []),
        )
        return out
    v = judge(pcre, rec["positive"], rec["negative"])
    out.update(
        status="ok" if v.ok else "wrong",
        pcre=pcre,
        ok=bool(v.ok),
        byte_exact=pcre == rec["expected_pcre"],
        judge=v.summary(),
    )
    return out


def run_e3_1(
    out_dir: str | Path | None = None,
    endpoint: str | None = None,
    model: str | None = None,
    timeout: float = 600.0,
) -> dict:
    """The A/B. Writes `results/phase-3/e3.1.json` (full audit record).

    `endpoint`/`model` default to the owner's .env (OLLAMA_ENDPOINT /
    OLLAMA_MODEL) and the snapshot of the running model is recorded in config.
    """

    out_dir = Path(out_dir) if out_dir is not None else default_phase_dir(3)  # results hygiene

    path = default_open_phrasing_path()
    records = load_open_phrasing(path)

    store = default_codex()  # ONE shared CODEX instance for both arms (P3.02)
    det_kernel = DeterministicKernel(store)
    backend = OllamaBackend(endpoint=endpoint, model=model, timeout=timeout)
    llm_kernel = LLMKernel(backend, fallback=det_kernel, fallback_score=0.5)

    model_info = backend.server_info()
    models_online = sorted(backend.ping())

    per_item: list[dict] = []
    for rec in records:
        item: dict = {
            "id": rec["id"],
            "description": rec["description"],
            "expected_pcre": rec["expected_pcre"],
            "deterministic": {},
            "llm": {},
        }
        _evaluate_arm(det_kernel, rec, store, item["deterministic"])
        gen_before = store.generation
        _evaluate_arm(llm_kernel, rec, store, item["llm"])
        item["llm"]["fallback_used"] = any(
            ev["text"] == rec["description"] and ev["fallback"] == "used" for ev in llm_kernel.fallback_events
        )
        item["llm"]["codex_generation_delta"] = store.generation - gen_before
        per_item.append(item)

    total = len(records)
    n_det_ok = sum(1 for i in per_item if i["deterministic"]["ok"])
    n_llm_ok = sum(1 for i in per_item if i["llm"]["ok"])
    n_det_exact = sum(1 for i in per_item if i["deterministic"].get("byte_exact"))
    n_llm_exact = sum(1 for i in per_item if i["llm"].get("byte_exact"))
    det_acc = n_det_ok / total
    llm_acc = n_llm_ok / total

    report = {
        "config": {
            "set": str(path),
            "set_hash": corpus_hash(path),
            "n_records": total,
            "backend": "ollama-native /api/chat (think=false, format=json, temperature=0)",
            "model": model_info,
            "models_online": models_online,
            "timeout_s": timeout,
            "fallback": {
                "policy": "DeterministicKernel on backend failure",
                "score": 0.5,
                "max_attempts": llm_kernel.max_attempts,
                "events": llm_kernel.fallback_events,
            },
            "codex": "ONE shared default_codex() instance across both arms (deterministic first, then LLM); growth below",
            "identical_downstream": True,
        },
        "llm_accuracy": round(llm_acc, 4),
        "deterministic_accuracy": round(det_acc, 4),
        "llm_byte_exact_rate": round(n_llm_exact / total, 4),
        "deterministic_byte_exact_rate": round(n_det_exact / total, 4),
        "n_llm_ok": n_llm_ok,
        "n_det_ok": n_det_ok,
        "passed": bool(llm_acc >= det_acc),
        "per_item": per_item,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "e3.1.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


class E3_1Experiment:
    """Registered as `e3.1` in the harness registry (P3.01–P3.02)."""

    name = "e3.1"
    hypothesis = (
        "an LLMKernel behind the same LanguageKernel interface handles open phrasing "
        "the deterministic kernel cannot, with the CODEX/reasoner identical in both arms"
    )
    metric = "judge-verified parse accuracy on the hand-labeled open-phrasing set (LLM arm vs deterministic arm)"
    threshold = "llm_accuracy >= deterministic_accuracy on open phrasing, downstream identical"

    def run(self):
        from kainos.harness.runner import Result

        # Reachability probe first: e3.1 is meaningless without the LLM server,
        # and a missing LAN server is a SKIP, never a pass or a false fail.
        try:
            backend = OllamaBackend()
            models_online = sorted(backend.ping())
        except Exception as e:  # noqa: BLE001 — reachability probe: any failure means SKIP, never a hang
            return Result(
                name=self.name,
                passed=False,
                value=0.0,
                threshold=self.threshold,
                skipped=True,
                config={"skip_reason": f"Ollama backend unreachable: {type(e).__name__}: {e}"},
            )
        if backend.model not in models_online:
            return Result(
                name=self.name,
                passed=False,
                value=0.0,
                threshold=self.threshold,
                skipped=True,
                config={
                    "skip_reason": f"model {backend.model!r} not loaded on the server "
                    f"(online: {', '.join(models_online) or 'none'})"
                },
            )

        report = run_e3_1()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=report["llm_accuracy"],
            threshold=self.threshold,
            evidence=[Path("results/phase-3/e3.1.json")],
            config={
                "deterministic_accuracy": report["deterministic_accuracy"],
                "llm_byte_exact_rate": report["llm_byte_exact_rate"],
                "n_records": report["config"]["n_records"],
                "model": report["config"]["model"]["model"],
                "fallback_events": len(report["config"]["fallback"]["events"]),
            },
        )
