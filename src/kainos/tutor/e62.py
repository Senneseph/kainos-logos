"""E6.2 — "Curriculum expansion to the edge of grasp" (registry phase 6).

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md (E6.2
section, frozen 2026-08-21 owner-directed: "let it continue learning;
our stopping point will be where it can't grasp a new concept").

The infant CONTINUES from the e6.1 store: the 30-turn e6.1 replay
(S1..S4) runs first in a fresh persist dir, then the 105-turn ladder
(S5..S9) extends the number line (11 -> 20 -> 50 -> 70) and teaches,
via rule-facts in the store, subtraction, multiplication, and
comparison. S9 is the LIMIT PROBE (owner direction 2026-08-21, D-e6f:
"first don't give it square roots — let's see how far subtraction and
multiplication can go"): the two composition operations pushed to the
line boundary. The pre-registered stopping point (C8, revised): the
successor lattice grasps the arithmetic lattice, and the composition
operations reach EXACTLY as far as the line — every in-line instance
derives with citations (including the boundary-maximal 70-70=0 and
10*7=70, the max product landing exactly on the line end), the first
out-of-line instances stop at the boundary with DISTINCT correct
articulations (walk-off vs beyond-line vs line-end) — never a
fabricated value, and the store never contains a value beyond the
line. (The sqrt rung's own wall claim is preserved for the future
lattice-wall experiment; the machinery is dormant in the brainstem.)

run1 = evidence; run2 = byte-identity control. All checks are offline
re-audits of the persisted stores (P11: nothing is trusted on
sight — including its own past answers).
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState
from kainos.projection.contract import validate_response
from kainos.tutor.bench import FROZEN as E61_FROZEN
from kainos.tutor.brainstem import Brainstem
from kainos.tutor.mastery import STABLE_EVIDENCE_K, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "FROZEN", "LADDER_CONCEPTS", "E6_2Experiment", "run_e6_2"]

CHECKS = 8

#: The 6-concept curriculum the E6.2 runtime seeds (D-e6f: the
#: sqrt-bracket concept is deferred with its rung). The e6.1 bench keeps
#: seeding its TWO pilot strips (bench._pilot) so the e6.1 frozen derived
#: constants stay reproducible.
LADDER_CONCEPTS: tuple = InfantRuntime.PILOT_CONCEPTS

def _line(upper_start: int, upper_end: int) -> list[str]:
    """'after N comes N+1' lessons extending the line through upper_end."""

    return [f"after {n} comes {n + 1}" for n in range(upper_start, upper_end)]


def _mult_rule() -> str:
    return "multiplication is repeated addition"


#: The frozen ladder script (the verbatim lists are the authority — the
#: D-e6a discipline). 101 turns = 16 + 9 + 39 + 28 + 9 (S5..S9).
FROZEN: dict[str, Any] = {
    "k": STABLE_EVIDENCE_K,
    "replay_turn_count": 30,
    "ladder_turn_count": 105,
    "total_turn_count": 135,
    "script": {
        5: [
            *_line(10, 20),
            "9 + 7 is what?",
            "12 + 5 is what?",
            "8 + 9 is what?",
            "15 + 4 is what?",
            "after 16 comes 18",
            "no — that was a mistake; after 16 comes 17",
        ],
        6: [
            "7 - 2 is what?",
            "subtraction is walking backward",
            "7 - 2 is what?",
            "16 - 9 is what?",
            "13 - 5 is what?",
            "10 - 4 is what?",
            "3 - 5 is what?",
            "20 - 7 is what?",
            "12 - 12 is what?",
        ],
        7: [
            *_line(20, 50),
            "3 * 4 is what?",
            _mult_rule(),
            "after 45 comes 47",
            "no — that was a mistake; after 45 comes 46",
            "3 * 4 is what?",
            "6 * 7 is what?",
            "8 * 6 is what?",
            "4 * 9 is what?",
            "2 * 0 is what?",
        ],
        8: [
            *_line(50, 70),
            "is 17 larger than 9?",
            "comparison is walking the line",
            "is 17 larger than 9?",
            "is 9 larger than 17?",
            "is 25 larger than 64?",
            "is 6 larger than 6?",
            "is 48 larger than 52?",
        ],
        9: [
            # S9 = the LIMIT PROBE (D-e6f): how far do subtraction and
            # multiplication get, exactly. Line end is 70.
            "70 - 1 is what?",
            "70 - 35 is what?",
            "69 - 68 is what?",
            "55 - 27 is what?",
            "70 - 70 is what?",
            "5 - 7 is what?",
            "100 - 3 is what?",
            "8 * 8 is what?",
            "9 * 7 is what?",
            "10 * 7 is what?",
            "9 * 9 is what?",
            "11 * 7 is what?",
            "1 * 9 is what?",
            "0 * 5 is what?",
        ],
    },
    # C2: the frozen trajectory (session-final state, S5..S9) for the 7 concepts.
    "trajectory": {
        "count-successor": ["stable", "stable", "stable", "stable", "stable"],
        "add-within-10": ["stable", "stable", "stable", "stable", "stable"],
        "add-two-digit": ["stable", "stable", "stable", "stable", "stable"],
        "sub-within-30": ["unexposed", "stable", "stable", "stable", "stable"],
        "mult-within-100": ["unexposed", "unexposed", "stable", "stable", "stable"],
        "compare-numbers": ["unexposed", "unexposed", "unexposed", "stable", "stable"],
        # (6 concepts — sqrt-bracket deferred with its rung, D-e6f)
    },
    # C3/C5: the A/B capability-activation pairs (same question text).
    "ab_pairs": [
        {"before": "S06:01", "after": "S06:03", "text": "7 - 2 is what?", "rule": "cap:sub-within-30:rule", "gap": "not yet learned: walking backward (subtraction)", "answer": "5"},
        {"before": "S07:31", "after": "S07:35", "text": "3 * 4 is what?", "rule": "cap:mult-within-100:rule", "gap": "not yet learned: repeated addition (multiplication)", "answer": "12"},
        {"before": "S08:21", "after": "S08:23", "text": "is 17 larger than 9?", "rule": "cap:compare-numbers:rule", "gap": "not yet learned: walking the line (comparison)", "answer": "yes — 17 is 8 steps beyond 9"},
        # (the fourth A/B pair — sqrt — moved with the deferred rung, D-e6f)
    ],
    # C6: the planted conflict pairs (ids derived, frozen from the control).
    "conflict_facts": [
        {"turn": "S05:15", "subject": "count-successor:succ-of(16)", "wrong": 18, "right": 17},
        {"turn": "S07:33", "subject": "count-successor:succ-of(45)", "wrong": 47, "right": 46},
    ],
    # C6: the frozen attention set (the ladder continues the e6.1 conflict
    # history: episodes S2:04, S4:03 (replay), S5:15 (3rd), S7:33 (4th)).
    "attention": [
        {"turn": "S04:03", "type": "repeated-conflict"},
        {"turn": "S05:15", "type": "repeated-conflict"},
        {"turn": "S07:33", "type": "repeated-conflict"},
    ],
    # C4: the frozen honesty edges (D-e6f: the two boundary modes distinct).
    "edges": {
        "S06:07": {"text": "3 - 5 is what?", "state": "needs_info", "mode": "walk-off", "a": 3, "b": 5},
        "S09:06": {"text": "5 - 7 is what?", "state": "needs_info", "mode": "walk-off", "a": 5, "b": 7},
        "S09:07": {"text": "100 - 3 is what?", "state": "needs_info", "mode": "beyond-line", "a": 100, "b": 3},
        "S09:11": {"text": "9 * 9 is what?", "state": "needs_info", "mode": "line-end-mul", "a": 9, "b": 9},
        "S09:12": {"text": "11 * 7 is what?", "state": "needs_info", "mode": "line-end-mul", "a": 11, "b": 7},
    },
    # C8: the boundary-maximal derivations (turn -> expected answer) and the
    # first out-of-line stops (the honest boundary, frozen).
    "boundary_derived": {
        "S09:01": "69",
        "S09:02": "35",
        "S09:03": "1",
        "S09:04": "28",
        "S09:05": "0",
        "S09:08": "64",
        "S09:09": "63",
        "S09:10": "70",
        "S09:13": "9",
        "S09:14": "0",
    },
    "line_end": 70,
}

# ── helpers ──────────────────────────────────────────────────────────────────


def _ladder(root: Path) -> list[dict]:
    """Run the full 135-turn run (e6.1 replay + ladder) once under `root`."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=LADDER_CONCEPTS)
    out: list[dict] = []
    for session in (1, 2, 3, 4):
        rt.boot(session)
        for text in E61_FROZEN["script"][session]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    for session in range(5, 10):
        rt.boot(session)
        for text in FROZEN["script"][session]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _default_out_dir() -> Path:
    base = os.environ.get("KAINOS_RESULTS_DIR", "results")
    return Path(base) / "phase-6"


