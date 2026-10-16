"""Spec loading + validation (bandgen).

Two layers:
1. JSON-schema validation (specs/band_spec.schema.json) — the shape.
2. Structural checks — the curriculum's own logic: prereq graphs
   point down and stay acyclic, theorem part sets are subsets of the
   band's taught lessons (scaffolds are STRICT subsets), turn refs
   are unique and padded, wall articulations name the line end, and
   the denied corpus scan (the carried S9_DENYLIST) is clean over
   every question and every declared byte.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from kainos.tutor.brainstem import S9_DENYLIST

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "specs" / "band_spec.schema.json"


def load_spec(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    doc = json.loads(p.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(doc, schema)
    return doc


def structural_checks(spec: dict[str, Any]) -> list[str]:
    """The curriculum-logic checks; returns a list of problem strings
    (empty = clean)."""
    bad: list[str] = []
    band = spec["band"]

    # Concept ids vs the new_concepts list.
    concept_ids = [c["id"] for c in band["concepts"]]
    if concept_ids != band["new_concepts"]:
        bad.append(f"new_concepts {band['new_concepts']} != concepts order {concept_ids}")

    # Prereqs point DOWN: an earlier concept of this band, or a seed
    # concept (the seed-side existence is verified by the dry-run
    # against the booted registry; here we only check acyclicity and
    # in-band ordering — prereqs must appear EARLIER in the list).
    seen: set[str] = set()
    for c in band["concepts"]:
        for p in c["prereqs"]:
            if p in set(concept_ids) and p not in seen:
                bad.append(f"prereq cycle/forward-ref: {c['id']} <- {p}")
        seen.add(c["id"])

    # Lesson slugs and theorem parts.
    lesson_slugs = {c["lesson"]["slug"] for c in band["concepts"]}
    for t in band["theorems"]:
        if t["concept"] not in concept_ids:
            bad.append(f"theorem {t['id']} owns unknown concept {t['concept']!r}")
        for part in t["parts"]:
            if part not in lesson_slugs:
                bad.append(f"theorem {t['id']} part {part!r} is not a taught lesson of the band")

    # new_fact_ids: the exact SET of lesson + theorem facts (the order
    # is the teach/derive order of the script; the structural layer
    # checks the set and the teach/derive presence).
    want_set = {f"lemma:{c['lesson']['slug']}" for c in band["concepts"]}
    want_set |= {f"theorem:{t['id']}" for t in band["theorems"]}
    if set(band["new_fact_ids"]) != want_set:
        bad.append(f"new_fact_ids set {sorted(set(band['new_fact_ids']) - want_set | want_set - set(band['new_fact_ids']))} != band lesson+theorem set")
    if len(band["new_fact_ids"]) != len(want_set):
        bad.append("new_fact_ids has duplicates")
    taught = [t["lesson"] for t in spec["turns"] if t["kind"] == "teach"]
    derived_th = [t["theorem"] for t in spec["turns"] if t["kind"] == "derive"]
    for c in band["concepts"]:
        if c["lesson"]["slug"] not in taught:
            bad.append(f"no teach turn for lesson {c['lesson']['slug']!r}")
    for t in band["theorems"]:
        if t["id"] not in derived_th:
            bad.append(f"no derive turn for theorem {t['id']!r}")

    # Turns: refs unique, padded, consistent with sessions, ordered.
    refs: list[str] = []
    per_session: dict[str, int] = {}
    for i, t in enumerate(spec["turns"]):
        r = t["ref"]
        if r in refs:
            bad.append(f"duplicate turn ref {r}")
        refs.append(r)
        sess = int(r[1:3])
        if sess not in spec["sessions"]:
            bad.append(f"turn {r} session {sess} not in sessions {spec['sessions']}")
        per_session[sess] = per_session.get(sess, 0) + 1
    for sess in spec["sessions"]:
        if len([r for r in refs if int(r[1:3]) == sess]) != per_session.get(sess, 0):
            bad.append(f"session {sess} turn count mismatch")
    expected = []
    for sess in spec["sessions"]:
        n = per_session.get(sess, 0)
        expected += [f"S{sess:02d}:{j:02d}" for j in range(1, n + 1)]
    if refs != expected:
        bad.append("turn refs are not the contiguous padded sequences of their sessions")

    # Kind-specific requirements.
    for t in spec["turns"]:
        k = t["kind"]
        if k == "gap" and not (t.get("concept") and t.get("fragment")):
            bad.append(f"{t['ref']}: gap needs concept + fragment")
        if k == "teach" and not t.get("lesson"):
            bad.append(f"{t['ref']}: teach needs lesson")
        if k == "derive":
            if not (t.get("theorem") and t.get("parts")):
                bad.append(f"{t['ref']}: derive needs theorem + parts")
            else:
                th = next((x for x in band["theorems"] if x["id"] == t["theorem"]), None)
                if th is None:
                    bad.append(f"{t['ref']}: derive unknown theorem {t['theorem']!r}")
                elif sorted(t["parts"]) != sorted(th["parts"]):
                    bad.append(f"{t['ref']}: derive parts {t['parts']} != sanctioned {th['parts']}")
        if k == "scaffold" and not (t.get("theorem") and t.get("parts") and t.get("expected")):
            bad.append(f"{t['ref']}: scaffold needs theorem + parts + expected")
        if k == "scaffold" and t.get("parts"):
            th = next((x for x in band["theorems"] if x["id"] == t.get("theorem")), None)
            if th and sorted(t["parts"]) == sorted(th["parts"]):
                bad.append(f"{t['ref']}: scaffold parts must DIFFER from the sanctioned set (the exact set is the derive path, not the failure path)")
        if k == "missing_parts" and not (t.get("expected") and t.get("theorem")):
            bad.append(f"{t['ref']}: missing_parts needs expected + theorem")
        if k == "wall":
            w = t.get("wall") or {}
            if not w.get("text", "").startswith("needs_info: "):
                bad.append(f"{t['ref']}: wall text must start with 'needs_info: '")
            artic = w.get("articulation", [])
            if not any("line end" in a for a in artic):
                bad.append(f"{t['ref']}: every wall articulation must name the line end")
        if k == "carry" and not (t.get("source") or {}).get("band"):
            bad.append(f"{t['ref']}: carry needs source.band")
        bed = t.get("bed")
        if bed:
            if bed["expect"] == "literal" and "value" not in bed:
                bad.append(f"{t['ref']}: literal bed needs value")
            if bed["expect"] == "frac" and not bed.get("ref"):
                bad.append(f"{t['ref']}: frac bed needs a reference")

    # Beds table: refs resolvable.
    from .reflib import REGISTRY

    for b in spec.get("beds", []):
        if "ref" in b and b["ref"] not in REGISTRY:
            bad.append(f"beds[{b['key']}]: unknown reference {b['ref']!r}")

    # Denylist: the carried S9 corpus scan over the script + every
    # declared byte (questions, wall texts, lesson statements, theorem
    # statements, and the declared expected bytes).
    corpus: list[tuple[str, str]] = []
    for t in spec["turns"]:
        corpus.append((f"script:{t['ref']}", t["question"]))
        w = t.get("wall") or {}
        if w.get("text"):
            corpus.append((f"wall:{t['ref']}", w["text"]))
        if t.get("expected"):
            corpus.append((f"expected:{t['ref']}", t["expected"]))
    for c in band["concepts"]:
        corpus.append(("lesson:" + c["lesson"]["slug"], c["lesson"]["statement"]))
    for t in band["theorems"]:
        corpus.append(("theorem:" + t["id"], t["statement"]))
    deny = set(S9_DENYLIST)
    for where, text in corpus:
        for wd in sorted(deny):
            if wd and wd in text:
                bad.append(f"denylist hit: {wd!r} in {where}: {text[:60]}...")

    return bad
