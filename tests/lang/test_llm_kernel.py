"""LLMKernel contract (P3.01): interface compliance, validation + one retry,
deterministic fallback with score marking, backend hygiene.

Hermetic: all completion calls are served by `MockBackend`/
`RaisingBackend`; the only network-shaped object exercised is the Ollama
`/api/tags` probe against a closed local port (connection refused, no route
required). Live-server behavior is the E3.1 experiment's job (step 17).
"""

from __future__ import annotations

import json

import pytest

from kainos.lang.deterministic import DeterministicKernel
from kainos.lang.kernel import Interpretation, LanguageKernel
from kainos.lang.llm import LLMKernel, MockBackend, OllamaBackend
from kainos.regex.bench import default_corpus_path
from kainos.regex.data import load_corpus
from kainos.regex.emitter import emit
from kainos.regex.ir import Class, ClassKind, to_ir
from kainos.regex.pipeline import default_codex


class RaisingBackend:
    """A backend that always fails (transport-level failure simulation)."""

    def __init__(self, exc: Exception) -> None:
        self.exc = exc
        self.calls = 0

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.calls += 1
        raise self.exc


def _doc_for(text: str) -> str:
    """The reference generic-IR document for `text`: whatever the DETERMINISTIC
    kernel parses, run through the same to_ir codec the LLM is prompted to emit.
    (The step-12 prompt claims byte-level parity with this codec; verifying it
    here keeps the mock's answers honest.)"""

    kernel = DeterministicKernel(default_codex())
    return json.dumps(to_ir(kernel.parse(text)[0].ir))


def _llm(replies: list[str], fallback: DeterministicKernel | None = None, **kw) -> LLMKernel:
    return LLMKernel(MockBackend(replies), fallback=fallback, **kw)


# ── P3.01 verify: interface compliance ──────────────────────────────────────


def test_llm_kernel_is_a_language_kernel():
    kernel = _llm(["{}"])
    assert isinstance(kernel, LanguageKernel)
    assert callable(kernel.parse) and callable(kernel.realize) and callable(kernel.propose)
    assert kernel.propose(Class(ClassKind.digit)) == []


def test_realize_uses_the_deterministic_emitter():
    node = DeterministicKernel(default_codex()).parse("three digits")[0].ir
    assert _llm(["{}"]).realize(node) == emit(node)
    with pytest.raises(TypeError, match="dialect Node"):
        _llm(["{}"]).realize("not a node")


# ── validation + one self-correction retry ──────────────────────────────────


def test_parse_valid_document_roundtrips_through_the_codec():
    kernel = _llm([_doc_for("three digits")], fallback=DeterministicKernel(default_codex()))
    interps = kernel.parse("three digits")
    assert len(interps) == 1 and isinstance(interps[0], Interpretation)
    det = emit(DeterministicKernel(default_codex()).parse("three digits")[0].ir)
    assert emit(interps[0].ir) == det
    assert interps[0].score == 1.0


def test_seed_corpus_parity_with_reference_documents():
    """The full Phase 1 seed corpus through the LLM's own validate->from_ir
    path, each mock answer being the deterministic kernel's own to_ir doc: the
    rebuilt tree must be document-identical for every record."""

    records = load_corpus(default_corpus_path())
    refs = [json.loads(_doc_for(r["description"])) for r in records]
    kernel = _llm([json.dumps(d) for d in refs])
    for rec, ref in zip(records, refs, strict=True):
        (interp,) = kernel.parse(rec["description"])
        assert to_ir(interp.ir) == ref, f"LLM parse diverged on {rec['id']!r}"


def test_invalid_then_valid_is_retried_once_with_the_error():
    backend = MockBackend(["totally not json", _doc_for("three digits")])
    kernel = LLMKernel(backend)
    (interp,) = kernel.parse("three digits")
    assert emit(interp.ir) == emit(DeterministicKernel(default_codex()).parse("three digits")[0].ir)
    assert len(backend.calls) == 2
    second = backend.calls[1]
    assert second[-1]["role"] == "user"
    assert "Invalid document" in second[-1]["content"]
    assert second[-2] == {"role": "assistant", "content": "totally not json"}