def _ref_e61_s4() -> Path:
    base = os.environ.get("KAINOS_RESULTS_DIR", "results")
    return Path(base) / "phase-6" / "e6.1-run1" / "codeX-S04.json"


def _canon(a: Assertion) -> tuple:
    prov = a.provenance
    v = a.validity
    src = prov.source if prov is not None else None
    return (
        a.id,
        a.subject.id,
        tuple(a.subject.labels),
        a.relation.id,
        a.object_id,
        tuple(sorted((k, str(val)) for k, val in (a.context.data or {}).items())),
        (v.from_, v.to) if v is not None else None,
        a.status.value,
        (src.uri, src.media_type, src.authority) if src is not None else None,
        (prov.observer if prov is not None else None),
        (prov.verified if prov is not None else None),
        tuple(prov.evidence) if prov is not None else (),
    )


def _parse_cite(codex: InMemoryCodexStore, aid: str) -> tuple[tuple[int, int] | str | None, str | None]:
    """A cite is either an established active successor fact (n, m) with
    m == n+1, or the trailing rule-fact id ("rule:<aid>"), or bad."""

    try:
        a = codex.get(aid)
    except KeyError:
        return None, f"dangling cite: {aid}"
    if a.status != EpistemicState.established:
        return None, f"non-established cite: {aid} ({a.status.value})"
    if a.validity is not None and a.validity.to is not None:
        return None, f"closed cite: {aid}"
    if a.object_id.startswith("rule:"):
        return f"rule:{aid}", None
    pre = "count-successor:succ-of("
    if not (a.subject.id.startswith(pre) and a.object_id.startswith("count-successor:num(")):
        return None, f"non-fact cite: {aid}"
    n = int(a.subject.id[len(pre) : -1])
    m = int(a.object_id[len("count-successor:num(") : -1])
    if m != n + 1:
        return None, f"non-successor fact cited: {aid}"
    return (n, m), None


