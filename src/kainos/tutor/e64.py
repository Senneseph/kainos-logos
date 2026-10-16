"""E6.4 — "Phrasology: learning to parse in its own way".

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md
section E6.4 (mechanism D-e6i, M1–M8). Phrasings are STORE FACTS
(relation phrasing-map): a learned parse maps a NEW template onto
one of the six frozen canonical templates. The frozen grammar stays
canonical (it runs first and wins); the established lexicon
consults ONLY where the grammar honestly says ambiguous. Parse !=
content: a learned-parse turn's response IR is byte-comparable to
its canonical twin (the grounded policies are unchanged — only the
intake mapping is learned). Unknown phrasings stay honestly
ambiguous (named "teach me the mapping"); no LLM rescue.

The run continues from the OFFICIAL e6.3 loop's final store (182
assertions, all six concepts stable, line end 70), seeded as
codeX-S01.json; sessions S2–S4 teach six phrasing families (one of
them wrong-then-corrected), and the surface wall is checked: taught
families parse 100%, untaught probes never parse, the line cap
semantics compose THROUGH learned phrasings, and two runs are
byte-identical.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.projection.contract import validate_response
from kainos.tutor.brainstem import REL_PHRASING, det_classify
from kainos.tutor.mastery import Concept, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E64", "FROZEN", "E6_4Experiment", "run_e6_4"]

CHECKS = 8

#: The official e6.3 loop's final store (the seed; M8), repo-relative.
E63_SEED = Path("results/phase-6/e6.3-run1/codeX-S03.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E63_SEED.exists():
        return E63_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E63_SEED
    return alt if alt.exists() else E63_SEED

#: The E6.4 curriculum: the six e6.3 concepts + the phrasology strip.
CONCEPTS_E64: tuple = InfantRuntime.PILOT_CONCEPTS + (
    Concept("phrasology", "Phrasology — learned intake phrasings", "k-5", "language"),
)

FROZEN: dict = {
    "seed": str(E63_SEED),
    "sessions": [2, 3, 4],
    "seed_total": 182,  # assertions in the official e6.3 S3 store
    "line_end_start": 70,
    "line_end_final": 72,  # after S3:05/06 (71) and S4:06/07 (72)
    "script": {
        2: [
            "what is the sum of 6 and 7?",
            "what number follows 11?",
            'the phrasing "what is the sum of {a} and {b}?" is the same as "{a} + {b} is what?"',
            "what is the sum of 6 and 7?",
            "6 + 7 is what?",
            "19 + 5 is what?",
            'the phrasing "what number follows {n}?" is the same as "what comes after {n}?"',
            "what number follows 11?",
            "what comes after 11?",
            'the phrasing "how many are left if you take {b} away from {a}?" is the same as "{a} - {b} is what?"',
            "how many are left if you take 5 away from 16?",
            "16 - 5 is what?",
            "is 25 bigger than 6?",
            'the phrasing "is {a} bigger than {b}?" is the same as "{a} - {b} is what?"',
            "is 17 bigger than 9?",
            'no — that was a mistake; the phrasing "is {a} bigger than {b}?" is the same as "is {a} larger than {b}?"',
            "is 17 bigger than 9?",
            "is 17 larger than 9?",
        ],
        3: [
            'the phrasing "what do you get when you count {a}, {b} times?" is the same as "{a} * {b} is what?"',
            "what do you get when you count 6, 7 times?",
            "6 * 7 is what?",
            'the phrasing "the number after {a} is {b}" is the same as "after {a} comes {b}"',
            "after 70 comes 71",
            "the number after 55 is 56",
            "after 55 comes 56",
            "how many are left if you take 3 away from 100?",
            "could you explain what the number 7 means?",
            "what is the sum of 12 and 9?",
            "what number follows 70?",
            "is 48 bigger than 52?",
            "what do you get when you count 9, 7 times?",
        ],
        4: [
            "what is the sum of 4 and 4?",
            "what number follows 45?",
            "how many are left if you take 7 away from 20?",
            "is 64 bigger than 25?",
            "what do you get when you count 5, 6 times?",
            "after 71 comes 72",
            "the number after 40 is 41",
            "after 40 comes 41",
            "how tall is the number 5, exactly?",
            "what is the sum of 30 and 30?",
            "is 7 bigger than 7?",
        ],
    },
    "total_turns": 42,
    # A/B arc pairs (frozen P2): (before_ref, after_ref)
    "ab_pairs": [
        ("S02:01", "S02:04"),
        ("S02:02", "S02:08"),
        ("S02:13", "S02:17"),
    ],
    # the standing unknowns: never parse, in ANY session (frozen refs)
    "unknown_probes": {
        "could you explain what the number 7 means?": "S03:09",
        "how tall is the number 5, exactly?": "S04:09",
    },
    # byte-comparable twins (frozen P3): (learned_ref, canonical_ref) — the
    # SAME question, one learned phrasing vs its canonical form
    "twin_pairs": [
        ("S02:04", "S02:05"),
        ("S02:08", "S02:09"),
        ("S02:11", "S02:12"),
        ("S02:17", "S02:18"),
        ("S03:02", "S03:03"),
        # lesson twins corroborate an EXISTING (seed) fact on both sides, so
        # the epistemic state-at-moment is the same on both (P3)
        ("S03:06", "S03:07"),
        ("S04:07", "S04:08"),
    ],
    # the wrong-mapping arc (frozen P2): the WRONG answer while the wrong
    # mapping is in effect (S02:15), the corrected one after (S02:17)
    "wrong_mapping": {"taught_at": "S02:14", "wrong_probe": "S02:15", "corrected_at": "S02:16", "after_probe": "S02:17"},
    "phrasing_lessons": 7,  # mapping facts written (6 distinct phrasings; one corrected)
    "phrasing_established_final": 6,
    "phrasing_superseded_final": 1,
    "unknown_articulation": "teach me the mapping",
    "boundary_probes": {"S03:08": "line-end"},  # learned phrasing + boundary semantics compose
}


#: frozen dataset identity
SCRIPT_HASH = hashlib.sha256(
    json.dumps({s: [t for t in ls] for s, ls in sorted(FROZEN["script"].items())}, sort_keys=True).encode("utf-8")
).hexdigest()[:16]


def _line_end(store) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid, oid = a.subject.id, a.object_id
        if sid.startswith("count-successor:succ-of(") and oid.startswith("count-successor:num(") and (a.validity is None or a.validity.to is None):
            end = max(end, int(oid[len("count-successor:num(") : -1]))
    return end


def _fresh_store(root: Path, s: int):
    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        return InMemoryCodexStore()
    return load_store(p)


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E64)
    out: list[dict] = []
    for s in FROZEN["sessions"]:
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P7: the seed dump is the official e6.3 S3 store, id-for-id."""

    seed_path = _resolve_seed()
    seed = load_store(seed_path) if seed_path.exists() else None
    pre = _fresh_store(root, 2)
    seed_ids = {a.id for a in seed.query()} if seed is not None else set()
    pre_ids = {a.id for a in pre.query()}
    return {"seed_total": len(seed_ids), "reproduced_in_s2_pre": len(seed_ids & pre_ids), "missing": sorted(seed_ids - pre_ids)}


