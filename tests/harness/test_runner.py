"""Harness tests (P0.08-P0.09) — registration, execution, config block,
persistence, reporting, resolution, phase selection, module entry point.

All tests write to tmp dirs (never the repo's results/).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from kainos.harness.dummy import DummyExperiment
from kainos.harness.report import render
from kainos.harness.runner import (
    REGISTRY,
    Result,
    git_commit,
    load_results,
    main,
    render_listing,
    resolve,
    run,
    run_experiments,
    selected,
)

# ── execution + persistence ─────────────────────────────────────────────────


def test_dummy_experiment_end_to_end(tmp_path):
    results, rc = run_experiments([DummyExperiment(tmp_path)], tmp_path)
    assert rc == 0
    r = results[0]
    assert r.name == "dummy"
    assert r.passed is True
    assert r.value == 1.0
    assert r.threshold == "== 1.0"

    # Persisted audit record + markdown table.
    data = json.loads((tmp_path / "dummy.json").read_text())
    assert data["passed"] is True
    assert data["evidence"] == [str(tmp_path / "dummy.evidence.json")]
    md = (tmp_path / "dummy.md").read_text()
    assert "| name | passed | value | threshold | evidence |" in md
    assert "| dummy | PASS | 1.0 | == 1.0 |" in md


def test_config_block_always_has_reproducibility_keys(monkeypatch, tmp_path):
    monkeypatch.setenv("KAINOS_GIT_COMMIT", "abc1234")
    r = run(DummyExperiment(tmp_path), tmp_path)
    assert set(r.config) >= {"seed", "commit", "dataset_hash"}
    assert r.config["seed"] == 0
    assert r.config["commit"] == "abc1234"
    assert r.config["dataset_hash"] is None  # settable by the caller; None until then


def test_git_commit_falls_back_to_unknown(monkeypatch, tmp_path):
    monkeypatch.delenv("KAINOS_GIT_COMMIT", raising=False)
    commit = git_commit()  # container has no git → "unknown" (host: the real hash)
    assert isinstance(commit, str) and commit  # always a non-empty string


def test_caller_config_is_preserved(tmp_path):
    class _Custom(DummyExperiment):
        def run(self):
            r = super().run()
            r.config["dataset_hash"] = "sha256:beef"
            r.config["seed"] = 42
            return r

    r = run(_Custom(tmp_path), tmp_path)
    assert r.config["dataset_hash"] == "sha256:beef"
    assert r.config["seed"] == 42


def test_result_json_round_trips_through_load_results(tmp_path):
    run(DummyExperiment(tmp_path), tmp_path)
    data = load_results(tmp_path)
    assert [d["name"] for d in data] == ["dummy"]
    assert data[0]["config"]["seed"] == 0


def test_load_results_phase_filter_matches_registry_prefix(tmp_path):
    # regression: the phase filter used to look up "e<p>." in a map keyed by
    # "e<p>" and found nothing — phase reports rendered as "no persisted results".
    rec = {"name": "e2.1", "passed": False, "value": 0.0, "config": {"seed": 42}, "threshold": "t", "evidence": []}
    (tmp_path / "e2.1.json").write_text(json.dumps(rec))
    run(DummyExperiment(tmp_path), tmp_path)  # name "dummy" (registry key "e0.dummy")
    assert [d["name"] for d in load_results(tmp_path, phase=2)] == ["e2.1"]
    assert [d["name"] for d in load_results(tmp_path, phase=0)] == []
    assert sorted(d["name"] for d in load_results(tmp_path)) == ["dummy", "e2.1"]


def test_failing_experiment_sets_exit_code(tmp_path):
    class _Failing(DummyExperiment):
        def run(self):
            from kainos.harness.runner import Result

            return Result(name="fails", passed=False, value=0.0, threshold=">= 1.0")

    _, rc = run_experiments([_Failing(tmp_path)], tmp_path)
    assert rc == 1  # a failing experiment must fail the run (gate contract)


# ── reporting ───────────────────────────────────────────────────────────────


def test_render_is_a_markdown_table():
    r = Result(
        name="x",
        passed=False,
        value=0.5,
        evidence=[Path("a.json"), Path("b.json")],
        config={},
        threshold="== 1.0",
    )
    t = render([r])
    assert "| x | FAIL | 0.5 | == 1.0 | `a.json`, `b.json` |" in t
    assert t.count("\n") >= 4  # header + separator + row


def test_rendering_persisted_results_from_registry(tmp_path):
    run(DummyExperiment(tmp_path), tmp_path)
    data = load_results(tmp_path)
    assert data  # report command renders exactly these persisted records


# ── registration / resolution / phase selection ─────────────────────────────


def test_registry_contains_dummy_under_phase_0_key():
    assert "e0.dummy" in REGISTRY
    assert REGISTRY["e0.dummy"].name == "dummy"


def test_resolve_exact_key_and_short_name():
    assert resolve("e0.dummy").name == "dummy"
    assert resolve("dummy").name == "dummy"
    with pytest.raises(LookupError, match="unknown experiment"):
        resolve("nope")


def test_selected_all_phase_and_errors():
    assert [e.name for e in selected(all=True)] == [
        "dummy", "e1.1", "e1.2", "e1.3", "e1.4", "e1.5", "e2.1", "e2.2", "e2.3", "e2.4", "e2.5", "e3.1", "e3.2", "e3.3", "e3.4", "e3.5", "e3.6", "e3.7", "e4.1", "e5.0", "e5.1", "e5.2", "e5.3", "e5.4", "e6.1", "e6.10", "e6.11", "e6.12", "e6.13", "e6.14", "e6.15", "e6.16", "e6.17", "e6.18", "e6.19", "e6.2", "e6.20", "e6.21", "e6.22", "e6.23", "e6.24", "e6.25", "e6.26", "e6.27", "e6.3", "e6.35", "e6.36", "e6.4", "e6.5", "e6.6", "e6.7", "e6.8", "e6.9",
    ]
    assert [e.name for e in selected(phase=0)] == ["dummy"]
    assert [e.name for e in selected(phase=1)] == ["e1.1", "e1.2", "e1.3", "e1.4", "e1.5"]
    assert [e.name for e in selected(phase=2)] == ["e2.1", "e2.2", "e2.3", "e2.4", "e2.5"]
    assert [e.name for e in selected(phase=3)] == ["e3.1", "e3.2", "e3.3", "e3.4", "e3.5", "e3.6", "e3.7"]
    assert [e.name for e in selected(phase=4)] == ["e4.1"]
    assert [e.name for e in selected(phase=5)] == ["e5.0", "e5.1", "e5.2", "e5.3", "e5.4"]
    assert [e.name for e in selected(phase=6)] == ["e6.1", "e6.10", "e6.11", "e6.12", "e6.13", "e6.14", "e6.15", "e6.16", "e6.17", "e6.18", "e6.19", "e6.2", "e6.20", "e6.21", "e6.22", "e6.23", "e6.24", "e6.25", "e6.26", "e6.27", "e6.3", "e6.35", "e6.36", "e6.4", "e6.5", "e6.6", "e6.7", "e6.8", "e6.9"]
    with pytest.raises(LookupError, match="no experiments registered for phase 9"):
        selected(phase=9)
    with pytest.raises(LookupError, match="nothing selected"):
        selected()


def test_listing_shows_names_and_thresholds():
    listing = render_listing()
    assert "| e0.dummy |" in listing
    assert "| e1.1 |" in listing
    assert "| e1.2 |" in listing
    assert "| e1.3 |" in listing
    assert "| e1.4 |" in listing
    assert "| e1.5 |" in listing
    assert "| e2.1 |" in listing
    assert "| e2.5 |" in listing
    assert "== 1.0" in listing


# ── module entry point (make bench) ─────────────────────────────────────────


def test_module_execution_has_no_runtime_warning():
    """`python -m kainos.harness.runner` (the make bench path) must be clean."""

    res = subprocess.run(
        [sys.executable, "-m", "kainos.harness.runner", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0
    assert "RuntimeWarning" not in res.stderr


def test_package_reexports_runner_symbols():
    import kainos.harness as h

    assert h.REGISTRY is REGISTRY  # lazy PEP 562 re-export resolves to the same object


def test_module_main_name_and_all(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)  # --all also runs e1.1, which writes results/phase-1/e1.1.json (CWD-relative)
    monkeypatch.setenv("KAINOS_E2_GAMES", "24")  # keep the gate fast; published runs use 500
    monkeypatch.setenv("KAINOS_E2_SEQ", "50")
    # e3.2/e3.5 fast sizes for the gate (the official runs use the defaults;
    # see benchmarks/topology/bench.py and benchmarks/phi/bench.py):
    monkeypatch.setenv("KAINOS_E32_SAMPLES", "48")
    monkeypatch.setenv("KAINOS_E32_STEPS", "30")
    monkeypatch.setenv("KAINOS_E35_DOTS", "40")
    monkeypatch.setenv("KAINOS_E35_HIST", "256")
    # e3.1 must SKIP hermetically (it needs the owner's LAN Ollama server):
    for var in ("OLLAMA_ENDPOINT", "OLLAMA_MODEL"):
        monkeypatch.delenv(var, raising=False)
    assert main(["--name", "dummy", "--results-dir", str(tmp_path)]) == 0
    assert "PASS  dummy: 1.0" in capsys.readouterr().out
    assert (tmp_path / "dummy.md").exists()

    # --all: e2.1 records a FAIL (its directive threshold is not met on the
    # published corpus — win-rate is capped at 46/149 for ANY policy and the
    # questions-to-solve medians are identical; see the "deviation" field in
    # results/phase-2/e2.1.json and phase-2 results.md). A failing experiment
    # must fail the run (gate contract), so --all exits 1.
    assert main(["--all", "--results-dir", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "running 53 experiment(s)" in out
    assert "PASS  e1.1: 1.0" in out
    assert "PASS  e1.2" in out
    assert "PASS  e1.3" in out
    assert "PASS  e1.4" in out
    assert "FAIL  e2.1" in out
    assert "PASS  e2.2" in out
    assert "PASS  e2.3" in out
    assert "PASS  e2.4" in out
    assert "PASS  e2.5" in out
    assert "SKIP  e3.1" in out  # no Ollama in the test env: skip, not pass-or-fail
    # e3.2/e3.5: the method gate PASSES when the A/B produced an explicit
    # adopt/reject verdict with a documented margin (P8) — the verdict itself
    # is the finding and lives in the config/evidence, not in PASS/FAIL.
    assert "PASS  e3.2" in out
    assert "PASS  e3.3" in out  # the distributed bear story converges hermetically
    assert "PASS  e3.5" in out
    assert "PASS  e3.6" in out  # projected over declared capabilities, refuses honestly
    assert "PASS  e3.4" in out  # text and synthetic scene share one abstract pattern
    assert "PASS  e3.7" in out  # recursive workspace: query at depth 2, promotion discipline holds
    assert "PASS  e4.1" in out  # constraint core: honest under degradation, transfers to a new 4x4
    assert "PASS  e5.0" in out  # multi-agent kernel: view isolation + dispute discipline, deterministic
    assert "PASS  e5.1" in out  # shared grid: ToM separation + structurally clean false-belief probe
    assert "PASS  e5.3" in out  # strategy-development sweeps: store-data policy develops, frozen control flat
    assert "PASS  e5.4" in out  # the LLM-surface messaging arm: E5.1 acceptance survives the NL surface exactly (SKIP arm)
    assert "PASS  e6.1" in out  # the attended pilot: taught a strip, honest about its edges, survives the restart
    assert "PASS  e6.2" in out  # the ladder: the composition operations are exactly line-bound
    assert "PASS  e6.3" in out  # the un-attended loop: converges on the E6.2 line, the wall a store property
    assert "PASS  e6.4" in out  # phrasology: the intake boundary is exactly the lexicon (grammar first, honest unknowns, parse != content)
    assert "PASS  e6.8" in out  # savant S4: the seam (lemma/conjecture store layer) + the measured power-growth wall
    assert "PASS  e6.9" in out  # savant S5: the number-field toolkit (A-cluster, shallow) + the why/magnitude walls
    assert "PASS  e6.10" in out  # savant S6: the geometric criterion (scaffolded generation — the leap)
    assert "PASS  e6.11" in out  # savant S7: the arithmetical half (tower => disproof, the savant test proper)
    assert "PASS  e6.12" in out  # RH-TRACK S8: the ζ apparatus (the conjecture enters as open; the attempt is the wall)
    assert "PASS  e6.13" in out  # RH-TRACK S9: the criterion gallery (the store's own derived gap grounds the S9-form attempt)
    assert "PASS  e6.14" in out  # RH-TRACK S10: the attempt (the maximal assembly rh-reach grounds the S10-form wall)
    assert "PASS  e6.15" in out  # FUNDAMENTALS-TRACK S11: the sieve (the backward divisibility layer + the scan ledger)
    assert "PASS  e6.16" in out  # FUNDAMENTALS-TRACK S12: the RH neighborhood (the conditional layer + the two roads + the declared queue)
    assert "PASS  e6.17" in out  # FUNDAMENTALS-TRACK S13: the zeta variants, three families (the unconditional variant layer under the euler product)
    assert "PASS  e6.18" in out  # PRIZE-ISLANDS-TRACK BSD band 1 of 3: the elliptic city (curve form/law, Hasse census, CM shadow)
    assert "PASS  e6.19" in out  # PRIZE-ISLANDS-TRACK BSD band 2 of 3: the L-function of the city (local factors, exact-rational partials, ramification corrections)
    assert "PASS  e6.20" in out  # PRIZE-ISLANDS-TRACK BSD band 3 of 3 (SUMMIT): the descent and the reaching (the island closes: statement stored, panel satisfied, line's side held)
    assert "PASS  e6.21" in out  # PRIZE-ISLANDS-TRACK Beal island (single band): the valuation line (valuation off the spf chain, the lte ledger 249,280/0, the statement as declared record fact, the 83-triple verification census, zero primitive on the line, NO theorem:beal)
    assert "PASS  e6.22" in out  # PRIZE-ISLANDS-TRACK P vs NP band 1 of 2: the decidable line (decision/tamable/reduction/cost register, the pi census 23 via the reduction, the scan cost 192, the pigeonhole zero rows, the halting + machine-universe walls, NO theorem:p-vs-np)
    assert "PASS  e6.23" in out  # PRIZE-ISLANDS-TRACK P vs NP band 2 of 2 (SUMMIT): the difficulty line (the p/np classes on the line, the island statement as declared record, the parity census 2^(k-1) up to 32768, the filed blowup, the three barriers + the ac0 wall, NO theorem:p-vs-np — the island closes)
    assert "PASS  e6.24" in out  # CONNECTING-WORK: the weaving line (the synthesis pass over the four closed islands: the soil weaves, the node, the summit shape over the four islands, the shadow form and the boundary form, the filed composition, the four declared territories, the marker census 12/2/24 -> 13/2/24, NO bare island theorem ids — the weaving is one band of the course, not a new island)
    assert "PASS  e6.25" in out  # LOT-1 (FUNDAMENTALS forward fan): the condition line (the hypothesis as a usable assumption — assumed in the lot, never proved by it; the marker census 3 exact + 1 variant -> 6 exact + 1 variant; the line's consequences one line under the assumption; the filing fills the line, not the condition; NO bare island theorem ids)
    assert "PASS  e6.26" in out  # COURSE A band 1 of 2 (FUNDAMENTALS forward fan): the proportion line (the proportion as the RELATION between two parts of the line, named by its reduced form; the fraction as its VALUE over a positive part — one division in two languages, five over three one and two thirds and five mod three two; the closed four-family, the three chain divisions, the two-to-three class walk at twenty-eight; 0:0 the evenness of the two empty parts, declared, never valued — NO 0/0 value in the store; the strict two-part filing, D-e6t(a) off-script two to three; the line-end marker census 16/2/24 of 42 -> 17/2/24 of 43; the condition marker census 6/1/7 conserved; NO bare island theorem ids; 1966 + 3 facts + 52 events = 2021)
    assert "PASS  e6.27" in out  # COURSE A band 2 of 2 (FUNDAMENTALS forward fan): the prime proportion (two distinct primes share no part above one — the pair is its own reduced proportion, the fingerprint: 253 pairs, 253 proportions, no collisions; the six drilled chains in both languages, the seven-step ceiling with its four tied pairs; the never-reduced and colliding-fingerprint walls; the strict two-part filing; D-e6u(b) off-script three to five; the line-end marker census 17/2/24 of 43 -> 18/2/24 of 44; the condition marker census 6/1/7 conserved; NO bare island theorem ids; 2021 + 3 facts + 50 events = 2074)
    assert "PASS  e6.35" in out  # COURSE E band 1 of 2 (FUNDAMENTALS forward fan): the seeded line (the fibonacci line for pi, e, and the golden seed — the line for a seed c at seed one and c under the sum law, reading on the sum line's own skeleton; the shift seeds one and two; the cassini weight silent at the golden equation; the golden seed off the floor named by the equation x squared equals x plus one, never by a digit; the filing files the line, not the constants; the marker census 6/1/7 conserved; NO bare island theorem ids)
    assert "PASS  e6.36" in out  # COURSE E band 2 of 2 (FUNDAMENTALS forward fan): the seed census (the seeded line's own residue story in the page's wordings — the pisano count with the class-three-mod-five shadow, the parity rotation, the law of my sums dividing; the off-line seed's value story with the lucas shadow and the one-over-eighty-nine declared never filed; the strict two-part filing, D-e6s(a) form; the line-end marker census 15/2/24 of 41 -> 16/2/24 of 42; the condition marker census 6/1/7 conserved; NO bare island theorem ids; the store-global event-id dedupe: 1921 + 3 facts + 42 events = 1966)
    e32 = json.loads((tmp_path / "e3.2.json").read_text())
    assert e32["config"]["verdict"] in ("adopt", "reject")
    assert e32["config"]["param_budget"]["equal"] is True  # same-budget claim is structural
    e35 = json.loads((tmp_path / "e3.5.json").read_text())
    assert e35["config"]["verdict"] in ("adopt", "reject")
    assert e35["config"]["bits_per_value"] == 8
    e33 = json.loads((tmp_path / "e3.3.json").read_text())
    assert e33["value"] == 1.0 and e33["config"]["converged"] is True
    assert e33["config"]["new_context_terms"] == ["ctx:time:polar_bear"]
    assert e33["config"]["idempotent_remerge"] is True
    e36 = json.loads((tmp_path / "e3.6.json").read_text())
    assert e36["config"]["validity"] == 1.0 and e36["config"]["refusal"] == 1.0
    assert e36["config"]["clarification_policy"]["high_stakes"] == "ask"
    assert e36["config"]["clarification_policy"]["low_stakes"] == "default"
    e34 = json.loads((tmp_path / "e3.4.json").read_text())
    assert e34["value"] == 1.0 and e34["config"]["pattern_matched"] is True
    assert e34["config"]["consolidated_entities"] == ["box"]
    e37 = json.loads((tmp_path / "e3.7.json").read_text())
    assert e37["value"] == 1.0 and e37["config"]["negative_control_passed"] is True
    assert e37["config"]["recursion_depth"] >= 2
    assert all(v == "candidate" for v in e37["config"]["promotion"]["status"].values())
    e41 = json.loads((tmp_path / "e4.1.json").read_text())
    assert e41["value"] == 1.0 and e41["passed"] is True
    assert e41["config"]["checks_passed"] == e41["config"]["checks"] == 14
    assert e41["config"]["arm_f_status"] == "SKIPPED"  # no Ollama in the test env
    assert e41["config"]["arm_c_solutions"] == 2
    e31 = json.loads((tmp_path / "e3.1.json").read_text())
    assert e31["skipped"] is True and e31["config"]["skip_reason"].startswith("Ollama backend unreachable")

    e21 = json.loads((tmp_path / "e2.1.json").read_text())
    assert e21["passed"] is False
    assert e21["config"]["deviation"]  # the deviation explanation is part of the harness record
    e21_full = json.loads((tmp_path / "results/phase-2/e2.1.json").read_text())
    assert e21_full["deviation"]
    assert e21_full["convergence_median_reduction"] >= 0.2  # A1 convergence holds strongly

    assert main(["--phase", "0", "--results-dir", str(tmp_path)]) == 0

    assert main(["--name", "nope", "--results-dir", str(tmp_path)]) == 1
    assert "unknown experiment" in capsys.readouterr().err
    assert main(["--phase", "9", "--results-dir", str(tmp_path)]) == 1
