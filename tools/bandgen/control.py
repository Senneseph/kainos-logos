"""The control (bandgen v0.1): dry-run the spec, capture the
mechanism's own output, build the frozen-shape table, and report the
diff between the spec's declarations/predictions and the mechanism.

The compiler never edits the mechanism: it drives the runtime exactly
as the experiments do (boot/turn/lapse), captures the session dumps,
and reports. The D-e6z deviation classes (hand letters, hand counts,
hand beds, hand carries, hand pre-states) all surface here as
prediction-vs-mechanism diffs on a clean, reviewable report — at SPEC
time, not at build time.
"""

from __future__ import annotations

import importlib
import json
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from kainos.tutor import brainstem as B
from kainos.tutor.session import load_store

from . import reflib, storeio
from .spec import REPO_ROOT, structural_checks


def turn_letter(t: dict[str, Any]) -> str:
    """The e614 letter mapping — the house's canonical domain letters
    (L lesson teach, U impossible/gap, F part-set failure, T
    derive-success, C conditional, H honest wall, S derived). Mirrors
    the experiments' ``_turn_domain`` exactly."""
    if t["kind"] == "assertion" and (t["slots"] or {}).get("lemma"):
        return "L"
    if t["kind"] == "ambiguous":
        # LOUD by design: an ambiguous turn must never read as a clean
        # 'S' in the letters — the spec author must see it and fix the
        # surface (the silent-S vacuum that let a mis-phrased S14
        # probe slide through the S03:13 check, 2026-08-24).
        return "A"
    if t["kind"] == "impossible":
        return "U"
    ir = t["response_ir"] or {}
    mode = (t["slots"] or {}).get("mode")
    if mode == "derive":
        return "T" if ir.get("uncertainty_state") == "derived" else "F"
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if ir.get("uncertainty_state") == "conditional":
        return "C"
    return "S"


def turn_answer(t: dict[str, Any]) -> str | None:
    return (t.get("response_ir") or {}).get("answer")


def _seeded_registry(spec: dict[str, Any]) -> tuple:
    """Resolve spec.registry as 'module:ATTR' (the house chain:
    CONCEPTS_E617 = CONCEPTS_E616 + the S13 concepts, and so on up).
    The spec's band concepts must all be IN the registry — the
    dry-run boots the mechanism's own carried registry."""
    name = spec.get("registry")
    if not name or ":" not in name:
        raise ValueError("spec.registry must be 'module:ATTR' (e.g. 'kainos.tutor.e617:CONCEPTS_E617')")
    mod_name, attr = name.rsplit(":", 1)
    mod = importlib.import_module(mod_name)
    reg = getattr(mod, attr)
    ids = [c.id for c in reg]
    for c in spec["band"]["concepts"]:
        if c["id"] not in ids:
            raise ValueError(
                f"band concept {c['id']!r} is not in the booted registry {name} — "
                "the brainstem module for this band must be merged before the dry-run"
            )
    return reg


SPECIAL_KINDS = {"wall", "zero_derive", "zero_touch", "unclassified", "gap", "teach", "scaffold", "missing_parts", "carry"}


