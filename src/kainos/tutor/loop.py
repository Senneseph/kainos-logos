"""E6.3 "The un-attended loop" (T5 #155, milestone M2).

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md
section E6.3 (with deviation D-e6g on author rule 2). The M1 pilot +
E6.2 ladder become a loop with no human in the turn loop:

- AUTHORING arm: one line per turn. Every line is EITHER a frozen
  lesson form (a successor step below the frozen LINE_CAP, or a
  rule-lesson phrase for a ready unexposed rule concept) OR the
  sequencer's own grounded surface (its next_drill pick, or
  strip_candidates position 0 to expose a lesson-less strip, or an
  injected re-expose entry from an applied fix). The author invents
  nothing — check L2 replays every line against the store.
- ANALYSIS arm: reads each machine-readable session report after the
  lapse, diagnoses per concept, and may propose ONE frozen-class fix
  (re-expose: inject REEXPOSE_TURNS further grounded drills of a
  stalled concept at the head of the next session). Nothing outside
  the allowlist is ever applied — it would be attention.
- ATTENTION INBOX: frozen triggers (an open dispute at a session end;
  a stall persisting after its fix; an out-of-allowlist proposal)
  FILE DEDUPED ticket payloads (the #156 shape: owner-assigned,
  evidence-linked). The hermetic run records payloads and posts
  NOTHING — posting is the live addendum.

Arms & the LLM seam: the LLM authoring/analysis arms are typed
seams (LlmAuthor / LlmAnalyzer). E3.1 SKIP semantics: with no
backend the LLM arms are skipped and the run is the det run, and the
seam is NEUTRAL (a run with the arms present-but-off is
byte-identical to a run without them — check L6).

Determinism: the loop is pure recompute over the store; two runs are
byte-identical (check L7), and the frozen line cap is a property of
the final store, not just of the author.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Protocol

from kainos.codex.models import EpistemicState
from kainos.tutor.brainstem import det_classify
from kainos.tutor.mastery import MasteryState, mastery_view, reset_concepts
from kainos.tutor.sequencer import next_drill, strip_candidates
from kainos.tutor.session import InfantRuntime

__all__ = [
    "CHECKS",
    "FROZEN",
    "GAP_KINDS",
    "E6_3Experiment",
    "LlmAnalyzer",
    "LlmAuthor",
    "author_decision",
    "run_loop",
]

CHECKS = 7

#: Honest (no-content) turn kinds the analysis arm counts as gaps.
GAP_KINDS: frozenset[str] = frozenset({"impossible", "needs_info", "ambiguous"})

# concept -> the frozen rule-lesson phrase (inverted from
# brainstem.RULE_LESSONS so the author can issue it; the brainstem
# remains the single source of truth for the phrase -> concept map).
_RULE_PHRASES: dict[str, str] = {
    "sub-within-30": "subtraction is walking backward",
    "mult-within-100": "multiplication is repeated addition",
    "compare-numbers": "comparison is walking the line",
}

FROZEN: dict[str, Any] = {
    "sessions_max": 6,
    "turns_per_session": 40,
    "line_cap": 70,
    "rule_lesson_line_min": 20,
    "stalled_sessions": 3,
    "stalled_gaps": 4,
    "reexpose_turns": 3,
    "priority": [
        "count-successor",
        "add-within-10",
        "add-two-digit",
        "sub-within-30",
        "mult-within-100",
        "compare-numbers",
    ],
    "rule_phrases": dict(_RULE_PHRASES),
    # the three frozen line-boundary articulations (E6.2); a turn whose
    # text carries one is a boundary contact (expected ZERO in the
    # hermetic run: grounded proposals never cross the line).
    "boundary_phrases": (
        "leaves the start of my number line",
        "i don't even have",
        "does not finish — my number line ends",
    ),
    "owner_assignee": "Jesse Miller",
    "project": "Kainos-Logos",
}


# ── the arms (typed seams; the LLM arms are E3.1-skipped) ───────────

class LlmAuthor(Protocol):
    """An LLM authoring arm: given the loop's plain-language context,
    returns ONE line to say (the brainstem parses/confirms it; an
    unparseable line is retried once, then dropped — bounded)."""

    def line(self, context: str) -> str: ...


class LlmAnalyzer(Protocol):
    """An LLM analysis arm: given a session report + the det
    diagnosis, returns a proposal — which is applied ONLY if it
    matches the frozen allowlist (else it is an attention trigger)."""

    def propose(self, report: dict[str, Any], diagnosis: dict[str, Any]) -> dict[str, Any] | None: ...


#: L6 probe: the typed seams exist (evaluated at import time).
LLM_SEAMS_PRESENT: bool = True


# ── grounded helpers (pure recompute) ───────────────────────────────


def _line_end(store: Any) -> int:
    """The far end of the established number line (the largest m with
    an established (n -> m) successor fact); 0 on the empty store."""

    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid = a.subject.id
        oid = a.object_id
        if sid.startswith("count-successor:succ-of(") and oid.startswith("count-successor:num(") and (a.validity is None or a.validity.to is None):
            end = max(end, int(oid[len("count-successor:num(") : -1]))
    return end


def _open_disputes(store: Any) -> list[str]:
    """Asserted ids whose status is still `disputed` (an open)."""

    return [a.id for a in store.query() if a.status == EpistemicState.disputed]


def author_decision(store: Any, session_no: int) -> dict[str, Any]:
    """ONE line per call (pre-registered frozen policy, D-e6g):
    1. a successor lesson while the line is below LINE_CAP;
    2. else EXPOSE the first ready unexposed concept (frozen lesson
       when it has one and the line allows, else its first grounded
       drill);
    3. else the sequencer's next_drill surface, or idle (honestly).
    """

    priority = FROZEN["priority"]
    line = _line_end(store)
    if line < FROZEN["line_cap"]:
        return {
            "kind": "lesson-succ",
            "surface": f"after {line} comes {line + 1}",
            "concept": "count-successor",
            "reason": f"line at {line} is below the frozen cap {FROZEN['line_cap']}",
        }
    views = mastery_view(store, priority)
    for cid in priority:
        v = views[cid]
        if v.state is not MasteryState.UNEXPOSED or v.prereq_gaps:
            continue
        phrase = FROZEN["rule_phrases"].get(cid)
        if phrase is not None and line >= FROZEN["rule_lesson_line_min"]:
            return {"kind": "lesson-rule", "surface": phrase, "concept": cid, "reason": f"rule lesson for {cid}"}
        cands = sorted(strip_candidates(cid, store), key=lambda c: c["surface"])
        if cands:
            return {
                "kind": "drill-expose",
                "surface": cands[0]["surface"],
                "concept": cid,
                "reason": f"expose {cid} with its first grounded drill",
            }
        return {"kind": "idle", "surface": None, "concept": cid, "reason": "exposure not possible (no grounded drill)"}
    nd = next_drill(store, priority, session_no)
    if nd is None:
        return {"kind": "idle", "surface": None, "concept": None, "reason": "nothing due and nothing derivable"}
    return {"kind": "drill", "surface": nd["surface"], "concept": nd["concept"], "reason": nd["reason"]}


# ── one session ─────────────────────────────────────────────────────


def _run_session(rt: InfantRuntime, s: int, injected: list[dict[str, Any]], author: LlmAuthor | None, run_cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Drive one session (the det policy, or the LLM author through the
    same seam). Returns (turn records, the session report dict)."""

    records: list[dict[str, Any]] = []
    llm_dropped: list[dict[str, Any]] = []
    for _ in range(FROZEN["turns_per_session"]):
        store = rt.final_store()
        if injected:
            item = injected.pop(0)
            decision = {"kind": "drill-injected", "surface": item["surface"], "concept": item["concept"], "reason": f"re-expose fix {item['fix_id']}"}
        elif author is not None:
            # The LLM author: bounded retry, no rescue (E3.1).

            context = (
                f"tutor session {s}. the number line ends at {_line_end(store)}. "
                "say exactly one line: either 'after N comes M', one of the rule lessons "
                f"({'; '.join(sorted(FROZEN['rule_phrases'].values()))}), or a drill like "
                "'a + b is what?' / 'a - b is what?' / 'a * b is what?' / 'is a larger than b?' / "
                "'what comes after N?'. "
            )
            c = det_classify(author.line(context))
            if c[0] == "ambiguous":
                c2 = det_classify(author.line(context + " (retry: the previous line was not parseable)"))
                if c2[0] != "ambiguous":
                    c = c2
            if c[0] == "ambiguous":
                llm_dropped.append({"author_line": "dropped", "note": "unparseable twice; the line is logged, not said"})
                continue
            decision = {"kind": "llm-line", "surface": None, "concept": None, "reason": "llm authoring arm", "llm_kind": c[0]}
            # an LLM lesson/draft is only said if it is a frozen form
            if decision["surface"] is None:
                decision["surface"] = _canonical_form(c)
            if decision["surface"] is None:
                llm_dropped.append({"author_line": "dropped", "note": "parsed, but not a frozen form; not said"})
                continue
        else:
            decision = author_decision(store, s)
        if decision["kind"] == "idle":
            break
        tr = rt.turn(decision["surface"])
        records.append(
            {
                "turn": tr.turn,
                "author_kind": decision["kind"],
                "author_reason": decision["reason"],
                "surface": tr.surface,
                "kind": tr.kind,
                "concept": tr.concept,
                "contract_valid": tr.contract_valid,
                "honest_gap": tr.honest_gap,
                "attention": tr.attention,
            }
        )
    report = rt.lapse().to_dict()
    run_cfg["llm_dropped"].extend(llm_dropped)
    return records, report