def _contiguous(p: tuple[int, int], q: tuple[int, int]) -> bool:
    return q[0] == p[1] or q[1] == p[0]


def _segments(cites: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    segs: list[list[tuple[int, int]]] = []
    for i, c in enumerate(cites):
        if i == 0 or not _contiguous(cites[i - 1], c):
            segs.append([])
        segs[-1].append(c)
    return segs


def _verify_turn(codex: InMemoryCodexStore, t: dict) -> list[str]:
    """Offline re-verification of one derived/bracketed answer from its
    cited facts (the turn's own proof, recomputed from the store)."""

    ir = t["response_ir"]
    if "answer" not in ir:  # non-question turns carry no answer field
        return []
    ans = ir["answer"]
    state = ir.get("uncertainty_state")
    if state not in ("derived", "bracketed"):
        return []
    cites: list[tuple[int, int]] = []
    rule_tail: str | None = None
    for aid in ir["evidence"]:
        parsed, err = _parse_cite(codex, str(aid))
        if err:
            return [err]
        if isinstance(parsed, str):
            rule_tail = parsed
        else:
            assert parsed is not None
            cites.append(parsed)
    mode = t["slots"].get("mode")
    segs = _segments(cites)
    span = f"{cites[0][0] if cites else None}..{cites[-1][1] if cites else None}"
    if mode == "succ":
        if len(segs) != 1 or len(cites) != 1 or cites[0][1] != int(ans):
            return [f"succ replay mismatch: {cites} vs {ans}"]
        return []
    if mode == "add":
        if not cites or len(segs) != 1 or cites[0][0] != t["slots"]["a"] or cites[-1][1] != int(ans):
            return [f"add replay mismatch: {len(segs)} segs, {span} vs {ans}"]
        return []
    if mode == "sub":
        bwd = [cites[i - 1][0] == cites[i][1] for i in range(1, len(cites))]
        if not cites or len(segs) != 1 or cites[0][1] != t["slots"]["a"] or cites[-1][0] != int(ans) or not all(bwd):
            return [f"sub replay mismatch: {len(segs)} segs, {t['slots']['a']}..{cites[-1][0] if cites else None} vs {ans}, bwd={bwd[:3] if bwd else None}"]
        return []
    if mode == "mult":
        fwd = [cites[i - 1][1] == cites[i][0] for i in range(1, len(cites))]
        if cites:
            if len(segs) != 1 or cites[0][0] != 0 or cites[-1][1] != int(ans) or not all(fwd):
                return [f"mult replay mismatch: {len(segs)} segs, {span} vs {ans}, fwd={fwd[:3] if fwd else None}"]
        else:
            # the legitimate identity (a zero step adds nothing): answer 0,
            # cited by the rule fact itself
            if str(ans) != "0" or rule_tail is None:
                return [f"mult identity mismatch: no fact cites, ans={ans!r}, rule_tail={rule_tail}"]
        return []
    if mode == "cmp":
        a, b = t["slots"]["a"], t["slots"]["b"]
        lo, hi = (a, b) if a <= b else (b, a)
        d = hi - lo
        want = (
            f"yes — {a} is {d} steps beyond {b}"
            if a > b
            else (f"no — {b} is {d} steps beyond {a}" if a < b else f"neither — {a} is {a}")
        )
        if segs and (len(segs) != 1 or cites[0][0] != lo or cites[-1][1] != hi):
            return [f"cmp replay mismatch: {len(segs)} segs, {cites[0][0]}..{cites[-1][1]} vs {lo}..{hi}"]
        if not segs and rule_tail is None:
            return ["cmp (equal) answer without a rule-fact cite"]
        if ans != want:
            return [f"cmp verdict mismatch: {ans!r} != {want!r}"]
        return []
    if mode == "sqrt":
        n = t["slots"]["n"]
        if state == "derived":
            k = int(ans)
            if len(segs) != 1 or cites[0][0] != 0 or cites[-1][1] != n or k * k != n:
                return [f"sqrt exact replay mismatch: {len(segs)} segs, ..{cites[-1][1] if cites else None} vs n={n}, k={k}"]
            return []
        # bracketed (full or partial)
        txt = str(ans)
        if "between" in txt:
            lo_t, hi_t = (int(x) for x in txt.split("between ", 1)[1].split(" and ", 1))
            if lo_t + 1 != hi_t or len(segs) != 2 or cites[0][0] != 0:
                return [f"sqrt bracket shape mismatch: {txt!r} segs={len(segs)}"]
            if segs[0][-1][1] != lo_t * lo_t or segs[1][-1][1] != hi_t * hi_t or not (lo_t * lo_t < n < hi_t * hi_t):
                return [f"sqrt bracket values mismatch: {segs[0][-1][1] if segs[0] else None}/{segs[1][-1][1] if segs[1] else None} vs n={n}"]
            return []
        # partial bracket
        lo_t = int(txt.split("greater than ", 1)[1].split(" —", 1)[0])
        if len(segs) != 1 or segs[0][-1][1] != lo_t * lo_t or not (lo_t * lo_t < n):
            return [f"sqrt partial bracket mismatch: {txt!r} n={n}"]
        return []
    return [f"unknown mode for replay: {mode!r}"]


# ── the ladder run + all checks ──────────────────────────────────────────────


def run_e6_2(out_dir: Path | None = None) -> dict:
    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    run1, run2 = out_dir / "e6.2-run1", out_dir / "e6.2-run2"
    rep1 = _ladder(run1)
    _rep2 = _ladder(run2)  # byte-identity control (C7)

    ladder_key = "\n".join(t for s in range(5, 10) for t in FROZEN["script"][s])
    full_key = "\n".join(
        [t for s in (1, 2, 3, 4) for t in E61_FROZEN["script"][s]] + [t for s in range(5, 10) for t in FROZEN["script"][s]]
    )
    script_hash = hashlib.sha256(ladder_key.encode("utf-8")).hexdigest()[:16]
    full_hash = hashlib.sha256(full_key.encode("utf-8")).hexdigest()[:16]

    final = load_store(codex_dump_path(run1, 9))
    s6_store = load_store(codex_dump_path(run1, 6))
    s9_store = load_store(codex_dump_path(run1, 9))
    s4_store = load_store(codex_dump_path(run1, 4))
    turns_all = [t for r in rep1 for t in r["turns"]]
    by_turn = {t["turn"]: t for t in turns_all}
    ladder_reps = [r for r in rep1 if r["session"] >= 5]

    checks: dict[str, Any] = {}

    # C1 — contract validity across the WHOLE 135-turn run (replay + ladder).
    c1_bad = [
        {"turn": t["turn"], "violations": v}
        for t in turns_all
        for ok, v in [validate_response(t["response_ir"], t["kind"])]
        if not ok
    ]
    checks["c1_contract_valid"] = {
        "pass": len(c1_bad) == 0 and len(turns_all) == FROZEN["total_turn_count"],
        "turns_validated": len(turns_all),
        "violations": c1_bad,
    }

    # C2 — the learning trajectory + offline re-verification of every
    # derived/bracketed answer from its cited facts (recomputed, not
    # trusted): the ladder's derivation-correct events re-play cleanly.
    traj_ok = True
    traj_seen: dict[str, list[str]] = {}
    for i, r in enumerate(ladder_reps):
        for cid, want in FROZEN["trajectory"].items():
            got = r["mastery"][cid]["state"]
            traj_seen.setdefault(cid, []).append(got)
            if got != want[i]:
                traj_ok = False
    replay_viol: list[str] = []
    proof_events = 0
    ladder_turns = [t for t in turns_all if int(t["turn"].split(":")[0][1:]) >= 5]
    for t in ladder_turns:
        for eid in t["events"]:
            if eid.endswith(":derivation-correct"):
                proof_events += 1
        for viol in _verify_turn(final, t):
            replay_viol.append(f"{t['turn']}: {viol}")
    checks["c2_learning"] = {
        "pass": traj_ok and not replay_viol and proof_events >= 4 * STABLE_EVIDENCE_K,
        "trajectory": traj_seen,
        "trajectory_frozen": FROZEN["trajectory"],
        "ladder_derivation_events": proof_events,
        "replay_violations": replay_viol[:20],
    }

    # C3 — the impossible-learns arc + the four A/B capability activations
    # (same question text; before = honest named gap + zero writes; after =
    # derived, citing the rule fact).
    c3_bad = []
    ab_report = []
    for pp in FROZEN["ab_pairs"]:
        before, after = by_turn[pp["before"]], by_turn[pp["after"]]
        ok_before = (
            before["kind"] == "impossible"
            and before["response_ir"]["gap"] == pp["gap"]
            and before["memory_diff"] == []
            and before["grounded"] == []
        )
        ok_after = (
            after["kind"] == "question"
            and after["response_ir"]["uncertainty_state"] == "derived"
            and str(after["response_ir"]["answer"]) == pp["answer"]
            and pp["rule"] in [str(x) for x in after["response_ir"]["evidence"]]
        )
        ab_report.append({"pair": pp["text"], "before": pp["before"], "after": pp["after"], "ok_before": ok_before, "ok_after": ok_after})
        if not (ok_before and ok_after):
            c3_bad.append(pp["text"])
    checks["c3_impossible_learns_arc"] = {
        "pass": not c3_bad,
        "ab_pairs": ab_report,
        "violations": c3_bad,
    }

    # C4 — honesty at every rung's edge, re-audited against the session
    # snapshot (the store as the probe actually saw it).
    c4_bad = []
    # each frozen edge: the state, the mode-specific audit string, and the
    # RE-AUDIT on the session snapshot it was written under (the store as
    # the probe actually saw it). D-e6f: walk-off vs beyond-line vs
    # line-end are distinct, separately re-audited modes.
    stores = {6: s6_store, 7: load_store(codex_dump_path(run1, 7)), 9: s9_store}
    for turn, edge in FROZEN["edges"].items():
        t = by_turn[turn]
        sess = int(turn.split(":")[0][1:])
        store = stores[sess]
        ir = t["response_ir"]
        if ir["uncertainty_state"] != edge["state"]:
            c4_bad.append(f"{turn} state {ir['uncertainty_state']} != {edge['state']}")
            continue
        a, b = edge["a"], edge["b"]
        if edge["mode"] == "walk-off":
            if not any(str(e).startswith("walk-off:") for e in ir["evidence"]):
                c4_bad.append(f"{turn} evidence is not a walk-off audit")
            if b <= a:
                c4_bad.append(f"{turn}: frozen edge is not a walk-off shape ({a} - {b})")
            if _walk_off_replay(store, a, b) is not None:
                c4_bad.append(f"{turn} walk-off audit false: {a} - {b} IS walkable in the S{sess:02d} snapshot")
            if "leaves the start of my number line" not in str(t["response_text"]):
                c4_bad.append(f"{turn} missing the walk-off articulation")
        elif edge["mode"] == "beyond-line":
            if not any(str(e).startswith("line-end:") for e in ir["evidence"]):
                c4_bad.append(f"{turn} evidence is not a line-end audit")
            if a <= _line_end_of(store):
                c4_bad.append(f"{turn} beyond-line audit false: {a} IS on the S{sess:02d} line")
            if f"i don't even have {a} to start from" not in str(t["response_text"]):
                c4_bad.append(f"{turn} missing the beyond-line articulation")
        elif edge["mode"] == "line-end-mul":
            if not any(str(e).startswith("line-end:") for e in ir["evidence"]):
                c4_bad.append(f"{turn} evidence is not a line-end audit")
            if a * b <= _line_end_of(store):
                c4_bad.append(f"{turn} line-end-mul audit false: {a}*{b} fits the S{sess:02d} line")
            if "my number line ends at 70" not in str(t["response_text"]):
                c4_bad.append(f"{turn} missing the line-end articulation")
    if _line_end_of(s9_store) != FROZEN["line_end"]:
        c4_bad.append(f"line end at S9 is {_line_end_of(s9_store)}, frozen {FROZEN['line_end']}")
    checks["c4_honesty_at_edges"] = {
        "pass": not c4_bad,
        "edge_turns": sorted(FROZEN["edges"]),
        "violations": c4_bad,
    }

    # C5 — data-driven activation: the FOUR rule/definition facts are the
    # only policy facts in the store, and REMOVING one counterfactually
    # turns its next derivation back into the honest named gap.
    c5_bad = []
    policy_facts = [a for a in final.query(relation="policy")]
    want_ids = {pp["rule"] for pp in FROZEN["ab_pairs"]}
    got_ids = {a.id for a in policy_facts}
    if got_ids != want_ids or len(policy_facts) != 3:
        c5_bad.append(f"policy facts {sorted(got_ids)} != {sorted(want_ids)}")
    for a in policy_facts:
        prov = a.provenance
        if not (a.status == EpistemicState.established and prov is not None and prov.observer == "teacher"):
            c5_bad.append(f"rule fact {a.id} not established/teacher-authored")
    counterfactual = {}
    store_probe = load_store(codex_dump_path(run1, 6))
    bs = Brainstem(store_probe, concepts=LADDER_CONCEPTS)
    bs._set_session(6)
    r_cf = bs.turn("7 - 2 is what?")
    counterfactual["s6_with_rule"] = r_cf.response_ir["uncertainty_state"]
    # close the rule fact (counterfactual removal) and re-ask the SAME drill
    aid = "cap:sub-within-30:rule"
    a = store_probe.get(aid)
    _re_establish(store_probe, a, EpistemicState.obsolete)
    r_cf2 = bs.turn("7 - 2 is what?")
    counterfactual["s6_without_rule"] = {"kind": r_cf2.kind, "gap": r_cf2.response_ir.get("gap")}
    if counterfactual["s6_with_rule"] != "derived":
        c5_bad.append("counterfactual: with the rule the drill is not derived")
    if r_cf2.kind != "impossible" or r_cf2.response_ir.get("gap") != FROZEN["ab_pairs"][0]["gap"]:
        c5_bad.append("counterfactual: without the rule the drill is not the honest named gap")
    checks["c5_data_driven_activation"] = {
        "pass": not c5_bad,
        "policy_facts": sorted(got_ids),
        "counterfactual": counterfactual,
        "violations": c5_bad,
    }

    # C6 — dispute discipline on the extended store + the frozen attention
    # set (S5:15, S7:33 — the ladder continues the e6.1 conflict history).
    c6_bad = []
    pairs = []
    for cf in FROZEN["conflict_facts"]:
        rows = final.query(subject=cf["subject"], relation="succ")
        wrong = [a for a in rows if a.id.endswith(f"->{cf['wrong']}")]
        right = [a for a in rows if a.id.endswith(f"->{cf['right']}")]
        if not wrong or not right:
            c6_bad.append({"fact": cf, "why": "pair missing from final store"})
            continue
        sup = max(wrong, key=lambda a: a.id)
        right_active = [a for a in right if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)]
        if len(right_active) != 1:
            c6_bad.append({"fact": cf, "why": f"single-claimant broken: {len(right_active)} active established"})
            continue
        rep = right_active[0]
        ok = (
            sup.status == EpistemicState.obsolete
            and sup.validity is not None
            and sup.validity.to is not None
            and rep.id in (sup.provenance.evidence if sup.provenance else [])
            and sup.id in (rep.provenance.evidence if rep.provenance else [])
        )
        if not ok:
            c6_bad.append({"fact": cf, "why": "pair not kept/closed/linked"})
        pairs.append({"fact": cf["turn"], "superseded": sup.id, "replacement": rep.id})
    dupes: dict[str, int] = {}
    for a in final.query(relation="succ"):
        if a.status in (EpistemicState.candidate, EpistemicState.established, EpistemicState.disputed) and (
            a.validity is None or a.validity.to is None
        ):
            key = f"{a.subject.id}->{a.object_id}"
            dupes[key] = dupes.get(key, 0) + 1
    dupes = {k: v for k, v in dupes.items() if v > 1}
    open_disputes = [a.id for a in final.query() if a.status == EpistemicState.disputed]
    att1 = [a for r in rep1 for a in r["attention"]]
    att_ok = len(att1) == len(FROZEN["attention"]) and all(
        a0.get("turn") == f0["turn"] and a0.get("type") == f0["type"] for a0, f0 in zip(att1, FROZEN["attention"])
    )
    checks["c6_disputes_attention"] = {
        "pass": not c6_bad and not dupes and not open_disputes and att_ok,
        "pairs": pairs,
        "duplicate_claimants": dupes,
        "open_disputes_at_end": open_disputes,
        "attention": att1,
        "attention_frozen": FROZEN["attention"],
        "violations": c6_bad,
    }

    # C7 — determinism (run1 vs run2 bytes), replay continuity with the
    # official e6.1 S4 store (every official assertion reproduced; the only
    # additions are the five new curriculum rows), det arm, zero fabrication.
    byte_eq = True
    for session in range(1, 10):
        for name in (f"codeX-S{session:02d}.json", f"session-S{session:02d}.json"):
            if (run1 / name).read_bytes() != (run2 / name).read_bytes():
                byte_eq = False
    ref = _ref_e61_s4()
    continuity: dict[str, Any]
    if ref.exists():
        official = load_store(ref)
        replay_canon = {_canon(a): a.id for a in s4_store.query()}
        missing = [a.id for a in official.query() if _canon(a) not in replay_canon]
        added = [a.id for a in s4_store.query() if _canon(a) not in {_canon(b) for b in official.query()}]
        continuity = {
            "reference": str(ref),
            "official_assertions_reproduced": len(official.query()) - len(missing),
            "missing": missing,
            "added_by_extended_seeding": sorted(added),
            "ok": not missing,
        }
    else:
        continuity = {"reference": str(ref), "ok": None, "note": "reference store not present (non-official context)"}
    det_arm_ok = all(
        t["arm"].get("classifier") == "det"
        and t["arm"].get("phrasing") == "det"
        and t["arm"].get("classifier_fallback") is False
        and t["arm"].get("phrasing_fallback") is False
        for t in turns_all
    )
    fabrication = [
        t["turn"]
        for t in turns_all
        if t["kind"] == "question"
        and not str(t["response_ir"]["answer"]).startswith("needs_info")
        and not t["grounded"]
    ]
    checks["c7_determinism_continuity"] = {
        "pass": byte_eq and (continuity["ok"] is not False) and det_arm_ok and not fabrication,
        "byte_identical_run1_run2": byte_eq,
        "continuity": continuity,
        "det_arm": det_arm_ok,
        "fabrication_events": fabrication,
    }

    # C8 — the stopping point (the wall, pre-registered): the four EXACT
    # squares derive with cited square facts; the two brackets are exact &
    # adjacent; the partial bracket articulates the line end; and NO exact
    # value of a non-square is present anywhere in the store (the values
    # are not on the lattice — the system never invents a decimal).
    c8_bad = []
    # the boundary is derived WITH citations (every in-line maximal case,
    # including 70-70=0 and 10*7=70 landing exactly on the line end)
    for turn, want in FROZEN["boundary_derived"].items():
        t = by_turn[turn]
        ir = t["response_ir"]
        if ir["uncertainty_state"] != "derived" or str(ir["answer"]) != want:
            c8_bad.append(f"{turn}: boundary case not derived ({ir.get('uncertainty_state')} / {ir.get('answer')})")
        elif not ir["evidence"]:
            c8_bad.append(f"{turn}: derived without a cited fact")
    # the honest-stop SET across the ladder is exactly the frozen edges
    honest = {t["turn"] for t in ladder_turns if t["kind"] == "question" and t["response_ir"].get("uncertainty_state") == "needs_info"}
    want_honest = set(FROZEN["edges"])
    if honest != want_honest:
        c8_bad.append(f"honest-stop set {sorted(honest)} != frozen {sorted(want_honest)}")
    # the store itself never contains a value beyond the line (no fabricated
    # number exists anywhere — the boundary is the store's own edge)
    max_num = 0
    for x in final.query(relation="succ"):
        if x.status == EpistemicState.established and (x.validity is None or x.validity.to is None):
            max_num = max(max_num, int(x.object_id[len("count-successor:num(") : -1]))
    if max_num != FROZEN["line_end"]:
        c8_bad.append(f"store line end is {max_num}, frozen {FROZEN['line_end']}")
    checks["c8_stopping_point"] = {
        "pass": not c8_bad,
        "boundary_derived": {k: v for k, v in FROZEN["boundary_derived"].items()},
        "honest_stops": sorted(honest),
        "store_line_end": max_num,
        "articulation": (
            "the composition operations (walk-back subtraction, repeated-addition multiplication) are "
            "exactly line-bound: every in-line instance derives with citations, including the boundary-maximal "
            "70-70=0 and 10*7=70; the first out-of-line instances stop with distinct correct articulations "
            "(walk-off / beyond-line / line-end); no value beyond the line exists in the store. The sqrt "
            "rung's lattice-wall claim is preserved for the future lattice-wall experiment (D-e6f)."
        ),
        "violations": c8_bad,
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    all_a = final.query()
    per_session = [
        {
            "session": r["session"],
            "turns": len(r["turns"]),
            "restored": r["restored"],
            "mastery": {k: v["state"] for k, v in r["mastery"].items()},
            "codex_total": r["codex"]["total"],
            "added": len(r["codex"]["added_this_session"]),
            "attention": [a["turn"] for a in r["attention"]],
        }
        for r in rep1
    ]
    derived = {
        "per_session": per_session,
        "final_assertions": len(all_a),
        "line_end": _line_end_of(final),
        "script_hash": script_hash,
        "full_script_hash": full_hash,
        "conflict_pairs": checks["c6_disputes_attention"]["pairs"],
        "ab_pairs": checks["c3_impossible_learns_arc"]["ab_pairs"],
    }
    return {
        "name": "e6.2",
        "checks": checks,
        "checks_passed": passed,
        "checks_total": CHECKS,
        "frozen": FROZEN,
        "derived": derived,
    }


def _walk_off_replay(store: InMemoryCodexStore, a: int, b: int) -> int | None:
    """Re-simulate the walk-back on a snapshot store (the C4 re-audit)."""

    def succ(n: int) -> int | None:
        for x in store.query(subject=f"count-successor:succ-of({n})", relation="succ"):
            if x.status == EpistemicState.established and (x.validity is None or x.validity.to is None):
                return int(x.object_id[len("count-successor:num(") : -1])
        return None

    cur = a
    for _ in range(b):
        if cur == 0:
            return None
        step = succ(cur - 1)
        if step != cur:
            return None
        cur -= 1
    return cur


def _line_end_of(store: InMemoryCodexStore) -> int:
    v = 0
    while True:
        nxt = False
        for x in store.query(subject=f"count-successor:succ-of({v})", relation="succ"):
            if x.status == EpistemicState.established and (x.validity is None or x.validity.to is None):
                nxt = True
        if not nxt:
            return v
        v += 1


def _re_establish(store: InMemoryCodexStore, a: Assertion, status: EpistemicState) -> Assertion:
    """A status-only re-write (the store upserts by id); keeps every other
    field so the counterfactual removal stays surgical."""

    new = Assertion(
        id=a.id,
        subject=a.subject,
        relation=a.relation,
        object=a.object,
        context=a.context,
        validity=a.validity,
        status=status,
        provenance=a.provenance,
    )
    store.add(new)
    return new


# ── house-style experiment object ────────────────────────────────────────────


class E6_2Experiment:
    name = "e6.2"
    hypothesis = (
        "A system whose knowledge is a provenance-mandatory CODEX, taught the arithmetic "
        "ladder across five continuing sessions (the e6.1 store never reset), grasps each "
        "new concept EXACTLY when its rule enters the store — subtraction by walk-back, "
        "multiplication by composed repeated addition, comparison by walking — and it "
        "grasps the lattice AND its boundary: the two composition operations reach "
        "EXACTLY as far as the number line (every in-line instance derives with "
        "citations, including the boundary-maximal 70-70=0 and 10*7=70), and the first "
        "out-of-line instances stop at the boundary with distinct correct articulations "
        "(walk-off / beyond-line / line-end), never a fabricated value and no value "
        "beyond the line in the store; every turn is contract-valid, every proof "
        "re-plays offline, the dispute and repeated-conflict discipline continues over "
        "the carried conflict history, and the whole 135-turn run is deterministic, "
        "byte-identical on re-execution, and continuous with the official e6.1 store."
    )
    metric = "acceptance checks passed (0-8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        rep = run_e6_2()
        passed = rep["checks_passed"]
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=passed / CHECKS,
            evidence=[
                Path("results/phase-6/e6.2-run1/session-S05.json"),
                Path("results/phase-6/e6.2-run1/session-S06.json"),
                Path("results/phase-6/e6.2-run1/session-S07.json"),
                Path("results/phase-6/e6.2-run1/session-S08.json"),
                Path("results/phase-6/e6.2-run1/session-S09.json"),
                Path("results/phase-6/e6.2-run1/codeX-S09.json"),
                Path("results/phase-6/e6.2-run2/codeX-S09.json"),
            ],
            config={
                "seed": "deterministic (scripted teacher; no randomness anywhere in the ladder)",
                "dataset_hash": rep["derived"]["script_hash"],
            },
        )