def run_control(spec: dict[str, Any], workdir: str | Path | None = None) -> dict[str, Any]:
    """Run the full control; returns the report:
    {ok, spec, checks: {name: {pass, bad[]}}, table: <frozen shape>,
    computed_beds, carry_map}."""
    checks: dict[str, dict[str, Any]] = {}
    bad: list[str] = []

    # C0 — structural (schema was validated at load; this is the
    # curriculum-logic layer).
    bad = structural_checks(spec)
    checks["c0_structural"] = {"pass": not bad, "bad": bad}
    if bad:
        return {"ok": False, "spec": spec["id"], "checks": checks, "table": {}, "computed_beds": {}, "carry_map": {}}

    registry = _seeded_registry(spec)
    seed_path = REPO_ROOT / spec["seed"]["store"]
    sessions = spec["sessions"]
    script: dict[int, list[str]] = {s: [] for s in sessions}
    turns = spec["turns"]
    by_ref: dict[str, dict[str, Any]] = {}
    for t in turns:
        script[int(t["ref"][1:3])].append(t["question"])
        by_ref[t["ref"]] = t

    # C1 — the seed (identity / total / line end, computed).
    seed = load_store(seed_path)
    c1: list[str] = []
    ident = storeio.store_identity(seed)
    total = len(seed.query())
    lend = storeio.line_end(seed)
    if ident != spec["seed"]["identity"]:
        c1.append(f"seed identity {ident} != declared {spec['seed']['identity']}")
    if total != spec["seed"]["total"]:
        c1.append(f"seed total {total} != declared {spec['seed']['total']}")
    if lend != spec["seed"]["line_end"]:
        c1.append(f"seed line end {lend} != declared {spec['seed']['line_end']}")
    checks["c1_seed"] = {"pass": not c1, "bad": c1, "identity": ident, "total": total, "line_end": lend}

    # C2 — the computed beds against the reference registry.
    c2: list[str] = []
    computed_beds: dict[str, Any] = {}
    for b in spec.get("beds", []):
        try:
            val = reflib.evaluate(b["ref"], b.get("args", {})) if "ref" in b else b["value"]
            render = b.get("render", "json")
            computed_beds[b["key"]] = (
                reflib.RENDERERS[render](val) if "ref" in b else val
            )
        except (KeyError, TypeError, ValueError, ArithmeticError) as e:
            c2.append(f"bed {b['key']}: {e!r}")
    checks["c2_beds"] = {"pass": not c2, "bad": c2}

    # C3 — the dry-runs (main x2 for the determinism twin + carry).
    work = Path(workdir) if workdir else Path(tempfile.gettempdir()) / "bandgen-scratch" / spec["id"]
    run1_root, run2_root, carry_root = work / "run1", work / "run2", work / "carry"
    for r in (run1_root, run2_root, carry_root):
        storeio.place_seed(seed_path, r)
    dump1 = storeio.run_main(run1_root, sessions, list(registry), script)
    dump2 = storeio.run_main(run2_root, sessions, list(registry), script)
    carry_surfaces = [t["question"] for t in turns if t["kind"] == "carry"]
    carry_surfaces += [o["question"] for o in spec.get("offscript", [])]
    carry_runs = storeio.run_carry(carry_root, list(registry), carry_surfaces) if carry_surfaces else []

    # Collect per-ref captured turns.
    captured: dict[str, dict[str, Any]] = {}
    for s in sessions:
        row = next(x for x in dump1 if x["session"] == s)
        ts = row["turns"]
        for j, t in enumerate(ts, start=1):
            captured[f"S{s:02d}:{j:02d}"] = t
    if len(captured) != len(turns):
        checks["c3_capture"] = {"pass": False, "bad": [f"captured {len(captured)} turns != {len(turns)} declared"]}
        return {"ok": False, "spec": spec["id"], "checks": checks, "table": {}, "computed_beds": computed_beds, "carry_map": {}}

    final = storeio.fresh_final(run1_root, max(sessions))
    final_ids = {a.id for a in final.query()}

    # C4 — the letters (the e614 mapping over the captured turns).
    c4: list[str] = []
    letters: dict[str, str] = {}
    for s in sessions:
        letters[str(s)] = "".join(turn_letter(captured[f"S{s:02d}:{j:02d}"]) for j in range(1, len(script[s]) + 1))
        want = spec["expect"]["letters"].get(str(s), "")
        if want and want != letters[str(s)]:
            c4.append(f"session {s}: predicted letters {want!r} != mechanism {letters[str(s)]!r}")
    checks["c4_letters"] = {"pass": not c4, "bad": c4, "letters": letters}

    # C5 — per-kind semantic checks (the spec declarations vs the
    # captured mechanism bytes).
    c5: list[str] = []
    gaps: dict[str, str] = {}
    teach: dict[str, str] = {}
    scf: dict[str, str] = {}
    mpf: dict[str, str] = {}
    dvs: dict[str, Any] = {}
    walls: dict[str, str] = {}
    wall_art: dict[str, list[str]] = {}
    beds_exact: dict[str, str] = {}
    bed_grounded: dict[str, list[str]] = {}
    bed_owners: dict[str, str] = {}
    thm_allowed: dict[str, list[str]] = {}
    derived: dict[str, str] = {}
    zero_derive_text = ""
    zero_touch_text = ""
    unclassified_text = ""
    carry_refs: list[str] = []

    for ref in sorted(by_ref):
        t = by_ref[ref]
        cap = captured[ref]
        kind = t["kind"]
        ans = turn_answer(cap)
        if kind == "gap":
            gap = (cap["response_ir"] or {}).get("gap") or ""
            if not gap.endswith(t["fragment"]):
                c5.append(f"{ref}: gap byte {gap!r} does not name the declared fragment {t['fragment']!r}")
            gaps[ref] = t["fragment"]
        elif kind == "teach":
            fid = f"lemma:{t['lesson']}"
            if fid not in final_ids:
                c5.append(f"{ref}: taught lesson {fid} is not in the final store")
            elif turn_letter(cap) != "L":
                c5.append(f"{ref}: teach turn did not take the lesson slot (letter {turn_letter(cap)})")
            teach[ref] = fid
        elif kind == "derive":
            if turn_letter(cap) != "T":
                c5.append(f"{ref}: derive turn letter {turn_letter(cap)} != T")
            fid = f"theorem:{t['theorem']}"
            if fid not in final_ids:
                c5.append(f"{ref}: derived theorem {fid} is not in the final store")
            dvs[ref] = [t["theorem"], [f"lemma:{p}" if not p.startswith("lemma:") else p for p in t["parts"]]]
        elif kind == "scaffold":
            ir = cap["response_ir"] or {}
            if ir.get("uncertainty_state") != "needs_info":
                c5.append(f"{ref}: the part-set failure is not needs_info ({ir.get('uncertainty_state')})")
            if t["expected"] not in (ans or ""):
                c5.append(f"{ref}: scaffold articulation missing: {ans!r}... != declared fragment {t['expected'][:50]!r}")
            if cap.get("grounded"):
                c5.append(f"{ref}: a scaffold failure cited evidence (fabrication)")
            if cap.get("memory_diff"):
                c5.append(f"{ref}: a scaffold failure wrote the store")
            scf[ref] = t["expected"]
        elif kind == "missing_parts":
            ir = cap["response_ir"] or {}
            if ir.get("uncertainty_state") != "needs_info":
                c5.append(f"{ref}: the missing-part articulation is not needs_info ({ir.get('uncertainty_state')})")
            if t["expected"] not in (ans or ""):
                c5.append(f"{ref}: missing-part articulation missing: {ans!r}... != declared fragment {t['expected'][:50]!r}")
            if cap.get("grounded"):
                c5.append(f"{ref}: a missing-part articulation cited evidence (fabrication)")
            if cap.get("memory_diff"):
                c5.append(f"{ref}: a missing-part articulation wrote the store")
            mpf[ref] = t["expected"]
        elif kind == "wall":
            w = t["wall"]
            if ans != w["text"]:
                c5.append(f"{ref}: wall byte drift: {ans!r} != declared {w['text'][:60]!r}...")
            for frag in w["articulation"]:
                if frag not in (ans or ""):
                    c5.append(f"{ref}: wall articulation fragment missing: {frag!r}")
            walls[ref] = w["text"]
            wall_art[ref] = list(w["articulation"])
        elif kind == "zero_derive":
            # S4:10-class: the mechanism's impossible-run has no ir
            # answer — the frozen byte is the RESPONSE TEXT.
            zans = cap.get("response_text") or ""
            if zans != t["expected"]:
                c5.append(f"{ref}: zero-derive text drift: {zans[:60]!r}... != declared")
            zero_derive_text = t["expected"]
        elif kind == "zero_touch":
            if ans != t["expected"]:
                c5.append(f"{ref}: zero-touch byte drift")
            zero_touch_text = t["expected"]
        elif kind == "unclassified":
            if ans != t["expected"]:
                c5.append(f"{ref}: unclassified byte drift")
            unclassified_text = t["expected"]
        elif kind == "carry":
            carry_refs.append(ref)
        bed = t.get("bed")
        if bed:
            if bed["expect"] == "literal":
                if ans != bed["value"]:
                    c5.append(f"{ref}: bed byte {ans!r} != declared literal {bed['value'][:60]!r}...")
            else:
                val = reflib.evaluate(bed["ref"], bed.get("args", {}))
                if isinstance(val, tuple) and len(val) == 2 and isinstance(val[1], str):
                    rendered = val[1]  # (prime, word) shapes like removal_max
                elif isinstance(val, Fraction):
                    rendered = reflib.RENDERERS["frac_words"](val)
                else:
                    rendered = str(val)
                tmpl = bed.get("template", "{v}")
                want = tmpl.format(v=rendered)
                if ans != want:
                    c5.append(f"{ref}: bed byte {ans!r} != reference rendering {want[:60]!r}...")
            beds_exact[ref] = ans or ""
            bed_grounded[ref] = list(bed["grounds"])
            bed_owners[ref] = bed["owner"]
            for g in bed["grounds"]:
                if g not in final_ids:
                    c5.append(f"{ref}: bed ground {g!r} is not in the final store")
        if t.get("cite"):
            thm_allowed[ref] = list(t["cite"])
            grounded = cap.get("grounded") or []
            for c in t["cite"]:
                if f"theorem:{c}" not in grounded:
                    c5.append(f"{ref}: theorem {c!r} not in the captured grounded set {grounded}")
        if kind not in SPECIAL_KINDS:
            if ans is None:
                c5.append(f"{ref}: expected a derived answer, got none (gap: {(cap['response_ir'] or {}).get('gap')!r})")
            else:
                derived[ref] = ans

    checks["c5_kinds"] = {"pass": not c5, "bad": c5}

    # C6 — the seam carries (the seed-only runtime must re-answer
    # byte-identically; the P6 mechanic).
    c6: list[str] = []
    offscript_carry: dict[str, Any] = {}
    carry_answers = {o["question"]: o for o in spec.get("offscript", [])}
    for i, rec in enumerate(carry_runs):
        ir = rec.response_ir or {}
        surf = carry_surfaces[i]
        if surf in carry_answers:
            offscript_carry[surf] = ir.get("answer")
            o = carry_answers[surf]
            if o.get("expect_derived", True) and ir.get("uncertainty_state") != "derived":
                c6.append(f"off-script {surf!r}: not a grounded derivation")
        else:
            ref = next(r for r, t in by_ref.items() if t["kind"] == "carry" and t["question"] == surf)
            main_ans = turn_answer(captured[ref])
            if ir.get("answer") != main_ans:
                c6.append(f"{ref}: seed-only carry drifted ({ir.get('answer')!r} != S-run {main_ans!r})")
    checks["c6_carry"] = {"pass": not c6, "bad": c6, "seam_carry_refs": sorted(carry_refs)}

    # C7 — mastery (pre-states computed from the seed, EXCLUDING the
    # band's new concepts (unexposed by definition before the band);
    # post from the final store; no regressions on carried concepts;
    # the new concepts at their declared band-end values; the drill
    # census over the carried concepts — the D-e6y family).
    c7: list[str] = []
    pre = storeio.pre_states(seed_path, registry)
    new_ids = list(spec["band"]["new_concepts"])
    for cid in new_ids:
        pre.pop(cid, None)
    post = storeio.mastery_snapshot(final, registry)
    drilled: dict[str, int] = {}
    improved: list[str] = []

    def _state_val(x: Any) -> str:
        return x if isinstance(x, str) else x.value

    for cid in sorted(pre):
        if cid not in post:
            c7.append(f"carried concept {cid} left the mastery view")
            continue
        base = _state_val(pre[cid]["state"])
        cur = _state_val(post[cid]["state"])
        # the sanctioned transition rule (the e618 P7 pattern): NO
        # regression (stable may only stay stable); a carried
        # concept may move PRACTICING->STABLE when the band's soil
        # carries close its prereq chain (island bands do this by
        # design — the S14 mod4-split chain, D-e6i(b)).
        if base == "stable":
            if cur != "stable":
                c7.append(f"{cid}: stable state REGRESSED to {cur} (no regressions)")
        else:
            if cur != base and cur != "stable":
                c7.append(f"{cid}: state changed {base} -> {cur} (only stable or unchanged is sanctioned)")
            elif cur == "stable" and base != "stable":
                improved.append(cid)
        delta = post[cid]["correct"] - pre[cid]["correct"]
        if delta < 0:
            c7.append(f"{cid}: correct-derivation count REGRESSED ({post[cid]['correct']} < {pre[cid]['correct']})")
        if delta > 0:
            drilled[cid] = delta
    for cid in new_ids:
        e = spec["expect"].get("mastery", {}).get(cid)
        if e is None:
            c7.append(f"new concept {cid} has no mastery expectation")
            continue
        v = post.get(cid)
        if v is None:
            c7.append(f"new concept {cid} not in the post mastery view")
            continue
        if v["state"] != e["state"] or v["correct"] != e["correct"]:
            c7.append(f"{cid}: post state {v} != declared {e}")
        want_gaps = spec["expect"].get("prereq_gaps", {}).get(cid, [])
        if tuple(v["prereq_gaps"]) != tuple(want_gaps):
            c7.append(f"{cid}: prereq gaps {v['prereq_gaps']} != declared {want_gaps}")
    checks["c7_mastery"] = {"pass": not c7, "bad": c7, "pre_states": len(pre), "drilled": drilled, "improved_to_stable": sorted(improved)}

    # C8 — the store totals (P8 family: delta accounting, line census,
    # new facts present, the determinism twin).
    c8: list[str] = []
    final_total = len(final_ids)
    new_facts = len(spec["band"]["new_fact_ids"])
    new_events = final_total - spec["seed"]["total"] - new_facts
    if final_total != spec["expect"]["final_total"]:
        c8.append(f"final total {final_total} != declared {spec['expect']['final_total']}")
    # the D-e6y 1:1 event-per-turn accounting is a PROPERTY of the
    # S13 band (every turn wrote exactly one event), not a rule: gap
    # turns write nothing (impossible runs are store-inert) and the
    # store is the referee via final_total. The drift is REPORTED
    # (S14: +6, the D-e6i(c) class), never failed on here.
    event_drift = new_events - len(turns)
    if new_events < 0 or new_events > 2 * len(turns):
        c8.append(f"new events {new_events} implausible against {len(turns)} turns")
    for fid in spec["band"]["new_fact_ids"]:
        if fid not in final_ids:
            c8.append(f"new fact {fid} is not in the final store")
    if storeio.line_end(final) != spec["seed"]["line_end"]:
        c8.append("the line end moved (a census wrote off-line)")
    succ = storeio.successor_objects(final)
    if succ != set(range(1, spec["seed"]["line_end"] + 1)):
        c8.append("the successor objects are not exactly 1..end")
    twin = dump1 == dump2 and storeio.store_identity(storeio.fresh_final(run2_root, max(sessions))) == storeio.store_identity(final)
    if not twin:
        c8.append("the determinism twin failed")
    checks["c8_totals"] = {
        "pass": not c8,
        "bad": c8,
        "final_total": final_total,
        "new_facts": new_facts,
        "new_events": new_events,
        "event_drift_vs_turns": event_drift,
        "twin": twin,
    }

    # C9 — the unconditional/conditional discipline (P0 family): the
    # marker ABSENT on band facts when the band is unconditional,
    # PRESENT on the kept marker facts; and the off-line hygiene:
    # declared off-line witness values must not float up into the
    # on-line derived answers.
    c9: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    band = spec["band"]
    if band.get("unconditional"):
        for fid in band["new_fact_ids"]:
            try:
                f = final.get(fid)
            except KeyError:
                c9.append(f"P0: {fid} missing")
                continue
            obj = f.object if isinstance(f.object, str) else str(f.object)
            if marker in obj:
                c9.append(f"P0: {fid} carries the condition marker (the band is declared unconditional)")
    for fid in band.get("marker_kept_facts", []):
        try:
            f = final.get(fid)
        except KeyError:
            c9.append(f"P0: carried fact {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if not (marker in obj or "under the condition that" in obj):
            c9.append(f"P0: {fid} lost the condition marker (drift)")
    # Off-line hygiene: the DECLARED off-line witness literals (the
    # author says which bed values are off-line witnesses) must not
    # float up into the on-line derived answers. The line end is on-
    # line content and is deliberately NOT watched (it names itself
    # in walls and partials alike).
    offline_literals = [str(x) for x in spec["expect"].get("offline_watch", [])]
    for lit in offline_literals:
        for ref, ans in derived.items():
            if lit in ans:
                c9.append(f"off-line literal {lit} leaked into on-line answer at {ref} (the D-e6z hygiene)")
    checks["c9_discipline"] = {"pass": not c9, "bad": c9}

    # The frozen-shape table (the FROZEN dict of the band, rebuildable
    # from the spec + the mechanism).
    table: dict[str, Any] = {
        "seed": spec["seed"]["store"],
        "seed_identity": spec["seed"]["identity"],
        "seed_total": spec["seed"]["total"],
        "line_end_final": spec["seed"]["line_end"],
        "total_turns": len(turns),
        "script": {str(s): list(script[s]) for s in sessions},
        "domain_sequence": letters,
        "derived_table": derived,
        "beds_exact": beds_exact,
        "bed_grounded": bed_grounded,
        "bed_owners": bed_owners,
        "pre_teach_gaps": gaps,
        "teach_turns": teach,
        "scaffold_failures": scf,
        "missing_parts_failure": mpf,
        "derive_successes": dvs,
        "rederive": None,
        "walls_honest": walls,
        "wall_articulations": wall_art,
        "rh_zero_text": zero_derive_text,
        "rh_touch_wall": zero_touch_text,
        "unclassified_honest": {"expected": unclassified_text},
        "seam_carry_refs": sorted(carry_refs),
        "offscript_carry": offscript_carry,
        "seam_crosscheck": spec["expect"].get("seam", {}),
        f"pre_{spec['session'].lower()}_states": pre,
        f"pre_{spec['session'].lower()}_drilled": drilled,
        "mastery_expected": spec["expect"].get("mastery", {}),
        "expected_prereq_gaps": spec["expect"].get("prereq_gaps", {}),
        "theorem_allowed": thm_allowed,
        "theorem_dag": {
            **{s: list(m["parts"]) for s, m in B.S6_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S7_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S8_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S9_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S10_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S11_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S12_THEOREMS.items()},
            **{s: list(m["parts"]) for s, m in B.S13_THEOREMS.items()},
        },
        "new_fact_ids": spec["band"]["new_fact_ids"],
        "new_facts": new_facts,
        "new_events": new_events,
        "final_total": final_total,
        "total_seam_facts": sum(1 for a in final.query() if a.id.startswith("lemma:") or a.id.startswith("theorem:")),
    }

    ok = all(c["pass"] for c in checks.values())
    return {
        "ok": ok,
        "spec": spec["id"],
        "checks": checks,
        "table": table,
        "computed_beds": computed_beds,
        "post_mastery": {cid: post[cid] for cid in sorted(post)},
    }


def render_markdown(report: dict[str, Any]) -> str:
    """The control report as a reviewable markdown table of
    prediction-vs-mechanism (the artifact a human reads before
    freezing)."""
    lines = [f"# bandgen control — {report['spec']}", "",
             f"**{'CLEAN — ready to freeze' if report['ok'] else 'DIFFS — the mechanism disagrees with the spec'}**", ""]
    for name, c in report["checks"].items():
        mark = "PASS" if c["pass"] else "DIFF"
        lines.append(f"## {name} — {mark}")
        for b in c.get("bad", []):
            lines.append(f"- {b}")
        for k in ("letters", "drilled", "identity", "total", "line_end", "final_total", "new_facts", "new_events", "twin", "pre_states", "seam_carry_refs"):
            if k in c:
                lines.append(f"- {k}: {c[k]}")
        lines.append("")
    tbl = report.get("table", {})
    for k in sorted(tbl):
        lines.append(f"- table.{k}: {len(tbl[k]) if isinstance(tbl[k], (dict, list, str)) else tbl[k]}")
    lines.append("")
    beds = report.get("computed_beds", {})
    if beds:
        lines.append("## computed beds (reference-evaluated)")
        for k, v in beds.items():
            lines.append(f"- {k} = {v!r}")
    return "\n".join(lines) + "\n"


def to_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, default=str) + "\n"
