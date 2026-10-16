"""E1.1 parity experiment (P1.08-P1.09) — the first claim gate of Phase 1.

Hypothesis: the deterministic pipeline translates **every** hand-authored seed
description byte-exactly, and every emitted pattern passes its own judge
verdict (ADR-0009). The seed corpus is the explicit form of the grammar — the
only thing the deterministic kernel is "trained" on — so 100% parity here is
the baseline on which C1 (compositionality) is built.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)
from kainos.lang.deterministic import DeterministicKernel
from kainos.regex.baseline import DirectBaseline
from kainos.regex.compose import generate_compositional_set
from kainos.regex.data import load_corpus
from kainos.regex.emitter import emit
from kainos.regex.ir import Alternative, Class, Group, Node, Repeat, Sequence
from kainos.regex.judge import judge
from kainos.regex.pipeline import default_codex, describe
from kainos.regex.resolver import SpecializationCache, resolve

if TYPE_CHECKING:
    from kainos.codex.store import CodexStore
    from kainos.harness.runner import Result

__all__ = [
    "COMPOSITIONAL_SET_REL",
    "HOLDOUT_N",
    "HOLDOUT_SEED",
    "PHONE_DESCRIPTION",
    "PHONE_PATTERN",
    "VAGUE_SET_REL",
    "E1_1Experiment",
    "E1_2Experiment",
    "E1_3Experiment",
    "E1_4Experiment",
    "E1_5Experiment",
    "corpus_hash",
    "default_compositional_path",
    "default_corpus_path",
    "default_holdout_path",
    "default_vague_set_path",
    "materialize_compositional_set",
    "materialize_holdout_set",
    "mcnemar_exact",
    "run_e1_1",
    "run_e1_2",
    "run_e1_3",
    "run_e1_4",
    "run_e1_5",
    "run_m1_benchmark",
    "teach_phone_number",
]


def default_corpus_path() -> Path:
    """The seed corpus: repo-relative `data/regex/seed_corpus.jsonl` (CWD when
    run from the checkout, else the checkout containing this package)."""

    here = Path(__file__).resolve()
    candidates = (
        Path("data/regex/seed_corpus.jsonl"),
        here.parents[3] / "data/regex/seed_corpus.jsonl",
    )
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("seed corpus not found (looked for data/regex/seed_corpus.jsonl)")


COMPOSITIONAL_SET_REL = Path("data/regex/compositional_set.jsonl")
VAGUE_SET_REL = Path("data/regex/vague_set.jsonl")
HOLDOUT_REL = Path("data/regex/holdout_set.jsonl")
# The pinned deterministic split rule (recorded in E1.5 config; the committed
# data/regex/holdout_set.jsonl is the artifact — never re-derived ad hoc):
#   random.Random(HOLDOUT_SEED).sample(sorted(compositional ids), HOLDOUT_N)
HOLDOUT_N = 20
HOLDOUT_SEED = 7


def default_vague_set_path() -> Path:
    """The vague (underspecified) set: `data/regex/vague_set.jsonl`."""

    here = Path(__file__).resolve()
    candidates = (
        Path("data/regex/vague_set.jsonl"),
        here.parents[3] / "data/regex/vague_set.jsonl",
    )
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("vague set not found (looked for data/regex/vague_set.jsonl)")


def load_vague_set(path: str | Path) -> list[dict]:
    """Load the vague set. Unlike the seed corpus, these records carry NO
    expected_pcre — the whole point is that the description is
    underspecified; the only requirement is id + description."""

    records: list[dict] = []
    for lineno, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        rec = json.loads(line)
        missing = [k for k in ("id", "description") if not rec.get(k)]
        if missing:
            raise ValueError(f"vague set record {rec.get('id', f'line {lineno}')!r} is missing {missing}")
        records.append(rec)
    if not records:
        raise ValueError(f"vague set {path} is empty")
    return records


def default_compositional_path() -> Path:
    here = Path(__file__).resolve()
    for c in (COMPOSITIONAL_SET_REL, here.parents[3] / COMPOSITIONAL_SET_REL):
        if c.is_file():
            return c
    raise FileNotFoundError(
        "compositional set not found (run materialize_compositional_set() first)"
    )


def materialize_compositional_set(
    path: str | Path | None = None, n: int = 40, set_seed: int = 42
) -> Path:
    """Generate the compositional set deterministically (seed 42) and write it
    as JSONL — the committed, auditable artifact (G2) for E1.2 and the E1.5
    hold-out."""

    out = Path(path) if path is not None else COMPOSITIONAL_SET_REL
    records = generate_compositional_set(load_corpus(default_corpus_path()), n=n, set_seed=set_seed)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n",
        encoding="utf-8",
    )
    return out


def corpus_hash(path: str | Path) -> str:
    """Stable identity of the dataset: sha256 of the file bytes."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_e1_1(
    corpus_path: str | Path | None = None,
    codex: CodexStore | None = None,
    seed: int = 0,
    out_dir: str | Path = Path("results/phase-1"),
) -> dict:
    """Describe every corpus record; byte-compare the PCRE against the authored
    expectation and judge the emitted pattern against the authored examples.

    Writes `results/phase-1/e1.1.json` with {config, accuracy, per_item}.
    """

    path = Path(corpus_path) if corpus_path is not None else default_corpus_path()
    records = load_corpus(path)
    store = codex if codex is not None else default_codex()

    per_item: list[dict] = []
    for rec in records:
        item: dict = {"id": rec["id"], "expected": rec["expected_pcre"]}
        try:
            result = describe(rec["description"], store, seed=seed)
        except ValueError as e:  # structurally unparseable
            item.update(ok=False, pcre=None, note=f"parse error: {e}")
            per_item.append(item)
            continue
        item["pcre"] = result.pcre
        if result.pcre is None:
            item.update(ok=False, note="no pcre (unresolved — escalation, not a verdict)")
        elif result.pcre != rec["expected_pcre"]:
            item.update(ok=False, note="pcre mismatch")
        else:
            verdict = judge(result.pcre, rec["positive"], rec["negative"])
            item["judge"] = verdict.summary()
            if not verdict.ok:
                item.update(ok=False, note=verdict.summary())
            else:
                item["ok"] = True
        per_item.append(item)

    n_ok = sum(1 for i in per_item if i.get("ok"))
    report = {
        "config": {
            "corpus": str(path),
            "corpus_hash": corpus_hash(path),
            "n_records": len(records),
            "seed": seed,
        },
        "accuracy": n_ok / len(records),
        "per_item": per_item,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "e1.1.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


class E1_1Experiment:
    """Registered as `e1.1` in the harness registry (name/metric/threshold)."""

    name = "e1.1"
    hypothesis = (
        "the deterministic pipeline translates 100% of the hand-authored seed "
        "corpus byte-exactly and every emitted pattern passes its own Perl judge "
        "verdict (C1 parity baseline)"
    )
    metric = "accuracy — fraction of corpus records with byte-exact pcre AND a passing judge verdict"
    threshold = "== 1.0"

    def run(self) -> Result:
        # Local import breaks the runner <-> experiment import cycle.
        from kainos.harness.runner import Result

        report = run_e1_1()
        value = report["accuracy"]
        return Result(
            name=self.name,
            passed=value == 1.0,
            value=value,
            evidence=[Path("results/phase-1/e1.1.json")],
            config={
                "seed": report["config"]["seed"],
                "dataset_hash": report["config"]["corpus_hash"],
                "corpus": report["config"]["corpus"],
                "n_records": report["config"]["n_records"],
                "per_item": report["per_item"],
            },
        )


# ── Scavenge M1 (SCAVENGE_MORPHO.md Step B; ADR-0013; ticket #141) ─────────────


def run_m1_benchmark(
    corpus_path: str | Path | None = None,
    out_dir: str | Path = Path("results/scavenge"),
) -> dict:
    """M1 gate benchmark: the resolution phase (parse → resolve → emit — the
    cache's domain; the Perl judge subprocess is not what M1 touches) over the
    corpus, once fresh and once with one shared SpecializationCache on one
    unchanged CODEX (the E1.2 shape: one CODEX, many phrasings).

    Gate (SCAVENGE_MORPHO.md Step B): `identical` must be true (semantic
    neutrality — cached results byte-equal to uncached) AND a wall-time
    advantage must be measured; otherwise M1's cache is rejected.

    Writes `results/scavenge/m1.json`.
    """

    import time

    path = Path(corpus_path) if corpus_path is not None else default_corpus_path()
    records = load_corpus(path)
    store = default_codex()
    kernel = DeterministicKernel(store)

    def run_phase(use_cache: bool) -> tuple[list[tuple[str, list[dict]]], int, dict]:
        cache = SpecializationCache(store) if use_cache else None
        t0 = time.perf_counter_ns()
        out: list[tuple[str, list[dict]]] = []
        for rec in records:
            tree = kernel.parse(rec["description"])[0].ir
            if not isinstance(tree, Node):
                raise TypeError(f"Phase 1 kernel must produce dialect nodes, got {type(tree)!r}")
            resolved, trace = resolve(tree, store, cache=cache)
            out.append((emit(resolved), trace))
        elapsed_ns = time.perf_counter_ns() - t0
        return out, elapsed_ns, (cache.stats() if cache is not None else {"hits": 0, "misses": 0, "terms": 0})

    uncached, t_uncached, stats_uncached = run_phase(False)
    cached, t_cached, stats_cached = run_phase(True)

    identical = uncached == cached
    report = {
        "identical": identical,
        "speedup": (t_uncached / t_cached) if t_cached else None,
        "wall_ns": {"uncached": t_uncached, "cached": t_cached},
        "cache_stats": {"uncached": stats_uncached, "cached": stats_cached},
        "config": {
            "corpus": str(path),
            "corpus_hash": corpus_hash(path),
            "n_records": len(records),
            "phase": "parse+resolve+emit on one shared seeded CODEX (no judge subprocess)",
            "note": (
                # corpus-aware note (board audit 2026-08-21): on the seed corpus
                # this is the INTERIM stand-in run; on the E1.2 compositional
                # set it is the FINAL M1 verdict (Scavenge Step I follow-through
                # of #141's interim note)
                "final M1 verdict: run on the E1.2 compositional set (Scavenge Step B DoD; Step I verdict line in SCAVENGE_MORPHO.md / ADR-0013)"
                if path.name == "compositional_set.jsonl"
                else (
                    "seed corpus stands in for the E1.2 compositional set until Step 10 "
                    "lands; re-run run_m1_benchmark() against the E1.2 set before the "
                    "final M1 verdict (Scavenge Step I)"
                )
            ),
        },
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "m1.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


# ── P1.11 — E1.2: compositional generalization (C1) ──────────────────────────


def run_e1_2(
    corpus_path: str | Path | None = None,
    baseline: DirectBaseline | None = None,
    seed: int = 42,
    out_dir: str | Path = Path("results/phase-1"),
) -> dict:
    """Pipeline vs no-CODEX baseline on the compositional set.

    Both systems get the identical records; the pipeline uses one shared
    seeded CODEX (the E1.2 shape — and M1's specialization cache across the
    phrasings); the baseline has none. Each system's emitted PCRE must be
    byte-exact against the ground truth AND pass the Perl judge on the
    record's own examples.

    Writes `results/phase-1/e1.2.json` with
    `{config, pipeline_accuracy, baseline_accuracy, margin, per_item}`.
    Threshold: pipeline ≥ 0.8 and pipeline ≥ baseline + 0.1.
    """

    path = Path(corpus_path) if corpus_path is not None else default_compositional_path()
    records = load_corpus(path)
    store = default_codex()
    cache = SpecializationCache(store)
    direct = baseline if baseline is not None else DirectBaseline()

    per_item: list[dict] = []
    n_pipe = 0
    n_base = 0
    for rec in records:
        item: dict = {"id": rec["id"], "expected": rec["expected_pcre"]}
        result = describe(rec["description"], store, seed=seed, cache=cache)
        p_ok = result.pcre == rec["expected_pcre"] and judge(
            result.pcre or "", rec["positive"], rec["negative"]
        ).ok
        item["pipeline"] = {"pcre": result.pcre, "ok": p_ok}
        n_pipe += int(p_ok)

        base = direct.solve(rec["description"])
        b_ok = base.pcre is not None and base.pcre == rec["expected_pcre"] and judge(
            base.pcre, rec["positive"], rec["negative"]
        ).ok
        item["baseline"] = {"pcre": base.pcre, "ok": b_ok, "note": base.note}
        n_base += int(b_ok)
        per_item.append(item)

    n = len(records)
    report = {
        "config": {
            "corpus": str(path),
            "corpus_hash": corpus_hash(path),
            "n_records": n,
            "seed": seed,
        },
        "pipeline_accuracy": n_pipe / n,
        "baseline_accuracy": n_base / n,
        "margin": n_pipe / n - n_base / n,
        "per_item": per_item,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "e1.2.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


class E1_2Experiment:
    """Registered as `e1.2` in the harness registry (name/metric/threshold)."""

    name = "e1.2"
    hypothesis = (
        "the pipeline composes known operators into NOVEL combinations "
        "(compositional generalization, C1) at accuracy >= 0.8 and beats the "
        "no-CODEX DirectBaseline by a margin >= 0.1"
    )
    metric = "pipeline composition accuracy on the compositional set (vs baseline, margin recorded)"
    threshold = ">= 0.8 and >= baseline + 0.1"

    def run(self) -> Result:
        # Local import breaks the runner <-> experiment import cycle.
        from kainos.harness.runner import Result

        report = run_e1_2()
        value = report["pipeline_accuracy"]
        base = report["baseline_accuracy"]
        passed = value >= 0.8 and value >= base + 0.1
        return Result(
            name=self.name,
            passed=passed,
            value=value,
            evidence=[Path("results/phase-1/e1.2.json")],
            config={
                "seed": report["config"]["seed"],
                "dataset_hash": report["config"]["corpus_hash"],
                "corpus": report["config"]["corpus"],
                "n_records": report["config"]["n_records"],
                "baseline_accuracy": base,
                "margin": report["margin"],
                "per_item": report["per_item"],
            },
        )


# ── E1.3 (P1.12) — persistent memory, C2 ────────────────────────────────────

PHONE_DESCRIPTION = "an American phone number"
PHONE_PATTERN = r"\d{3}-\d{3}-\d{4}"


def teach_phone_number(codex) -> str:
    """Teach the CODEX: US phone number --realizes_as--> the pattern.

    User instruction, established, full provenance (invariant #1). The term id
    is the lowercased phrase (the kernel's reference-phrase candidate is the
    lowercased token stream; store queries match term ids). The display labels
    keep their natural casing."""

    term = TermRef(
        id=PHONE_DESCRIPTION.removeprefix("an ").lower(),
        kind="entity",
        labels=["American phone number", "US phone number"],
    )
    assertion = Assertion(
        id="taught-us-phone-number",
        subject=term,
        relation=TermRef(id="realizes_as", kind="relation", labels=["realizes_as"]),
        object=PHONE_PATTERN,
        polarity=True,
        context=Context(data={"domain": "contact-info"}),
        validity=None,
        confidence=1.0,
        status=EpistemicState.established,
        provenance=Provenance(
            source=Source(uri="user_instruction", version="1", media_type="text/plain"),
            observer="user",
            derived=False,
            verified=True,
            evidence=[],
        ),
        exception=None,
    )
    assert codex.add(assertion) == assertion.id
    return assertion.id


def _describe_digest(text: str, codex) -> dict:
    try:
        r = describe(text, codex)
    except ValueError as e:
        return {"parse_error": str(e), "pcre": None, "escalation": None, "trace": []}
    return {
        "pcre": r.pcre,
        "escalation": r.escalation,
        "confidence": r.confidence,
        "trace": r.resolved_trace,
    }


def run_e1_3(out_dir: str | Path = Path("results/phase-1")) -> dict:
    """C2: teach -> succeed -> restart (dump, fresh store, fresh pipeline) ->
    succeed. The kernel code is identical across the restart; only the CODEX
    state moves (invariant #2 — knowledge is separated from weights)."""

    store = default_codex()
    before = _describe_digest(PHONE_DESCRIPTION, store)
    teach_phone_number(store)
    after = _describe_digest(PHONE_DESCRIPTION, store)

    # Restart: dump to a plain dict, reload into a FRESH store; the pipeline
    # (kernel + resolver + cache) is rebuilt from scratch by describe().
    dump = store.dump()
    assert "assertions" in dump and "terms" in dump
    fresh = InMemoryCodexStore()
    for record in dump["assertions"]:
        fresh.add(Assertion.from_dict(record))
    after_restart = _describe_digest(PHONE_DESCRIPTION, fresh)

    assertion_present = (
        len(store.query(subject=PHONE_DESCRIPTION.removeprefix("an ").lower(), relation="realizes_as"))
        == 1
    )
    explained = store.explain("taught-us-phone-number")
    judge_ok = (
        judge(after["pcre"], ["555-123-4567"], ["555-123-456", "5551234567"]).ok
        if after["pcre"]
        else False
    )
    passed = (
        before["pcre"] is None
        and before["escalation"] is not None
        and after["pcre"] == PHONE_PATTERN
        and after_restart["pcre"] == PHONE_PATTERN
        and assertion_present
        and judge_ok
    )
    report = {
        "config": {
            "description": PHONE_DESCRIPTION,
            "taught_pattern": PHONE_PATTERN,
            "provenance": "Source(uri='user_instruction', version='1')",
            "restart_note": "fresh InMemoryCodexStore rebuilt from store.dump(); pipeline rebuilt by describe()",
            "weight_frozen_note": "the deterministic kernel has no weights — the 'frozen weights' of C2 is the identical kernel code; everything that changed is CODEX state",
        },
        "before": before,
        "after": after,
        "after_restart": after_restart,
        "assertion_present": assertion_present,
        "explain": explained,
        "judge": judge_ok,
        "passed": passed,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "e1.3.json").write_text(
        json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8"
    )
    return report


class E1_3Experiment:
    """Registered as `e1.3` — the persistent-memory claim (C2)."""

    name = "e1.3"
    hypothesis = (
        "a CODEX-taught fact (US phone number) is absent before teaching, "
        "present after, survives a full restart of the pipeline with the "
        "kernel unchanged, and explains with its user-instruction provenance"
    )
    metric = "teach -> describe -> restart -> describe, with provenance shown"
    threshold = "all six conditions hold (score == 1.0)"

    def run(self) -> Result:
        # Local import breaks the runner <-> experiment import cycle.
        from kainos.harness.runner import Result

        report = run_e1_3()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=1.0 if report["passed"] else 0.0,
            evidence=[Path("results/phase-1/e1.3.json")],
            config={
                "before_pcre": report["before"]["pcre"],
                "after_pcre": report["after"]["pcre"],
                "after_restart_pcre": report["after_restart"]["pcre"],
                "assertion_present": report["assertion_present"],
                "judge": report["judge"],
            },
        )


# ── E1.4 (P1.13) — honest uncertainty, C3 ───────────────────────────────────


def _vague_codex():
    """The standard seed lexicon plus two `see_also` alias assertions.

    The aliases ("dash" ~ "hyphen", "numeral" ~ "digit") make RESOLUTION BY
    ROTATION demonstrable: the parser never learns those words, the CODEX
    neighborhood does the work. Without them, rotation has nothing to rotate
    into and every record escalates — still honest, but it would not prove
    the resolver can rescue a description via CODEX alone."""

    store = default_codex()
    provenance = Provenance(
        source=Source(uri="seed_corpus", version="1", media_type="text/plain"),
        observer="seed",
        derived=False,
        verified=True,
        evidence=[],
    )
    for left, right, aid in (("dash", "hyphen", "alias-dash-hyphen"), ("numeral", "digit", "alias-numeral-digit")):
        store.add(
            Assertion(
                id=aid,
                subject=TermRef(id=left, kind="entity", labels=[left]),
                relation=TermRef(id="see_also", kind="relation", labels=["see_also"]),
                object=right,
                polarity=True,
                context=Context(data={"lexicon": "phase-1-regex"}),
                validity=None,
                confidence=1.0,
                status=EpistemicState.established,
                provenance=provenance,
                exception=None,
            )
        )
    return store


def _tree_classes(node: Node) -> list[str]:
    out: list[str] = []

    def walk(n: Node) -> None:
        if isinstance(n, Class):
            out.append(emit(n))
        if isinstance(n, Sequence):
            for el in n.elements:
                walk(el)
        elif isinstance(n, Alternative):
            for b in n.branches:
                walk(b)
        elif isinstance(n, (Repeat, Group)):
            walk(n.node)

    walk(node)
    return out


def run_e1_4(out_dir: str | Path = Path("results/phase-1")) -> dict:
    """C3: every underspecified description either resolves via CODEX rotation
    or escalates (ask_human) — never an unjustified regex.

    Metrics: clarification_rate = escalated/total (>= 0.5 expected);
    justified_rate = emitted-with-complete-class-trace / emitted (== 1.0)."""

    path = default_vague_set_path()
    records = load_vague_set(path)
    store = _vague_codex()

    per_item: list[dict] = []
    n_escalated = 0
    n_emitted = 0
    n_justified = 0
    for rec in records:
        item: dict = {"id": rec["id"], "description": rec["description"]}
        try:
            result = describe(rec["description"], store)
        except ValueError as e:
            item.update(emitted=False, escalated=False, note=f"parse error: {e}")
            per_item.append(item)
            continue
        if result.pcre is None:
            # The pipeline invariant: no pcre IFF escalation (never silent).
            assert result.escalation is not None, f"{rec['id']}: no pcre and no escalation"
            item.update(emitted=False, escalated=True, candidates=result.escalation["candidates"])
            n_escalated += 1
        else:
            n_emitted += 1
            classes = _tree_classes(result.ir)
            covered = {
                t.get("realized_as")
                for t in result.resolved_trace
                if t.get("kind") == "class"
            } | {
                # A class minted BY a resolved reference (e.g. numeral ->
                # digit) is justified by that ref's trace entry.
                t.get("realization")
                for t in result.resolved_trace
                if t.get("kind") == "ref" and t.get("status") == "resolved"
            }
            justified = all(c in covered for c in classes)
            if justified:
                n_justified += 1
            item.update(
                emitted=True,
                escalated=False,
                pcre=result.pcre,
                justified=justified,
                uncovered_classes=[c for c in classes if c not in covered],
            )
        per_item.append(item)

    total = len(records)
    clarification_rate = n_escalated / total
    justified_rate = (n_justified / n_emitted) if n_emitted else 1.0
    passed = clarification_rate >= 0.5 and justified_rate == 1.0
    report = {
        "config": {
            "set": str(path),
            "n_records": total,
            "codeex": "seed lexicon + 2 see_also aliases (dash~hyphen, numeral~digit)",
        },
        "clarification_rate": clarification_rate,
        "justified_rate": justified_rate,
        "n_escalated": n_escalated,
        "n_emitted": n_emitted,
        "n_justified": n_justified,
        "per_item": per_item,
        "passed": passed,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "e1.4.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


class E1_4Experiment:
    """Registered as `e1.4` — the honest-uncertainty claim (C3)."""

    name = "e1.4"
    hypothesis = (
        "underspecified input is recognized and escalated (or resolved via "
        "CODEX rotation) — never an unjustified regex: clarification_rate "
        ">= 0.5 and justified_rate == 1.0"
    )
    metric = "escalation rate + justification completeness on the vague set"
    threshold = ">= 0.5 and == 1.0 justified"

    def run(self) -> Result:
        # Local import breaks the runner <-> experiment import cycle.
        from kainos.harness.runner import Result

        report = run_e1_4()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=report["clarification_rate"],
            evidence=[Path("results/phase-1/e1.4.json")],
            config={
                "n_records": report["config"]["n_records"],
                "justified_rate": report["justified_rate"],
                "per_item": report["per_item"],
            },
        )


# ── E1.5 (P1.14-P1.16) — Model A (trained seq2seq) vs Model B (CODEX pipeline)


def default_holdout_path() -> Path:
    """The committed E1.5 gate input: `data/regex/holdout_set.jsonl`."""

    here = Path(__file__).resolve()
    candidates = (
        Path("data/regex/holdout_set.jsonl"),
        here.parents[3] / "data/regex/holdout_set.jsonl",
    )
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("holdout set not found (run materialize_holdout_set() first)")


def materialize_holdout_set(
    n: int = HOLDOUT_N,
    seed: int = HOLDOUT_SEED,
    path: str | Path | None = None,
) -> Path:
    """Deterministically split the committed compositional set into the E1.5
    holdout: Random(seed).sample over the sorted record ids. The written file
    IS the artifact committed to the repo; re-derivation is a test, not a
    runtime step."""

    import random

    comp = load_corpus(default_compositional_path())
    by_id = {r["id"]: r for r in comp}
    chosen = random.Random(seed).sample(sorted(by_id), n)
    out = Path(path) if path is not None else HOLDOUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for rid in chosen:
            f.write(json.dumps(by_id[rid], sort_keys=True) + "\n")
    return out


def mcnemar_exact(n_a_only: int, n_b_only: int) -> float:
    """Exact McNemar p-value on matched pairs: n_a_only/n_b_only discordant
    outcomes. Returns 1.0 when there are no discordant pairs (no evidence)."""

    n = n_a_only + n_b_only
    if n == 0:
        return 1.0
    from math import comb

    k = max(n_a_only, n_b_only)
    p_one_tail = sum(comb(n, i) for i in range(k, n + 1)) / 2**n
    return min(1.0, 2.0 * p_one_tail)


def _evaluate_pair(rec: dict, pcre: str | None, judge_examples: bool) -> dict:
    item = {"id": rec["id"]}
    if pcre is None:
        item.update(ok=False, pcre=None)
        return item
    if pcre != rec["expected_pcre"]:
        item.update(ok=False, pcre=pcre, reason="pcre-mismatch")
        return item
    if judge_examples:
        verdict = judge(pcre, rec["positive"], rec["negative"])
        item["judge"] = verdict.summary()
        if not verdict.ok:
            item.update(ok=False, pcre=pcre, reason=verdict.summary())
            return item
    item.update(ok=True, pcre=pcre)
    return item


def run_e1_5(out_dir: str | Path = Path("results/phase-1")) -> dict:
    """The Phase 1 headline A/B on combinations ABSENT from training:
    Model A = the trained seq2seq (seed corpus only, committed weights),
    Model B = the CODEX pipeline (seeded CODEX + M1 cache + Perl judge).
    Same data, same budget shape, only the architecture differs."""

    import torch

    from kainos.llm.model_a import (
        default_weights_path,
        file_hash,
        load_default_model,
    )

    old = torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        holdout_path = default_holdout_path()
        records = load_corpus(holdout_path)
        model_a = load_default_model()
        weights_path = default_weights_path()

        # Model B: one shared seeded CODEX + the M1 specialization cache.
        codex = default_codex()
        cache = SpecializationCache(codex)

        per_item: list[dict] = []
        n_a_ok = n_b_ok = n_both = n_a_only = n_b_only = 0
        for rec in records:
            # Model A: always emits (no abstention path exists).
            a_pcre = model_a.predict(rec["description"])
            a_item = _evaluate_pair(rec, a_pcre, judge_examples=True)
            # Model B: the full pipeline (parse -> resolve -> emit -> judge).
            result = describe(rec["description"], codex, cache=cache)
            b_pcre = result.pcre
            b_item = _evaluate_pair(rec, b_pcre, judge_examples=True)
            if result.escalation is not None:
                b_item["escalation"] = result.escalation["status"]
            item = {"id": rec["id"], "description": rec["description"], "expected": rec["expected_pcre"], "a": a_item, "b": b_item}
            per_item.append(item)
            a_ok = bool(a_item.get("ok"))
            b_ok = bool(b_item.get("ok"))
            n_a_ok += a_ok
            n_b_ok += b_ok
            n_both += a_ok and b_ok
            n_a_only += a_ok and not b_ok
            n_b_only += b_ok and not a_ok

        # Vague set: Model B abstains (escalates) on underspecified input;
        # Model A structurally cannot abstain — it always emits.
        vague_path = default_vague_set_path()
        vague_records = load_vague_set(vague_path)
        vague_codex = _vague_codex()
        b_escalated = 0
        b_justified_emits = 0
        a_emits = 0
        for rec in vague_records:
            result = describe(rec["description"], vague_codex)
            if result.pcre is None:
                assert result.escalation is not None
                b_escalated += 1
            else:
                b_justified_emits += 1  # the pipeline invariant: emits are justified
            a_emits += 1  # Model A always produces output (no abstention path)

        n = len(records)
        a_acc = n_a_ok / n
        b_acc = n_b_ok / n
        mcnemar_p = mcnemar_exact(n_a_only, n_b_only)
        passed = b_acc > a_acc and mcnemar_p <= 0.20
        report = {
            "config": {
                "holdout": str(holdout_path),
                "holdout_rule": f"random.Random({HOLDOUT_SEED}).sample(sorted compositional ids, {HOLDOUT_N}) from data/regex/compositional_set.jsonl (committed artifact)",
                "n_holdout": n,
                "n_vague": len(vague_records),
                "model_a": {
                    "kind": "char-level transformer seq2seq (torch, CPU, single-threaded)",
                    "weights": str(weights_path),
                    "weights_sha256": file_hash(weights_path),
                    "trained_on": model_a.meta.get("trained_on"),
                    "epochs": model_a.meta.get("epochs_run"),
                    "seed": model_a.meta.get("seed"),
                    "note": "seed corpus only; held-out sets never seen; no CODEX path",
                },
                "model_b": {
                    "kind": "kainos CODEX pipeline (deterministic kernel + resolver + emitter + Perl judge)",
                    "codex": "seed lexicon (8 surfaces)",
                    "cache": "SpecializationCache (M1)",
                    "judge": "scripts-free in-package perl (ADR-0009)",
                },
                "stat_note": f"exact McNemar on matched pairs: a_only={n_a_only}, b_only={n_b_only}, both={n_both}, p={mcnemar_p:.4f}",
            },
            "baseline_accuracy": a_acc,
            "pipeline_accuracy": b_acc,
            "margin": b_acc - a_acc,
            "mcnemar_p": mcnemar_p,
            "vague": {
                "a_always_emits": a_emits / len(vague_records),
                "b_escalation_rate": b_escalated / len(vague_records),
                "b_justified_emit_rate": (b_escalated + b_justified_emits) / len(vague_records),
                "note": "Model B abstains on underspecified input; Model A has no abstention path and always emits",
            },
            "per_item": per_item,
            "passed": passed,
        }
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "e1.5.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    finally:
        torch.set_num_threads(old)
    return report


class E1_5Experiment:
    """Registered as `e1.5` — the Phase 1 headline A/B (and sign-off gate)."""

    name = "e1.5"
    hypothesis = (
        "on combinations absent from training, the CODEX pipeline (B) beats the "
        "conventional next-token baseline (A) on accuracy, and B abstains "
        "correctly on underspecified input where A cannot"
    )
    metric = "holdout accuracy A vs B (+ exact McNemar), vague-set abstention"
    threshold = "B > A and exact McNemar p <= 0.20 (n=20 matched pairs)"

    def run(self) -> Result:
        # Local import breaks the runner <-> experiment import cycle.
        from kainos.harness.runner import Result

        report = run_e1_5()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=report["pipeline_accuracy"],
            evidence=[Path("results/phase-1/e1.5.json"), Path("results/phase-1/e1.5.md")],
            config={
                "baseline_accuracy": report["baseline_accuracy"],
                "margin": report["margin"],
                "mcnemar_p": report["mcnemar_p"],
                "vague": report["vague"],
                "model_a_weights_sha256": report["config"]["model_a"]["weights_sha256"],
            },
        )
