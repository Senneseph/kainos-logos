"""E3.3 — the distributed-CODEX contradiction demo (P3.08, experiments.md).

Narrative (the Phase 2 bear story, distributed):

- **Node A** (winter arctic observation) consolidates two games into the
  established assertion ``polar_bear --has_property--> hibernates=yes``
  (the Phase 2 learning path, :func:`kainos.q20.learn.consolidate`) and
  stamps it with its own observation context ``{"time": "winter"}``.
- **Node B** (summer) consolidates the same probe as ``hibernates=no``
  under ``{"time": "summer"}``.
- The nodes **exchange deltas** (``AssertionDelta`` over the JSON contract)
  in both directions; **merge** idempotently flags both sides ``disputed``
  with cross-linked evidence — nobody's side disappears, nothing is averaged.
- **Reconcile** on each node discovers the missing dimension (``time``),
  creates the new context TERM ``ctx:time:polar_bear`` (declared as
  knowledge), re-expresses every side under its context and re-establishes
  them — independently, from identical post-merge evidence (Principle 4:
  convergence, not consensus).

Threshold (pre-registered, verbatim): new context TERM >= 1; both
conflicting assertions retained ``established`` under distinct contexts;
disputed count 0 for the pair; plus Principle-4 convergence: the two nodes
hold **identical** assertion sets (value, status, context) afterwards.
No averaging: no third (blended) value may exist.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Context, EpistemicState
from kainos.exchange.protocol import AssertionDelta, merge
from kainos.exchange.reconciler import reconcile
from kainos.harness.paths import default_results_dir
from kainos.q20.learn import consolidate

__all__ = ["E3_3Experiment", "run_e3_3", "write_report"]

SUBJECT = "polar_bear"
RELP = "has_property"
WINTER = "node_arctic_winter"
SUMMER = "node_arctic_summer"
SEASON = {WINTER: "winter", SUMMER: "summer"}
VALUE = {WINTER: "yes", SUMMER: "no"}
# Deterministic exchange timestamps (fixed, like seeds): the transport would
# stamp wall-clock time; the demo pins them so the report is reproducible.
DELTA_TS = {WINTER: "2026-08-21T00:00:00+00:00", SUMMER: "2026-08-21T00:01:00+00:00"}


def _learn_node(node: str) -> InMemoryCodexStore:
    """One node's local learning: two corroborating games -> established,
    annotated with the node's observation context (Phase 2 path)."""

    store = InMemoryCodexStore()
    hiber_q = {"id": "q_hibernates", "surface": "Does it hibernate?", "kind": "property_probe", "property": "hibernates"}
    value = VALUE[node]
    for g in ("g1", "g2"):
        consolidate(
            SUBJECT,
            [{"question": "q_hibernates", "answer": value}],
            store,
            game_id=f"{node}_{g}",
            extra_questions={hiber_q["id"]: hiber_q},
        )
    for a in store.query():  # stamp the node's own observation context
        store.add(dataclasses.replace(a, context=Context(data={"time": SEASON[node]})))
    return store


def _export(node: str, store: InMemoryCodexStore) -> list[AssertionDelta]:
    return [AssertionDelta(assertion=a, node_id=node, timestamp=DELTA_TS[node]) for a in store.query()]


def _fact_fingerprint(store: InMemoryCodexStore) -> list[dict[str, Any]]:
    """The node's knowledge about the pair + the context declaration,
    canonical (sorted) — compared across nodes for Principle-4 convergence."""

    out = []
    for a in store.query():
        if a.relation.id == RELP or a.relation.id == "declares_context":
            out.append(
                {
                    "id": a.id,
                    "value": a.object if isinstance(a.object, str) else a.object.id,
                    "polarity": a.polarity,
                    "status": a.status.value,
                    "context": {k: a.context.data[k] for k in sorted(a.context.data)},
                }
            )
    return sorted(out, key=lambda r: (r["id"], r["value"]))


