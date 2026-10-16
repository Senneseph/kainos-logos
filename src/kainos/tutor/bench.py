"""E6.1 — "The attended pilot" (registry phase 6; epic #150 T2/T3/T4 core).

Question (pre-registered in plan/30-phases/phase-6-tutor/experiments.md):
can a system whose knowledge is a CODEX learn a narrow arithmetic strip
from dialogue across sessions — verified, grounded, honest, persistent?

The pilot runs the frozen 30-turn scripted teacher through the
Brainstem/InfantRuntime TWICE (run1 = evidence, run2 = byte-identity
control) and re-audits everything offline: contracts, proof chains,
absence audits, dispute accounting, provenance, determinism, and the
LLM-surface seam (MockBackend — no Ollama in the official hermetic run,
E3.1 SKIP semantics: the structured results stand on the det arm).
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState
from kainos.lang.llm import MockBackend
from kainos.projection.contract import validate_response
from kainos.tutor.brainstem import Brainstem, det_classify
from kainos.tutor.mastery import STABLE_EVIDENCE_K, Concept
from kainos.tutor.session import (
    InfantRuntime,
    codex_dump_path,
    load_store,
)

__all__ = ["CHECKS", "FROZEN", "E6_1Experiment", "run_e6_1"]

CHECKS = 8

#: The frozen pilot script (D-e6a: 30 turns = 14+6+6+4; the verbatim lists
#: are the authority). The un-attended regime (T5) replaces THIS teacher
#: with the LLM authoring arm through the same `turn` seam.
FROZEN: dict[str, Any] = {
    "k": STABLE_EVIDENCE_K,
    "turn_count": 30,
    "script": {
        1: [
            "after 0 comes 1",
            "after 1 comes 2",
            "after 2 comes 3",
            "after 3 comes 4",
            "after 4 comes 5",
            "after 5 comes 6",
            "after 6 comes 7",
            "after 7 comes 8",
            "after 8 comes 9",
            "after 9 comes 10",
            "what comes after 3?",
            "what comes after 5?",
            "what comes after 7?",
            "what comes after 9?",
        ],
        2: [
            "2 + 3 is what?",
            "4 + 2 is what?",
            "0 + 5 is what?",
            "after 2 comes 5",
            "no — that was a mistake; after 2 comes 3",
            "3 + 3 is what?",
        ],
        3: [
            "7 + 8 is what?",
            "4 + 9 is what?",
            "what comes after 40?",
            "2 + 3 is what?",
            "0 + 5 is what?",
            "blue",
        ],
        4: [
            "after 10 comes 11",
            "what comes after 10?",
            "after 3 comes 9",
            "i misspoke; after 3 comes 4",
        ],
    },
    # C2: the mastery trajectory (session-final state per concept) — frozen.
    "trajectory": {
        "count-successor": ["stable", "stable", "stable", "stable"],
        "add-within-10": ["unexposed", "stable", "stable", "stable"],
    },
    # C3: the S3 out-of-strip probes (frozen: honest needs_info, zero fabrication).
    "s3_probes": ["7 + 8 is what?", "4 + 9 is what?", "what comes after 40?"],
    # C4: the two conflict pairs (the exact assertion ids are DERIVED below and
    # frozen from the control run BEFORE the official run; the facts are frozen).
    "conflict_facts": [
        {"turn": "S02:04", "subject": "count-successor:succ-of(2)", "wrong": 5, "right": 3},
        {"turn": "S04:03", "subject": "count-successor:succ-of(3)", "wrong": 9, "right": 4},
    ],
    # C5: the persistence probes (S2-taught drills, re-asked after the restart).
    "persistence": [{"s2_turn": "S02:01", "s3_turn": "S03:04"}, {"s2_turn": "S02:03", "s3_turn": "S03:05"}],
    # C7: the frozen attention set (exactly ONE on-call event: the SECOND
    # teacher conflict episode, S4:03 — the first, S2:04, is logged but silent).
    "attention": [{"turn": "S04:03", "type": "repeated-conflict"}],
}

# ── helpers ──────────────────────────────────────────────────────────────────


def _pilot(root: Path, backend: Any = None, concepts: Any = None) -> list[dict]:
    """Run the frozen script once under `root`; returns the 4 session reports.
    The e6.1 pilot seeds its TWO pilot strips only (E6.2 seeds the full 7) so
    the e6.1 frozen derived constants stay reproducible on re-execution."""

    rt = InfantRuntime(root, backend=backend, concepts=(concepts if concepts is not None else InfantRuntime.PILOT_CONCEPTS[:2]))
    out: list[dict] = []
    for session, turns in FROZEN["script"].items():
        rt.boot(session)
        for text in turns:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _facts(codex: InMemoryCodexStore, subject: str) -> list[Assertion]:
    return codex.query(subject=subject, relation="succ")


def _parse_fact_id(aid: str) -> tuple[str, int, int]:
    """`cs-fS0204:2->5` -> ("cs-fS0204", 2, 5); `cs-cS0205:2->3` likewise."""

    head, tail = aid.rsplit(":", 1)
    a, b = tail.split("->")
    return head, int(a), int(b)


def _replay_trace(codex: InMemoryCodexStore, trace: list[str]) -> tuple[int | None, list[str]]:
    """Replay a proof chain offline: consecutive citations must chain
    (num(m_i) == succ-of(n_{i+1})), every cite established and present.
    Returns (final value or None, violations)."""

    violations: list[str] = []
    x: int | None = None
    for i, aid in enumerate(trace):
        try:
            a = codex.get(aid)
        except KeyError:
            violations.append(f"dangling cite: {aid}")
            return None, violations
        if a.status != EpistemicState.established:
            violations.append(f"non-established cite: {aid} ({a.status.value})")
            continue
        sid = _parse_fact_id(a.id)
        n, m = sid[1], sid[2]
        if x is not None and n != x:
            violations.append(f"chain break at {aid}: expected from {x}, subject is {n}")
        x = m
    return x, violations


def _seam_checks() -> dict[str, Any]:
    """C8's MockBackend seam: the LLM confirms (used), the LLM disagrees
    (deterministic fallback, recorded), and the LLM phrase falls back —
    while the grounded IR is IDENTICAL across arms (content from CODEX)."""

    texts = ["after 2 comes 3", "after 2 comes 5", "what comes after 2?"]
    concepts = (
        Concept("count-successor", "Successor on the number line", "pre-k", "arithmetic"),
        Concept("add-within-10", "Addition with sum within the number line", "k-5", "arithmetic", prereqs=("count-successor",)),
    )
    # det arm (no backend)
    codex_det = InMemoryCodexStore()
    bs_det = Brainstem(codex_det, concepts=concepts)
    bs_det._set_session(9)
    det_results = [bs_det.turn(t) for t in texts]
    # llm arm (MockBackend; per turn: classify reply, then phrase reply)
    replies = [
        '{"kind": "assertion", "slots": {"a": 2, "b": 3}}',
        "Alright! After 2 comes 3, just as I said.",
        '{"kind": "impossible", "slots": {"a": 2, "b": 5, "op": "multiply"}}',
        "That cannot be done at all.",
        '{"kind": "question", "slots": {"mode": "succ", "n": 2}}',
        "",  # empty phrase -> deterministic phrasing fallback
    ]
    codex_llm = InMemoryCodexStore()
    bs_llm = Brainstem(codex_llm, backend=MockBackend(replies), concepts=concepts)
    bs_llm._set_session(9)
    llm_results = [bs_llm.turn(t) for t in texts]

    irs_identical = all(det.response_ir == llm.response_ir for det, llm in zip(det_results, llm_results))
    c8a = (
        llm_results[0].arm.get("classifier") == "llm"
        and llm_results[0].arm.get("phrasing") == "llm"
        and llm_results[0].arm.get("phrasing_fallback") is False
        and llm_results[0].arm.get("content_from") == "codeX"
        and llm_results[0].response_ir == det_results[0].response_ir
        and llm_results[0].response_text == "Alright! After 2 comes 3, just as I said."
    )
    c8b = (
        llm_results[1].kind == "assertion"  # det kind stood, despite the LLM
        and llm_results[1].arm.get("classifier") == "det"
        and llm_results[1].arm.get("classifier_fallback") is True
        and llm_results[1].arm.get("phrasing") == "llm"
        and llm_results[1].response_ir == det_results[1].response_ir
        and llm_results[1].conflict is not None  # the disagreement still disputed, honestly
    )
    c8c = (
        llm_results[2].arm.get("classifier") == "llm"
        and llm_results[2].arm.get("phrasing") == "det"
        and llm_results[2].arm.get("phrasing_fallback") is True
        and llm_results[2].response_text == det_results[2].response_text
        and llm_results[2].response_ir == det_results[2].response_ir
    )
    return {
        "llm_used_and_identical": c8a,
        "disagreement_falls_back_recorded": c8b,
        "phrase_fallback_identical": c8c,
        "irs_identical_across_arms": irs_identical,
        "fallback_events": bs_llm.fallback_events,
        "llm_events": bs_llm.llm_events,
        "det_kinds": [det_classify(t)[0] for t in texts],
    }


# ── the pilot run + all checks ───────────────────────────────────────────────


def run_e6_1(out_dir: Path | None = None) -> dict:
    if out_dir is None:
        base = os.environ.get("KAINOS_RESULTS_DIR", "results")
        out_dir = Path(base) / "phase-6"
    out_dir.mkdir(parents=True, exist_ok=True)
    run1, run2 = out_dir / "e6.1-run1", out_dir / "e6.1-run2"
    rep1 = _pilot(run1)
    _rep2 = _pilot(run2)  # run2 exists for the byte-identity check (C7); its reports are compared as bytes
    scripts_key = "\n".join(t for session in sorted(FROZEN["script"]) for t in FROZEN["script"][session])
    script_hash = hashlib.sha256(scripts_key.encode("utf-8")).hexdigest()[:16]

    # final store (run1, S4) for the offline re-audits
    final = load_store(codex_dump_path(run1, 4))
    s3_store = load_store(codex_dump_path(run1, 3))
    turns_all = [t for r in rep1 for t in r["turns"]]
    by_turn = {t["turn"]: t for t in turns_all}

    checks: dict[str, Any] = {}

    # C1 — contract validity: every response validates (re-run offline).
    c1_bad = [
        {"turn": t["turn"], "violations": v}
        for t in turns_all
        for ok, v in [validate_response(t["response_ir"], t["kind"])]
        if not ok
    ]
    checks["c1_contract_valid"] = {
        "pass": len(c1_bad) == 0 and len(turns_all) == FROZEN["turn_count"],
        "turns_validated": len(turns_all),
        "violations": c1_bad,
    }

    # C2 — learning: trajectory + proof re-verification (0 dangling cites).
    traj_ok = True
    traj_seen: dict[str, list[str]] = {}
    for r in rep1:
        for cid, want in FROZEN["trajectory"].items():
            got = r["mastery"][cid]["state"]
            traj_seen.setdefault(cid, []).append(got)
            if got != want[r["session"] - 1]:
                traj_ok = False
    c1_viol: list[Any] = []
    proof_events = 0
    for r in rep1:
        for t in r["turns"]:
            for eid in t["events"]:
                if ":ev-" not in eid or not eid.endswith(":derivation-correct"):
                    continue
                proof_events += 1
                a = final.get(eid)
                ev = a.provenance.evidence if a.provenance is not None else []
                for cite in ev:
                    if cite.startswith("turn:"):
                        continue  # turn refs are not fact cites
                    if _finds(final, cite) is None:
                        c1_viol.append({"turn": t["turn"], "violation": f"event {eid} has a dangling cite {cite}"})
                # re-play the turn's own trace (the canonical chain) offline
                x, viol = _replay_trace(final, list(t["response_ir"].get("evidence") or []))
                if viol:
                    c1_viol.append({"turn": t["turn"], "violations": viol})
                elif not str(t["response_ir"]["answer"]).startswith("needs_info") and x != int(t["response_ir"]["answer"]):
                    c1_viol.append({"turn": t["turn"], "violation": f"replay {x} != answer {t['response_ir']['answer']}"})
    checks["c2_learning"] = {
        "pass": traj_ok and not c1_viol and proof_events >= 2 * STABLE_EVIDENCE_K,
        "trajectory": traj_seen,
        "trajectory_frozen": FROZEN["trajectory"],
        "proof_events": proof_events,
        "replay_violations": c1_viol,
    }

    # C3 — no fabrication: S3 probes needs_info + absence audits re-audited
    # against the S3 snapshot (the codeX as the probe actually saw it).
    c3_bad = []
    for i, probe in enumerate(FROZEN["s3_probes"], start=1):
        t = by_turn[f"S03:{i:02d}"]
        if t["kind"] != "question" or t["response_ir"]["uncertainty_state"] != "needs_info" or not str(
            t["response_ir"]["answer"]
        ).startswith("needs_info"):
            c3_bad.append({"probe": probe, "why": "not an honest needs_info question"})
            continue
        for audit in t["response_ir"]["evidence"]:
            if not str(audit).startswith("absence-audit:"):
                c3_bad.append({"probe": probe, "why": f"evidence is not an absence audit: {audit}"})
                continue
            # absence-audit:<subject>:no-established-at-...
            subject = str(audit).split(":no-established-at-", 1)[0].removeprefix("absence-audit:")
            est = [a for a in s3_store.query(subject=subject, relation="succ") if a.status.value == "established"]
            if est:
                c3_bad.append({"probe": probe, "why": f"absence audit false: {subject} HAS an established fact in S3"})
    checks["c3_no_fabrication"] = {
        "pass": not c3_bad,
        "s3_probe_answers": {FROZEN["s3_probes"][i]: by_turn[f"S03:{i + 1:02d}"]["response_ir"]["answer"] for i in range(3)},
        "violations": c3_bad,
    }

    # C4 — correction discipline: both dispute pairs survive (kept, closed,
    # linked); the replacements re-established; zero disputes left open.
    c4_bad = []
    pairs = []
    for cf in FROZEN["conflict_facts"]:
        subject = cf["subject"]
        rows = final.query(subject=subject, relation="succ")
        wrong = [a for a in rows if a.id.endswith(f"->{cf['wrong']}")]
        right = [a for a in rows if a.id.endswith(f"->{cf['right']}")]
        if not wrong or not right:
            c4_bad.append({"fact": cf, "why": "pair missing from final store"})
            continue
        sup = max(wrong, key=lambda a: a.id)  # the most recent wrong claimant (now closed)
        # D-e6c single claimant: exactly ONE active established claimant of the
        # replacement value (the original fact the correction vindicates).
        right_active = [
            a
            for a in right
            if a.status.value == "established" and (a.validity is None or a.validity.to is None)
        ]
        if len(right_active) != 1:
            c4_bad.append({"fact": cf, "why": f"single-claimant invariant broken: {len(right_active)} active established for the right value"})
            continue
        rep = right_active[0]
        ok = sup.status.value == "obsolete"
        ok = ok and sup.validity is not None and sup.validity.to is not None
        ok = ok and rep.id in (sup.provenance.evidence if sup.provenance else [])
        ok = ok and sup.id in (rep.provenance.evidence if rep.provenance else [])
        if not ok:
            c4_bad.append(
                {"fact": cf, "why": f"sup={sup.status.value} rep={rep.status.value} links={sup.id in (rep.provenance.evidence if rep.provenance else [])}"}
            )
        pairs.append({"fact": cf["turn"], "superseded": sup.id, "replacement": rep.id, "superseded_validity_to": sup.validity.to if sup.validity is not None else None})
    # single-current-claimant audit (D-e6c) over the WHOLE final store
    claimant_audit: dict[str, int] = {}
    for a in final.query(relation="succ"):
        if a.status.value in ("candidate", "established", "disputed") and (a.validity is None or a.validity.to is None):
            key = f"{a.subject.id}->{a.object_id}"
            claimant_audit[key] = claimant_audit.get(key, 0) + 1
    dupes = {k: v for k, v in claimant_audit.items() if v > 1}
    open_disputes = [a.id for a in final.query() if a.status.value == "disputed"]
    checks["c4_correction_discipline"] = {
        "pass": not c4_bad and not open_disputes and not dupes,
        "pairs": pairs,
        "open_disputes_at_end": open_disputes,
        "duplicate_claimants": dupes,
        "violations": c4_bad,
    }

    # C5 — persistence across the restart: S3 probes bit-equal to S2 originals,
    # and S3 booted restored over an EMPTY workspace.
    c5_pairs = []
    c5_bad = []
    r3 = rep1[2]
    if not r3["restored"] or not r3["workspace_empty_at_boot"]:
        c5_bad.append("S3 did not boot restored with an empty workspace")
    for pp in FROZEN["persistence"]:
        a, b = by_turn[pp["s2_turn"]], by_turn[pp["s3_turn"]]
        same = all(a[k] == b[k] for k in ("kind", "slots", "response_ir", "response_text", "grounded"))
        c5_pairs.append(
            {
                "s2": pp["s2_turn"],
                "s3": pp["s3_turn"],
                "answer": a["response_ir"]["answer"],
                "trace": a["response_ir"]["evidence"],
                "bit_equal": same,
            }
        )
        if not same:
            c5_bad.append(f"persistence mismatch for {pp}")
    checks["c5_persistence"] = {"pass": not c5_bad, "pairs": c5_pairs, "violations": c5_bad}

    # C6 — provenance completeness (the final store, audited offline).
    c6_bad = []
    all_a = final.query()
    for a in all_a:
        prov = a.provenance
        if prov is None or prov.source is None or not (prov.observer or ""):
            c6_bad.append(f"missing provenance: {a.id}")
            continue
        if a.status.value == "established" and not (prov.evidence or []):
            c6_bad.append(f"established without evidence: {a.id}")
        if (a.context.data or {}).get("kind") == "mastery-event" and not str(prov.source.uri).startswith("turn:"):
            c6_bad.append(f"mastery event without a turn source: {a.id}")
    unbacked = [c for t in turns_all for c in t["grounded"] if _finds(final, c) is None]
    checks["c6_provenance"] = {
        "pass": not c6_bad and not unbacked and len(all_a) > 0,
        "assertions": len(all_a),
        "violations": c6_bad,
        "unbacked_grounded": unbacked,
    }

    # C7 — determinism & hygiene: run1 vs run2 byte-identity; the frozen
    # attention set; the det arm (no fallbacks, no fabrication).
    byte_eq = True
    for session in (1, 2, 3, 4):
        for name in (f"codeX-S{session:02d}.json", f"session-S{session:02d}.json"):
            if (run1 / name).read_bytes() != (run2 / name).read_bytes():
                byte_eq = False
    att1 = [a for r in rep1 for a in r["attention"]]
    att_frozen = FROZEN["attention"]
    att_ok = len(att1) == len(att_frozen) and all(
        r.get("turn") == f.get("turn") and r.get("type") == f.get("type") for r, f in zip(att1, att_frozen)
    )
    det_arm_ok = all(
        t["arm"].get("classifier") == "det" and t["arm"].get("phrasing") == "det"
        and t["arm"].get("classifier_fallback") is False and t["arm"].get("phrasing_fallback") is False
        for t in turns_all
    )
    fabrication = [
        t["turn"]
        for t in turns_all
        if t["kind"] == "question"
        and not str(t["response_ir"]["answer"]).startswith("needs_info")
        and not t["grounded"]
    ]
    checks["c7_determinism"] = {
        "pass": byte_eq and att_ok and det_arm_ok and not fabrication,
        "byte_identical_run1_run2": byte_eq,
        "attention": att1,
        "attention_frozen": att_frozen,
        "fabrication_events": fabrication,
    }

    # C8 — the surface arm: the official run is the det arm (SKIP semantics);
    # the MockBackend seam proves the LLM path (confirm/validate/fallback).
    seam = _seam_checks()
    arm_all_det = all(
        t["arm"].get("classifier") == "det" and t["arm"].get("phrasing") == "det" and t["arm"].get("content_from") == "codeX"
        for t in turns_all
    )
    checks["c8_surface_arm"] = {
        "pass": arm_all_det and seam["llm_used_and_identical"] and seam["disagreement_falls_back_recorded"] and seam["phrase_fallback_identical"] and seam["irs_identical_across_arms"],
        "official_arm": "det (no LLM backend present; SKIP semantics — structured results stand)",
        "seam": seam,
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    # per-session shape (derived constants for the results doc)
    per_session = [
        {
            "session": r["session"],
            "turns": len(r["turns"]),
            "restored": r["restored"],
            "mastery": {k: v["state"] for k, v in r["mastery"].items()},
            "codex_total": r["codex"]["total"],
            "added": len(r["codex"]["added_this_session"]),
            "attention": [a["turn"] for a in r["attention"]],
            "workspace_entries": r["workspace"]["entries"],
        }
        for r in rep1
    ]
    derived = {"per_session": per_session, "final_assertions": len(all_a), "script_hash": script_hash}
    return {"name": "e6.1", "checks": checks, "checks_passed": passed, "checks_total": CHECKS, "frozen": FROZEN, "derived": derived}


def _finds(codex: InMemoryCodexStore, id: str) -> Assertion | None:
    try:
        return codex.get(id)
    except KeyError:
        return None


# ── house-style experiment object ────────────────────────────────────────────


class E6_1Experiment:
    """House-style experiment object (benches lazily import Result and
    write their full report themselves)."""

    name = "e6.1"
    hypothesis = (
        "A system whose knowledge is a provenance-mandatory CODEX (an 'infant') "
        "is teachable in the open-ended regime: across four attended sessions of a "
        "narrow pre-K/grade-1 arithmetic strip it (1) reaches stable mastery of "
        "both concepts with verified, replayable derivation evidence, (2) answers "
        "out-of-strip probes with the honest needs_info and ZERO fabricated "
        "values, (3) keeps every correction pair (superseded + replacement, "
        "closed and linked — never averaged), (4) survives a restart with "
        "bit-equal answers (learning is in the CODEX, not the session context), "
        "and (5) does all of it with 100% contract-valid turns and 100% "
        "provenance-complete store — deterministically, byte-identical on "
        "re-execution."
    )
    metric = "acceptance checks passed (0-8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        rep = run_e6_1()
        passed = rep["checks_passed"]
        base = os.environ.get("KAINOS_RESULTS_DIR", "results")
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=passed / CHECKS,
            evidence=[
                Path(base, "phase-6/e6.1-run1/session-S01.json"),
                Path(base, "phase-6/e6.1-run1/session-S02.json"),
                Path(base, "phase-6/e6.1-run1/session-S03.json"),
                Path(base, "phase-6/e6.1-run1/session-S04.json"),
                Path(base, "phase-6/e6.1-run1/codeX-S04.json"),
                Path(base, "phase-6/e6.1-run2/codeX-S04.json"),
            ],
            config={
                "seed": "deterministic (scripted teacher; no randomness anywhere in the pilot)",
                "dataset_hash": rep["derived"]["script_hash"],
            },
        )