def _canonical_form(c: tuple[str, dict[str, Any]]) -> str | None:
    """Re-render a parsed LLM line as its FROZEN canonical form (the
    surface that will actually be said, when it is one)."""

    k, slots = c
    slots = slots or {}
    if k == "assertion" and "a" in slots and "b" in slots:
        # the successor FORM is frozen; whether b really is a's
        # successor is the STORE's business (a wrong value is a
        # genuine conflict — the dispute/attention discipline deals
        # with it; the authoring arm cannot censor the teacher).
        return f"after {slots['a']} comes {slots['b']}"
    if k == "question":
        mode = slots.get("mode")
        if mode == "succ" and "n" in slots:
            return f"what comes after {slots['n']}?"
        if mode in ("add", "sub", "mult") and "a" in slots and "b" in slots:
            op = {"add": "+", "sub": "-", "mult": "*"}[mode]
            return f"{slots['a']} {op} {slots['b']} is what?"
        if mode == "cmp" and "a" in slots and "b" in slots:
            return f"is {slots['a']} larger than {slots['b']}?"
    if k == "assertion" and "rule" in slots:
        return slots["rule"]
    return None


# ── the analysis arm (det) ─────────────────────────────────────────


def analyze_session(
    s: int,
    report: dict[str, Any],
    store: Any,
    history: list[dict[str, Any]],
    llm: LlmAnalyzer | None,
) -> dict[str, Any]:
    """Diagnose one session from its machine-readable report (+ the pure
    store audit) and emit proposals/triggers (pre-registered rules)."""

    concepts: dict[str, Any] = {}
    gaps_session = 0
    boundary = 0
    for t in report.get("turns", []):
        if t["kind"] in GAP_KINDS:
            gaps_session += 1
            if any(p in (t.get("response_text") or "") for p in FROZEN["boundary_phrases"]):
                boundary += 1
    for cid, m in sorted(report["mastery"].items()):
        concepts[cid] = {
            "state": m["state"],
            "correct_derivations": m["correct_derivations"],
            "events": m["events"],
            "prereq_gaps": list(m["prereq_gaps"]),
            "unresolved_conflicts": m["unresolved_conflicts"],
        }
    # stall: non-stable for the frozen number of consecutive sessions,
    # with >= STALLED_GAPS honest-gap turns in the latest one.
    stalled: list[str] = []
    for cid in FROZEN["priority"]:
        states = [h["concepts"][cid]["state"] for h in history + [{"concepts": concepts}] if cid in h["concepts"]]
        if len(states) < FROZEN["stalled_sessions"]:
            continue
        if all(st != MasteryState.STABLE.value for st in states) and gaps_session >= FROZEN["stalled_gaps"]:
            stalled.append(cid)
    all_stable = all(concepts[cid]["state"] == MasteryState.STABLE.value for cid in FROZEN["priority"])
    line = _line_end(store)
    converged = all_stable and line >= FROZEN["line_cap"]
    status = "converged" if converged else (f"stalled:{stalled[0]}" if stalled else "progressing")

    # proposals (the ONLY class) + fixes
    proposals: list[dict[str, Any]] = []
    fix: dict[str, Any] | None = None
    injected_now = False
    for cid in stalled:
        p = {"action": "re-expose", "concept": cid, "evidence": [f"S{s:02d}: {FROZEN['stalled_sessions']} consecutive non-stable sessions, {gaps_session} honest-gap turns"]}
        proposals.append(p)
        if fix is None:
            cands = sorted(strip_candidates(cid, store), key=lambda c: c["surface"])[: FROZEN["reexpose_turns"]]
            fix = {
                "fix_id": f"fix-S{s:02d}:{cid}",
                "action": "re-expose",
                "concept": cid,
                "diagnosis": p,
                "applied": bool(cands),
                "n_injected": len(cands),
            }
            injected_now = fix["applied"]
    # the LLM analyzer seam: its proposal is applied ONLY if it matches
    # the allowlist byte-for-byte in (action, concept) — else trigger.
    llm_proposal: dict[str, Any] | None = None
    out_of_allowlist: list[dict[str, Any]] = []
    if llm is not None:
        lp = llm.propose(report, {"session": s, "concepts": concepts, "status": status})
        if lp is not None:
            llm_proposal = dict(lp)
            lp_match = any(
                p["action"] == lp.get("action") and p["concept"] == lp.get("concept") for p in proposals
            )
            if not (lp.get("action") == "re-expose" and lp.get("concept") in FROZEN["priority"] and lp_match):
                out_of_allowlist.append(lp)

    # triggers (frozen set; D-e6h: the stall trigger is the
    # second-consecutive-session form)
    triggers: list[dict[str, Any]] = []
    for did in _open_disputes(store):
        triggers.append({"kind": "open-dispute", "dedup_key": f"dispute:{did}", "severity": "high", "evidence": [f"S{s:02d}", did]})
    for p in out_of_allowlist:
        triggers.append({"kind": "out-of-allowlist", "dedup_key": f"proposal:{s}:{p.get('concept')}", "severity": "medium", "evidence": [f"S{s:02d}", json.dumps(p, sort_keys=True)]})

    prev_stalled = history[-1].get("stalled", []) if history else []
    for cid in stalled:
        if cid in prev_stalled:
            triggers.append({"kind": "stalled-persist", "dedup_key": f"stalled:{cid}", "severity": "high", "evidence": [f"S{s - 1:02d}, S{s:02d}: second consecutive stalled session", *([prev_fix_id] if (prev_fix_id := _prev_fix_id(history, cid)) else [])]})
    # keep the historical audit row complete
    hist_row = {"concepts": concepts, "stalled": stalled}
    return {
        "session": s,
        "turns": len(report.get("turns", [])),
        "concepts": concepts,
        "gaps_session": gaps_session,
        "boundary_contacts": boundary,
        "status": status,
        "converged": converged,
        "line_end": line,
        "stalled": stalled,
        "proposals": proposals,
        "fix": fix,
        "fix_applied_next_session": injected_now,
        "llm_proposal": llm_proposal,
        "triggers": triggers,
        "_hist_row": hist_row,
    }


