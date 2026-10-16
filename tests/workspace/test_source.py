"""Sources vs analyses — immutable, versioned, append-only; hash-dependency
stale-flagging (ADR-0012)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from kainos.workspace.source import DERIVED_FROM, SourceRef, SourceRegistry


def _registry(tmp_path: Path) -> tuple[SourceRegistry, str]:
    f = tmp_path / "doc.txt"
    f.write_text("v1 content\n")
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    reg = SourceRegistry()
    reg.register(SourceRef(uri="doc.txt", hash=h))
    return reg, "doc.txt"


def test_analyses_are_append_only_and_versioned(tmp_path: Path) -> None:
    reg, sid = _registry(tmp_path)
    a1 = reg.add_analysis(sid, {"kind": "state", "relationships": [{"subject": "v1", "relation": DERIVED_FROM, "object": sid}]}, created_at="t1")
    a2 = reg.add_analysis(sid, {"kind": "state", "relationships": [{"subject": "v2", "relation": DERIVED_FROM, "object": sid}]}, created_at="t2")
    assert (a1.version, a2.version) == (1, 2)
    # v1 is still exactly what it was after v2 landed (never overwritten):
    assert reg.analyses(sid)[0] == a1
    assert reg.analyses(sid) == [a1, a2]
    assert reg.latest_analysis(sid) == a2


def test_latest_analysis_requires_an_analysis(tmp_path: Path) -> None:
    reg, sid = _registry(tmp_path)
    with pytest.raises(KeyError):
        reg.latest_analysis(sid)
    reg.add_analysis(sid, {"kind": "state"}, created_at="t1")
    assert reg.latest_analysis(sid).version == 1


def test_stale_derivations_flagged_on_hash_change_only(tmp_path: Path) -> None:
    reg, sid = _registry(tmp_path)
    ir = {"kind": "state", "relationships": [{"subject": "x", "relation": DERIVED_FROM, "object": sid}]}
    reg.add_analysis(sid, ir, created_at="t1")
    ir_plain = {"kind": "state", "relationships": [{"subject": "x", "relation": "about", "object": "y"}]}
    reg.add_analysis(sid, ir_plain, created_at="t2")  # declares NO dependency

    same_hash = reg.source(sid).hash
    assert reg.stale_derivations(sid, same_hash) == []
    flagged = reg.stale_derivations(sid, "f" * 64)
    assert flagged == [f"{sid}:1"]  # only the analysis that declared derived_from


def test_hash_file_and_registration_errors(tmp_path: Path) -> None:
    from kainos.workspace.source import hash_file

    f = tmp_path / "x.txt"
    f.write_text("abc")
    assert hash_file(f) == hashlib.sha256(b"abc").hexdigest()

    reg, _ = _registry(tmp_path)
    with pytest.raises(ValueError):
        reg.register(SourceRef(uri="doc.txt", hash="x"))  # duplicate uri
    with pytest.raises(KeyError):
        reg.add_analysis("nope", {"kind": "state"}, created_at="t")
