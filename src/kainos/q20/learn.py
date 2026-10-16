"""Post-game learning: consolidation + contradiction -> dimension (step 15).

Learning here never touches neural weights. Game answers become
assertions with mandatory provenance; verification against the existing
CODEX promotes / disputes / keeps them; a repeated ``sometimes`` or a
genuine conflict becomes a NEW context TERM (invariant #6: contradiction
drives ontology expansion) and the conflicting assertions are re-expressed
under distinct contexts — never averaged.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Provenance,
    Source,
    TermRef,
)
from kainos.q20.oracle import load_questions
from kainos.q20.seed import HAS_PROPERTY, IS_A

__all__ = ["DECLARES_DIMENSION", "DIM_KIND", "consolidate", "detect_dimension"]

DECLARES_DIMENSION = "declares_dimension"
DIM_KIND = "dimension"


def _game_provenance(game_id: str) -> Provenance:
    return Provenance(source=Source(uri=f"game_{game_id}", version="1"), observer="oracle", verified=False)


def _dimension_id(property: str) -> str:
    return f"dim:{property}"


_QUESTION_INDEX: dict[str, dict] | None = None


def _load_question(question_id: str, extra_questions: dict[str, dict] | None = None) -> dict:
    global _QUESTION_INDEX
    if extra_questions is not None and question_id in extra_questions:
        return extra_questions[question_id]
    if _QUESTION_INDEX is None:
        _QUESTION_INDEX = {q["id"]: q for q in load_questions()}
    if question_id not in _QUESTION_INDEX:
        raise KeyError(f"unknown question id: {question_id!r}")
    return _QUESTION_INDEX[question_id]


def consolidate(target: str, trace: list[dict], codex, game_id: str = "g1", corpus: list[dict] | None = None, extra_questions: dict[str, dict] | None = None) -> dict:
    """Turn one game's (question, answer) trace into CODEX assertions.

    Each row becomes an assertion by ``target``:
      property_probe            -> target --has_property--> "<prop>=<answer>"
      category_probe yes/no     -> target --is_a--> category (polarity False for 'no')
    ``unknown`` answers are SKIPPED (absence is the signal — we never write
    'unknown' assertions).

    Verification against existing assertions (excluding the new one itself):
      same value, any existing sibling -> independent corroboration: all
        non-disputed same-value siblings AND the new one are promoted to
        established with provenance.verified=True (game-spec learning loop:
        verify consistent -> consolidate established); first observation
        (no sibling) stays candidate (unverified);
      conflicting value & one side established -> BOTH become disputed,
        evidence-linked, exception=conflicting (kept, never dropped).
    """

    label = target
    if corpus:
        for c in corpus:
            if c["id"] == target:
                label = c["label"]
                break
    subject = TermRef(id=target, labels=[label])
    stats: dict[str, Any] = {"game_id": game_id, "processed": 0, "promoted": 0, "disputed_pairs": 0, "kept_candidate": 0, "skipped_unknown": 0}
    for i, row in enumerate(trace):
        qid = row["question"]
        answer = row["answer"]
        if answer == "unknown":
            stats["skipped_unknown"] += 1
            continue
        stats["processed"] += 1
        q = _load_question(qid, extra_questions)
        a_id = f"as_{game_id}_{i}_{qid}"
        if q["kind"] == "property_probe":
            assertion = Assertion(
                id=a_id,
                subject=subject,
                relation=TermRef(id=HAS_PROPERTY),
                object=f"{q['property']}={answer}",
                status=EpistemicState.candidate,
                provenance=_game_provenance(game_id),
            )
        else:
            assertion = Assertion(
                id=a_id,
                subject=subject,
                relation=TermRef(id=IS_A),
                object=TermRef(id=q["category"], labels=[q["category"]]),
                polarity=answer == "yes",
                status=EpistemicState.candidate,
                provenance=_game_provenance(game_id),
            )
        codex.add(assertion)
        verdict = _verify(assertion, codex)
        if verdict == "promoted":
            stats["promoted"] += 1
        elif verdict == "disputed":
            stats["disputed_pairs"] += 1
        else:
            stats["kept_candidate"] += 1
    return stats


def _verify(new: Assertion, codex) -> str:
    """Compare one fresh assertion against its existing siblings. Returns
    'promoted' | 'disputed' | 'kept'. A sibling 'matches' when it has the
    same property key (has_property) or the same category (is_a); 'same'
    adds value + polarity agreement."""

    def val_of(a: Assertion) -> str:
        v = a.object if isinstance(a.object, str) else a.object.id
        if a.relation.id == IS_A:
            return v + (":yes" if a.polarity else ":no")
        return v

    def key_of(v: str) -> str:
        return v.split(":")[0].split("=")[0]

    new_val = val_of(new)
    existing = codex.query(subject=new.subject.id, relation=new.relation.id)
    siblings = [a for a in existing if a.id != new.id]  # the new assertion is already in the store
    matched = [a for a in siblings if key_of(val_of(a)) == key_of(new_val)]
    if not matched:
        return "kept"  # first independent observation: stays a candidate (unverified)
    same = [a for a in matched if val_of(a) == new_val]
    conflict = [a for a in matched if val_of(a) != new_val]
    if not conflict and same:
        # independent corroboration: >=2 observations (distinct game
        # provenances) agree on the same value — the game-spec learning loop
        # (verify consistent -> consolidate established). Both sides are
        # cross-verified, so both become established with verified provenance
        # (a disputed sibling stays disputed until reconciliation).
        for s in same:
            if s.status == EpistemicState.disputed:
                continue
            codex.add(
                dataclasses.replace(
                    s,
                    status=EpistemicState.established,
                    provenance=dataclasses.replace(s.provenance, verified=True) if s.provenance is not None else None,
                )
            )
        codex.add(
            dataclasses.replace(
                new,
                status=EpistemicState.established,
                provenance=dataclasses.replace(new.provenance, verified=True) if new.provenance is not None else None,
            )
        )
        return "promoted"
    if conflict and any(a.status == EpistemicState.established for a in conflict):
        for a in conflict:
            codex.update_status(a.id, EpistemicState.disputed, evidence=[new.id])
            current = codex.get(a.id)
            codex.add(dataclasses.replace(current, exception=ExceptionState.conflicting))
        codex.add(dataclasses.replace(new, exception=ExceptionState.conflicting))
        codex.update_status(new.id, EpistemicState.disputed, evidence=[a.id for a in conflict])
        return "disputed"
    return "kept"


def detect_dimension(codex, property: str, game_id: str = "dimension", reconcile: bool = True) -> dict | None:
    """Propose the context TERM for ``property`` when it is exceptional.

    With ``reconcile=True`` (default), conflicting pairs re-expressed under
    distinct contexts are RE-ESTABLISHED: once each side carries its own
    context, the contradiction is explained (not hidden) and the dispute
    closes. Non-conflicting (sometimes-only) assertions keep their status.

    Trigger: an established/candidate assertion with value ``sometimes``, or a
    subject carrying >= 2 distinct established values for the property
    (a contradiction). Registers ``dim:<property>`` via a
    ``<property> --declares_dimension--> dim:<property>`` assertion (the
    dimension is KNOWLEDGE the reasoner can see, not a code comment) and
    re-expresses every implicated assertion under a distinct context
    (``dimension`` + ``value``/``conditional`` + exception=requires_context).
    Never averages: both sides stay, fully distinguished.

    Returns ``{"dimension", "declaration", "reexpressed"}`` or None.
    """

    prefix = f"{property}="
    relevant = [
        a
        for a in codex.query(relation=HAS_PROPERTY)
        if isinstance(a.object, str) and a.object.startswith(prefix)
    ]
    by_subject: dict[str, dict[str, Assertion]] = {}
    sometimes: list[Assertion] = []
    for a in relevant:
        value = a.object.split("=", 1)[1]
        by_subject.setdefault(a.subject.id, {})[value] = a
        if value == "sometimes":
            sometimes.append(a)
    conflicts = {s: vals for s, vals in by_subject.items() if len(vals) > 1}
    if not conflicts and not sometimes:
        return None

    dim_id = _dimension_id(property)
    prop_term = TermRef(id=property, labels=[property], kind="property")
    dim_term = TermRef(id=dim_id, labels=[f"{property} (dimension)"], kind=DIM_KIND)
    decl_id = f"as_{DECLARES_DIMENSION}_{property}"
    if not codex.query(relation=DECLARES_DIMENSION, subject=property):
        codex.add(
            Assertion(
                id=decl_id,
                subject=prop_term,
                relation=TermRef(id=DECLARES_DIMENSION),
                object=dim_term,
                status=EpistemicState.candidate,
                provenance=_game_provenance(game_id),
            )
        )
    conflict_ids: set[str] = {vals[v].id for vals in conflicts.values() for v in vals}
    reexpressed: list[str] = []
    implicated: list[Assertion] = []
    seen: set[str] = set()
    for a in sometimes + [vals[v] for vals in conflicts.values() for v in vals]:
        if a.id not in seen:  # Assertion objects are unhashable (TermRef list fields)
            seen.add(a.id)
            implicated.append(a)
    for a in implicated:
        current = codex.get(a.id)
        if not isinstance(current.object, str):
            continue  # implicated are has_property assertions (str objects); guard for the type checker
        value = current.object.split("=", 1)[1]
        data: dict[str, Any] = {"dimension": dim_id, "value": value}
        if value == "sometimes":
            data["conditional"] = True
        replace_kwargs: dict[str, Any] = {
            "context": Context(data={**current.context.data, **data}),
            "exception": ExceptionState.requires_context,
        }
        if reconcile and a.id in conflict_ids and current.status == EpistemicState.disputed:
            # reconciled: distinct contexts explain the conflict -> re-established
            replace_kwargs["status"] = EpistemicState.established
        codex.add(dataclasses.replace(current, **replace_kwargs))
        reexpressed.append(a.id)
    return {"dimension": dim_id, "declaration": decl_id, "reexpressed": reexpressed}