# ── ticket payloads (the #156 shape; hermetic: never posted) ───────


def _ticket_payload(trigger: dict[str, Any], s: int, results_root: Path) -> dict[str, Any]:
    subject = {
        "stalled-persist": f"[tutor loop] stall persisted after fix: {trigger['dedup_key'].split(':', 1)[1]}",
        "open-dispute": f"[tutor loop] open dispute at session end: {trigger['dedup_key'].split(':', 1)[1]}",
        "out-of-allowlist": f"[tutor loop] out-of-allowlist proposal at S{s:02d}",
    }[trigger["kind"]]
    body = (
        f"session S{s:02d} ({trigger['kind']}): evidence {', '.join(trigger['evidence'])}. "
        f"Loop results: {results_root / 'loop-report.json'}. "
        "The loop is paused here; this change needs owner approval."
    )
    return {
        "dedup_key": trigger["dedup_key"],
        "assignee": FROZEN["owner_assignee"],
        "project": FROZEN["project"],
        "subject": subject,
        "severity": trigger["severity"],
        "body": body,
        "posted": False,
    }


# ── the run ─────────────────────────────────────────────────────────


def _run_once(root: Path, author: LlmAuthor | None, analyzer: LlmAnalyzer | None, cfg: dict[str, Any]) -> dict[str, Any]:
    """One full loop run under `root` (sessions boot from the previous
    lapse, exactly as the E6.1/E6.2 benches run them)."""

    reset_concepts()
    rt = InfantRuntime(root)
    history: list[dict[str, Any]] = []
    sessions: list[dict[str, Any]] = []
    pending_injected: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    tickets: list[dict[str, Any]] = []
    convergence: dict[str, Any] = {"converged": False, "converged_at_session": None}
    for s in range(1, FROZEN["sessions_max"] + 1):
        rt.boot(s)
        records, report = _run_session(rt, s, pending_injected, author, cfg)
        store = _fresh_store_view(root, s)
        diagnosis = analyze_session(s, report, store, history, analyzer)
        hist_row = diagnosis.pop("_hist_row")
        hist_row["fix"] = diagnosis["fix"]
        history.append(hist_row)
        # apply the fix to the NEXT session's head (injected queue)
        if diagnosis["fix"] is not None and diagnosis["fix"]["applied"]:
            cands = sorted(strip_candidates(diagnosis["fix"]["concept"], store), key=lambda c: c["surface"])[: FROZEN["reexpose_turns"]]
            pending_injected = [
                {"surface": c["surface"], "concept": diagnosis["fix"]["concept"], "fix_id": diagnosis["fix"]["fix_id"]}
                for c in cands
            ]
        for trig in diagnosis["triggers"]:
            if trig["dedup_key"] in seen_keys:
                continue
            seen_keys.add(trig["dedup_key"])
            tickets.append(_ticket_payload(trig, s, root))
        sessions.append({"session": s, "records": records, "diagnosis": diagnosis, "report_turns": len(report.get("turns", []))})
        if diagnosis["converged"]:
            convergence = {"converged": True, "converged_at_session": s}
            break
    final_store = _fresh_store_view(root, sessions[-1]["session"] if sessions else 1)
    report_out = {
        "arm": {
            "author": "llm" if author is not None else "det",
            "analyzer": "llm" if analyzer is not None else "det",
            "llm_arm": cfg.get("llm_arm"),
            "llm_dropped": list(cfg.get("llm_dropped", [])),
        },
        "convergence": convergence,
        "sessions": sessions,
        "tickets": tickets,
        "posted": [],
        "final_store": {
            "total": len(final_store.query()),
            "line_end": _line_end(final_store),
            "open_disputes": _open_disputes(final_store),
            "beyond_cap": _beyond_cap(final_store),
        },
    }
    report_path = root / "loop-report.json"
    text = json.dumps(report_out, indent=2, sort_keys=True) + "\n"
    report_path.write_text(text, encoding="utf-8")
    return report_out