def _default_out_dir() -> Path:
    base = Path(os.environ.get("KAINOS_RESULTS_DIR", "results")) / "phase-6"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_e6_4(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.3 S3 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P1–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = {}
    for name in ("e6.4-run1", "e6.4-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.3 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed (M8)
        runs[name] = _run_once(root)
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.4-run1", "e6.4-run2"):
        (out_dir / name / "e6.4-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.4-run1"]:
        for t in srow.get("turns", []):
            turns[t["turn"]] = {
                "surface": t["surface"],
                "kind": t["kind"],
                "concept": t["concept"],
                "arm": t["arm"],
                "grounded": t["grounded"],
                "contract_valid": t["contract_valid"],
                "response_ir": t["response_ir"],
                "response_text": t["response_text"],
                "parse_source": t["response_ir"].get("parse_source"),
                "memory_diff": t["memory_diff"],
                "attention": t["attention"],
            }
    return {
        "arm": {"classifier": "det", "llm_arm": "skipped-no-backend", "note": "hermetic official: no Ollama, no backend"},
        "turns": turns,
        "seed": str(E63_SEED),
        "script_hash": SCRIPT_HASH,
    }


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.4-run1"

    # P1 — script & contract
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the A/B arc + the standing unknowns
    p2_bad: list[str] = []
    for before, after in FROZEN["ab_pairs"]:
        b, a = turns.get(before), turns.get(after)
        if b is None or a is None:
            p2_bad.append(f"missing {before}/{after}")
            continue
        if b["kind"] not in ("ambiguous",):
            p2_bad.append(f"{before}: not honestly ambiguous before (got {b['kind']})")
        if b["memory_diff"]:
            p2_bad.append(f"{before}: an unknown phrasing wrote the store")
        if a["kind"] == "ambiguous" or a["parse_source"] is None or not a["parse_source"].startswith("lexicon:"):
            p2_bad.append(f"{after}: not parsed via the lexicon after teaching")
    before_sum = turns.get("S02:01", {})
    after_sum = turns.get("S02:04", {})
    if before_sum.get("kind") == "ambiguous" and "mapping" not in (before_sum.get("response_text") or ""):
        p2_bad.append("S02:01: the unknown articulation must name the mapping gap")
    if after_sum and (after_sum.get("response_ir") or {}).get("answer") != "13":
        p2_bad.append(f"S02:04: expected 13 (got {after_sum.get('response_ir', {}).get('answer')})")
    for up, ref in FROZEN["unknown_probes"].items():
        surface = (turns.get(ref, {}) or {}).get("surface") or ""
        if up not in surface:
            p2_bad.append(f"{ref}: the frozen unknown probe is not there")
        if turns.get(ref, {}).get("kind") != "ambiguous":
            p2_bad.append(f"{ref}: an untaught phrasing parsed")
    wm = FROZEN["wrong_mapping"]
    wrong_t = turns.get(wm["wrong_probe"])
    after_t = turns.get(wm["after_probe"])
    if wrong_t and (wrong_t.get("response_ir") or {}).get("answer") != "8":
        p2_bad.append(f"{wm['wrong_probe']}: the wrong mapping must answer the subtraction (8) — got {wrong_t.get('response_ir', {}).get('answer') if wrong_t else None}")
    if after_t and not (after_t.get("response_text") or "").startswith("yes"):
        p2_bad.append(f"{wm['after_probe']}: the corrected mapping must answer the comparison")
    checks["p2_ab_arc"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — parse != content (byte-comparable twins)
    p3_bad: list[str] = []
    for learned, canon in FROZEN["twin_pairs"]:
        l, c = turns.get(learned), turns.get(canon)
        if l is None or c is None:
            p3_bad.append(f"missing twin {learned}/{canon}")
            continue
        li, ci = dict(l["response_ir"]), dict(c["response_ir"])
        ps_l, ps_c = li.pop("parse_source", None), ci.pop("parse_source", None)
        if ps_l is None or not ps_l.startswith("lexicon:") or ps_c != "grammar":
            p3_bad.append(f"{learned}/{canon}: parse_source {ps_l}/{ps_c}")
        # the provenance 'turn:<ref>' marker is the when-confirmed audit,
        # not content: strip it, compare everything else byte-for-byte
        if "provenance" in li:
            li["provenance"] = [x for x in li["provenance"] if not str(x).startswith("turn:")]
        if "provenance" in ci:
            ci["provenance"] = [x for x in ci["provenance"] if not str(x).startswith("turn:")]
        if li != ci:
            p3_bad.append(f"{learned}/{canon}: the IRs differ beyond parse_source: {li} vs {ci}")
        if l["response_text"] != c["response_text"]:
            p3_bad.append(f"{learned}/{canon}: the response texts differ")
    checks["p3_parse_not_content"] = {"pass": not p3_bad, "bad": p3_bad, "twin_pairs": FROZEN["twin_pairs"]}

    # P4 — re-auditable parses + the phrasing-fact audit
    p4_bad: list[str] = []
    final = _fresh_store(run1_root, 4)
    phrasings = [a for a in final.query(relation=REL_PHRASING)]
    established = [a for a in phrasings if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)]
    superseded = [a for a in phrasings if a.status == EpistemicState.obsolete]
    if len(phrasings) != FROZEN["phrasing_lessons"]:
        p4_bad.append(f"{len(phrasings)} phrasing facts != {FROZEN['phrasing_lessons']} lessons")
    if len(established) != FROZEN["phrasing_established_final"]:
        p4_bad.append(f"{len(established)} established != {FROZEN['phrasing_established_final']}")
    if len(superseded) != FROZEN["phrasing_superseded_final"]:
        p4_bad.append(f"{len(superseded)} superseded != {FROZEN['phrasing_superseded_final']} (the wrong mapping stays, closed)")
    open_disp = [a for a in phrasings if a.status == EpistemicState.disputed]
    if open_disp:
        p4_bad.append(f"open-disputed phrasing facts: {[a.id for a in open_disp]}")
    dupes = [a for a in established if sum(1 for b in established if b.subject.id == a.subject.id) > 1]
    if dupes:
        p4_bad.append(f"duplicate active claimants: {[a.id for a in dupes]}")
    # offline template re-instantiation for every lexicon turn
    for ref, t in turns.items():
        ps = t.get("parse_source") or ""
        if not ps.startswith("lexicon:"):
            continue
        fact = final.get(ps.split(":", 1)[1])
        if fact is None:
            p4_bad.append(f"{ref}: the phrasing fact {ps} is gone from the final store")
            continue
        new_tpl = fact.context.data["new"]
        parts = re.split(r"(\{[a-z]+\})", new_tpl)
        rx = re.compile("".join(r"(\d+)" if part.startswith("{") else re.escape(part) for part in parts) + r"\Z")
        m = rx.match(t["surface"])
        if m is None:
            p4_bad.append(f"{ref}: the stored template does not re-instantiate on its own turn text")
    # the correction pair is linked
    corr = [a for a in final.query(context_match={"kind": "mastery-event", "concept": "phrasology"}) if a.object_id == "correction"]
    if len(corr) != 1:
        p4_bad.append(f"{len(corr)} phrasology correction events != 1")
    checks["p4_reauditable_facts"] = {"pass": not p4_bad, "bad": p4_bad, "facts": len(phrasings), "established": len(established), "superseded": len(superseded)}

    # P5 — grammar first, lexicon extends, parse_source passes contracts
    p5_bad: list[str] = []
    for ref, t in turns.items():
        if t["kind"] == "ambiguous":
            continue
        ps = t.get("parse_source")
        g_kind, _ = det_classify(t["surface"])
        if g_kind != "ambiguous":
            if ps != "grammar":
                p5_bad.append(f"{ref}: the grammar matches but parse_source={ps}")
        else:
            if ps is None or not ps.startswith("lexicon:"):
                p5_bad.append(f"{ref}: not grammar and not lexicon (parse_source={ps})")
        valid, _v = validate_response(t["response_ir"], t["kind"])
        if not valid:
            p5_bad.append(f"{ref}: the parse_source field breaks the contract")
    checks["p5_grammar_first"] = {"pass": not p5_bad, "bad": p5_bad}

    # P6 — honest unknowns, no rescue
    p6_bad: list[str] = []
    unknown_refs = [r for r, t in turns.items() if t["kind"] == "ambiguous"]
    for ref in unknown_refs:
        t = turns[ref]
        if "teach me the mapping" not in (t["response_text"] or ""):
            p6_bad.append(f"{ref}: the frozen unknown-phrasing articulation is missing")
        if t["memory_diff"]:
            p6_bad.append(f"{ref}: an ambiguous turn wrote the store")
    checks["p6_honest_unknowns"] = {"pass": not p6_bad, "bad": p6_bad, "ambiguous_refs": sorted(unknown_refs)}

    # P7 — seed continuity + determinism + no fabrication
    p7_bad: list[str] = []
    seed_check = _seed_check(run1_root)
    if seed_check["seed_total"] != FROZEN["seed_total"] or seed_check["reproduced_in_s2_pre"] != FROZEN["seed_total"]:
        p7_bad.append(f"seed continuity: {seed_check}")
    files_a = sorted(x.name for x in (out_dir / "e6.4-run1").iterdir() if x.is_file())
    files_b = sorted(x.name for x in (out_dir / "e6.4-run2").iterdir() if x.is_file())
    identical = files_a == files_b and all(
        hashlib.sha256((out_dir / "e6.4-run1" / f).read_bytes()).hexdigest() == hashlib.sha256((out_dir / "e6.4-run2" / f).read_bytes()).hexdigest() for f in files_a
    )
    if not identical:
        p7_bad.append(f"run1 != run2 ({files_a} vs {files_b})")
    if _line_end(final) != FROZEN["line_end_final"]:
        p7_bad.append(f"final line end {_line_end(final)} != {FROZEN['line_end_final']}")
    det_arm_ok = all(t["arm"].get("classifier") == "det" for t in turns.values())
    if not det_arm_ok:
        p7_bad.append("a turn was not served by the det arm")
    fab = [
        r
        for r, t in turns.items()
        if t["kind"] == "question" and not str(t["response_ir"].get("answer", "")).startswith("needs_info") and not t["grounded"]
    ]
    if fab:
        p7_bad.append(f"fabrication turns (ungrounded answer): {sorted(fab)}")
    checks["p7_continuity_determinism"] = {
        "pass": not p7_bad,
        "bad": p7_bad,
        "seed": seed_check,
        "files": files_a,
        "line_end_final": _line_end(final),
        "det_arm": det_arm_ok,
        "fabrication_events": fab,
    }

    # P8 — the surface wall
    p8_bad: list[str] = []
    # a learned parse may never appear BEFORE its own lesson (ordering)
    def lesson_ref_for(new_tpl: str):
        for sn, lines in sorted(FROZEN["script"].items()):
            for tn, line in enumerate(lines, 1):
                if f'"{new_tpl}" is the same as' in line:
                    return f"S{sn:02d}:{tn:02d}"
        return None

    for ref, t in turns.items():
        ps = t.get("parse_source") or ""
        if not ps.startswith("lexicon:"):
            continue
        fact = final.get(ps.split(":", 1)[1])
        lr = lesson_ref_for(fact.context.data["new"]) if fact is not None else None
        if lr is None:
            p8_bad.append(f"{ref}: the applied phrasing was never taught")
            continue
        s, tn = int(ref.split(":")[0][1:]), int(ref.split(":")[1])
        ls, lt = int(lr.split(":")[0][1:]), int(lr.split(":")[1])
        if (s, tn) < (ls, lt):
            p8_bad.append(f"{ref}: a learned parse BEFORE its lesson {lr}")
    # the learned-phrasing boundary probe (S03:07) must stop at the honest
    # line-end boundary (learned surface + grounded semantics compose)
    bp = turns.get("S03:08")
    if bp is None:
        p8_bad.append("S03:08 missing")
    else:
        if (bp["response_ir"] or {}).get("uncertainty_state") != "needs_info":
            p8_bad.append("S03:08: the boundary probe must be honest needs_info")
        if "i don't even have" not in (bp["response_text"] or ""):
            p8_bad.append(f"S03:08: the line-end articulation is missing: {(bp['response_text'] or '')[:80]}")
    # the phrasology strip reached stable (P7 trajectory folded here)
    mastery4 = None
    s4_report = json.loads((run1_root / "session-S04.json").read_text())
    mastery4 = s4_report["mastery"].get("phrasology", {})
    if mastery4.get("state") != "stable":
        p8_bad.append(f"phrasology final state {mastery4.get('state')} != stable")
    if mastery4.get("correct_derivations", 0) < 4:
        p8_bad.append(f"phrasology applications {mastery4.get('correct_derivations')} < 4 (K)")
    checks["p8_surface_wall"] = {"pass": not p8_bad, "bad": p8_bad, "phrasology": mastery4}

    passed = sum(1 for c in checks.values() if c["pass"])
    return {"checks": checks, "passed": passed, "value": round(passed / CHECKS, 4)}


class E6_4Experiment:
    """E6.4 — phrasology (the intake becomes a curriculum strip)."""

    name = "e6.4"
    hypothesis = (
        "Phrasings are store facts: taught by their frozen lesson forms, applied only where "
        "the grammar honestly says ambiguous, byte-comparable in content to their canonical "
        "twins, corrected through the existing single-current-claimant pair — so the infant's "
        "INTAKE boundary is exactly its lexicon: every taught phrasing family parses (and "
        "composes with the grounded layer, including the line-cap semantics) and every "
        "untouched phrasing stays an honestly named ambiguity, all with the run "
        "two-runs-byte-identical and seed-continuous with the official e6.3 store."
    )
    metric = "phrasology checks passed (P1..P8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_4()
        if "error" in report:
            return Result(name=self.name, passed=False, value=0.0, evidence=[Path("results/phase-6")], config={"seed": FROZEN["seed"], "error": report["error"]})
        return Result(
            name=self.name,
            passed=report["passed"] == CHECKS,
            value=report["value"],
            evidence=[
                Path("results/phase-6/e6.4-run1/session-S02.json"),
                Path("results/phase-6/e6.4-run1/session-S03.json"),
                Path("results/phase-6/e6.4-run1/session-S04.json"),
                Path("results/phase-6/e6.4-run1/codeX-S04.json"),
                Path("results/phase-6/e6.4-run2/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "seed_assertions": FROZEN["seed_total"],
                "script_hash": SCRIPT_HASH,
            },
        )
