"""LLMKernel tests (P1.14) — the LLM behind the SAME LanguageKernel protocol,
with a MOCKED backend (the gate's requirement). The live server smoke test is
skipped unless the owner's Ollama endpoint is reachable (hermetic gate).
"""

from __future__ import annotations

import json
import urllib.request

import pytest

from kainos.lang.kernel import LanguageKernel
from kainos.lang.llm import LLMKernel, MockBackend, OllamaBackend
from kainos.regex.ir import Node

SPEC_DOC = {
    "kind": "pattern",
    "entities": [
        {"id": "e0", "type": "Sequence"},
        {"id": "e1", "type": "Repeat"},
        {"id": "e2", "type": "Class", "labels": ["digit"]},
    ],
    "relationships": [
        {"subject": "e1", "relation": "repeat", "object": "e2", "context": {"kind": "exactly", "n": 3}},
        {"subject": "e0", "relation": "sequence", "object": "e1", "context": {"position": 0}},
        {"subject": "e0", "relation": "sequence", "object": "u0", "context": {"position": 1}},
    ],
    "unresolved": [{"id": "u0", "surface": "hyphen", "candidates": ["hyphen"]}],
    "meta": {"dialect": "kainos/regex/1"},
}


def _schema_path(tmp_path=None):
    from pathlib import Path

    p = Path("specs/ir.schema.json")
    return p if p.is_file() else Path(__file__).resolve().parents[3] / "specs" / "ir.schema.json"


def test_llmkernel_is_a_language_kernel():
    kernel = LLMKernel(MockBackend(["{}"]), schema_path=_schema_path())
    assert isinstance(kernel, LanguageKernel)


def test_parse_valid_ast_returns_interpretation():
    backend = MockBackend([json.dumps(SPEC_DOC)])
    kernel = LLMKernel(backend, schema_path=_schema_path())
    interpretations = kernel.parse("three digits, then a hyphen")
    assert len(interpretations) == 1
    interp = interpretations[0]
    assert isinstance(interp.ir, Node)
    assert interp.score == 1.0
    assert interp.unresolved == ["hyphen"]
    # One completion call, AST prompt in front.
    assert len(backend.calls) == 1
    assert backend.calls[0][0]["role"] == "system"
    assert backend.calls[0][1]["content"] == "three digits, then a hyphen"


def test_parse_retries_on_invalid_then_succeeds():
    garbage = "definitely not json"
    good = json.dumps(SPEC_DOC)
    backend = MockBackend([garbage, good])
    kernel = LLMKernel(backend, schema_path=_schema_path())
    interp = kernel.parse("x")[0]
    assert isinstance(interp.ir, Node)
    assert len(backend.calls) == 2
    # The retry carries the assistant's bad answer + a correction instruction.
    retry = backend.calls[1]
    assert retry[-1]["role"] == "user"
    assert "Invalid document" in retry[-1]["content"]


def test_parse_raises_when_model_cannot_recover():
    kernel = LLMKernel(MockBackend(["no json here", "still no json"]), schema_path=_schema_path())
    with pytest.raises(ValueError, match="could not produce a valid AST"):
        kernel.parse("x")


def test_parse_rejects_schema_invalid_document():
    bad = dict(SPEC_DOC, kind="not-a-kind")
    kernel = LLMKernel(MockBackend([json.dumps(bad)] * 2), schema_path=_schema_path())
    with pytest.raises(ValueError):
        kernel.parse("x")


def test_parse_rejects_dangling_relationship():
    bad = json.loads(json.dumps(SPEC_DOC))
    bad["relationships"] = [
        {"subject": "e0", "relation": "sequence", "object": "u99", "context": {"position": 0}}
    ]
    kernel = LLMKernel(MockBackend([json.dumps(bad)] * 2), schema_path=_schema_path())
    with pytest.raises(ValueError):
        kernel.parse("x")


def test_parse_accepts_fenced_json():
    backend = MockBackend([f"```json\n{json.dumps(SPEC_DOC)}\n```"])
    kernel = LLMKernel(backend, schema_path=_schema_path())
    interp = kernel.parse("x")[0]
    assert isinstance(interp.ir, Node)


def test_realize_is_the_deterministic_emitter():
    kernel = LLMKernel(MockBackend([json.dumps(SPEC_DOC)]), schema_path=_schema_path())
    interp = kernel.parse("three digits, then a hyphen")[0]
    # Unresolved ref -> the emitter refuses (no justified regex); propose is empty.
    from kainos.regex.emitter import UnresolvedError

    with pytest.raises(UnresolvedError):
        kernel.realize(interp.ir)
    assert kernel.propose(interp.ir) == []


def test_ollama_backend_env_parsing(monkeypatch):
    monkeypatch.setenv("OLLAMA_ENDPOINT", '"http://192.168.1.65:11434/v1"')
    monkeypatch.setenv("OLLAMA_MODEL", '"pi-qwen-fast:latest"')
    backend = OllamaBackend()
    # Quoting stripped; the native API base strips the /v1 suffix.
    assert backend.base == "http://192.168.1.65:11434"
    assert backend.model == "pi-qwen-fast:latest"


def test_ollama_backend_requires_config(monkeypatch):
    monkeypatch.delenv("OLLAMA_ENDPOINT", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    with pytest.raises(ValueError, match="OLLAMA_ENDPOINT"):
        OllamaBackend()
    with pytest.raises(ValueError, match="OLLAMA_MODEL"):
        OllamaBackend(endpoint="http://x:11434")


# ── live smoke (skipped when the owner's server is unreachable) ─────────────


def _endpoint_from_env() -> tuple[str, str] | None:
    import os

    ep = os.environ.get("OLLAMA_ENDPOINT", "").strip().strip('"')
    model = os.environ.get("OLLAMA_MODEL", "").strip().strip('"')
    if not ep or not model:
        return None
    return ep.removesuffix("/v1").rstrip("/"), model


def _reachable(base: str) -> bool:
    try:
        with urllib.request.urlopen(base + "/api/tags", timeout=3):
            return True
    except (TimeoutError, urllib.error.URLError, OSError):
        return False


def _ollama_target() -> tuple[str, str] | None:
    t = _endpoint_from_env()
    if t is None:
        return None
    return t if _reachable(t[0]) else None


@pytest.mark.skipif(
    _ollama_target() is None,
    reason="owner's Ollama endpoint not reachable from here (offline gate stays hermetic)",
)
def test_live_ollama_parses_a_canonical_description():
    t = _ollama_target()
    assert t is not None
    backend = OllamaBackend(endpoint=t[0], model=t[1], timeout=300)
    kernel = LLMKernel(backend, schema_path=_schema_path(), max_attempts=2)
    interp = kernel.parse("three digits, then a hyphen")[0]
    assert isinstance(interp.ir, Node)
    info = backend.server_info()
    assert info["model"] == t[1]
    # The model's AST must contain the digit class somewhere.
    from kainos.regex.ir import to_ir

    assert "digit" in json.dumps(to_ir(interp.ir))