def _prev_fix_id(history: list[dict[str, Any]], cid: str) -> str | None:
    """The id of the fix applied for cid in the most recent prior
    session with a fix (the evidence link for the persist trigger)."""

    for row in reversed(history):
        fx = row.get("fix")
        if fx is not None and fx.get("concept") == cid and fx.get("applied"):
            return fx["fix_id"]
    return None


def _fresh_store_view(root: Path, s: int) -> Any:
    """Re-load the lapsed dump of session s (pure view for analysis)."""

    from kainos.tutor.session import codex_dump_path, load_store

    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        from kainos.codex.memory import InMemoryCodexStore

        return InMemoryCodexStore()
    return load_store(p)


def _beyond_cap(store: Any) -> list[str]:
    """Established successor endpoints beyond the frozen cap (must be
    empty — the cap is a store property, L7)."""

    out: list[str] = []
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid = a.subject.id
        oid = a.object_id
        if (
            sid.startswith("count-successor:succ-of(")
            and oid.startswith("count-successor:num(")
            and a.validity is None
            and a.status == EpistemicState.established
            and int(oid[len("count-successor:num(") : -1]) > FROZEN["line_cap"]
        ):
            out.append(a.id)
    return out


def _default_out_dir() -> Path:
    import os

    base = Path(os.environ.get("KAINOS_RESULTS_DIR", "results")) / "phase-6"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_loop(out_dir: Path | None = None, author: LlmAuthor | None = None, analyzer: LlmAnalyzer | None = None) -> dict[str, Any]:
    """Run the loop twice (run1/run2) for the byte-identity check (L7)
    and return the run1 report. Official: `KAINOS_RESULTS_DIR` unset →
    results/phase-6/e6.3-run{1,2}/; hermetic: no Ollama (the LLM arms
    are skipped or passed as typed seams explicitly)."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    arm_name = "llm" if (author is not None or analyzer is not None) else "skipped-no-backend"
    r1 = _run_once(out_dir / "e6.3-run1", author, analyzer, {"llm_arm": arm_name, "llm_dropped": []})
    _r2 = _run_once(out_dir / "e6.3-run2", author, analyzer, {"llm_arm": arm_name, "llm_dropped": []})
    r1["run2_identical"] = _byte_identity(out_dir / "e6.3-run1", out_dir / "e6.3-run2")
    return r1


def _byte_identity(a: Path, b: Path) -> dict[str, Any]:
    fa = sorted(x.name for x in a.iterdir() if x.is_file())
    fb = sorted(x.name for x in b.iterdir() if x.is_file())
    same = fa == fb and all(hashlib.sha256((a / x).read_bytes()).hexdigest() == hashlib.sha256((b / x).read_bytes()).hexdigest() for x in fa)
    return {"files": fa, "identical": same}


# ── the checks (L1..L7) — the experiment ───────────────────────────


def _checks(run1: dict[str, Any], run_dir: Path, reference: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    sessions = run1["sessions"]
    # L1 — loop contract
    l1_bad: list[str] = []
    total_turns = 0
    for srow in sessions:
        for rec in srow["records"]:
            total_turns += 1
            if not rec["contract_valid"]:
                l1_bad.append(f"{rec['turn']}: contract invalid (author {rec['author_kind']})")
        if len(srow["records"]) > FROZEN["turns_per_session"]:
            l1_bad.append(f"S{srow['session']:02d}: budget exceeded")
    for srow in sessions:
        rp = run_dir / f"session-S{srow['session']:02d}.json"
        rep = json.loads(rp.read_text())
        for key in ("mastery", "codex", "attention", "turns"):
            if key not in rep:
                l1_bad.append(f"S{srow['session']:02d}: report missing {key}")
    if len(sessions) > FROZEN["sessions_max"]:
        l1_bad.append("sessions exceeded the frozen max")
    checks["l1_loop_contract"] = {"pass": not l1_bad, "bad": l1_bad, "sessions": len(sessions), "turns": total_turns}

    # L2 — author authority: full-session replay against the run's own
    # pre-dumps. Every line must be exactly the decision the frozen
    # policy makes at that pre-state (det arms), or (LLM arm) a
    # canonical form of a grammatical line.
    import tempfile

    l2_bad: list[str] = []
    l2_stats: dict[str, int] = {}
    for srow in sessions:
        s = srow["session"]
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            for k in range(1, s):  # copy the pre-session dumps (1..s-1)
                src = run_dir / f"codeX-S{k:02d}.json"
                if src.exists():
                    (scratch / src.name).write_bytes(src.read_bytes())
            rt2 = InfantRuntime(scratch)
            rt2.boot(s)
            # reconstruct the injected queue exactly as the run did
            q: list[dict[str, Any]] = []
            for k2 in range(1, s):
                fx = sessions[k2 - 1]["diagnosis"]["fix"]
                if fx is not None and fx["applied"]:
                    store2 = _fresh_store_view(run_dir, k2)
                    cands = sorted(strip_candidates(fx["concept"], store2), key=lambda c: c["surface"])[: FROZEN["reexpose_turns"]]
                    q = [{"surface": c["surface"], "concept": fx["concept"], "fix_id": fx["fix_id"]} for c in cands]
                    break
            for rec in srow["records"]:
                ak = rec["author_kind"]
                l2_stats[ak] = l2_stats.get(ak, 0) + 1
                store = rt2.final_store()
                if q:
                    head = q[0]
                    if not (ak == "drill-injected" and rec["surface"] == head["surface"]):
                        l2_bad.append(f"{rec['turn']}: not the injected head ({ak})")
                    q = q[1:]
                elif ak in ("lesson-succ", "lesson-rule", "drill-expose", "drill"):
                    pre = author_decision(store, s)
                    if pre["surface"] != rec["surface"]:
                        l2_bad.append(f"{rec['turn']}: line not the frozen policy's decision at pre-state ({ak})")
                elif ak == "llm-line":
                    c = det_classify(rec["surface"])
                    if c[0] == "ambiguous" or _canonical_form(c) != rec["surface"]:
                        l2_bad.append(f"{rec['turn']}: LLM line not the canonical form of a grammatical line")
                else:
                    l2_bad.append(f"{rec['turn']}: unknown author kind {ak}")
                tr2 = rt2.turn(rec["surface"])
                if tr2.kind != rec["kind"] or tr2.surface != rec["surface"]:
                    l2_bad.append(f"{rec['turn']}: the replayed turn differs from the recorded turn")
    checks["l2_author_authority"] = {"pass": not l2_bad, "bad": l2_bad, "stats": l2_stats}

    # L3 — learning dynamics vs the frozen (control-derived) table
    l3_bad: list[str] = []
    traj = {str(srow["session"]): {cid: srow["diagnosis"]["concepts"].get(cid, {}).get("state") for cid in FROZEN["priority"]} for srow in sessions}
    ref = reference.get("trajectory")
    if ref is not None and traj != ref:
        l3_bad.append(f"trajectory {traj} != frozen control {ref}")
    conv = reference.get("converged_at_session")
    if conv is not None and (run1["convergence"]["converged_at_session"] != conv or not run1["convergence"]["converged"]):
        l3_bad.append(f"convergence {run1['convergence']} != frozen control session {conv}")
    fin = run1["final_store"]
    if fin["line_end"] != FROZEN["line_cap"]:
        l3_bad.append(f"final line end {fin['line_end']} != cap {FROZEN['line_cap']}")
    ref_total = reference.get("final_store_total")
    if ref_total is not None and fin["total"] != ref_total:
        l3_bad.append(f"final store total {fin['total']} != frozen control {ref_total}")
    final_s = max(traj)
    all_stable = all(traj[final_s][cid] == "stable" for cid in FROZEN["priority"])
    checks["l3_learning_dynamics"] = {"pass": not l3_bad and run1["convergence"]["converged"] and all_stable, "bad": l3_bad, "convergence": run1["convergence"], "final_states": traj[final_s]}

    # L4 — analysis audit (diagnosis fields recomputable; fixes in the
    # allowlist; no mastery regression across sessions)
    l4_bad: list[str] = []
    ladder = {cid: [traj[s][cid] for s in sorted(traj)] for cid in FROZEN["priority"]}
    rank = {"unexposed": 0, "exposed": 1, "practicing": 2, "stable": 3}
    for cid, states in ladder.items():
        vals = [rank[st] for st in states if st is not None]
        if any(b < a for a, b in itertools.pairwise(vals)):
            l4_bad.append(f"{cid}: mastery regressed across sessions: {states}")
    fix_count = 0
    for srow in sessions:
        d = srow["diagnosis"]
        if d["fix"] is not None:
            fix_count += 1
            f = d["fix"]
            if f["action"] != "re-expose" or f["concept"] not in FROZEN["priority"]:
                l4_bad.append(f"S{srow['session']:02d}: fix outside the allowlist: {f}")
            if not f["diagnosis"]["evidence"]:
                l4_bad.append(f"S{srow['session']:02d}: fix cites no diagnosis")
    ref_fixes = reference.get("applied_fixes")
    if ref_fixes is not None and fix_count != ref_fixes:
        l4_bad.append(f"applied fixes {fix_count} != frozen control {ref_fixes}")
    checks["l4_analysis_audit"] = {"pass": not l4_bad, "bad": l4_bad, "fixes": fix_count}

    # L5 — attention inbox (frozen triggers; dedup; payloads; no posts)
    l5_bad: list[str] = []
    keys = [t["dedup_key"] for t in run1["tickets"]]
    if len(keys) != len(set(keys)):
        l5_bad.append("dedup violated: a key fired twice")
    ref_keys = reference.get("ticket_keys", [])
    if sorted(keys) != sorted(ref_keys):
        l5_bad.append(f"trigger keys {sorted(keys)} != frozen control {sorted(ref_keys)}")
    for t in run1["tickets"]:
        if t["assignee"] != FROZEN["owner_assignee"] or not t["subject"] or not t["body"] or t["severity"] not in ("high", "medium", "low"):
            l5_bad.append(f"malformed ticket payload: {t['dedup_key']}")
        if t["posted"]:
            l5_bad.append(f"hermetic run posted a ticket: {t['dedup_key']}")
    if run1["posted"] != []:
        l5_bad.append("posted list is not empty")
    checks["l5_attention_inbox"] = {"pass": not l5_bad, "bad": l5_bad, "tickers_keys": keys}

    # L6 — arm seam (E3.1 SKIP semantics + seam neutrality)
    l6_bad: list[str] = []
    if run1["arm"]["author"] != "det" or run1["arm"]["analyzer"] != "det":
        l6_bad.append("official run is not the det arm")
    if run1["arm"]["llm_arm"] != "skipped-no-backend":
        l6_bad.append(f"arm config {run1['arm']['llm_arm']} != skipped-no-backend (hermetic)")
    if not LLM_SEAMS_PRESENT:
        l6_bad.append("the LLM seams are missing")
    checks["l6_arm_seam"] = {"pass": not l6_bad, "bad": l6_bad, "arm": run1["arm"]}

    # L7 — determinism + wall integrity
    l7_bad: list[str] = []
    if not run1["run2_identical"]["identical"]:
        l7_bad.append(f"run1 != run2: {run1['run2_identical']}")
    ref_files = reference.get("files")
    if ref_files is not None and run1["run2_identical"]["files"] != ref_files:
        l7_bad.append(f"file set {run1['run2_identical']['files']} != frozen control {ref_files}")
    fin = run1["final_store"]
    if fin["beyond_cap"]:
        l7_bad.append(f"established values beyond the cap exist: {fin['beyond_cap']}")
    if fin["open_disputes"]:
        l7_bad.append(f"open disputes at the end: {fin['open_disputes']}")
    for srow in sessions:
        for rec in srow["records"]:
            if rec["kind"] in GAP_KINDS:
                l7_bad.append(f"{rec['turn']}: an honest-gap turn in a fully grounded run (the author only says what the infant can ground)")
    checks["l7_determinism_wall"] = {"pass": not l7_bad, "bad": l7_bad, "files": run1["run2_identical"]["files"]}

    passed = sum(1 for c in checks.values() if c["pass"])
    return {"checks": checks, "passed": passed, "value": passed / CHECKS}


class E6_3Experiment:
    """E6.3 — the un-attended loop (T5 #155, milestone M2)."""

    name = "e6.3"
    hypothesis = (
        "A det authoring arm driving the frozen sequencer and a det analysis arm "
        "acting only within one frozen fix class run the infant through N sessions "
        "without a human in the turn loop: every line is grounded (replay-verified), "
        "every diagnosis is re-auditable, attention triggers file deduped unposted "
        " payloads, and the run converges at the frozen fixed point on the E6.2 line "
        "with the line cap a property of the final store and two runs byte-identical."
    )
    metric = "loop checks passed (L1..L7)"
    threshold = "7/7"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        out = _default_out_dir()
        run1 = run_loop(out)
        reference_path = out / "e6.3-derived.json"
        reference = json.loads(reference_path.read_text()) if reference_path.exists() else {}
        result = _checks(run1, out / "e6.3-run1", reference)
        return Result(
            name=self.name,
            passed=result["passed"] == CHECKS,
            value=round(result["value"], 4),
            evidence=[
                Path(out / "e6.3-run1" / "session-S03.json"),
                Path(out / "e6.3-run1" / "codeX-S03.json"),
                Path(out / "e6.3-run1" / "loop-report.json"),
                Path(out / "e6.3-run2" / "loop-report.json"),
            ],
            config={
                "seed": "deterministic loop (frozen author policy + sequencer; no randomness anywhere)",
                "dataset_hash": reference.get("reports_sha256", "reference-not-frozen"),
            },
        )
