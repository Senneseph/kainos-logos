"""The curriculum sequencer + spaced re-exposure queue (T4, layer 4).

"Sequencer (prereqs stable ^ max learning value)" and "spaced re-exposure
queue" from the spec — implemented as PURE RECOMPUTE from the CODEX
(P11: the curriculum's decisions are store data, not mutable state):
nothing here is written to the store; the same store + session number
always yields the same decision.

Frozen policy (deterministic, no clock, no randomness):

- readiness: only concepts whose prereqs are all `stable` may be proposed
  (the mastery recompute already enforces the prereq gate downstream).
- value (the learning-value order, frozen): a concept that is
  `practicing` (close to stable — finish it) beats one that is `exposed`
  (started, not yet derived) beats one that is `unexposed`-but-ready
  (new material); tiebreak: band order, then concept id.
- re-exposure: an UNSTABLE (exposed/practicing) ready concept is due at
  EVERY boot until stable (the re-drill); a stable concept is retested at
  a spaced interval — frozen REEXPOSE_INTERVAL = 3 sessions after the
  last session that recorded a derivation for it (spaced recall, the
  substrate's "forgetting is logged" generalized: the lapse between
  sessions IS the forgetting the spacing defends against).
- proposals are GROUNDED: a drill is only proposed for a fact the infant
  can actually derive (established chain), so a proposed drill always has
  an answer. Nothing derivable => no proposal (honest empty, not a
  fabricated drill).

The frozen E6.1 pilot does NOT call this module (the scripted teacher is
the driver there); the sequencer is the driver for the un-attended
regime (T5) and for the tutor's autonomous mode behind the OpenAI face
(T1).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kainos.codex.models import EpistemicState
from kainos.tutor.mastery import BANDS, MasteryState, concept, mastery_view

if TYPE_CHECKING:  # pragma: no cover
    from kainos.codex.memory import InMemoryCodexStore

__all__ = ["REEXPOSE_INTERVAL", "due_concepts", "next_drill", "strip_candidates"]

#: Frozen spacing: retest a stable concept every N sessions after its last
#: derivation (session numbers come from the store, not the wall clock).
REEXPOSE_INTERVAL = 3

_VALUE_ORDER = {MasteryState.PRACTICING: 0, MasteryState.EXPOSED: 1, MasteryState.UNEXPOSED: 2}


def _facts_for(concept_id: str, codex: InMemoryCodexStore) -> tuple[tuple[int, int], ...]:
    """The ESTABLISHED successor facts of the concept, as (n, m) pairs."""

    out: list[tuple[int, int]] = []
    for a in codex.query(context_match={"kind": "fact", "concept": concept_id}):
        sid = a.subject.id
        oid = a.object_id
        pre = f"{concept_id}:succ-of("
        if sid.startswith(pre) and oid.startswith(f"{concept_id}:num("):
            n = int(sid[len(pre) : -1])
            m = int(oid[len(f"{concept_id}:num(") : -1])
            if a.validity is None or a.validity.to is None:
                out.append((n, m))
    return tuple(sorted(out))


def _chain_complete(concept_id: str, facts: tuple[tuple[int, int], ...], a: int, b: int) -> bool:
    have = {n: m for n, m in facts}
    x = a
    for _ in range(b):
        if x not in have:
            return False
        x = have[x]
    return True


def _rule_established(concept_id: str, codex: InMemoryCodexStore) -> bool:
    """E6.2: is the capability's rule/definition fact established?
    Grounded proposals never cross an unlearned capability (honest
    non-proposal, like the honest no)."""

    for a in codex.query(relation="policy"):
        if a.context.data.get("concept") != concept_id or a.context.data.get("kind") not in ("rule", "definition"):
            continue
        if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None):
            return True
    return False


def _repeated_add_reachable(facts: tuple[tuple[int, int], ...], a: int, b: int) -> bool:
    """Can a*b be computed by repeated addition on the established facts?
    Simulate total=0, a times total+=b, requiring each chain complete."""

    x = 0
    for _ in range(a):
        if not _chain_complete("count-successor", facts, x, b):
            return False
        x += b
    return True


def strip_candidates(concept_id: str, codex: InMemoryCodexStore) -> list[dict[str, Any]]:
    """Grounded drill candidates for a concept (always answerable)."""

    if concept_id in ("add-within-10",):
        # addition rides the successor strip: the candidate drills chain
        # count-successor facts, so those are the facts consulted.
        out: list[dict[str, Any]] = []
        facts = _facts_for("count-successor", codex)
        have = {n: m for n, m in facts}
        for a in sorted(have):
            for b in (1, 2, 3, 4, 5):
                if a + b <= 10 and _chain_complete("count-successor", facts, a, b):
                    out.append({"concept": concept_id, "surface": f"{a} + {b} is what?", "slots": {"mode": "add", "a": a, "b": b}})
        return out
    if concept_id == "add-two-digit":
        # E6.2: the wide addition strip (sums 11..30), same chaining.
        out = []
        facts = _facts_for("count-successor", codex)
        have = {n: m for n, m in facts}
        for a in sorted(have):
            for b in (1, 2, 3, 4, 5):
                if 11 <= a + b <= 30 and _chain_complete("count-successor", facts, a, b):
                    out.append({"concept": concept_id, "surface": f"{a} + {b} is what?", "slots": {"mode": "add", "a": a, "b": b}})
        return out
    if concept_id == "sub-within-30":
        # E6.2: walk-back — derivable iff the line covers a (facts 0..a).
        if not _rule_established(concept_id, codex):
            return []
        out = []
        facts = _facts_for("count-successor", codex)
        for a in sorted({n for n, _ in facts}):
            for b in (1, 2, 3, 4, 5):
                if 0 < a <= 30 and a >= b and _chain_complete("count-successor", facts, 0, a):
                    out.append({"concept": concept_id, "surface": f"{a} - {b} is what?", "slots": {"mode": "sub", "a": a, "b": b}})
        return out
    if concept_id == "mult-within-100":
        # E6.2: repeated addition — derivable iff every inner chain stays
        # established (simulated, nothing guessed).
        if not _rule_established(concept_id, codex):
            return []
        out = []
        facts = _facts_for("count-successor", codex)
        for a in range(2, 10):
            for b in range(2, 10):
                if a * b <= 100 and _repeated_add_reachable(facts, a, b):
                    out.append({"concept": concept_id, "surface": f"{a} * {b} is what?", "slots": {"mode": "mult", "a": a, "b": b}})
        return out
    if concept_id == "compare-numbers":
        # E6.2: walk between — derivable iff the line covers both ends.
        if not _rule_established(concept_id, codex):
            return []
        out = []
        facts = _facts_for("count-successor", codex)
        for a in sorted({n for n, _ in facts}):
            for d in (1, 2, 3, 4, 5):
                if a > d and _chain_complete("count-successor", facts, a - d, d):
                    out.append({"concept": concept_id, "surface": f"is {a} larger than {a - d}?", "slots": {"mode": "cmp", "a": a, "b": a - d}})
        return out
    if concept_id == "sqrt-bracket":
        # E6.2: exact squares and FULL brackets only (partial brackets are
        # honest answers, not grounded proposals — they end at the wall).
        if not _rule_established(concept_id, codex):
            return []
        out = []
        facts = _facts_for("count-successor", codex)
        squares: dict[int, int] = {}
        k = 1
        while _repeated_add_reachable(facts, k, k):
            squares[k * k] = k
            k += 1
        for n in sorted(squares):
            out.append({"concept": concept_id, "surface": f"the square root of {n} is what?", "slots": {"mode": "sqrt", "n": n}})
        return out
    facts = _facts_for(concept_id, codex)
    return [
        {"concept": concept_id, "surface": f"what comes after {n}?", "slots": {"mode": "succ", "n": n}}
        for n, _ in facts
    ]


def _last_derivation_session(codex: InMemoryCodexStore, concept_id: str) -> int:
    """The most recent session (from event ids) with a derivation for the
    concept; 0 if none."""

    last = 0
    for a in codex.query(context_match={"kind": "mastery-event", "concept": concept_id}):
        if a.object_id != "derivation-correct":
            continue
        # id shape: <concept>:ev-s<SS>t<TT>:derivation-correct
        try:
            s = int(a.id.split(":ev-s")[1].split("t")[0])
        except (IndexError, ValueError):
            continue
        last = max(last, s)
    return last


def due_concepts(codex: InMemoryCodexStore, concept_ids: list[str], session_no: int) -> list[dict[str, Any]]:
    """The re-exposure queue as a PURE RECOMPUTE: which concepts are due
    at session `session_no`, and why."""

    views = mastery_view(codex, concept_ids)
    due: list[dict[str, Any]] = []
    for cid in concept_ids:
        v = views[cid]
        if v.state in (MasteryState.UNEXPOSED,):
            continue
        if v.state in (MasteryState.EXPOSED, MasteryState.PRACTICING):
            if v.prereq_gaps:
                continue  # not ready: the prereq gate says wait
            due.append({"concept": cid, "reason": f"unstable ({v.state}) — re-drill", "due_at": session_no})
            continue
        # stable: spaced retest
        last = _last_derivation_session(codex, cid)
        if last > 0 and session_no - last >= REEXPOSE_INTERVAL:
            due.append({"concept": cid, "reason": f"stable spacing (last derivation S{last:02d}, interval {REEXPOSE_INTERVAL})", "due_at": session_no})
    # value order: practicing > exposed > (stable retests last); then band; then id
    def key(row: dict[str, Any]) -> tuple:
        cid = row["concept"]
        v = views[cid]
        band = BANDS.index(concept(cid).band) if concept(cid).band in BANDS else len(BANDS)
        return (0 if v.state is MasteryState.PRACTICING else (1 if v.state is MasteryState.EXPOSED else 2), band, cid)

    return sorted(due, key=key)


def next_drill(codex: InMemoryCodexStore, concept_ids: list[str], session_no: int) -> dict[str, Any] | None:
    """The next drill to propose (deterministic choice from the frozen
    value order), or None — honestly — when nothing is due or nothing is
    derivable."""

    due = due_concepts(codex, concept_ids, session_no)
    for row in due:
        cands = strip_candidates(row["concept"], codex)
        if not cands:
            continue
        cands.sort(key=lambda c: (c["surface"]))
        pick = cands[(session_no * 7) % len(cands)]
        return {"concept": row["concept"], "reason": row["reason"], "due_at": row["due_at"], **pick}
    return None
