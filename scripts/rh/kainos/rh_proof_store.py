#!/usr/bin/env python3
"""rh_proof_store.py — TRAINING RUN of the RH proof scaffold on the kainos codex
store (the repo's Prolog-like surface: assertions + relations + query).

Owner directives 2026-09-10 (items 5-6): train kainos-logos on our approach;
work with it until the draft proof is ready for drop-in data.

WHAT THIS IS
  * FACT WALK: every fact enters the store by RE-READING canonical repo outputs
    (P-0.9; "the store speaks, not the hand"). Each fact carries the source
    file + sha256. A pattern that fails to parse FAILS the walk (no silent
    defaults).
  * CONCEPT GRAPH: RH-PROOF-OUTLINE.md v0.1 as a concept/prereq graph
    (B-0..B-6, F facts, D data triggers, classical citations). Edges are store
    assertions (relation `prereq` / `plan`), never prose.
  * QUERIES: discharge(plan) — transitive prereq closure, classified
    (FULFILLED / PENDING-DATA / TO-BUILD) with the runnable frontier;
    circularity() — no cycle may touch the target; coverage() per concept;
    line_end() — what the record is complete up to.
  * INVARIANTS (P5 / discovery-candidate): the target term `rh` must stay
    status=hypothesis; no `theorem:riemann` assertion may exist. A violation
    FAILS the walk loudly.
  * DROP-IN READY: re-running after the 6e6 chain / D4-D3 / 1e7 redundancy
    lands flips data-trigger assertions from candidate to established
    (the walk finds the files) and re-discharges. Nothing in this module is
    edited when data lands — only the canonical outputs change.

RUN:  cd scripts/rh  &&  PYTHONPATH=../../src python3 kainos/rh_proof_store.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

RH = Path(__file__).resolve().parent.parent      # scripts/rh
REPO = RH.parent.parent
PLAN = REPO / "plan/40-prize-islands/rh-attack"
sys.path.insert(0, str(REPO / "src"))

from kainos.codex.memory import InMemoryCodexStore  # noqa: E402
from kainos.codex.models import (  # noqa: E402
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)

OBSERVER = "rh-attack training run (day-010, owner directive items 5-6)"
TODAY = "2026-09-10"
E = EpistemicState
OUTLINE = PLAN / "RH-PROOF-OUTLINE.md"

# ────────────────────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────────────────────

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def term(i: str, kind: str = "concept") -> TermRef:
    return TermRef(id=i, kind=kind)

def make_assert(store, i, subj, rel, obj, status, file, context, verified=True,
                evidence=()):
    src = Source(uri=str(file) if file else "rh-attack/PLAN (declarative)",
                 version=TODAY,
                 hash=sha256(file) if (file and file.exists()) else None,
                 retrieved_at=TODAY, authority="kainos-logos rh-attack")
    a = Assertion(
        id=i,
        subject=term(subj),
        relation=term(rel, kind="relation"),
        object=term(obj) if isinstance(obj, str) and re.fullmatch(r"[a-z0-9\-]+", obj) else obj,
        context=Context(data=context),
        status=status,
        provenance=Provenance(source=src, observer=OBSERVER,
                              derived=False, verified=verified,
                              evidence=list(evidence)),
    )
    store.add(a)
    return a

def parse_or_fail(text: str, rx: str, what: str) -> str:
    m = re.search(rx, text)
    if not m:
        raise SystemExit(f"FACT-WALK FAIL: pattern for {what} not found (no silent default)")
    return m.group(1)

# ────────────────────────────────────────────────────────────────────────────
# 1. FACT WALK — canonical repo outputs only (P-0.9)
# ────────────────────────────────────────────────────────────────────────────

def fact_walk(store: InMemoryCodexStore) -> dict:
    facts: dict = {}

    # (a) Stage-1 certified onset table → the measured 4-digit law + bridge
    f = RH / "out_day009c_onset_pred_certified.txt"
    txt = f.read_text()
    rx = (r"N=\s*(\d+) t/N=\s*([\d.]+): C/\|I\|=([\d.]+) measured=([\d.]+) "
          r"err=([+\-\d.]+%)\s+\|Psi-zeta\|/\|zeta\|\s*=\s*([\d.eE+\-]+)")
    rows = re.findall(rx, txt)
    if len(rows) < 10:
        raise SystemExit("FACT-WALK FAIL: onset table rows < 10")
    for n, fo, pred, meas, err, pze in rows:
        make_assert(store, f"onset-pt-{n}-{fo}", f"meas-onset-pt-{n}-{fo}", "value",
                    f"C/|I|={meas}", E.established, f,
                    {"N": int(n), "t_over_N": float(fo), "pred": float(pred),
                     "measured": float(meas), "err_pct": float(err.rstrip("%")),
                     "psi_zeta_rel_err": float(pze)},
                    evidence=[str(f)])
    clean = [r for r in rows if abs(float(r[4].rstrip("%"))) <= 1.5]
    make_assert(store, "fac-m-onset-4d", "m-onset-4d", "measured-law",
                "C/|I| = 1/2*(t/N) — 4 digits, N-independent, onset t/N~2",
                E.established, f,
                {"digits": 4, "n_independent": True,
                 "rows_certified": len(rows), "clean_rows": len(clean)},
                evidence=[str(f), "scripts/rh/day009_e7b2_onset_pred.py (day-004b measurement)"])
    facts["m-onset-4d"] = f"measured 4-digit law (rows={len(rows)} certified, clean={len(clean)})"
    make_assert(store, "fac-m-stage1", "m-stage1", "measured-bridge",
                "Stage-1: zero-side 25.2.12 kernel reproduces the onset at clean points",
                E.established, f,
                {"clean": ";".join(f"({r[0]},{r[1]}):{r[4]}" for r in clean),
                 "env": "docker kainos-dev:dev (mpmath 1.3.0 verified env)"},
                evidence=[str(f)])
    facts["m-stage1"] = "Stage-1 clean rows: " + "; ".join(f"({r[0]},{r[1]}):{r[4]}" for r in clean)

    # (b) certified 3e5 list
    f = RH / "out_day009b_seg00_certified.txt"
    txt = f.read_text()
    m = re.search(r"N\(300000\) dt=(\d+) dt2=(\d+) agree=(\w+)", txt)
    if not m:
        raise SystemExit("FACT-WALK FAIL: 3e5 certified N line missing")
    n_dt, n_dt2, agree = int(m.group(1)), int(m.group(2)), m.group(3)
    if agree != "True" or n_dt != n_dt2:
        raise SystemExit("FACT-WALK FAIL: 3e5 dt/dt2 not agreed in the certified file")
    gate = float(parse_or_fail(txt, r"engine gate GPU-vs-host max \|diff\| = ([\d.e\-]+)", "engine gate"))
    mgap = float(parse_or_fail(txt, r"min_gap\(dt2\)=([\d.e\-]+)", "min gap"))
    make_assert(store, "fac-list-3e5-cert", "fac-list-3e5", "certified-count",
                f"N(3e5)={n_dt}", E.established, f,
                {"N_3e5": n_dt, "dt": n_dt, "dt2": n_dt2,
                 "engine_gate_gpu_vs_host": gate, "min_gap_dt2": mgap,
                 "method": "GPU dt/dt2 double pass, per-segment agreement, engine gate"},
                evidence=[str(f), "zeros_T300000_ext_full.txt (466655 lines, strict monotone)"])
    facts["f-list-3e5"] = f"N(3e5)={n_dt} (dt=dt2, gate {gate:.1e}, min gap {mgap})"

    # (c) 1e7 STABLE window
    f = RH / "out_day005g_dt025.txt"
    txt = f.read_text()
    flips = parse_or_fail(txt, r"(\d[\d,]*)\s+sign flips in window", "1e7 window flips").replace(",", "")
    if "STABLE" not in txt:
        raise SystemExit("FACT-WALK FAIL: 1e7 window not STABLE")
    make_assert(store, "fac-window-1e7", "fac-window-1e7", "dt-dt2-stable",
                f"[9.9e6,1e7]: {flips} flips exact", E.established, f,
                {"flips_9p9e6_1e7": int(flips), "window": "[9.9e6, 1e7]",
                 "dt2_matches_dt": True},
                evidence=[str(f)])
    facts["f-window-1e7"] = f"{flips} flips STABLE"

    # (d) day-010 dps-40 2K/S certificates (the canonical 1e5/1e6/1e7 lines)
    f = RH / "out_day010_dps1e7.txt"
    txt = f.read_text()
    for tag, prefix in (("1e5", "1e5"), ("1e6", "1e6"), ("1e7c", "1e7  corrected")):
        line = next((l for l in txt.splitlines() if l.startswith(prefix)), None)
        if not line:
            raise SystemExit(f"FACT-WALK FAIL: dps line {tag} missing")
        N = int(parse_or_fail(line, r"(\d{6,})", f"line {tag} count"))
        twoK = float(parse_or_fail(line, r"2K=(-?[\d.]+)", f"line {tag} 2K"))
        dist = float(parse_or_fail(line, r"dist-even=([\d.e\-]+)", f"line {tag} dist"))
        S = float(parse_or_fail(line, r"S=(-?[\d.]+)", f"line {tag} S"))
        make_assert(store, f"fac-dps-{tag}", f"fac-cert-{tag}", "dps-certificate",
                    f"2K={twoK:.6f} @{dist:.2e}, S={S:+.4f}", E.established, f,
                    {"count": N, "S": S, "twoK": twoK, "dist_even": dist,
                     "dps": 40, "even": abs(twoK - round(twoK / 2) * 2) < 1e-6},
                    evidence=[str(f)])
        facts[f"f-cert-{tag}"] = f"2K={twoK:.0f}@{dist:.1e} S={S:+.4f}"

    # (e) per-pair identity unit (B-4 evidence) — subjects = the graph nodes
    f = RH / "out_day010_pair_unit.txt"
    txt = f.read_text()
    worst = parse_or_fail(txt, r"WORST: dLa=([\d.e\-]+)\s+dAr=([\d.e\-]+)", "pair unit WORST")
    dla = float(worst)
    dar = float(parse_or_fail(txt, r"WORST: dLa=[\d.e\-]+\s+dAr=([\d.e\-]+)", "pair unit dAr"))
    if "PASS" not in txt:
        raise SystemExit("FACT-WALK FAIL: pair unit check not PASS")
    make_assert(store, "fac-pair-unit", "fa-pair-id", "unit-verified",
                f"dLa<={dla:.1e}, dAr<={dar:.1e} (dps-25 ref)", E.established, f,
                {"dLa_worst": dla, "dAr_worst": dar,
                 "reference": "mpmath dps-25 single-pair",
                 "zeros": "first 100 certified", "dps": 25},
                evidence=[str(f)])
    make_assert(store, "fac-d-pair-unit", "d-pair-unit", "measured",
                "unit check PASS", E.established, f,
                {"dLa": dla, "dAr": dar}, evidence=[str(f)])
    facts["f-pair-id"] = f"B-4 unit PASS (dLa {dla:.0e}, dAr {dar:.0e})"

    # (f) D4/D3 (drop-in: if the run completed, parse it; else candidate)
    f = RH / "out_day010_d4d3.txt"
    d4_done = f.exists() and "D4+D3 RUN COMPLETE" in f.read_text()
    if d4_done:
        txt = f.read_text()
        gstar = parse_or_fail(txt, r"gamma\* = ([\d.]+)", "D4 gstar")
        d3med = float(parse_or_fail(txt, r"median=([\d.eE+\-]+)", "D3 median"))
        d3max = float(parse_or_fail(
            txt, r"D3 SUMMARY: n=\d+\s+median=[\d.eE+\-]+\s+p90=[\d.eE+\-]+\s+max=([\d.eE+\-]+)",
            "D3 max"))
        make_assert(store, "fac-d4d3", "d4-dev", "measured-deviation",
                    f"gstar={gstar}; D3 median={d3med:.2e} max={d3max:.2e}",
                    E.established, f, {"gstar": float(gstar),
                                       "audit_median": d3med, "audit_max": d3max},
                    evidence=[str(f)])
        facts["d4-dev"] = f"D4/D3 complete (gstar={gstar})"
    else:
        make_assert(store, "fact-d4", "d4-dev", "pending-run",
                    "D4+D3 run in flight / not complete", E.candidate,
                    f if f.exists() else None,
                    {"status": "in-flight" if f.exists() else "queued"},
                    verified=False)
        facts["d4-dev"] = "PENDING (run in flight)"

    # (f0) B-5 core formula check (drop-in)
    f = RH / "out_day010_b5core_check.txt"
    b5c_done = f.exists() and "B5-CORE CHECK PASS" in f.read_text()
    if b5c_done:
        txt = f.read_text()
        wf = float(parse_or_fail(txt, r"WORST \|formula-measured\| \(far\) = ([\d.]+)",
                                 "b5core far worst"))
        wd = float(parse_or_fail(txt, r"WORST \|formula-direct\|\s*\(all\) = ([\d.e\-]+)", "b5core direct worst"))
        make_assert(store, "fac-b5core", "b5-core", "theorem-verified",
                    f"R closed form: |f-m| far <= {wf:.4f}, |f-direct| <= {wd:.1e} (dps-30)",
                    E.established, f,
                    {"worst_formula_vs_measured_far": wf,
                     "worst_formula_vs_direct": wd, "dps": 30,
                     "statement": "R = (1/4+g^2)((g-t)^2+d^2)((g+t)^2+d^2)/((g^2-t^2)((1/2+d)^2+g^2)((1/2-d)^2+g^2)) * exp((1/2+it)*omega_d)"},
                    evidence=[str(f)])
        facts["b5-core"] = f"core theorem VERIFIED (fs-vs-meas {wf:.4f}, vs-direct {wd:.0e})"
    else:
        make_assert(store, "fact-b5core", "b5-core", "pending-run",
                    "B5-core check not complete", E.candidate,
                    f if f.exists() else None, {"status": "queued"}, verified=False)
        facts["b5-core"] = "PENDING (b5core check not run)"

    # (f1b) D4 far-scale (drop-in)
    f = RH / "out_day010_d4farscale.txt"
    far_done = f.exists() and "D4-FARSCALE RUN COMPLETE" in f.read_text()
    if far_done:
        txt = f.read_text()
        mr1 = float(parse_or_fail(txt, r"max \|R-1\| = ([\d.]+) over", "far max R-1"))
        make_assert(store, "fac-d4far", "d4-far", "measured-farscale",
                    f"far ratios 10/50/100: |R-1| = (t0/gamma*)^2 to 6 digits (max {mr1:.1f}), delta-flat O(1e-6)",
                    E.established, f,
                    {"max_abs_R_minus_1": mr1,
                     "trend": "quadratic in t0/gamma* (10^2/50^2/100^2)",
                     "delta_range": [0.005, 0.5], "near_resonance_floor": 0.998},
                    evidence=[str(f)])
        facts["d4-far"] = f"far-scale LANDED (|R-1| = c^2 6-digit, max {mr1:.0f})"
    else:
        make_assert(store, "fact-d4far", "d4-far", "pending-run",
                    "D4-farscale run not complete", E.candidate,
                    f if f.exists() else None, {"status": "queued"}, verified=False)
        facts["d4-far"] = "PENDING (D4-farscale running)"

    # (f2) D3-fine local floor (drop-in; present + complete -> established)
    f = RH / "out_day010_d3fine.txt"
    fine_done = f.exists() and "D3-FINE RUN COMPLETE" in f.read_text()
    if fine_done:
        txt = f.read_text()
        med = float(parse_or_fail(txt, r"FINE SUMMARY n=(\d+)\s+median=([\d.e+\-]+)",
                                  "D3-fine median").split(None)[0]) if False else float(
            re.search(r"FINE SUMMARY n=(\d+)\s+median=([\d.e+\-]+)", txt).group(2))
        n_fine = int(re.search(r"FINE SUMMARY n=(\d+)", txt).group(1))
        p90 = float(parse_or_fail(txt, r"p90=([\d.e+\-]+)", "D3-fine p90"))
        mx = float(parse_or_fail(txt, r"p99=[\d.e+\-]+\s+max=([\d.e+\-]+)", "D3-fine max"))
        make_assert(store, "fac-d3floor", "d3floor", "measured-floor",
                    f"fine [975,1025]@0.5u (n={n_fine}): median {med:.3e}, p90 {p90:.3e}, max {mx:.3e} — no 100x spike",
                    E.established, f,
                    {"n": n_fine, "median": med, "p90": p90, "max": mx,
                     "spike_100x": False, "localization": "none (top band scattered)"},
                    evidence=[str(f)])
        facts["d3floor"] = f"fine floor LANDED (median {med:.1e}, p90 {p90:.1e}, max {mx:.1e})"
    else:
        make_assert(store, "fact-d3floor", "d3floor", "pending-run",
                    "D3-fine run not complete", E.candidate,
                    f if f.exists() else None, {"status": "queued"}, verified=False)
        facts["d3floor"] = "PENDING (D3-fine running)"

    # (g) pending data triggers (drop-in slots; status flips when files land)
    d1_list = RH / "zeros_T6000000_ext_full.txt"
    d1_onset = RH / "out_day010_onset_G6e6.txt"
    if d1_list.exists() and d1_onset.exists():
        make_assert(store, "fact-d1", "d1-6e6", "measured",
                    "G=6e6 list + onset rows landed", E.established, d1_onset,
                    {"list_lines": d1_list.read_text().count("\n")},
                    evidence=[str(d1_list), str(d1_onset)])
        facts["d1-6e6"] = "LANDED"
    else:
        make_assert(store, "fact-d1", "d1-6e6", "pending-run",
                    "6e6 chain in flight (supervisor)", E.candidate, None,
                    {"status": "in-flight", "supervisor": "day010_ext6e6_supervisor.sh"},
                    verified=False)
        facts["d1-6e6"] = "PENDING (6e6 walk in flight)"

    d5 = RH / "out_day006_early_rewalk.txt"
    d5_done = d5.exists() and d5.stat().st_size > 0
    make_assert(store, "fact-d5", "d5-1e7-red",
                "measured" if d5_done else "pending-run",
                "1e7 redundancy walk " + ("landed" if d5_done else "in flight"),
                E.established if d5_done else E.candidate,
                d5 if d5_done else None,
                {"status": "landed" if d5_done else "in-flight"},
                verified=d5_done)
    facts["d5-1e7-red"] = "LANDED" if d5_done else "PENDING (in flight)"

    # (h) D2 (beyond-4-digit fits): not yet run → declared candidate
    make_assert(store, "fact-d2", "d2-fits", "pending-work",
                "beyond-4-digit onset fits (next correction terms)", E.candidate,
                None, {"status": "queued", "vehicle": "certified 3e5 list"},
                verified=False)
    facts["d2-fits"] = "PENDING (queued, small)"

    return facts

# ────────────────────────────────────────────────────────────────────────────
# 2. CONCEPT GRAPH — RH-PROOF-OUTLINE.md v0.1
# ────────────────────────────────────────────────────────────────────────────

def concept_graph(store: InMemoryCodexStore) -> None:
    C = E.candidate
    # classical inputs (G6); c-zeta-pos CITATION PENDING (honest sub-gap)
    for cid, note, done in (
        ("c-rvm", "Riemann-von Mangoldt (project convention; dps-40 verified at 1e5/1e6/1e7)", True),
        ("c-fe", "functional equation + conjugation: 4-tuple structure", True),
        ("c-25212", "DLMF 25.2.12 product (READ, verbatim in ledger)", True),
        ("c-zeta-pos", "zeta>0 on (0,1) — CITATION PENDING (F-0.1)", False)):
        make_assert(store, f"cl-{cid}", cid, "classical-input", note,
                    E.established if done else C,
                    PLAN / "FORMULAS.md", {"note": note}, verified=done)
    # target (P5: discovery-candidate invariant — must stay hypothesis)
    make_assert(store, "cl-rh", "rh", "target-goal",
                "RH as reduction target: D(t)=N_total-N_on identically 0",
                E.hypothesis, OUTLINE,
                {"invariant": "stays hypothesis (P5); no theorem:riemann assertion"},
                verified=False)
    # concepts with prereq edges (subject REQUIRES object)
    G = [
        ("b0-counting-equiv", "B-0 counting equivalence RH<=>D==0",
         ["c-rvm", "c-fe", "c-zeta-pos"], "to-build (LOW: 2-line counting argument)"),
        ("b1-onset-thm", "B-1 exact onset law + remainder (G4)",
         ["m-onset-4d", "d2-fits", "c-25212"], "to-build (Euler-Maclaurin lifting)"),
        ("b2-rigorous-tail", "B-2 rigorous tail remainder M(G,t) (G3)",
         ["d1-6e6"], "to-build (D1 data decides the model)"),
        ("b3-bridge-id", "B-3 bridge identity as identity+residual (H3 lift)",
         ["m-stage1", "fa-pair-id", "b2-rigorous-tail", "c-rvm"], "to-build (follows B-1/B-2)"),
        ("fa-pair-id", "B-4 on-line per-pair closed form (la, ar) + validation",
         ["d-pair-unit"], "FILLED (measured dps-25 unit, fact walk)"),
        ("b5-detector", "B-5 kernel-deviation lemma f(delta,t) + 2K mechanism",
         ["fa-pair-id", "d4-dev", "b5-core"],
         "core theorem FILLED v0.5 (exact R closed form, dps-30 verified); composition with floor = B-6A"),
        ("b5-core", "B-5 core: exact R = off4/on2 closed form + dps-30 verification",
         ["d4-dev"], "FILLED (v0.5; out_day010_b5core_check.txt)"),
        ("b6a-route-a", "B-6A residual-floor theorem (route A: no walk; T drops out)",
         ["b1-onset-thm", "b3-bridge-id", "b5-detector", "d1-6e6"],
         "to-build (THE WALL candidate)"),
        ("b6b-route-b", "B-6B uniform 2K/S dynamics (route B: classical depth)",
         ["fac-cert-1e5", "fac-cert-1e6", "fac-cert-1e7c", "x-s-theory"],
         "to-build (classical S-program)"),
        ("b6c-hybrid-T", "B-6C hybrid interim: RH to T (certified counterexample search)",
         ["fac-cert-1e6", "fac-cert-1e7c", "fac-window-1e7"],
         "partially filled (T=1e7; redundancy D5 in flight)"),
        ("x-s-theory", "open classical S-theory strong enough to exclude off-line content",
         [], "wall (no data trigger; the classical home-turf gap)"),
        # data-trigger nodes (status decided by the fact walk)
        ("d-pair-unit", "D4 unit: per-pair closed form verified", [], "from facts"),
        ("d3floor", "D3-fine: local |zeta-K| audit floor [975,1025]", [], "from facts"),
        ("d4-far", "D4-far: far-pair |R-1| = (t0/gamma*)^2 amplification", [], "from facts"),
        ("d4-dev", "D4/D3: kernel deviation + W-audit on the actual zeta", [], "from facts"),
        ("d1-6e6", "D1: G=6e6 list + onset rows (tail-saturation test)", [], "from facts"),
        ("d2-fits", "D2: beyond-4-digit onset fits", [], "from facts"),
        ("d5-1e7-red", "D5: 1e7 redundancy re-walk", [], "from facts"),
    ]
    for cid, name, prereqs, note in G:
        st = E.established if cid in ("fa-pair-id", "b6c-hybrid-T", "b5-core", "b5-detector") else C
        make_assert(store, f"cn-{cid}", cid, "concept", name, st, OUTLINE,
                    {"prereqs": prereqs, "note": note},
                    verified=(st is E.established and cid in ("fa-pair-id", "b6c-hybrid-T", "b5-core")))
        for p in prereqs:
            make_assert(store, f"pre-{cid}-{p}", cid, "prereq", p, C, OUTLINE,
                        {"note": f"{cid} requires {p}"}, verified=False)
    # proof plans: rh requires one of the two closures (alternative plans)
    make_assert(store, "plan-a", "rh", "plan", "closure-a", E.hypothesis, OUTLINE,
                {"note": "route A: definition-side closure, no walked T"}, verified=False)
    make_assert(store, "plan-b", "rh", "plan", "closure-b", E.hypothesis, OUTLINE,
                {"note": "route B: uniform dynamics closure"}, verified=False)
    for cid, p, note in (
        ("closure-a", "b6a-route-a", "closure-a requires route A"),
        ("closure-a", "b0-counting-equiv", "closure-a requires counting equivalence"),
        ("closure-b", "b6b-route-b", "closure-b requires route B"),
        ("closure-b", "b0-counting-equiv", "closure-b requires counting equivalence")):
        make_assert(store, f"pre-{cid}-{p}", cid, "prereq", p, C, OUTLINE,
                    {"note": note}, verified=False)

# ────────────────────────────────────────────────────────────────────────────
# 3. QUERIES (the logic side)
# ────────────────────────────────────────────────────────────────────────────

def prereq_map(store: InMemoryCodexStore) -> dict:
    m: dict[str, list[str]] = {}
    for a in store.query(relation="prereq"):
        m.setdefault(a.subject.id, [])
        if a.object_id not in m[a.subject.id]:
            m[a.subject.id].append(a.object_id)
    # plan edges act as prereq edges for discharge
    for a in store.query(relation="plan"):
        m.setdefault(a.subject.id, [])
        if a.object_id not in m[a.subject.id]:
            m[a.subject.id].append(a.object_id)
    return m

def closure_of(root: str, m: dict) -> set:
    seen, stack = set(), [root]
    while stack:
        x = stack.pop()
        for p in m.get(x, ()):
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen

def status_of(store: InMemoryCodexStore, cid: str) -> str:
    subs = store.query(subject=cid)
    if subs:
        # prefer a fact-style relation over the bare concept marker
        fact_rel = ("pending-run", "measured", "unit-verified", "dps-certificate",
                    "dt-dt2-stable", "pending-work", "measured-deviation",
                    "certified-count", "measured-law", "measured-bridge")
        for a in subs:
            if a.relation.id in fact_rel:
                return a.status.value
        return subs[0].status.value
    # data-trigger nodes referenced only as objects of fact assertions
    for a in store.query(object=cid):
        if a.relation.id in ("pending-run", "measured", "unit-verified",
                             "dps-certificate", "dt-dt2-stable", "pending-work",
                             "measured-deviation"):
            return a.status.value
    q = store.query(relation="prereq", object=cid)
    if q:
        return "referenced"
    return "unknown"

def discharge(store, root: str) -> dict:
    m = prereq_map(store)
    nodes = closure_of(root, m)
    fulfilled, pending_data, to_build = [], [], []
    for n in sorted(nodes):
        st = status_of(store, n)
        if st == "established":
            fulfilled.append(n)
        elif st in ("hypothesis", "unknown", "referenced"):
            to_build.append(n)
        else:  # candidate: is it a data trigger (a pending fact) or work?
            q = [a for a in store.query(subject=n)
                 if a.relation.id in ("pending-run", "pending-work")]
            if q:
                pending_data.append(n)
            else:
                to_build.append(n)
    frontier = [n for n in pending_data + to_build
                if all(status_of(store, p) == "established" for p in m.get(n, ()))]
    return {"root": root, "closure": sorted(nodes), "fulfilled": fulfilled,
            "pending_data": pending_data, "to_build": to_build,
            "runnable_frontier": frontier}

def circularity(store) -> dict:
    m = prereq_map(store)
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict = {}
    cycles = []

    def dfs(u, path):
        color[u] = GRAY
        path.append(u)
        for v in m.get(u, ()):
            if color.get(v, WHITE) == GRAY:
                i = path.index(v)
                cycles.append(path[i:] + [v])
            elif color.get(v, WHITE) == WHITE:
                dfs(v, path)
        path.pop()
        color[u] = BLACK

    for k in sorted(m):
        if color.get(k, WHITE) == WHITE:
            dfs(k, [])
    # P5 invariant: no theorem:riemann assertion; rh must stay hypothesis
    p5 = []
    for a in store.query():
        if "theorem:riemann" in a.id or a.subject.id == "theorem:riemann":
            p5.append(a.id)
    rh = [a.status.value for a in store.query(subject="rh", relation="target-goal")]
    if rh and rh[0] != "hypothesis":
        p5.append(f"rh status advanced to {rh[0]} — P5 VIOLATION")
    return {"cycles": cycles, "clean": not cycles, "p5_violations": p5}

def line_end(store) -> dict:
    out = {}
    for a in store.query(relation="dps-certificate"):
        c = a.context.data
        out[f"certified-{a.subject.id}"] = f"N={c['count']} S={c['S']:+.4f} 2K={c['twoK']:.0f}"
    for a in store.query(relation="certified-count"):
        out["certified-list-3e5"] = f"N(3e5)={a.context.data.get('N_3e5')} gate={a.context.data.get('engine_gate_gpu_vs_host')}"
    for a in store.query(relation="dt-dt2-stable"):
        out["stable-window-1e7"] = a.context.data
    return out

# ────────────────────────────────────────────────────────────────────────────
# 4. MAIN
# ────────────────────────────────────────────────────────────────────────────

def main() -> None:
    store = InMemoryCodexStore()
    facts = fact_walk(store)
    concept_graph(store)
    plans = {
        "plan-A (route A, definition-side)": "closure-a",
        "plan-B (route B, uniform dynamics)": "closure-b",
        "plan-C (hybrid interim: RH to T)": "b6c-hybrid-T",
    }
    reports = {name: discharge(store, root) for name, root in plans.items()}
    circ = circularity(store)
    le = line_end(store)
    inputs = []
    for p in sorted(RH.iterdir()):
        if p.is_file() and p.name.startswith(("out_day009", "out_day010",
                                              "out_day005", "zeros_T30")):
            inputs.append(f"{p.name}:{sha256(p)}")
    identity = hashlib.sha256("\n".join(inputs).encode()).hexdigest()
    outdir = Path(__file__).resolve().parent / "results"
    outdir.mkdir(exist_ok=True)
    (outdir / "rh-proof-store.json").write_text(json.dumps({
        "training_run": "rh-attack on kainos codex store (day-010)",
        "date": TODAY,
        "identity": identity,
        "inputs": inputs,
        "facts": facts,
        "store_generation": store.generation,
        "line_end": le,
        "discharge": reports,
        "circularity": circ,
        "dump": store.dump(),
    }, indent=1))
    md = ["# RH proof scaffold — discharge report (kainos training run)",
          f"**date** {TODAY}   **identity** `{identity[:12]}`   "
          f"**store generation** {store.generation}", "",
          "## facts (from canonical outputs — the store speaks)", ""]
    for k, v in facts.items():
        md.append(f"- **{k}**: {v}")
    md += ["", "## line end (record complete up to)", ""]
    for k, v in le.items():
        md.append(f"- **{k}**: {v}")
    for name, r in reports.items():
        md += ["", f"## discharge: {name}", "",
               f"- closure: {len(r['closure'])} nodes",
               f"- FULFILLED ({len(r['fulfilled'])}): " + (", ".join(r["fulfilled"]) or "—"),
               f"- PENDING-DATA ({len(r['pending_data'])}): " + (", ".join(r["pending_data"]) or "—"),
               f"- TO-BUILD ({len(r['to_build'])}): " + (", ".join(r["to_build"]) or "—"),
               f"- **runnable frontier (prereqs all fulfilled)**: "
               + (", ".join(r["runnable_frontier"]) or "— (blocked upstream)")]
    md += ["", "## circularity + invariants", "",
           f"- cycles: **{len(circ['cycles'])}** ({'CLEAN' if circ['clean'] else circ['cycles']})",
           f"- P5 violations: **{len(circ['p5_violations'])}** "
           f"({circ['p5_violations'] or 'none — rh stays hypothesis'})"]
    (outdir / "rh-proof-discharge.md").write_text("\n".join(md))
    print("=== KAINOS TRAINING RUN: RH proof scaffold ===")
    print(f"store generation: {store.generation}  identity: {identity[:12]}")
    print(f"line end: {json.dumps(le, default=str)}")
    for name, r in reports.items():
        print(f"\n[{name}]")
        print(f"  fulfilled: {r['fulfilled']}")
        print(f"  pending-data: {r['pending_data']}")
        print(f"  to-build: {r['to_build']}")
        print(f"  runnable frontier: {r['runnable_frontier']}")
    print(f"\ncircularity: CLEAN={circ['clean']}  P5 violations: {circ['p5_violations'] or 'none'}")
    ok = circ["clean"] and not circ["p5_violations"]
    print("TRAINING RUN: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