def test_invalid_twice_raises_after_exactly_two_attempts():
    backend = MockBackend(["nope", "still nope"])
    with pytest.raises(ValueError, match="after 2 attempts"):
        LLMKernel(backend).parse("three digits")
    assert len(backend.calls) == 2  # one self-correction retry, not a loop


def test_schema_violation_counts_as_invalid():
    bad = json.dumps({"kind": "bogus", "entities": [], "relationships": []})
    backend = MockBackend([bad, _doc_for("three digits")])
    (interp,) = LLMKernel(backend).parse("three digits")
    assert emit(interp.ir) == emit(DeterministicKernel(default_codex()).parse("three digits")[0].ir)


def test_markdown_fences_are_stripped():
    doc = "```json\n" + _doc_for("three digits") + "\n```"
    (interp,) = _llm([doc]).parse("three digits")
    assert emit(interp.ir) == emit(DeterministicKernel(default_codex()).parse("three digits")[0].ir)


# ── P3.01: deterministic fallback with lowered score ────────────────────────


def test_fallback_used_on_transport_error_marks_score():
    backend = RaisingBackend(ConnectionError("boom"))
    fallback = DeterministicKernel(default_codex())
    kernel = LLMKernel(backend, fallback=fallback, fallback_score=0.25)
    interps = kernel.parse("three digits")
    assert backend.calls == 2  # attempted, retried, then fell back
    (interp,) = interps
    assert interp.score == 0.25  # marked LOWER than a first-hand reading
    assert emit(interp.ir) == emit(fallback.parse("three digits")[0].ir)
    assert kernel.fallback_events == [{"text": "three digits", "error": "ConnectionError: boom", "fallback": "used"}]


def test_fallback_score_never_exceeds_the_reading_score():
    backend = RaisingBackend(OSError("down"))
    kernel = LLMKernel(backend, fallback=DeterministicKernel(default_codex()), fallback_score=0.9)
    (interp,) = kernel.parse("three digits")
    assert interp.score == 0.9


def test_fallback_failure_propagates_an_error():
    backend = RaisingBackend(ConnectionError("boom"))
    kernel = LLMKernel(backend, fallback=DeterministicKernel(default_codex()))
    # 'either' is structurally unparseable for the deterministic kernel too:
    with pytest.raises(ValueError, match="fallback kernel also failed"):
        kernel.parse("either")
    assert kernel.fallback_events == [
        {"text": "either", "error": "ConnectionError: boom", "fallback": "failed"}
    ]


def test_without_fallback_the_error_propagates():
    backend = RaisingBackend(ConnectionError("boom"))
    with pytest.raises(ValueError, match="after 2 attempts"):
        LLMKernel(backend).parse("three digits")
    assert backend.calls == 2  # retried once before giving up


# ── Ollama backend hygiene ──────────────────────────────────────────────────


def test_ollama_base_derives_native_api_from_v1_url():
    for url in ("http://192.168.1.65:11434/v1", "http://192.168.1.65:11434/v1/", "http://192.168.1.65:11434"):
        assert OllamaBackend(endpoint=url, model="m").base == "http://192.168.1.65:11434"


def test_ollama_requires_env_when_not_passed():
    import os

    saved = {k: os.environ.pop(k, None) for k in ("OLLAMA_ENDPOINT", "OLLAMA_MODEL")}
    try:
        with pytest.raises(ValueError, match="OLLAMA_ENDPOINT"):
            OllamaBackend()
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def test_ping_raises_when_server_unreachable():
    b = OllamaBackend(endpoint="http://127.0.0.1:9", model="none")
    with pytest.raises(OSError):
        b.ping()