def run_e3_3(out_dir: Path | None = None) -> dict:
    """Run the full two-node exchange + reconciliation; return the report."""

    out_dir = out_dir if out_dir is not None else default_results_dir()  # results hygiene

    nodes = {node: _learn_node(node) for node in (WINTER, SUMMER)}

    # pre-exchange sanity: each node holds its side, established
    pre = {
        node: [
            {"id": a.id, "value": a.object if isinstance(a.object, str) else a.object.id, "status": a.status.value}
            for a in store.query()
        ]
        for node, store in nodes.items()
    }

    # ── exchange (both directions) + merge ────────────────────────────
    merge_reports = {}
    merge_reports[SUMMER] = merge(nodes[SUMMER], _export(WINTER, nodes[WINTER]))
    merge_reports[WINTER] = merge(nodes[WINTER], _export(SUMMER, nodes[SUMMER]))
    # idempotency evidence: re-merge the same deltas — everything must be a dup
    re_merge = {
        SUMMER: merge(nodes[SUMMER], _export(WINTER, nodes[WINTER])),
        WINTER: merge(nodes[WINTER], _export(SUMMER, nodes[SUMMER])),
    }
    idempotent = all(re_merge[n].merged == [] for n in nodes)

    # ── reconcile (independently, on both nodes) ──────────────────────
    recs = {node: reconcile(nodes[node], SUBJECT, RELP) for node in nodes}

    # ── thresholds ────────────────────────────────────────────────────
    verdict = {}
    new_terms = {
        node: [t for t in store.dump()["terms"] if t.get("kind") == "context"] for node, store in nodes.items()
    }
    verdict["new_context_term_ge_1"] = all(len(t) >= 1 for t in new_terms.values())

    retained_ok = True
    per_node_facts = {}
    for node, store in nodes.items():
        facts = [a for a in store.query() if a.relation.id == RELP]
        per_node_facts[node] = sorted(
            (a.object if isinstance(a.object, str) else a.object.id) for a in facts
        )
        values = {a.object for a in facts if isinstance(a.object, str)}
        established_by_value = {
            v: all(f.status == EpistemicState.established for f in facts if isinstance(f.object, str) and f.object == v)
            for v in values
        }
        retained_ok &= values == {"hibernates=yes", "hibernates=no"} and all(established_by_value.values())
    verdict["both_values_retained_established"] = retained_ok

    contexts = {
        node: {json.dumps(a.context.data, sort_keys=True) for a in store.query() if a.relation.id == RELP}
        for node, store in nodes.items()
    }
    verdict["distinct_contexts_ge_2"] = all(len(c) >= 2 for c in contexts.values())

    disputed = {
        node: len([a for a in store.query() if a.relation.id == RELP and a.status == EpistemicState.disputed])
        for node, store in nodes.items()
    }
    verdict["disputed_count_zero"] = all(v == 0 for v in disputed.values())

    # no averaging: exactly the two original values exist — never a third
    all_values = set().union(*[set(per_node_facts[n]) for n in nodes])
    verdict["no_averaging"] = all_values == {"hibernates=yes", "hibernates=no"}

    # Principle 4: the nodes converge on IDENTICAL knowledge (not consensus)
    verdict["converged_identical_knowledge"] = _fact_fingerprint(nodes[WINTER]) == _fact_fingerprint(nodes[SUMMER])

    passed = all(verdict.values()) and idempotent

    report = {
        "name": "e3.3",
        "passed": passed,
        "idempotent_remerge": idempotent,
        "new_terms": len({t["id"] for node_ts in new_terms.values() for t in node_ts}),  # distinct term ids across nodes
        "per_node": {
            node: {
                "assertions": [_slim(a.to_dict()) for a in store.query()],
                "merge_report": merge_reports[node].to_dict(),
                "reconciliation": recs[node].to_dict(),
                "new_context_terms": [t["id"] for t in new_terms[node]],
                "disputed": disputed[node],
            }
            for node, store in nodes.items()
        },
        "pre_exchange": pre,
        "evidence": {
            "context_terms": {n: [t["id"] for t in ts] for n, ts in new_terms.items()},
            "fingerprints_identical": verdict["converged_identical_knowledge"],
        },
        "threshold": verdict,
        "config": {
            "narrative": "winter 'hibernates=yes' vs summer 'hibernates=no' — the E2.5 bear story with two stores instead of one",
            "candidate_dimensions": ["time", "location", "role", "modality", "context"],
            "thresholds": "new context TERM >= 1; both conflicting assertions retained established under distinct contexts; disputed count 0 for the pair; converged identical knowledge; zero averaged/blended facts",
        },
    }
    if out_dir is not None:
        write_report(out_dir, report)
    return report


def _slim(d: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": d["id"],
        "subject": d["subject"]["id"],
        "relation": d["relation"]["id"],
        "object": d["object"] if isinstance(d["object"], str) else d["object"]["id"],
        "polarity": d["polarity"],
        "status": d["status"],
        "context": d["context"],  # serialized Context = flat data dict

        "exception": d.get("exception"),
        "observer": d["provenance"]["observer"],
        "source_uri": d["provenance"]["source"]["uri"] if d.get("provenance") and d["provenance"].get("source") else None,
    }


def write_report(results_dir: Path | str | None, report: dict) -> Path:
    """Write the full report to results/e3.3.json (flat) AND
    results/phase-3/e3.3.json (the canonical location); the harness then
    overwrites the flat file with its own Result record, exactly like
    E3.2/E3.5 (their run_e3_x default is also the flat root)."""

    if results_dir is None:
        raise ValueError("results_dir is required")
    base = Path(results_dir)
    flat = base / "e3.3.json"
    flat.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    phase_dir = base / "phase-3"
    phase_dir.mkdir(parents=True, exist_ok=True)
    phase = phase_dir / "e3.3.json"
    phase.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    md = [
        "# E3.3 — Distributed-CODEX contradiction (two-node exchange + reconciliation)",
        "",
        f"Result: {report['passed']}",
        "",
        "| check | outcome |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in report["threshold"].items()],
        f"| idempotent re-merge | {report['idempotent_remerge']} |",
        "",
        f"New context terms: {report['evidence']['context_terms']}",
        "",
        "Narrative: see `plan/30-phases/phase-3-generalization/results.md`.",
        "",
    ]
    (base / "e3.3.md").write_text("\n".join(md))
    return phase


class E3_3Experiment:
    name = "e3.3"
    hypothesis = "a contradiction between two nodes becomes a new context TERM — never a blended fact"
    metric = (
        "new context TERM >= 1; both conflicting assertions retained established under distinct "
        "contexts; disputed -> 0; nodes converged on identical knowledge; zero averaged/blended facts"
    )
    threshold = (
        ">= 1 new context TERM, both conflicting assertions retained as established under "
        "distinct contexts, disputed -> 0, nodes converged, zero averaged/blended facts"
    )

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e3_3()
        verdict: dict[str, bool] = report["threshold"]
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=float(report["new_terms"]),
            evidence=[Path("results/phase-3/e3.3.json")],
            config={
                "new_context_terms": sorted({t for ts in report["evidence"]["context_terms"].values() for t in ts}),
                "disputed_after": {n: r["disputed"] for n, r in report["per_node"].items()},
                "checks": {k: bool(v) for k, v in verdict.items()},
                "idempotent_remerge": bool(report["idempotent_remerge"]),
                "converged": bool(verdict["converged_identical_knowledge"]),
            },
        )
