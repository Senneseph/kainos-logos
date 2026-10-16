"""CLI tests (P0.07) — in-process main() with tmp --db, plus one subprocess check
that the installed `kainos` entry point is wired.

Directive scenarios: add via CLI then dump shows the assertion; `ir validate`
exits 0 with OK on the golden IR and 1 on {}.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from kainos.cli import main
from kainos.codex.models import EpistemicState
from tests.codex.helpers import make_assertion, make_provenance

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_IR = REPO_ROOT / "tests" / "ir" / "golden" / "minimal.json"


@pytest.fixture()
def db(tmp_path: Path) -> str:
    return str(tmp_path / "data" / "codex.sqlite")


def _write(tmp_path: Path, name: str, obj: object) -> str:
    p = tmp_path / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


# ── codex add / dump round trip ────────────────────────────────────────────


def test_add_then_dump_shows_assertion(tmp_path, db, capsys):
    f = _write(tmp_path, "a1.json", make_assertion("a1", "France", "CAPITAL_OF", "Paris").to_dict())
    assert main(["codex", "add", "--file", f, "--db", db]) == 0
    assert "added a1" in capsys.readouterr().out

    assert main(["codex", "dump", "--db", db]) == 0
    dumped = json.loads(capsys.readouterr().out)
    assert {a["id"] for a in dumped["assertions"]} == {"a1"}
    # "Paris" is a raw string object (not a TermRef) — correctly absent from terms.
    assert sorted(t["id"] for t in dumped["terms"]) == ["CAPITAL_OF", "France"]


def test_add_rejects_invalid_assertion(tmp_path, db, capsys):
    f = _write(tmp_path, "bad.json", {"id": "x"})  # no provenance
    assert main(["codex", "add", "--file", f, "--db", db]) == 1
    assert "not a valid assertion" in capsys.readouterr().err


def test_add_missing_file_is_exit_1(tmp_path, db, capsys):
    assert main(["codex", "add", "--file", str(tmp_path / "nope.json"), "--db", db]) == 1
    assert "cannot read" in capsys.readouterr().err


# ── codex query / explain ──────────────────────────────────────────────────


def test_query_prints_json_lines(tmp_path, db, capsys):
    a1 = make_assertion("a1", "France", "CAPITAL_OF", "Paris", status=EpistemicState.established)
    a2 = make_assertion("a2", "France", "CAPITAL_OF", "Lyon", status=EpistemicState.disputed)
    for a in (a1, a2):
        f = _write(tmp_path, f"{a.id}.json", a.to_dict())
        assert main(["codex", "add", "--file", f, "--db", db]) == 0
        capsys.readouterr()  # drain the "added" line

    assert main(["codex", "query", "--subject", "France", "--db", db]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert [json.loads(line)["id"] for line in lines] == ["a1", "a2"]

    # Status filter.
    assert main(["codex", "query", "--subject", "France", "--status", "disputed", "--db", db]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert [json.loads(line)["id"] for line in lines] == ["a2"]

    # Bad status value is a handled error.
    assert main(["codex", "query", "--status", "riddle", "--db", db]) == 1
    assert "unknown status" in capsys.readouterr().err


def test_explain_prints_chain(tmp_path, db, capsys):
    a1 = make_assertion("a1", "S1", "R1", "O1")
    a2 = make_assertion("a2", "S2", "R2", "O2", provenance=make_provenance(evidence=["a1", "ghost"]))
    for a in (a1, a2):
        f = _write(tmp_path, f"{a.id}.json", a.to_dict())
        assert main(["codex", "add", "--file", f, "--db", db]) == 0
        capsys.readouterr()  # drain the "added" line

    assert main(["codex", "explain", "a2", "--db", db]) == 0
    ex = json.loads(capsys.readouterr().out)
    assert [e["id"] for e in ex["chain"]] == ["a1", "ghost"]
    assert ex["chain"][0]["assertion"]["id"] == "a1"
    assert ex["chain"][1] == {"id": "ghost", "missing": True}


def test_explain_unknown_id_renders_missing_with_exit_0(db, capsys):
    assert main(["codex", "explain", "nope", "--db", db]) == 0
    assert json.loads(capsys.readouterr().out) == {"id": "nope", "missing": True}


def test_dump_out_writes_file(tmp_path, db, capsys):
    f = _write(tmp_path, "a1.json", make_assertion("a1", "S1", "R1", "O1").to_dict())
    main(["codex", "add", "--file", f, "--db", db])
    out = str(tmp_path / "exports" / "dump.json")  # nested path — CLI must mkdir
    assert main(["codex", "dump", "--out", out, "--db", db]) == 0
    assert json.loads(Path(out).read_text())["assertions"][0]["id"] == "a1"
    assert "to " + out in capsys.readouterr().err  # confirmation goes to stderr


# ── ir validate ────────────────────────────────────────────────────────────


def test_ir_validate_golden_ok(capsys):
    assert main(["ir", "validate", str(GOLDEN_IR)]) == 0
    assert capsys.readouterr().out.strip() == "OK"


def test_ir_validate_empty_dict_fails(tmp_path, capsys):
    f = _write(tmp_path, "empty.json", {})
    assert main(["ir", "validate", f]) == 1
    assert "invalid" in capsys.readouterr().err


def test_ir_validate_unknown_kind_fails_with_path(tmp_path, capsys):
    f = _write(tmp_path, "bad.json", {"kind": "riddle"})
    assert main(["ir", "validate", f]) == 1
    assert "$.kind" in capsys.readouterr().err


def test_ir_validate_missing_file_is_exit_1(tmp_path, capsys):
    assert main(["ir", "validate", str(tmp_path / "nope.json")]) == 1
    assert "cannot read" in capsys.readouterr().err


# ── installed entry point ──────────────────────────────────────────────────


def test_console_script_is_wired():
    """The `kainos` console script (pip install -e .) must exist and work."""

    res = subprocess.run(
        ["kainos", "ir", "validate", str(GOLDEN_IR)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, res.stderr
    assert res.stdout.strip() == "OK"
