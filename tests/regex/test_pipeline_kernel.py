"""The `kernel` seam in `describe` (P3.01): the CODEX/reasoner/emitter path must
be kernel-independent — E3.1's isolation guarantee, unit-tested hermetically.
"""

from __future__ import annotations

import json

from kainos.lang.deterministic import DeterministicKernel
from kainos.lang.llm import LLMKernel, MockBackend
from kainos.regex.ir import to_ir
from kainos.regex.pipeline import default_codex, describe


class RaisingBackend:
    def complete(self, messages: list[dict[str, str]]) -> str:
        raise ConnectionError("backend down")


def _doc_for(text: str) -> str:
    return json.dumps(to_ir(DeterministicKernel(default_codex()).parse(text)[0].ir))


def test_default_kernel_is_still_deterministic_and_score_one():
    r = describe("three digits")
    assert r.pcre is not None and r.parse_score == 1.0
    assert r.to_dict()["parse_score"] == 1.0


def test_explicit_llm_kernel_is_parity_identical_downstream():
    """Same text, two kernels, same CODEX: identical resolved tree + pcre +
    confidence; only the kernel's own marking differs."""

    text = "a hyphen, then whitespace, then exactly two letters"
    store = default_codex()  # one shared store, as in E3.1

    det = describe(text, codex=store, kernel=DeterministicKernel(store))
    llm = describe(text, codex=store, kernel=LLMKernel(MockBackend([_doc_for(text)])))

    assert llm.pcre == det.pcre
    assert to_ir(llm.ir) == to_ir(det.ir)
    assert llm.confidence == det.confidence
    assert llm.parse_score == 1.0
    assert llm.resolved_trace == det.resolved_trace


def test_fallback_mark_flows_through_describe():
    """LLM backend down + configured fallback: describe still returns the
    deterministic reading, marked with the lowered parse score (P3.01)."""

    text = "three digits"
    store = default_codex()
    fallback = DeterministicKernel(store)
    kernel = LLMKernel(RaisingBackend(), fallback=fallback, fallback_score=0.5)
    ref = describe(text, codex=store, kernel=DeterministicKernel(store))
    res = describe(text, codex=store, kernel=kernel)

    assert res.pcre == ref.pcre
    assert res.parse_score == 0.5
    assert res.to_dict()["parse_score"] == 0.5
    assert kernel.fallback_events[0]["fallback"] == "used"


def test_llm_failure_without_fallback_propagates():
    kernel = LLMKernel(RaisingBackend())
    try:
        describe("three digits", codex=default_codex(), kernel=kernel)
        raise AssertionError("expected ValueError to propagate from the kernel")
    except ValueError as e:
        assert "after 2 attempts" in str(e)


def test_unresolved_escalation_uses_the_llm_reading():
    """An LLM reading containing an unresolved surface escalates through the
    SAME pipeline invariant (no pcre, ask_human) as a deterministic one."""

    from kainos.lang.deterministic import _unresolved_surfaces

    # "the dash thing" is the vague-set idiom: an UnresolvedRef with no seeded
    # see_also alias to rotate it (default_codex, unlike the E1.4 test codex).
    text = "three digits, then the dash thing"
    det_kernel = DeterministicKernel(default_codex())
    doc = det_kernel.parse(text)[0].ir
    resolved_det = describe(text, codex=default_codex(), kernel=det_kernel)

    llm_kernel = LLMKernel(MockBackend([json.dumps(to_ir(doc))]))
    resolved_llm = describe(text, codex=default_codex(), kernel=llm_kernel)

    assert _unresolved_surfaces(doc)  # sanity: the test input really is ambiguous
    assert resolved_det.pcre is None and resolved_det.escalation is not None
    assert resolved_llm.pcre is None and resolved_llm.escalation is not None
    assert resolved_llm.escalation["recommended_action"] == "ask_human"
