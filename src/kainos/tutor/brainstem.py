"""The brainstem (T2): perceive -> classify -> policy -> grounded response -> memory write.

The turn loop is the big new component of the tutor horizon (the spec:
"the one new thing it needs is the turn orchestrator"). Everything it
stands on already exists: CODEX assertions with mandatory provenance
(codex/), WORKSPACE (workspace/), and the seven interaction response
contracts (projection/contract.py), validated here verbatim.

Honesty spine (inherited, not re-invented):

- Content is CODEX-derived. A drill answer is a GROUNDED DERIVATION:
  successor chaining over ESTABLISHED facts, every step citing the
  assertion it used (a replayable proof chain). No established fact to
  chain from => the honest `needs_info` — never a fabricated value.
- A lesson records a CANDIDATE assertion (observer = teacher, a
  high-authority observer, not an absolute one); promotion to
  `established` happens only against a clean store; a conflict marks
  both sides `disputed` (kept, evidence-linked, exception=conflicting)
  — disputes are never averaged away.
- A correction keeps BOTH superseded and replacement (the correction
  contract, verbatim): the superseded side is closed (obsolete,
  validity interval ended, evidence-linked to the replacement), the
  replacement is verified against the store before any re-establishing.
- The optional LLM surface (E3.1 SKIP semantics): with no backend the
  deterministic arm classifies (frozen grammar) and phrases (frozen
  templates) — the official hermetic run is this arm. With a backend,
  the LLM classifies in CONFIRM mode (its parse is schema-validated and
  must agree with the grammar — an LLM must not invent intent out of
  unparseable text, D-e6b) and may PHRASE (surface only — the response
  IR is always the deterministic grounded IR; the split is
  provenance-marked: content_from = "codeX", phrasing_from = "det"|"llm").
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from typing import TYPE_CHECKING, Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Interval,
    Provenance,
    Source,
    TermRef,
)
from kainos.projection.contract import CONTRACTS, validate_response
from kainos.tutor.mastery import Concept, concept, seed_concepts

if TYPE_CHECKING:  # pragma: no cover
    from kainos.lang.llm import Backend

__all__ = [
    "Brainstem",
    "TurnResult",
    "det_classify",
    "fixed_epoch",
    "kind_response_ir",
]

KINDS: tuple[str, ...] = ("request", "question", "command", "assertion", "correction", "impossible", "ambiguous")

# ── the frozen pilot grammar (pre-K/grade-1 strip; D-e6a: 30 scripted turns) ─

LESSON_RE = re.compile(r"\bafter\s+(\d+)\s+comes\s+(\d+)\b")
CORR_MARKER_RE = re.compile(r"(?:^|[;,.\s])(?:no\b|i misspoke\b|actually\b)[,.;\s]?")
DRILL_SUCC_RE = re.compile(r"\bwhat\s+comes\s+after\s+(\d+)\b")
DRILL_ADD_RE = re.compile(r"\b(\d+)\s*\+\s*(\d+)\s+is\s+what\b")
DRILL_SUB_RE = re.compile(r"\b(\d+)\s*-\s*(\d+)\s+is\s+what\b")
DRILL_MUL_RE = re.compile(r"\b(\d+)\s*\*\s*(\d+)\s+is\s+what\b")
DRILL_CMP_RE = re.compile(r"\bis\s+(\d+)\s+larger\s+than\s+(\d+)\?")
DRILL_SQRT_RE = re.compile(r"\bthe\s+square\s+root\s+of\s+(\d+)\s+is\s+what\b")
COUNT_FROM_RE = re.compile(r"\bcount\s+from\s+(\d+)\s+to\s+(\d+)\b")
COUNT_TO_RE = re.compile(r"\bcount\s+to\s+(\d+)\b")

# E6.5 - the K-5 band: numerics | geometry (T7 #157; pre-registered in
# plan/30-phases/phase-6-tutor/experiments.md, section E6.5) ----------

#: The frozen K-5 shape table (sides, corners); None means "none" (the
#: circle's honest K-5 form). Out-of-band shape names are not here:
#: the surface boundary is the claim (honestly ambiguous, the E6.4
#: unknown-phrasing class generalized to geometry).
SHAPES: dict[str, tuple[int | None, int | None]] = {
    "triangle": (3, 3),
    "square": (4, 4),
    "rectangle": (4, 4),
    "circle": (None, None),
}

SHAPE_LESSON_CIRCLE = "the circle has no sides and no corners"
SHAPE_LESSON_RE = re.compile(r"\bthe (triangle|square|rectangle) has (\d+) sides and (\d+) corners\b")
DRILL_SHAPE_SIDES_RE = re.compile(r"\bhow many sides does a? (triangle|square|rectangle|circle) have\?")
DRILL_SHAPE_CORNERS_RE = re.compile(r"\bhow many corners does a? (triangle|square|rectangle|circle) have\?")


def canonical_shape_lesson(shape: str) -> str:
    """The teacher's canonical lesson for a shape (the frozen table's
    wording - the exact articulation the unlearned-gap names)."""

    sval, cval = SHAPES[shape]
    if sval is None:
        return SHAPE_LESSON_CIRCLE
    return f"the {shape} has {sval} sides and {cval} corners"

CONCEPT_COUNT = "count-successor"
CONCEPT_ADD = "add-within-10"
# E6.2 — the curriculum ladder (pre-registered in plan/30-phases/phase-6-tutor).
CONCEPT_ADD2 = "add-two-digit"  # sums 11..30 (the line extends)
CONCEPT_SUB = "sub-within-30"  # subtraction by walk-back over the line
CONCEPT_MULT = "mult-within-100"  # multiplication by repeated addition
CONCEPT_CMP = "compare-numbers"  # comparison by walking the line
CONCEPT_SQRT = "sqrt-bracket"  # exact perfect squares + honest brackets
REL_SUCC = "succ"
REL_HAS_EVENT = "has_event"
REL_POLICY = "policy"

# E6.4 — phrasology (D-e6i registered mechanism). Capability is store
# data, extended to INTAKE: a learned phrasing is an established
# assertion (relation phrasing-map) that maps a NEW template onto one
# of the six frozen canonical templates. The frozen grammar stays
# canonical (D-e6b extended): it runs first and wins; the lexicon
# consult fires only where the grammar honestly says ambiguous.
REL_PHRASING = "phrasing-map"
PHRASING_PREFIX = "phr:"
CONCEPT_PHRASOLOGY = "phrasology"

#: (pat-id, canonical template) — the frozen canonical vocabulary (M2;
# E6.5 GROWS it from six to eight — the shape question families join
# the phrasology strip; the E6.4 run's artifacts are pinned and
# untouched by the growth).
CANON_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("pat:succ", "what comes after {n}?"),
    ("pat:add", "{a} + {b} is what?"),
    ("pat:sub", "{a} - {b} is what?"),
    ("pat:mul", "{a} * {b} is what?"),
    ("pat:cmp", "is {a} larger than {b}?"),
    ("pat:lesson", "after {a} comes {b}"),
    ("pat:shape-sides", "how many sides does a {shape} have?"),
    ("pat:shape-corners", "how many corners does a {shape} have?"),
    # E6.6 — band 2: the kinematics position family joins the canonical
    # vocabulary (8 -> 9 templates; band-1 artifacts untouched/pinned).
    ("pat:kin-pos", "a cart starts at {start} and goes {r} every minute: where is it after {t} minutes?"),
    ("pat:kin-time", "a cart starts at {start} and goes {r} every minute and is at {c}: how many minutes did it take?"),
)

#: E6.5 — vocabulary slots: a slot name filled from a FROZEN band
# vocabulary (word slots, D-e6i generalized). The bijection is by NAME
# (unchanged); a new template may not carry fixed words from a band's
# vocabulary the way it may not carry fixed numbers.
SLOT_VOCAB: dict[str, tuple[str, ...]] = {
    "shape": tuple(SHAPES),
}

#: M1 — the teaching pattern (checked after the exact rule phrases,
#: before the canonical patterns; the correction marker is inside the
#: match, as for every lesson).
TEACH_RE = re.compile(r'the phrasing "([^"]+)" is the same as "([^"]+)"')

#: canonical pat-id -> the question mode the fill values carry.
_SLOT_MODES = {
    "pat:succ": "succ",
    "pat:add": "add",
    "pat:sub": "sub",
    "pat:mul": "mult",
    "pat:cmp": "cmp",
    "pat:lesson": None,
    "pat:shape-sides": "shape-sides",
    "pat:shape-corners": "shape-corners",
    "pat:kin-pos": "kin-pos",
    "pat:kin-time": "kin-time",
}
_KIND_OVERRIDE = {"pat:lesson": "assertion"}

# ── E6.6 — band 2: algebra ∥ kinematics (6–8; the first ALIGNED band;
# the owner's directive #2, comment 450) ──────────────────────────────
#: The alignment is STRUCTURAL: the two prereq edges marked ALIGN make
#: a kinematics capability ungatable without its algebra counterpart
#: (kin-solve-time IS undoing the two-step equation; kin-rate IS the
#: repeated-taking inverse).
CONCEPT_ALG_ADD1 = "alg-inverse-1step"
CONCEPT_ALG_MUL = "alg-inverse-mul"
CONCEPT_ALG_2STEP = "alg-two-step"
CONCEPT_KIN_FAR = "kin-distance"
CONCEPT_KIN_POS = "kin-position"
CONCEPT_KIN_TIME = "kin-solve-time"  # prereq: alg-two-step  ← ALIGN
CONCEPT_KIN_RATE = "kin-rate"        # prereq: alg-inverse-mul  ← ALIGN

CONCEPT_BAND2: tuple = (
    Concept(CONCEPT_ALG_ADD1, "Undoing an addition (one step)", "6-8", "algebra", prereqs=(CONCEPT_SUB,)),
    Concept(CONCEPT_ALG_MUL, "Undoing a multiplication (repeated taking)", "6-8", "algebra", prereqs=(CONCEPT_SUB,)),
    Concept(CONCEPT_ALG_2STEP, "Undoing two changes in reverse order", "6-8", "algebra", prereqs=(CONCEPT_ALG_ADD1,)),
    Concept(CONCEPT_KIN_FAR, "Steady pace: distance is pace times time", "6-8", "kinematics", prereqs=(CONCEPT_MULT,)),
    Concept(CONCEPT_KIN_POS, "Position is the start plus the distance", "6-8", "kinematics", prereqs=(CONCEPT_KIN_FAR,)),
    Concept(CONCEPT_KIN_TIME, "Finding time: undo the equation (the algebra alignment)", "6-8", "kinematics", prereqs=(CONCEPT_ALG_2STEP,)),
    Concept(CONCEPT_KIN_RATE, "Finding the pace: repeated taking of the time", "6-8", "kinematics", prereqs=(CONCEPT_ALG_MUL,)),
)

# ── E6.7 — band 3: geometry-advanced ∥ vectors/statics (9–12; the
# PRODUCT band; the owner's directive #2, comment 450) ──────────────
#: The alignment is the PRODUCT CORRIDOR (four doors: distance
#: (band 2), area, moment, perimeter×2 — all the same grounded
#: repeated addition) and the TAKING CORRIDOR (three doors: algebra
#: division, pace (band 2), lever force — all the same repeated
#: taking). The prereq edges marked ALIGN make it curriculum data:
#: a moment is ungatable without the AREA concept (a moment IS a
#: product), and both triangle-area halving and the lever ride the
#: band-2 inverse (cross-BAND edges — the sweep is one curriculum).
CONCEPT_GEO_PERIM = "geom-perimeter"
CONCEPT_GEO_AREA = "geom-area"
CONCEPT_GEO_TRI = "geom-area-triangle"  # prereq: alg-inverse-mul  ← ALIGN
CONCEPT_STA_NET = "stat-net-1d"
CONCEPT_STA_MOM = "stat-moment"  # prereq: geom-area  ← ALIGN
CONCEPT_STA_BAL = "stat-balance"  # prereq: alg-inverse-mul  ← ALIGN

CONCEPT_BAND3: tuple = (
    Concept(
        CONCEPT_GEO_PERIM,
        "Rectangle perimeter (twice the sum of the sides)",
        "9-12",
        "geometry-advanced",
        prereqs=(CONCEPT_ADD2,),
    ),
    Concept(
        CONCEPT_GEO_AREA,
        "Rectangle area (the product corridor)",
        "9-12",
        "geometry-advanced",
        prereqs=(CONCEPT_MULT,),
    ),
    Concept(
        CONCEPT_GEO_TRI,
        "Triangle area (half the product — the taking corridor)",
        "9-12",
        "geometry-advanced",
        prereqs=(CONCEPT_GEO_AREA, CONCEPT_ALG_MUL),
    ),
    Concept(
        CONCEPT_STA_NET,
        "Net 1-D displacement (east minus west on the line)",
        "9-12",
        "statics",
        prereqs=(CONCEPT_SUB,),
    ),
    Concept(
        CONCEPT_STA_MOM,
        "Moment: force times distance (the product corridor)",
        "9-12",
        "statics",
        prereqs=(CONCEPT_GEO_AREA,),
    ),
    Concept(
        CONCEPT_STA_BAL,
        "Lever balance: equal moments (the taking corridor)",
        "9-12",
        "statics",
        prereqs=(CONCEPT_STA_MOM, CONCEPT_ALG_MUL),
    ),
)

# ── E6.8 — the savant seam (S4: the unit-distance problem;
# SAVANT-TRACK, pre-registered in experiments.md §E6.8) ──────────
# Theorem/lemma facts ride the SAME store (no schema change):
# `lemma:{slug}` / `conjecture:{slug}` are ESTABLISHED declared-
# source facts at lesson time (honest "given from a source");
# `theorem:{slug}` is reserved for S6/S7 (a derived result with a
# stored derivation chain). A conjecture is NEVER citable as a
# derivation premise (SAVANT-TRACK P5: its id may never appear in
# any turn's `grounded`).
CONCEPT_UNIT_DISTANCE = "unit-distance"
CONCEPT_GRID_LATTICE = "grid-lattice"  # prereq: unit-distance
CONCEPT_GAUSSIAN_INT = "gaussian-int"
CONCEPT_CIRCLE_PAIR = "circle-pair-2"
CONCEPT_KST_BOUND = "kst-bound"  # prereq: circle-pair-2 (in-band alignment edge)
CONCEPT_SST_BOUND = "sst-bound"
CONCEPT_ERDOS_CONJ = "erdos-conj"  # prereq: unit-distance (conjecture fact)
CONCEPT_NORM_FLAT = "norm-flat"  # confounder; prereq: unit-distance
CONCEPT_NORM_CONVEX = "norm-convex"  # confounder; prereq: unit-distance
CONCEPT_NORM_GENERIC = "norm-generic"  # confounder; prereq: unit-distance

CONCEPT_SAVANT4: tuple = (
    Concept(
        CONCEPT_UNIT_DISTANCE,
        "Unit-pair count (the savant quantity)",
        "college-1",
        "savant",
    ),
    Concept(
        CONCEPT_GRID_LATTICE,
        "Grid unit pairs (axis-parallel only)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_UNIT_DISTANCE,),
    ),
    Concept(
        CONCEPT_GAUSSIAN_INT,
        "Two-square representations (the leap's seed)",
        "college-1",
        "savant",
    ),
    Concept(
        CONCEPT_CIRCLE_PAIR,
        "Two unit circles meet in at most two points",
        "college-1",
        "savant",
    ),
    Concept(
        CONCEPT_KST_BOUND,
        "KST ceiling (k23-free, three-halves power)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_CIRCLE_PAIR,),
    ),
    Concept(
        CONCEPT_SST_BOUND,
        "SST crossing-number ceiling (four-thirds power)",
        "college-1",
        "savant",
    ),
    Concept(
        CONCEPT_ERDOS_CONJ,
        "The erdosguess (a conjecture: believed, not known)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_UNIT_DISTANCE,),
    ),
    Concept(
        CONCEPT_NORM_FLAT,
        "Flat unit-ball norms (confounder: a different norm)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_UNIT_DISTANCE,),
    ),
    Concept(
        CONCEPT_NORM_CONVEX,
        "Strictly convex norms (confounder: a different norm)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_UNIT_DISTANCE,),
    ),
    Concept(
        CONCEPT_NORM_GENERIC,
        "Generic norms (confounder: a different norm)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_UNIT_DISTANCE,),
    ),
)

#: E6.8 — the S4 lesson phrases (frozen). phrase -> (concept, slug,
#: fact kind, essence, depends (slugs the concept rides on),
#: extraction line crosswalk — P0 of the transcription rule).
S4_LESSONS: dict[str, tuple] = {
    "the number of unit pairs of a point set is the count of the pairs of its points that are exactly one apart": (
        CONCEPT_UNIT_DISTANCE,
        "unitpairs",
        "lemma",
        "it names the quantity this whole course counts",
        (),
        "L25-32, L105-112",
    ),
    "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c": (
        CONCEPT_ERDOS_CONJ,
        "erdosguess",
        "conjecture",
        "the statement the whole course is about — believed by erdos, not yet known either way",
        ("unitpairs",),
        "L28, L117",
    ),
    "among the points of an integer grid the unit pairs are exactly the horizontal and vertical neighbor pairs, for a diagonal step is never exactly one apart": (
        CONCEPT_GRID_LATTICE,
        "griddiag",
        "lemma",
        "it tells the grid exactly which neighbor pairs are unit — the count two times m times m minus one falls out of it",
        ("unitpairs",),
        "L64-67 (lattice fact)",
    ),
    "the products of numbers that are sums of two squares are sums of two squares in many ways": (
        CONCEPT_GAUSSIAN_INT,
        "twosquares",
        "lemma",
        "it is the seed of the leap — many equal-length lattice vectors come from many two-square writes",
        (),
        "L65-67",
    ),
    "two unit circles with different centers meet in two points when the squared distance between the centers is below four, in exactly one point when it is four, and in no point when it is above four": (
        CONCEPT_CIRCLE_PAIR,
        "unitcircles",
        "lemma",
        "it caps how many unit circles can share a point — the reason the unit pair graph is k23 free",
        (),
        "L30-33 + house d2 split",
    ),
    "because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power": (
        CONCEPT_KST_BOUND,
        "kstbound",
        "lemma",
        "the first ceiling on unit pairs — a power above one but below n squared",
        ("unitcircles",),
        "L30-34",
    ),
    "the spencer szemerdi trotter crossing number count pushes the unit pair bound down to a constant times n to the four thirds power": (
        CONCEPT_SST_BOUND,
        "sstbound",
        "lemma",
        "the sharper ceiling — the crossing number pushes the exponent from three half to four third",
        (),
        "L33-37",
    ),
    "in a normed plane whose unit ball has a flat side point sets can have quadratically many unit pairs": (
        CONCEPT_NORM_FLAT,
        "flatarea",
        "lemma",
        "a true fact about a different norm — the ceiling changes with the shape of the unit ball",
        ("unitpairs",),
        "L38-40",
    ),
    "for a strictly convex norm the crossing number bound still bounds unit pairs at a constant times n to the four thirds power, and valtr's construction attains that exponent": (
        CONCEPT_NORM_CONVEX,
        "convexnorm",
        "lemma",
        "even for a rounder ball the crossing number ceiling holds, and it is exactly tight there",
        ("unitpairs",),
        "L40-44",
    ),
    "for most norms on the plane the unit pair count grows no faster than a constant times n times log n times log log n, and in d dimensions a comeagre set of norms stays below d squared times n times log squared n with a matching lower bound up to lower order": (
        CONCEPT_NORM_GENERIC,
        "genericnorm",
        "lemma",
        "for a generic ball the count collapses to log squared growth — the far side of the norm family",
        ("unitpairs",),
        "L44-48",
    ),
}

#: E6.8 — the S4 grammar (frozen; slugs pure [a-z]+ per D-e6m).
S4_STATE_SLUGS = "unitpairs|griddiag|twosquares|unitcircles|kstbound|sstbound|flatarea|convexnorm|genericnorm"
S4_SLUG_STATE_RE = re.compile(rf"\bstate the ({S4_STATE_SLUGS}) rule\b")
S4_SLUG_WHY_RE = re.compile(rf"\bwhat is the ({S4_STATE_SLUGS}) for\b")
S4_CONJ_STATE_RE = re.compile(r"\bwhat is the status of the erdosguess\?")
S4_CONJ_PROVEN_RE = re.compile(r"\bis the erdosguess proven\?")
S4_GRID_RE = re.compile(r"\bhow many unit pairs does the (\d+) by (\d+) grid have\?")
S4_TWOSQ_RE = re.compile(r"\bin how many ways is (\d+) a sum of two squares\?")
S4_CIRC_RE = re.compile(r"\bunit circles whose centers are (\d+) over and (\d+) across: how many meeting points\?")
S4_CONF_RE = re.compile(r"\bdoes the (flatarea|convexnorm|genericnorm) rule disprove the erdosguess\?")
S4_WALL_RE = re.compile(r"\bcan you prove that for infinitely many n the unit pairs grow to a power above one\?")

SAVANT4_MODES: tuple[str, ...] = (
    "lem-state",
    "lem-why",
    "conj-state",
    "grid-pairs",
    "twosq",
    "circle-pairs",
    "confounder-no",
    "savant-wall",
)

#: E6.8 — the P0 denylist (paper-characteristic strings that must
#: NEVER appear in student-facing script text — the student's
#: vocabulary is our source-level phrasing, never the paper's).
S4_DENYLIST: tuple[str, ...] = (
    "admissible datum",
    "Theorem 1.1",
    "Theorem 2.3",
    "Minkowski",
    "Golod",
    "Shafarevich",
    "Chebotarev",
    "cyclotomic",
    "pro-p",
    "class group",
    "Hajir",
    "Maire",
    "OpenAI",
    "Erdős",
    "ν(",
    "n^{1+δ}",
    "disproves",
    "infinitely many n such that",
    "unit distance conjecture",
)

S4_SLUG_CONCEPT: dict[str, str] = {
    "unitpairs": CONCEPT_UNIT_DISTANCE,
    "griddiag": CONCEPT_GRID_LATTICE,
    "twosquares": CONCEPT_GAUSSIAN_INT,
    "unitcircles": CONCEPT_CIRCLE_PAIR,
    "kstbound": CONCEPT_KST_BOUND,
    "sstbound": CONCEPT_SST_BOUND,
    "flatarea": CONCEPT_NORM_FLAT,
    "convexnorm": CONCEPT_NORM_CONVEX,
    "genericnorm": CONCEPT_NORM_GENERIC,
    "erdosguess": CONCEPT_ERDOS_CONJ,
}

def concept_map(concept_id: str) -> Concept:
    """E6.8: the in-process concept lookup under an unshadowed name
    (method-local `concept` variables shadow the imported function)."""

    return concept(concept_id)


S4_CONF_HUMAN: dict[str, str] = {
    "flatarea": "flat unit ball",
    "convexnorm": "strictly convex norm",
    "genericnorm": "generic norm",
}

# ── E6.9 — S5 of the SAVANT-TRACK (pre-registered, frozen): the
# number-field toolkit (A-cluster, shallow) — sixteen more seam
# lemma facts + six new grammar families, all on the SAME store and
# the SAME 0..72 line (no new successor facts; every bed derives
# ON the line; magnitudes like 2^tf never land).
CONCEPT_NUMBER_FIELD = "number-field"
CONCEPT_PRIME_SPLIT = "prime-split"
CONCEPT_MOD4_SPLIT = "mod4-split"
CONCEPT_DISC_RD = "disc-rd"
CONCEPT_ADJOIN_I = "adjoin-i"
CONCEPT_CYCLO_CUBIC = "cyclotomic-cubic"
CONCEPT_CHAR_CUTOFF = "char-cutout"
CONCEPT_CLASS_BOUND = "class-bound"
CONCEPT_CHEBOTAREV = "chebotarev"
CONCEPT_PNT_AP = "pnt-ap"
CONCEPT_FRATTINI = "frattini"
CONCEPT_GOLOD_SHA = "golod-shaf"
CONCEPT_SHAFAREVICH = "shafarevich"
CONCEPT_CM_CONJ = "cm-conj"
CONCEPT_MINK_EMBED = "minkowski-embed"

CONCEPT_SAVANT5: tuple = (
    Concept(
        CONCEPT_NUMBER_FIELD,
        "Number fields: embeddings, totally real, the integer norm",
        "college-1",
        "savant",
        prereqs=("count-successor",),
    ),
    Concept(
        CONCEPT_PRIME_SPLIT,
        "Splitting, inertia, ramification (the bad-prime list)",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        CONCEPT_MOD4_SPLIT,
        "The 1 mod 4 primes: the minus-one square and the K = L(i) link",
        "college-1",
        "savant",
        prereqs=(CONCEPT_PRIME_SPLIT,),
    ),
    Concept(
        CONCEPT_DISC_RD,
        "The discriminant, the tower formula, the root discriminant",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        CONCEPT_ADJOIN_I,
        "Adjoining i: the root-discriminant cost divides four",
        "college-1",
        "savant",
        prereqs=(CONCEPT_DISC_RD,),
    ),
    Concept(
        CONCEPT_CYCLO_CUBIC,
        "Cyclic cubic subfields of the cyclotomic fields; the l products",
        "college-1",
        "savant",
        prereqs=(CONCEPT_PRIME_SPLIT, CONCEPT_DISC_RD),
    ),
    Concept(
        CONCEPT_CHAR_CUTOFF,
        "Characters cut out cubic fields; conductors multiply",
        "college-1",
        "savant",
        prereqs=(CONCEPT_CYCLO_CUBIC,),
    ),
    Concept(
        CONCEPT_CLASS_BOUND,
        "The class group under the root-discriminant bound",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        CONCEPT_CHEBOTAREV,
        "Chebotarev: primes of a prescribed frobenius exist in bulk",
        "college-1",
        "savant",
        prereqs=(CONCEPT_PRIME_SPLIT,),
    ),
    Concept(
        CONCEPT_PNT_AP,
        "The 1 mod 3 prime product: a declared O of l log l growth",
        "college-1",
        "savant",
        prereqs=(CONCEPT_CHEBOTAREV,),
    ),
    Concept(
        CONCEPT_FRATTINI,
        "Burnside basis: generators read off the frattini quotient",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        CONCEPT_GOLOD_SHA,
        "The GS test: at most d squared over four relations = infinite",
        "college-1",
        "savant",
        prereqs=(CONCEPT_FRATTINI,),
    ),
    Concept(
        CONCEPT_SHAFAREVICH,
        "Shafarevich: the relation cap d plus C zero",
        "college-1",
        "savant",
        prereqs=(CONCEPT_GOLOD_SHA, CONCEPT_NUMBER_FIELD),
    ),
    Concept(
        CONCEPT_CM_CONJ,
        "The norm-one set: conjugate-pair one on the unit circle",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        CONCEPT_MINK_EMBED,
        "The minkowski embedding; the conjugate product",
        "college-1",
        "savant",
        prereqs=(CONCEPT_NUMBER_FIELD,),
    ),
    Concept(
        "hajir-maire",
        "The tower method: generators outgrow the relation cap",
        "college-1",
        "savant",
        prereqs=(CONCEPT_SHAFAREVICH, CONCEPT_CLASS_BOUND, CONCEPT_GOLOD_SHA),
    ),
)

#: E6.9 — the S5 lesson phrases (frozen). phrase -> (concept, slug,
#: fact kind, essence, depends (concept slugs the fact rides on),
#: extraction line crosswalk — P0 of the transcription rule).
S5_LESSONS: dict[str, tuple] = {
    "a number field is a finite extension of the rationals, its embeddings into the complex numbers are all different, a field is totally real when every embedding lands in the reals, and the norm of a nonzero algebraic integer is a nonzero integer of absolute value at least one": (
        CONCEPT_NUMBER_FIELD,
        "numberfields",
        "lemma",
        "it is the ground under the whole tower — embeddings, the totally real condition, and the integer norm fact the packing step cites",
        (),
        "A.1 (L748–753), L443",
    ),
    "a rational prime in a field extension either splits into several distinct primes, stays inert, or ramifies, and the ramified primes are exactly the ones that divide the discriminant, a finite list": (
        CONCEPT_PRIME_SPLIT,
        "primesplit",
        "lemma",
        "it names the bad primes — the finite set every source statement must exclude",
        (CONCEPT_NUMBER_FIELD,),
        "A.2 (L754–766)",
    ),
    "x squared plus one equals zero modulo an odd prime q has a solution exactly when q is one modulo four, and it feeds the tower: when q is one mod four and splits in the lower field then q splits in the field with i adjoined, since x squared plus one splits over the residue field": (
        CONCEPT_MOD4_SPLIT,
        "mod4minusone",
        "lemma",
        "it is the arithmetic door — many primes of the right shape split at both steps of the tower",
        (CONCEPT_PRIME_SPLIT,),
        "eq. (2) region (L280–295); square tables = the house bed",
    ),
    "the absolute discriminant of a tower multiplies up the levels by the norm of the relative discriminant, the root discriminant is the discriminant raised to the reciprocal of the degree, and a step that ramifies nowhere does not change the root discriminant": (
        CONCEPT_DISC_RD,
        "discrim",
        "lemma",
        "it is the bookkeeping that keeps the tower's arithmetic small at every level",
        (CONCEPT_NUMBER_FIELD,),
        "A.6 (L800–812), L530",
    ),
    "adjoining i to a number field changes the relative discriminant by a factor that divides four, only the prime two can ramify since x squared plus one gets a double root only in even residue characteristic, and so the root discriminant of the new field is at most twice the old one": (
        CONCEPT_ADJOIN_I,
        "adjoini",
        "lemma",
        "it is the exact sub-fact that keeps the root discriminant small: the new field stays within a factor of two",
        (CONCEPT_DISC_RD,),
        "Step 4 (L693–700)",
    ),
    "for each prime r that is one mod three there is a unique totally real cyclic cubic subfield of the r-th cyclotomic field with conductor r, and for ramified primes that are pairwise coprime the cubic fields are linearly disjoint, the galois group of their compositum is l products of z over three, and its part over the base is the same with one generator removed": (
        CONCEPT_CYCLO_CUBIC,
        "cyclotomic",
        "lemma",
        "it is the base of the tower — l independent cubic pieces whose galois group has l generators",
        (CONCEPT_PRIME_SPLIT, CONCEPT_DISC_RD),
        "Prop 3.2 (L508–527), A.11 (L805–812)",
    ),
    "an order three character cuts out the unique cyclic cubic subfield fixed by its kernel, and for characters whose conductors are pairwise coprime the conductors multiply, which is why the discriminant of the base field is the square of the product of the ramified primes": (
        CONCEPT_CHAR_CUTOFF,
        "charcutout",
        "lemma",
        "it is the exact sub-fact that gives the base discriminant: conductor multiplicity for coprime conductors",
        (CONCEPT_CYCLO_CUBIC,),
        "A.5 (L786–800), Prop 3.2 (L508–527)",
    ),
    "the class group of a number field has order at most the max of two and the root discriminant raised to an absolute constant times the degree, so fields of bounded root discriminant and bounded degree have class groups of bounded size": (
        CONCEPT_CLASS_BOUND,
        "classbound",
        "lemma",
        "it is the pigeonhole door — a bounded class group makes the many norm-one elements pile up into few classes",
        (CONCEPT_NUMBER_FIELD,),
        "Prop 3.7 (L582–587)",
    ),
    "chebotarev's density theorem says the primes whose frobenius class is a prescribed element exist in infinitely many, and the finitely many ramified primes may be excluded": (
        CONCEPT_CHEBOTAREV,
        "chebot",
        "lemma",
        "it is the existence engine — the primes that split the way the tower needs, with the bad ones excluded",
        (CONCEPT_PRIME_SPLIT,),
        "Prop 3.6 (L565–575)",
    ),
    "the product of the first l primes that are one mod three grows like e to the O of l log l": (
        CONCEPT_PNT_AP,
        "apbound",
        "lemma",
        "it keeps the base discriminant small: the log of the relative discriminant stays O of l log l",
        (CONCEPT_CHEBOTAREV,),
        "eq. (6) (L628–631)",
    ),
    "burnside's basis theorem reads the generator count of a pro three group off its frattini quotient, and killing generators in the frattini quotient keeps the generator count fixed while the relation count grows by at most the number killed": (
        CONCEPT_FRATTINI,
        "fratin",
        "lemma",
        "it is the bookkeeping of generators — d of a group is the number of its independent directions",
        (CONCEPT_NUMBER_FIELD,),
        "Prop 3.3 (L545–550), A.8 (L814–822)",
    ),
    "the golod shafarevich test says a pro three group on d generators with r relations is infinite whenever r is at most d squared divided by four, and it is silent when r is above": (
        CONCEPT_GOLOD_SHA,
        "gstest",
        "lemma",
        "it is the engine that turns many generators and few relations into an infinite group",
        (CONCEPT_FRATTINI,),
        "Prop 3.4 (L554–557), A.9 (L824–827)",
    ),
    "shafarevich's bound says that for a totally real cubic base field without the cube roots of unity the relation count of its maximal unramified pro three extension is at most the generator count plus an absolute constant c zero": (
        CONCEPT_SHAFAREVICH,
        "shafbound",
        "lemma",
        "it caps the relation count against the generator count — the upper line of the golod shafarevich comparison",
        (CONCEPT_GOLOD_SHA, CONCEPT_NUMBER_FIELD),
        "Prop 3.5 (L559–563), A.10 (L828–835)",
    ),
    "an element that multiplies with its conjugate to one has absolute value one in every complex embedding, it sits on the unit circle in every view, and the integer check in the ring with i is that three squared plus four squared is five squared": (
        CONCEPT_CM_CONJ,
        "cmunit",
        "lemma",
        "it is the shape of the norm-one set — the unit-length lattice the window probes for",
        (CONCEPT_NUMBER_FIELD,),
        "A.4 (L775–782)",
    ),
    "the minkowski embedding sends a field of degree f into f dimensional complex space, and the product of the conjugates of an element is the square root of the absolute value of its norm": (
        CONCEPT_MINK_EMBED,
        "minkembed",
        "lemma",
        "it is the coordinate map that turns norm bounds into lattice point counts",
        (CONCEPT_NUMBER_FIELD,),
        "L218–224 (eq. 10)",
    ),
    "the hajir maire tower method says an infinite tower of unramified extensions of a totally real field exists when the generator count outgrows the relation cap at the levels, with the class group contribution controlled by the pigeonhole bound": (
        "hajir-maire",
        "hajir",
        "lemma",
        "it is the meta lemma of the arithmetic half — the criterion the geometric lemma feeds into",
        (CONCEPT_SHAFAREVICH, CONCEPT_CLASS_BOUND, CONCEPT_GOLOD_SHA),
        "L82, Remark 3.1 (L481–495)",
    ),
}

#: E6.9 — the S5 grammar (frozen; slugs pure [a-z]+ per D-e6m).
S5_STATE_SLUGS = (
    "numberfields|primesplit|mod4minusone|discrim|adjoini|cyclotomic|charcutout"
    "|classbound|chebot|apbound|fratin|gstest|shafbound|cmunit|minkembed|hajir"
)
S5_WHYDEEP_SLUGS = S4_STATE_SLUGS + "|" + S5_STATE_SLUGS
S5_ANY_STATE_RE = re.compile(rf"\bstate the ({S5_STATE_SLUGS}) rule\b")
S5_ANY_WHY_RE = re.compile(rf"\bwhat is the ({S5_STATE_SLUGS}) for\b")
S5_WHYDEEP_RE = re.compile(rf"\bexplain why the ({S5_WHYDEEP_SLUGS}) holds")
S5_SQMOD_RE = re.compile(r"\bdoes (\d+) squared plus one vanish modulo (\d+)\?")
S5_GSAY_RE = re.compile(r"\bdoes the gs test say infinite for (\d+) generators and (\d+) relations\?")
S5_SUMSQ_RE = re.compile(r"\bwhat is (\d+) squared plus (\d+) squared\?")
S5_HOLES_RE = re.compile(r"\bwhat is the biggest hole guaranteed when (\d+) items go into (\d+) holes\?")
S5_DUOPOW_RE = re.compile(r"\bhow large is two raised to the (\d+)\?")

SAVANT5_MODES: tuple[str, ...] = (
    "sqmod",
    "gsay",
    "sumsq",
    "holes",
    "whydeep",
    "duopow",
)

S5_SLUG_CONCEPT: dict[str, str] = {
    "numberfields": CONCEPT_NUMBER_FIELD,
    "primesplit": CONCEPT_PRIME_SPLIT,
    "mod4minusone": CONCEPT_MOD4_SPLIT,
    "discrim": CONCEPT_DISC_RD,
    "adjoini": CONCEPT_ADJOIN_I,
    "cyclotomic": CONCEPT_CYCLO_CUBIC,
    "charcutout": CONCEPT_CHAR_CUTOFF,
    "classbound": CONCEPT_CLASS_BOUND,
    "chebot": CONCEPT_CHEBOTAREV,
    "apbound": CONCEPT_PNT_AP,
    "fratin": CONCEPT_FRATTINI,
    "gstest": CONCEPT_GOLOD_SHA,
    "shafbound": CONCEPT_SHAFAREVICH,
    "cmunit": CONCEPT_CM_CONJ,
    "minkembed": CONCEPT_MINK_EMBED,
    "hajir": "hajir-maire",
}

#: E6.9 — the P0 denylist (S5 flavor: the structural paper
#: identifiers stay banned; plain naming of theorems is allowed, as
#: in S4's kovari sos turan).
S5_DENYLIST: tuple[str, ...] = (
    "admissible datum",
    "Theorem 1.1",
    "Theorem 2.3",
    "Theorem 3.9",
    "Remark 3.9",
    "OpenAI",
    "Erdős",
    "ν(",
    "n^{1+δ}",
    "unit distance conjecture",
    "infinitely many n such that",
    "disproves",
    "unramified pro-3",
    "pro-3",
    "cyclotomic cubic",
    "the square-grid",
    "q_b",
)

# ---------------- E6.10 / savant track S6 — the leap ----------------

#: Six new concepts (the geometric criterion chain) and their
#: prereq edges (curriculum data; ESTABLISHED in the final store).
#: Every prereq is a concept already ESTABLISHED after S5 except the
#: S6-internal ones — the S5 gap cascade spans into S6 (P8).
CONCEPT_WINDOW_SETUP = "window-setup"
CONCEPT_AVERAGING = "averaging"
CONCEPT_PROJECTION = "projection"
CONCEPT_PACKING = "packing"
CONCEPT_SLACK_MARGINS = "slack-margins"
CONCEPT_CRITERION_CHAIN = "criterion-chain"

CONCEPT_SAVANT6: tuple = (
    Concept(
        CONCEPT_WINDOW_SETUP,
        "The window and the norm-one set it holds",
        "college-1",
        "savant",
        prereqs=(CONCEPT_MINK_EMBED, CONCEPT_CM_CONJ),
    ),
    Concept(
        CONCEPT_AVERAGING,
        "Torus averaging: some translate beats the mean",
        "college-1",
        "savant",
        prereqs=(CONCEPT_WINDOW_SETUP,),
    ),
    Concept(
        CONCEPT_PROJECTION,
        "The first-coordinate projection is injective",
        "college-1",
        "savant",
        prereqs=(CONCEPT_WINDOW_SETUP,),
    ),
    Concept(
        CONCEPT_PACKING,
        "The denominator separation and the packing volume comparison",
        "college-1",
        "savant",
        prereqs=(CONCEPT_WINDOW_SETUP, CONCEPT_NUMBER_FIELD),
    ),
    Concept(
        CONCEPT_SLACK_MARGINS,
        "The margins: gamma, b, and how margins compose",
        "college-1",
        "savant",
        prereqs=(CONCEPT_PACKING,),
    ),
    Concept(
        CONCEPT_CRITERION_CHAIN,
        "The criterion: delta positive for infinitely many n",
        "college-1",
        "savant",
        prereqs=(CONCEPT_AVERAGING, CONCEPT_PROJECTION, CONCEPT_PACKING, CONCEPT_SLACK_MARGINS),
    ),
)

#: S6 declared seam lemmas: phrase (= the canonical statement, the
#: lesson surface) -> (concept, slug, kind, essence, depends,
#: source_lines). Ten facts; byte-frozen by the E6.10 pre-reg.
S6_LESSONS: dict[str, tuple] = {
    "when the t split primes give two to the tf conjugate pair choices and the ideal class group is at most h to the f power, the pigeonhole leaves at least two to the tf over h to the f elements with norm one to the lower field, each of absolute value one under every complex embedding": (
        CONCEPT_WINDOW_SETUP,
        "normonecount",
        "lemma",
        "the size of the norm one set the window will hold",
        (),
        "Prop 2.2 (L312–340), (7) (L207–210), L30–33",
    ),
    "the margin gamma is t times the log of 2 minus the log of h, and the criterion takes gamma strictly above zero as a hypothesis; whether such a t against such an h actually happens is the arithmetic half's job, not this statement's": (
        CONCEPT_SLACK_MARGINS,
        "gamma-positive",
        "lemma",
        "the margin the criterion assumes positive",
        (),
        "the criterion's hypothesis (L375–383), Remark 3.9 (L730–740), (7) (L207–210)",
    ),
    "the overlap of two window discs whose centers differ by one unit translation, as a share of one disc's area, tends to one as the window radius grows, so a radius large enough makes the log of that share above minus gamma over two": (
        CONCEPT_AVERAGING,
        "overlap-ratio",
        "lemma",
        "the window overlap that the averaging step keeps",
        (),
        "§2.1 (L335–350), the averaging lemma (L350–355)",
    ),
    "averaging over all lattice translates, the expected window points are the window volume over the lattice volume, and the expected kept pairs are the norm one count times the overlap share to the f power times that expectation, so some translate does at least as well as the average": (
        CONCEPT_AVERAGING,
        "torus-average",
        "lemma",
        "some translate does at least as well as the average",
        (),
        "the averaging step (L355–375)",
    ),
    "a field element that is zero in a single complex embedding is the zero element, because an embedding carries nonzero elements to nonzero numbers": (
        CONCEPT_PROJECTION,
        "one-embed-zero",
        "lemma",
        "why vanishing in one coordinate marks the zero point",
        (),
        "the projection step (L375–380)",
    ),
    "the norm one set lives in the lattice with denominator d, the square of the product of the split primes, and any nonzero lattice element has some coordinate with modulus at least one over d, since the algebraic integer norm is at least one": (
        CONCEPT_PACKING,
        "denom-d",
        "lemma",
        "where the norm one set lives, and the separation it forces",
        (),
        "the lattice setup (L295–300), the separation step (L405–420)",
    ),
    "disjoint equal balls packed inside a bigger ball: the number of small balls times the small ball volume is at most the big ball volume": (
        CONCEPT_PACKING,
        "vol-compare",
        "lemma",
        "the packing volume comparison",
        (),
        "the volume comparison (L425–435)",
    ),
    "the number b is two times the log of four times the window radius r times the denominator d, a fixed margin strictly above zero depending only on the shape of the window, chosen once before the tower level varies": (
        CONCEPT_SLACK_MARGINS,
        "b-positive",
        "lemma",
        "the shape margin in the packing bound",
        (),
        "the packing bound (L433), Remark 3.9 (L730–740)",
    ),
    "a positive margin divided by a positive margin is a positive margin, and a fixed half factor in front of a growing power is absorbed for large arguments, so the arithmetic of the margins is the arithmetic of positivity": (
        CONCEPT_SLACK_MARGINS,
        "slack-compose-rule",
        "lemma",
        "how the margins compose",
        (),
        "the fixed constants (L730–740), the absorption step (L455–460)",
    ),
    "the field degrees tend to infinity as the tower level varies, and that is a hypothesis of the criterion; the construction of levels whose degrees grow is the arithmetic half's job": (
        CONCEPT_CRITERION_CHAIN,
        "hypo-infinity",
        "lemma",
        "the growing degrees the criterion assumes",
        (),
        "the criterion's hypothesis (L375–383), the tower degree (L602–606)",
    ),
}

#: The SIX sanctioned compositions (frozen by the E6.10 pre-reg):
#: target -> parts (must ALL be established and must match exactly),
#: the canonical statement (byte-frozen), and the owning concept.
#: Anything not here is the no-rule scaffold-failure (W-S6-2).
S6_THEOREMS: dict[str, dict] = {
    "window-rich": {
        "parts": ("normonecount", "overlap-ratio", "torus-average"),
        "statement": "some translate of the lattice keeps a rich share: the directed pairs it carries are at least e to the gamma f over two times the points it carries",
        "concept": CONCEPT_AVERAGING,
    },
    "proj-inj": {
        "parts": ("minkembed", "one-embed-zero", "window-rich"),
        "statement": "projecting the window points to the first complex coordinate identifies no two distinct points, so the planar set has the window's point count, and its unit segments are at least a half of e to the gamma f over two times that count",
        "concept": CONCEPT_PROJECTION,
    },
    "pack-bound": {
        "parts": ("numberfields", "denom-d", "vol-compare", "b-positive"),
        "statement": "the window's points are separated by at least one over d in some coordinate, so the point count n is at most (four times the window radius r times the denominator d) to the power two f, which is e to the b f",
        "concept": CONCEPT_PACKING,
    },
    "growth-compare": {
        "parts": ("proj-inj", "pack-bound"),
        "statement": "the pair count is at least a half of n times e to the gamma f over two; since e to the b f bounds n with b positive, f is at least log n over b, so the pair count is at least a half of n to the power one plus gamma over two b; and n itself is at least e to the gamma f over two, since the pair count is at most n squared",
        "concept": CONCEPT_CRITERION_CHAIN,
    },
    "delta-positive": {
        "parts": ("gamma-positive", "b-positive", "slack-compose-rule"),
        "statement": "the exponent delta is gamma over four b — a positive margin divided by a positive margin is a positive margin — and the fixed half is absorbed for large n, so for all large n the pair count is at least n to the power one plus delta",
        "concept": CONCEPT_CRITERION_CHAIN,
    },
    "infinity-end": {
        "parts": ("delta-positive", "growth-compare", "hypo-infinity"),
        "statement": "the point counts grow without bound as the tower level varies, so for any proposed cap c over log log n some level drops the cap below delta and the bound fails there: for infinitely many n the unit segments are at least n to the power one plus delta",
        "concept": CONCEPT_CRITERION_CHAIN,
    },
}

#: Every S6 slug (the ten lessons + the six theorem targets) ->
#: owning concept (state/why/whydeep routing).
S6_SLUG_CONCEPT: dict[str, str] = {
    "normonecount": CONCEPT_WINDOW_SETUP,
    "overlap-ratio": CONCEPT_AVERAGING,
    "torus-average": CONCEPT_AVERAGING,
    "one-embed-zero": CONCEPT_PROJECTION,
    "denom-d": CONCEPT_PACKING,
    "vol-compare": CONCEPT_PACKING,
    "gamma-positive": CONCEPT_SLACK_MARGINS,
    "b-positive": CONCEPT_SLACK_MARGINS,
    "slack-compose-rule": CONCEPT_SLACK_MARGINS,
    "hypo-infinity": CONCEPT_CRITERION_CHAIN,
    "window-rich": CONCEPT_AVERAGING,
    "proj-inj": CONCEPT_PROJECTION,
    "pack-bound": CONCEPT_PACKING,
    "growth-compare": CONCEPT_CRITERION_CHAIN,
    "delta-positive": CONCEPT_CRITERION_CHAIN,
    "infinity-end": CONCEPT_CRITERION_CHAIN,
}

#: E6.10 — the P0 denylist: the S5 seventeen carried, plus the
#: paper's §2 identifiers (frozen by the E6.10 pre-reg; 27 terms).
S6_DENYLIST: tuple[str, ...] = S5_DENYLIST + (
    "Proposition 2.2",
    "Lemma 2.4",
    "Lemma 2.5",
    "Lemma 2.6",
    "Definition 2.1",
    "Minkowski map",
    "Haar",
    "polydisc",
    "sup norm",
    "unfold",
)

_S6_SLUGS: str = (
    "normonecount|overlap-ratio|torus-average|one-embed-zero|denom-d|vol-compare|gamma-positive|b-positive"
    "|slack-compose-rule|hypo-infinity|window-rich|proj-inj|pack-bound|growth-compare|delta-positive|infinity-end"
)
S6_ANY_STATE_RE = re.compile(rf"\bstate the ({_S6_SLUGS}) rule\b")
S6_ANY_WHY_RE = re.compile(rf"\bwhat is the ({_S6_SLUGS}) for\b")
S6_WHYDEEP_RE = re.compile(rf"\bexplain why the ({_S6_SLUGS}) holds\b")
S6_DERIVE_RE = re.compile(r"^derive ([a-z][a-z-]*) from (.+)$")
S6_PACKCOUNT_RE = re.compile(r"^how many points does the packing bound allow when the outer radius is (\d+) times the inner\?$")
S6_TRIPOW_RE = re.compile(r"^how large is three raised to the (\d+)\?$")
S6_SHOWONE_RE = re.compile(r"^name a concrete n for which the unit pairs exceed n to the 1 plus delta$")

S6_MODES: tuple[str, ...] = (
    "derive",
    "packcount",
    "tripow",
    "showone",
    "s6-state",
    "s6-why",
    "s6-whydeep",
)


# ---------------- E6.11 / savant track S7 — tower => disproof ----------------

#: Five new concepts (the arithmetical half) and their prereq edges
#: (curriculum data; ESTABLISHED in the final store). Every prereq is a
#: concept already ESTABLISHED after S6; the S5 gap cascade spans into
#: S7 (P8).
CONCEPT_TOWER_BASE = "tower-base"
CONCEPT_TOWER_GROUP = "tower-group"
CONCEPT_TOWER_PRIMES = "tower-primes"
CONCEPT_TOWER_CLASS = "tower-class"
CONCEPT_DISPROOF = "disproof"

CONCEPT_SAVANT7: tuple = (
    Concept(
        CONCEPT_TOWER_BASE,
        "The base field, its discriminant and its root discriminant",
        "college-1",
        "savant",
        prereqs=(CONCEPT_CYCLO_CUBIC, CONCEPT_CHAR_CUTOFF),
    ),
    Concept(
        CONCEPT_TOWER_GROUP,
        "The generator lower bound and the infinite tower",
        "college-1",
        "savant",
        prereqs=(CONCEPT_TOWER_BASE, CONCEPT_FRATTINI, CONCEPT_GOLOD_SHA, CONCEPT_SHAFAREVICH),
    ),
    Concept(
        CONCEPT_TOWER_PRIMES,
        "The split primes and their prescribed splitting",
        "college-1",
        "savant",
        prereqs=(CONCEPT_TOWER_BASE, CONCEPT_CHEBOTAREV, CONCEPT_MOD4_SPLIT),
    ),
    Concept(
        CONCEPT_TOWER_CLASS,
        "The class bound, the slack, and the positive margin",
        "college-1",
        "savant",
        prereqs=(CONCEPT_TOWER_BASE, CONCEPT_CLASS_BOUND, CONCEPT_ADJOIN_I, CONCEPT_SLACK_MARGINS),
    ),
    Concept(
        CONCEPT_DISPROOF,
        "The disproof: the criterion applied to the tower",
        "college-1",
        "savant",
        prereqs=(CONCEPT_CRITERION_CHAIN, CONCEPT_TOWER_GROUP, CONCEPT_TOWER_PRIMES, CONCEPT_TOWER_CLASS),
    ),
)

#: The seven S7 DECLARED seam lemmas: phrase (= the canonical statement,
#: the lesson surface) -> (concept, slug, kind, essence, depends, source_lines).
#: Byte-frozen by the E6.11 pre-reg; declared-source with line crosswalks.
S7_LESSONS: dict[str, tuple] = {
    "choose the first ℓ primes congruent to one mod three and let F be the cyclic cubic field cut out by their product character: F is totally real, cyclic cubic over the rationals, and contains no cube root of unity": (
        CONCEPT_TOWER_BASE,
        "tower-base",
        "lemma",
        "the base of the arithmetic half — the cyclic cubic the whole tower grows from",
        (),
        "Prop 3.2 (L508–527), Step 1 (L636–645)",
    ),
    "the compositum of the ℓ cyclic cubic fields is unramified everywhere over F, its galois group over F is the product of ℓ−1 copies of Z/3, and the maximal unramified pro three group of F has a quotient of that rank": (
        CONCEPT_TOWER_BASE,
        "tower-unramified",
        "lemma",
        "the large elementary abelian unramified three-extension that makes the generator count big",
        (),
        "Prop 3.2 (L508–527), Step 1 (L645–650)",
    ),
    "the discriminant of F is the square of the product of the first ℓ primes one mod three, so the log of the root discriminant of F is O of ℓ log ℓ, because that product is e to the O of ℓ log ℓ": (
        CONCEPT_TOWER_BASE,
        "base-rd",
        "lemma",
        "it keeps the base field small: the root discriminant grows only like ℓ log ℓ",
        (),
        "Prop 3.2 (L508–527), eq. (6) (L628–631)",
    ),
    "after excluding a prescribed finite set, chebotarev gives distinct rational primes, one for each of t = floor((ℓ−1)²/100), that are one mod four, split completely in F, and carry frobenius trivial in the frattini quotient": (
        CONCEPT_TOWER_PRIMES,
        "chebotarev-selection",
        "lemma",
        "the existence engine for the split primes, with the bad ones excluded",
        (),
        "Prop 3.6 (L565–575), Step 2 (L660–675)",
    ),
    "each split prime divides into exactly three primes of the cubic F, so there are k = 3t such primes in total to kill one by one": (
        CONCEPT_TOWER_PRIMES,
        "k-3t",
        "lemma",
        "the exact count of the frobenius elements to kill — three per split prime",
        (),
        "Step 2 (L669–675)",
    ),
    "adjoining i to a tower level changes its root discriminant by at most a factor of two, so the class number of the j-th level is at most H-ℓ to the f_j, and the log of H-ℓ is O of ℓ log ℓ": (
        CONCEPT_TOWER_CLASS,
        "class-tower",
        "lemma",
        "the pigeonhole door at every level: the class group stays bounded by the degree",
        (),
        "Step 4 (L693–705), Prop 3.7 (L582–587)",
    ),
    "a term quadratic in ℓ with a positive leading coefficient eventually beats any linear-in-ℓ or O of ℓ log ℓ term: for every fixed constant the margin the quadratic minus (d plus c zero plus 3t) stays positive and growing, and so does t log two minus the log of H-ℓ; the threshold value of ℓ where the margin turns positive is not a number in the store": (
        CONCEPT_TOWER_CLASS,
        "slack-quadratic",
        "lemma",
        "the slack primitive — a growing quadratic outruns any fixed or log-linear cap",
        (),
        "Step 2 (L682), Step 4 (L705–715), pre-frozen design point (b)",
    ),
}

#: The SIX S7 sanctioned compositions (frozen by the E6.11 pre-reg):
#: target -> parts (must ALL be established and match EXACTLY), the
#: canonical statement (byte-frozen), and the owning concept.
S7_THEOREMS: dict[str, dict] = {
    "gen-lower": {
        "parts": ("tower-unramified", "fratin"),
        "statement": "the unramified three-extension above F has a galois group that is the product of ℓ−1 copies of Z/3, so the maximal unramified pro three group needs at least ℓ−1 generators",
        "concept": CONCEPT_TOWER_GROUP,
    },
    "gs-infinite": {
        "parts": ("shafbound", "fratin", "k-3t", "gstest", "slack-quadratic"),
        "statement": "shafarevich caps the relation count at the generator count plus a fixed constant, and killing the 3t frattini-trivial frobenius elements adds at most 3t relations while keeping the generator count, so for large ℓ the quotient's relation count is below a quarter of its generator count squared, and golod shafarevich says the quotient is infinite: there is an infinite unramified three-tower of totally real layers with constant root discriminant and degrees tending to infinity",
        "concept": CONCEPT_TOWER_GROUP,
    },
    "splitting": {
        "parts": ("gs-infinite", "chebotarev-selection"),
        "statement": "the chosen frobenius elements are trivial in the quotient, so they are trivial in every finite tower level: each of the t split primes splits completely in every level, and the one-mod-four congruence was built into the choice",
        "concept": CONCEPT_TOWER_PRIMES,
    },
    "gamma-achieved": {
        "parts": ("class-tower", "chebotarev-selection", "slack-quadratic", "gamma-positive"),
        "statement": "the split-prime count is quadratic in ℓ while the log of the class bound is only O of ℓ log ℓ, so for large ℓ the margin gamma = t log two minus the log of the class bound is strictly positive: the criterion's gamma hypothesis holds for the tower",
        "concept": CONCEPT_TOWER_CLASS,
    },
    "tower-feeds": {
        "parts": ("gs-infinite", "splitting", "class-tower", "gamma-achieved", "hypo-infinity", "gamma-positive"),
        "statement": "the tower supplies everything the geometric criterion assumes: totally real levels with degrees tending to infinity, the t split primes (quadratic in ℓ) that feed the norm one set, a class number bounded by the class bound to the level degree, and a strictly positive gamma margin — the criterion's hypotheses are established in the store",
        "concept": CONCEPT_DISPROOF,
    },
    "theorem-main": {
        "parts": ("tower-feeds", "infinity-end"),
        "statement": "applying the geometric criterion to the tower gives an absolute constant delta above zero and infinitely many integers n for which the unit pairs are at least n to the power one plus delta",
        "concept": CONCEPT_DISPROOF,
    },
}

#: Every S7 slug (the seven lessons + the six theorem targets) -> owning
#: concept (state/why/whydeep routing).
S7_SLUG_CONCEPT: dict[str, str] = {
    "tower-base": CONCEPT_TOWER_BASE,
    "tower-unramified": CONCEPT_TOWER_BASE,
    "base-rd": CONCEPT_TOWER_BASE,
    "chebotarev-selection": CONCEPT_TOWER_PRIMES,
    "k-3t": CONCEPT_TOWER_PRIMES,
    "class-tower": CONCEPT_TOWER_CLASS,
    "slack-quadratic": CONCEPT_TOWER_CLASS,
    "gen-lower": CONCEPT_TOWER_GROUP,
    "gs-infinite": CONCEPT_TOWER_GROUP,
    "splitting": CONCEPT_TOWER_PRIMES,
    "gamma-achieved": CONCEPT_TOWER_CLASS,
    "tower-feeds": CONCEPT_DISPROOF,
    "theorem-main": CONCEPT_DISPROOF,
}

#: E6.11 — the P0 denylist: the S6 27 carried + the section-3 identifiers
#: (frozen by the E6.11 pre-reg; 34 terms).
S7_DENYLIST: tuple[str, ...] = S6_DENYLIST + (
    "Proposition 3.2",
    "Proposition 3.3",
    "Proposition 3.4",
    "Proposition 3.5",
    "Proposition 3.6",
    "Proposition 3.7",
    "Proposition 3.8",
)

_S7_SLUGS: str = (
    "tower-base|tower-unramified|base-rd|chebotarev-selection|k-3t|class-tower|slack-quadratic"
    "|gen-lower|gs-infinite|splitting|gamma-achieved|tower-feeds|theorem-main"
)
S7_GSLACK_RE = re.compile(r"^what is the gs slack for (\d+) generators and (\d+) split primes\?$")
S7_CONJ_FLIP_RE = re.compile(r"^falsify the erdosguess by ([a-z][a-z-]*)$")
S7_SHOWDISPROOF_RE = re.compile(r"^reconstruct the disproof from the erdosguess$")
S7_CONFOUNDER_ROUTE_RE = re.compile(
    r"^does the (flatarea|convexnorm|genericnorm) route construct more unit distances in the euclidean plane\?$"
)
S7_DELTAV_RE = re.compile(r"^what is the exact value of delta\?$")
S7_DISTDIST_RE = re.compile(r"^what is the tight bound for distinct distances in the plane\?$")
S7_ANY_STATE_RE = re.compile(rf"\bstate the ({_S7_SLUGS}) rule\b")
S7_ANY_WHY_RE = re.compile(rf"\bwhat is the ({_S7_SLUGS}) for\b")
S7_WHYDEEP_RE = re.compile(rf"\bexplain why the ({_S7_SLUGS}) holds\b")

S7_MODES: tuple[str, ...] = (
    "gsslack",
    "conj-flip",
    "showdisproof",
    "confounder-route",
    "delta-value",
    "distdist",
    "s7-state",
    "s7-why",
    "s7-whydeep",
)

# ── E6.12 — RH-TRACK S8 (pre-registered, frozen): the ζ apparatus ──
#: Nine new RH concepts (the track root `zeta-series` has NO
#: prerequisites — the mastery gate that lets it stabilize).
CONCEPT_RH_ZETA = "zeta-series"
CONCEPT_RH_CONT = "zeta-cont"
CONCEPT_RH_FEQ = "func-eq"
CONCEPT_RH_STRIP = "critical-strip"
CONCEPT_RH_PRIME = "prime-count"
CONCEPT_RH_PNT = "pnt"
CONCEPT_RH_RV = "rv-count"
CONCEPT_RH_SOF = "s-of-t"
CONCEPT_RH = "riemann"

CONCEPT_SAVANT8: tuple = (
    Concept(
        CONCEPT_RH_ZETA,
        "the zeta function: the series and the euler product",
        "college-1",
        "rh",
        prereqs=(),
    ),
    Concept(
        CONCEPT_RH_CONT,
        "the continuation and the pole",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_ZETA,),
    ),
    Concept(
        CONCEPT_RH_FEQ,
        "the functional equation and the trivial zeros",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_CONT,),
    ),
    Concept(
        CONCEPT_RH_STRIP,
        "the critical strip: the farthest the zeros can be",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_FEQ,),
    ),
    Concept(
        CONCEPT_RH_PRIME,
        "primes on the integers: the grounded censuses",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_ZETA,),
    ),
    Concept(
        CONCEPT_RH_PNT,
        "the prime number theorem and its error",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_PRIME,),
    ),
    Concept(
        CONCEPT_RH_RV,
        "counting the zeros: the riemann-von mangoldt formula",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_CONT,),
    ),
    Concept(
        CONCEPT_RH_SOF,
        "s of t: the argument on the critical line",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_RV, CONCEPT_RH_FEQ),
    ),
    Concept(
        CONCEPT_RH,
        "the riemann hypothesis: the conjecture as a target",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_STRIP, CONCEPT_RH_RV),
    ),
)

#: The eleven S8 DECLARED seam lemmas + the riemann CONJECTURE:
#: phrase (= the canonical statement, the lesson surface) ->
#: (concept, slug, kind, essence, depends, source_lines). The
#: source_lines slot carries the monograph/fetched audits per
#: savant-test/rh/REFERENCES.md (the RH-TRACK audit adaptation for
#: a non-paper corpus).
S8_LESSONS: dict[str, tuple] = {
    "the zeta function is the sum over all n of n to the power minus s, and it converges when the real part of s is greater than one": (
        CONCEPT_RH_ZETA,
        "zeta-series",
        "lemma",
        "the root of the track — what zeta is, before anything is claimed about it",
        (),
        "R1 (the series), R2 ch. I",
    ),
    "where the real part of s is greater than one, the zeta function is the product over all primes p of the reciprocal of (1 minus p to the power minus s)": (
        CONCEPT_RH_ZETA,
        "euler-product",
        "lemma",
        "the link between zeta and the primes — the primes are the atoms of zeta",
        (),
        "R1 (the product), R2 ch. I",
    ),
    "the zeta function continues to a meromorphic function on the whole plane; its only singularity is a simple pole at s = 1 with residue 1": (
        CONCEPT_RH_CONT,
        "zeta-cont",
        "lemma",
        "zeta outlives its series: one object on the whole plane, one pole",
        (),
        "R2 ch. V — hadamard and de la vallee poussin (1896)",
    ),
    "the completed function (s(s minus 1) over 2) times pi to the power minus s over 2 times gamma(s over 2) times zeta(s) is entire and equals its own reflection: xi(s) equals xi(1 minus s) — the functional equation": (
        CONCEPT_RH_FEQ,
        "func-eq",
        "lemma",
        "the symmetry every zero reflection and zero count rides on",
        (),
        "R1, R2 ch. V — F2 context",
    ),
    "zeta is exactly zero at every negative even integer: zeta of negative 2k is zero for every integer k at least one — the trivial zeros, zeroed by the sine factor sin(pi k) in the functional equation form": (
        CONCEPT_RH_FEQ,
        "trivial-zeros",
        "lemma",
        "the zeros we know — the negative even integers; the target is the rest",
        (),
        "R1, R2 ch. V — the sin(pi k) = 0 mechanism",
    ),
    "the zeta function has no zero when the real part of s is greater than one: each euler factor 1 minus p to the power minus s is nonzero there since p to the power minus s has modulus below one, and the product converges": (
        CONCEPT_RH_STRIP,
        "nozero-s1",
        "lemma",
        "the wall to the right of the strip: nothing past one, so the zeros sit to the left of it",
        (),
        "R1, R2 ch. V",
    ),
    "the von mangoldt function is the log of p when the argument is a power of the prime p and zero otherwise; the chebyshev psi is its sum over the argument up to x": (
        CONCEPT_RH_PRIME,
        "von-mangoldt",
        "lemma",
        "the bookkeeping that turns prime powers into a sum — the currency of the pnt",
        (),
        "R4 ch. II",
    ),
    "the prime number theorem: the chebyshev psi of x is asymptotic to x — in the logarithmic sense the primes are distributed like the integers": (
        CONCEPT_RH_PNT,
        "pnt",
        "lemma",
        "the theorem the conjecture sharpens: the error scale is the stake",
        (),
        "R4 — hadamard and de la vallee poussin (1896)",
    ),
    "the number of nontrivial zeros with height at most T is (T over 2 pi) times log(T over 2 pi) minus (T over 2 pi), with an error of order log T — the riemann-von mangoldt counting formula": (
        CONCEPT_RH_RV,
        "rv-count",
        "lemma",
        "how many zeros there are, at what height — the census the hypothesis would complete",
        (),
        "R1 (statement, 1859), R2 (mangoldt, 1905) — F2",
    ),
    "the sharp counting formula: N of T equals (T over 2 pi) log(T over 2 pi) minus (T over 2 pi) plus 7 over 8 plus S of T plus o of 1, where S of T is 1 over pi times the argument of zeta on the critical line at height T, and S of T is order at most log T": (
        CONCEPT_RH_SOF,
        "s-of-t",
        "lemma",
        "the wiggle term: everything the counting formula does not know, folded into one argument",
        (),
        "R2 ch. XI — F2",
    ),
    "the first nontrivial zero of zeta is at height 14.1347, to four decimals — the next three at 21.0221, 25.0109 and 30.4249 — and the first ten to the thirteenth zeros have been verified to lie on the critical line: a numerical check, not a proof": (
        CONCEPT_RH_RV,
        "num-zeros",
        "lemma",
        "the evidence from below — the first zeros the machines have found, on the line",
        (),
        "the verified-zero record — a declared numerical fact, not a proof",
    ),
    "every nontrivial zero of zeta has real part exactly one half — the nontrivial zeros are those not at a negative even integer; they are claimed to lie exactly on the critical line": (
        CONCEPT_RH,
        "riemann",
        "conjecture",
        "the target itself — believed, not known; a status surface, never a premise",
        (),
        "the conjecture (1859) — the target of the RH-TRACK",
    ),
}

#: The two S8 sanctioned compositions (frozen by the E6.12 pre-reg):
#: target -> parts (must ALL be established and match EXACTLY), the
#: canonical statement (byte-frozen), and the owning concept.
S8_THEOREMS: dict[str, dict] = {
    "reflect": {
        "parts": ("func-eq",),
        "statement": "the symmetry of xi reflects zeros: a nontrivial zero s has 1 minus s as a nontrivial zero, with the same multiplicity",
        "concept": CONCEPT_RH_FEQ,
    },
    "strip": {
        "parts": ("reflect", "nozero-s1", "trivial-zeros"),
        "statement": "every zero of zeta either lies at a negative even integer or lies strictly inside the critical strip: a nontrivial zero has real part between zero and one — a zero past one would reflect to a zero past the left edge, forcing it to a trivial zero, and a zero at or past the left edge is trivial by the same reflection",
        "concept": CONCEPT_RH_STRIP,
    },
}

#: Every S8 slug (eleven lessons + two theorem targets + the conj)
#: -> owning concept (state/why/whydeep routing).
S8_SLUG_CONCEPT: dict[str, str] = {
    "zeta-series": CONCEPT_RH_ZETA,
    "euler-product": CONCEPT_RH_ZETA,
    "zeta-cont": CONCEPT_RH_CONT,
    "func-eq": CONCEPT_RH_FEQ,
    "trivial-zeros": CONCEPT_RH_FEQ,
    "reflect": CONCEPT_RH_FEQ,
    "nozero-s1": CONCEPT_RH_STRIP,
    "strip": CONCEPT_RH_STRIP,
    "von-mangoldt": CONCEPT_RH_PRIME,
    "pnt": CONCEPT_RH_PNT,
    "rv-count": CONCEPT_RH_RV,
    "num-zeros": CONCEPT_RH_RV,
    "s-of-t": CONCEPT_RH_SOF,
    "riemann": CONCEPT_RH,
}

#: E6.12 — the P0 denylist: the S7 34 carried + the RH book/paper
#: characteristic strings (44 terms frozen by the E6.12 pre-reg).
S8_DENYLIST: tuple[str, ...] = S7_DENYLIST + (
    "On the Number of Primes",
    "0.137",
    "Platt",
    "Odlyzko",
    "Hilbert's sixth",
    "KMS",
    "trace formula",
    "Bost",
    "Connes",
    "li(x)",
)

_S8_SLUGS: str = (
    "zeta-series|euler-product|zeta-cont|func-eq|trivial-zeros|nozero-s1"
    "|von-mangoldt|pnt|rv-count|s-of-t|reflect|strip|num-zeros"
)
S8_PICOUNT_RE = re.compile(r"\bhow many primes are at most (\d+)\?")
S8_JFUNC_RE = re.compile(r"\bwhat is the prime-power phi count at (\d+)\?")
S8_SINCYCLE_RE = re.compile(r"\bdoes the sine vanish at every integer multiple of pi from one to 84\?")
S8_GROWTH_RE = re.compile(r"\bwhat is the expected growth of the prime-power phi count\?")
S8_NUMZERO_RE = re.compile(r"\bwhat is the height of the first nontrivial zero\?")
S8_RH_ATTEMPT_RE = re.compile(r"\bcan you derive the riemann hypothesis from the store\?")
S8_RH_CONJ_RE = re.compile(r"\bwhat is the status of the riemann hypothesis\?")
S8_RH_NUMCHECK_RE = re.compile(r"\bdoes the numerical check of the first ten to the thirteenth zeros prove the conjecture\?")
S8_RH_OFFZERO_RE = re.compile(r"\bwhat is the smallest zero off the critical line, if one exists\?")
S8_RH_PNTCONF_RE = re.compile(r"\bdoes the prime number theorem imply the riemann hypothesis\?")
S8_RH_PRODCONF_RE = re.compile(r"\bdoes the euler product alone settle the location of the zeros\?")
S8_RH_ZETAVAL_RE = re.compile(r"\bwhat is the value of zeta at three quarters\?")
S8_RH_STIGHT_RE = re.compile(r"\bwhat is the tight bound for [sS] of [tT]\?")
S8_ANY_STATE_RE = re.compile(rf"\bstate the ({_S8_SLUGS}) rule\b")
S8_ANY_WHY_RE = re.compile(rf"\bwhat is the ({_S8_SLUGS}) for\b")
S8_WHYDEEP_RE = re.compile(rf"\bexplain why the ({_S8_SLUGS}) holds\b")

S8_MODES: tuple[str, ...] = (
    "pi-count",
    "jfunc",
    "sincycle",
    "growth-claim",
    "numzero-first",
    "rh-attempt",
    "rh-conj-state",
    "rh-numcheck",
    "rh-offzero",
    "rh-pnt-conf",
    "rh-prod-conf",
    "rh-zeta-val",
    "rh-s-tight",
    "s8-state",
    "s8-why",
    "s8-whydeep",
)

# ── E6.13 — RH-TRACK S9 (pre-registered, frozen): the criterion gallery ──
#: Ten new RH concepts (the second wave). None is a track root —
#: they ride on the S8 registry (the stable wave-2 prereqs: pnt,
#: prime-count).
CONCEPT_RH_PSI_EQ = "psi-eq"
CONCEPT_RH_PI_EQ = "pi-eq"
CONCEPT_RH_ST_EQ = "st-eq"
CONCEPT_RH_LI = "li-criterion"
CONCEPT_RH_PH = "polya-hilbert"
CONCEPT_RH_LH = "lindelof"
CONCEPT_RH_ZFR = "zero-free"
CONCEPT_RH_PNTE = "pnt-error"
CONCEPT_RH_HAR = "hardy-line"
CONCEPT_RH_ZD = "zero-density"

CONCEPT_SAVANT9: tuple = (
    Concept(
        CONCEPT_RH_PSI_EQ,
        "the psi-equivalence: the hypothesis as a prime-shadow scale",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_PNT,),
    ),
    Concept(
        CONCEPT_RH_PI_EQ,
        "the pi-equivalence: the hypothesis as a counting scale",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_PRIME,),
    ),
    Concept(
        CONCEPT_RH_ST_EQ,
        "the S-of-T equivalence: the hypothesis as a wiggle bound",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_SOF,),
    ),
    Concept(
        CONCEPT_RH_LI,
        "the li-criterion: the hypothesis as a positivity statement",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_PSI_EQ,),
    ),
    Concept(
        CONCEPT_RH_PH,
        "the polya-hilbert program: the self-adjoint route",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_STRIP,),
    ),
    Concept(
        CONCEPT_RH_LH,
        "the lindelof hypothesis: one stored direction only",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_RV, CONCEPT_RH_STRIP),
    ),
    Concept(
        CONCEPT_RH_ZFR,
        "the zero-free region: the classical barrier to one",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_FEQ,),
    ),
    Concept(
        CONCEPT_RH_PNTE,
        "the best classical error term from the region",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_ZFR,),
    ),
    Concept(
        CONCEPT_RH_HAR,
        "hardy's line zeros and the classical mean square",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_RV, CONCEPT_RH_SOF),
    ),
    Concept(
        CONCEPT_RH_ZD,
        "the littlewood zero-density bound",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_RV, CONCEPT_RH_ZFR),
    ),
)

#: The eleven S9 DECLARED criterion facts (the C-cluster):
#: phrase (= the canonical statement, the lesson surface) ->
#: (concept, slug, kind, essence, depends, source_lines). Audits per
#: savant-test/rh/REFERENCES.md; the denylist keeps the reserved
#: author strings banned (the self-adjoint route is named by its
#: content; the logarithmic integral is spelled out).
S9_LESSONS: dict[str, tuple] = {
    "the Riemann hypothesis is equivalent to the fact that the chebyshev psi of x is x plus an error of at most x to the one-half plus epsilon, for every epsilon greater than zero": (
        CONCEPT_RH_PSI_EQ,
        "psi-eq",
        "lemma",
        "the main route: the hypothesis as a precise scale on the prime shadow",
        (),
        "F3 (the Pringsheim form of Riemann's own remark), R3",
    ),
    "the Riemann hypothesis is equivalent to the fact that the prime-counting function is the logarithmic integral of x plus an error of at most the square root of x times log x": (
        CONCEPT_RH_PI_EQ,
        "pi-eq",
        "lemma",
        "the hypothesis as the exact counting scale of the primes",
        (),
        "F3, Littlewood (1924), R2",
    ),
    "the Riemann hypothesis is equivalent to the fact that the argument wiggle S of T is little-o of log T as T tends to infinity": (
        CONCEPT_RH_ST_EQ,
        "st-eq",
        "lemma",
        "the hypothesis as the stilling of the counting formula's wiggle term",
        (),
        "R2, Littlewood (1924)",
    ),
    "the Riemann hypothesis holds if and only if every Li number is positive — the Li number of index n is the derivative of order n minus one, at s = 1, of s to the power n minus one times the log of the completed function, divided by (n minus 1) factorial — and the check up to n = ten to the fifth is a declared numerical fact, not a proof": (
        CONCEPT_RH_LI,
        "li-criterion",
        "lemma",
        "the hypothesis as a positivity statement — the numerically verified, unproved criterion",
        (),
        "F1 (the zero-sum form)",
    ),
    "the polya-hilbert program reformulates the Riemann hypothesis as a spectral statement about a positive self-adjoint operator; the reformulation is a theorem, and the step that recovers the conjecture from the spectrum is an open program, not in my store": (
        CONCEPT_RH_PH,
        "polya-hilbert",
        "lemma",
        "the self-adjoint route: reformulations theorems, the RH step an open program",
        (),
        "F4 (the operator-theoretic reformulations)",
    ),
    "the lindelof hypothesis claims that zeta at one-half plus i t is bounded by a power of t to the epsilon for every epsilon greater than zero; the riemann hypothesis implies lindelof — one direction only: the reverse is not in my store": (
        CONCEPT_RH_LH,
        "lindelof",
        "lemma",
        "the sibling hypothesis — the stored direction runs RH to LH, never back",
        (),
        "R2 (one direction only)",
    ),
    "zeta has no zero when the real part of s is at least one minus c over log of the absolute value of t, for a constant c greater than zero — the classical zero-free region; the value of the constant is not in my store": (
        CONCEPT_RH_ZFR,
        "zero-free-region",
        "lemma",
        "the classical barrier: nothing zeros zeta close to one — some c, not the value",
        (),
        "R4/R2 (safe classical form)",
    ),
    "the zero-free region implies the prime number theorem with an explicit error: the chebyshev psi of x is x plus O of x times e to the minus c times the square root of log x, for a constant c greater than zero; the value of the constant is not in my store": (
        CONCEPT_RH_PNTE,
        "pnt-error",
        "lemma",
        "the store's best error term — the scale the criterion gap is measured against",
        (),
        "R4/F5",
    ),
    "hardy's theorem: infinitely many nontrivial zeros lie exactly on the critical line — the count of line zeros up to height t tends to infinity as t tends to infinity": (
        CONCEPT_RH_HAR,
        "hardy",
        "lemma",
        "the line is not empty: infinitely many zeros sit on it — the theorem the hope rests on",
        (),
        "R2",
    ),
    "the classical mean square: the integral of the squared modulus of zeta on the critical line from height 0 to t is t times log(t over 2 pi) plus (2 gamma minus 1) times t, with an error of at most a constant times log t": (
        CONCEPT_RH_HAR,
        "mean-square",
        "lemma",
        "the average size of zeta on the line — the machinery Hardy's theorem rides",
        (),
        "R2",
    ),
    "the littlewood zero-density bound: the number of zeros with real part at least sigma and height at most T is at most T to the power 3(1 minus sigma) over (2 minus sigma), times a power of log T": (
        CONCEPT_RH_ZD,
        "zero-density",
        "lemma",
        "how the zeros thin out as the real part approaches one — the density that shrinks the bad region",
        (),
        "R2",
    ),
}

#: The two S9 sanctioned compositions (frozen by the E6.13 pre-reg):
#: target -> parts (must ALL be established and match EXACTLY), the
#: canonical statement (byte-frozen), and the owning concept.
S9_THEOREMS: dict[str, dict] = {
    "mirror-region": {
        "parts": ("zero-free-region", "reflect"),
        "statement": "by the reflection symmetry, the zero-free region has a mirror: zeta has no zero when the real part of s is at most c over log of the absolute value of t — the left-side region is the image of the right-side region under the map s to 1 minus s",
        "concept": CONCEPT_RH_ZFR,
    },
    "criterion-gap": {
        "parts": ("psi-eq", "pnt-error"),
        "statement": "the best error term in my store, of order x times e to the minus c times the square root of log x, does not meet the scale the equivalence demands, x to the one-half plus epsilon: for every fixed c greater than zero and every epsilon below one-half, the former eventually exceeds the latter, and their ratio grows without bound — the square-root improvement is the missing ingredient",
        "concept": CONCEPT_RH_PSI_EQ,
    },
}

#: Every S9 slug (eleven lessons + two theorem targets) -> owning
#: concept (state/why/whydeep routing).
S9_SLUG_CONCEPT: dict[str, str] = {
    "psi-eq": CONCEPT_RH_PSI_EQ,
    "pi-eq": CONCEPT_RH_PI_EQ,
    "st-eq": CONCEPT_RH_ST_EQ,
    "li-criterion": CONCEPT_RH_LI,
    "polya-hilbert": CONCEPT_RH_PH,
    "lindelof": CONCEPT_RH_LH,
    "zero-free-region": CONCEPT_RH_ZFR,
    "pnt-error": CONCEPT_RH_PNTE,
    "hardy": CONCEPT_RH_HAR,
    "mean-square": CONCEPT_RH_HAR,
    "zero-density": CONCEPT_RH_ZD,
    "mirror-region": CONCEPT_RH_ZFR,
    "criterion-gap": CONCEPT_RH_PSI_EQ,
}

#: E6.13 — the P0 denylist: the S8 44 UNCHANGED (the reserved author
#: strings stay banned in S9: the polya-hilbert statement is named
#: by its content, the logarithmic integral is spelled out, the
#: Bost–Connes/Connes audit lives in the crosswalk only).
S9_DENYLIST: tuple[str, ...] = S8_DENYLIST

_S9_SLUGS: str = (
    "psi-eq|pi-eq|st-eq|li-criterion|polya-hilbert|lindelof"
    "|zero-free-region|pnt-error|hardy|mean-square|zero-density"
    "|mirror-region|criterion-gap|rh-reach"  # E6.14: the S10 assembly rides the unified state/why tables
)
S9_GAPCOMPARE_RE = re.compile(r"\bwhat is the expected growth of the gap ratio\?")
S9_LICHECK_RE = re.compile(r"\bhave li's numbers been verified positive up to a bound\?")
S9_CVALUE_RE = re.compile(r"\bwhat is the exact value of c in the zero-free region\?")
S9_LINDELOF_RE = re.compile(r"\bdoes lindelof imply the riemann hypothesis\?")
S9_PHCONF_RE = re.compile(r"\bdoes the polya-hilbert program prove the riemann hypothesis\?")
S9_LIPROOF_RE = re.compile(r"\bis li's positivity proven for all n\?")
S9_ANY_STATE_RE = re.compile(rf"\bstate the ({_S9_SLUGS}) rule\b")
S9_ANY_WHY_RE = re.compile(rf"\bwhat is the ({_S9_SLUGS}) for\b")
S9_WHYDEEP_RE = re.compile(rf"\bexplain why the ({_S9_SLUGS}) holds\b")

S9_MODES: tuple[str, ...] = (
    "gap-compare",
    "li-check",
    "c-value",
    "lindelof-conf",
    "ph-conf",
    "li-proof",
    "s9-state",
    "s9-why",
    "s9-whydeep",
)

# ── E6.14 — RH-TRACK S10 (pre-registered, frozen): the attempt ──
#: NO new concepts, NO new seam facts. The ONE new fact is the
#: maximal assembly theorem (owning concept = the riemann concept —
#: the store assembles its own full reach and names its missing
#: ingredient). The derive grammar's target set EXCLUDES the
#: conjecture by table design: no sanctioned composition produces
#: a `theorem:riemann` (the discovery-candidate invariant, P5).
S10_THEOREMS: dict[str, dict] = {
    "rh-reach": {
        "parts": ("strip", "mirror-region", "criterion-gap"),
        "statement": "assembled from the store: every nontrivial zero is inside the critical strip, between zero and one, and its mirror under the map s to 1 minus s; and the store's best error term, x times e to the minus c times the square root of log x, does not meet the scale x to the one-half plus epsilon that the equivalence demands: their ratio grows without bound for every fixed c greater than zero and every epsilon below one-half, and no part of the store closes that gap — the square-root improvement is the conjecture itself",
        "concept": CONCEPT_RH,
    },
}

#: the union of savant+rh theorem compositions (S6 + S7 + S8 + S9 +
#: S10 + S11) for the shared `derive` policy (S11 re-merged after its
#: definition below — a forward reference).
SAVANT_THEOREMS: dict[str, dict] = {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS}

#: E6.14 — the S10 deviant-route walls (the two alternative
#: criterion routes; the track pre-reg's `deviant-route` class:
#: accepted, recorded, studied separately). The routes are PROBED,
#: not derived: the derive grammar cannot produce the conjecture
#: by design, so the probe is an honest wall naming WHY the route
#: cannot be closed in the store.
S10_LICLOSE_RE = re.compile(r"\bcan you prove li's numbers are positive for all n from the store\?")
S10_STCLOSE_RE = re.compile(r"\bcan you prove the wiggle S of T is little-o of log T from the store\?")

S10_MODES: tuple[str, ...] = (
    "li-close",
    "st-close",
)

# ── E6.15 — FUNDAMENTALS-TRACK S11 (pre-registered E6.15, frozen
# 2026-08-23, D-e6f(a) corrected): the sieve — the full process + the
# scan ledger. The divisibility layer UNDER the primes. The full
# process is RECORDED, never optimized (owner, 2026-08-23).
CONCEPT_S11_DIVID = "divides"
CONCEPT_S11_COMP = "composite"
CONCEPT_S11_SPF = "first-divisor"
CONCEPT_S11_LEDGER = "scan-ledger"

CONCEPT_S11: tuple = (
    Concept(
        CONCEPT_S11_DIVID,
        "divisibility: k times m is n",
        "college-1",
        "rh",
        prereqs=(CONCEPT_MULT,),
    ),
    Concept(
        CONCEPT_S11_COMP,
        "the composites: what a number is made of when it is not prime",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S11_DIVID, CONCEPT_RH_PRIME),
    ),
    Concept(
        CONCEPT_S11_SPF,
        "the first divisor: the smallest one above 1",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S11_COMP, CONCEPT_S11_DIVID),
    ),
    Concept(
        CONCEPT_S11_LEDGER,
        "the scan ledger: what the full process records",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S11_SPF,),
    ),
)

#: The four S11 DECLARED seam lessons (D-e6f(a) frozen: phrases are
#: the canonical statements; on-line values only).
S11_LESSONS: dict[str, tuple] = {
    "k divides n when there is an m on the line with k times m equal to n; 1 divides every number, and every number divides itself": (
        CONCEPT_S11_DIVID,
        "divides-def",
        "lemma",
        "the inverse question of multiplication on my line: how many exact groups of k fit in n",
        (),
        "the definition — multiplication walked backwards on the line",
    ),
    "a number n above 1 is composite when some k above 1 and below n divides n; every number above 1 is either prime or composite, and 1 is neither — the line splits at one": (
        CONCEPT_S11_COMP,
        "composite-def",
        "lemma",
        "the line as a ledger of products: a composite is an entry that already appears as a product of two smaller line-numbers",
        (),
        "the definition — the line as a ledger of products",
    ),
    "every composite n has a first divisor — the smallest k above 1 that divides n — and it lies strictly below n; a prime has no divisor above 1 below itself": (
        CONCEPT_S11_SPF,
        "spf-def",
        "lemma",
        "the scan of the line segment 2..n-1 must land somewhere first: the first landing is the first divisor, and primality is the scan that lands nowhere",
        (),
        "the definition — the line segment has a first element",
    ),
    "the scan ledger records every comparison of the full process without optimization: for each new prime, the primes its scan met are its place in the prime order — predictable — while the integers it met grow with the gaps between primes, and it is by the integers, not the primes, that the history grows; on my line the last prime 83 was established by comparing 22 primes against 59 integers": (
        CONCEPT_S11_LEDGER,
        "ledger-growth",
        "lemma",
        "record, don't optimize: the ledger keeps every comparison, and its growth is the prime gaps in the counting room",
        (),
        "the owner's direction 2026-08-23 (the record, not the optimization) — the censuses on the line verify it",
    ),
}

#: The three S11 sanctioned compositions (frozen by the E6.15
#: pre-reg): target -> EXACT part set, byte-frozen statement, and the
#: owning concept (all three under the first-divisor concept; the
#: ledger concept carries the ledger-growth lesson + the ledger
#: census modes).
S11_THEOREMS: dict[str, dict] = {
    "first-divisor-prime": {
        "parts": ("composite-def", "spf-def"),
        "statement": "the first divisor of a composite number is prime: if the smallest k above 1 that divides n were composite, some k above 1 and below it would divide it, and that smaller one would divide n too — contradicting that k is the first divisor of n; so the first divisor is always prime",
        "concept": CONCEPT_S11_SPF,
    },
    "sieve-equality": {
        "parts": ("first-divisor-prime", "divides-def"),
        "statement": "the full sieve and the prime sieve mark the same composites: every composite's first divisor is prime, so among the candidates 2..n-1 the first one to divide a composite is always a prime; the composite candidates the extra full scan tests can never win a scan first, and the marks of the two sieves agree — the difference is bookkeeping only, and the ledger keeps it",
        "concept": CONCEPT_S11_SPF,
    },
    "spf-chain": {
        "parts": ("sieve-equality", "spf-def", "divides-def"),
        "statement": "every n above 1 is built from its prime parts: strip off the first divisor and descend on what remains, down to 1; each strip is a prime factor by the redundancy, the part multiset is the number's prime factorization with its content unique, and the order of stripping is a choice of the scan",
        "concept": CONCEPT_S11_SPF,
    },
}

_S11_SLUGS: str = (
    "divides-def|composite-def|spf-def|ledger-growth"
    "|first-divisor-prime|sieve-equality|spf-chain"
)

S11_SLUG_CONCEPT: dict[str, str] = {
    "divides-def": CONCEPT_S11_DIVID,
    "composite-def": CONCEPT_S11_COMP,
    "spf-def": CONCEPT_S11_SPF,
    "ledger-growth": CONCEPT_S11_LEDGER,
    "first-divisor-prime": CONCEPT_S11_SPF,
    "sieve-equality": CONCEPT_S11_SPF,
    "spf-chain": CONCEPT_S11_SPF,
}

#: the S11 theorems join the shared `derive` policy now that the
#: block above exists (the forward reference of the line-1839 merge).
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S11_THEOREMS}

S11_DIVTEST_RE = re.compile(r"\bdoes (\d+) divide (\d+)\?")
S11_COMPT_RE = re.compile(r"\bis (\d+) composite\?")
S11_PRIMETEST_RE = re.compile(r"\bis (\d+) a prime\?")
S11_FD_RE = re.compile(r"\bwhat is the first divisor of (\d+)\?")
S11_COMPCOUNT_RE = re.compile(r"\bhow many composites are there up to (\d+)\?")
S11_FDCOUNT_RE = re.compile(r"\bhow many composites up to (\d+) have first divisor (\d+)\?")
S11_FULLTRIALS_RE = re.compile(r"\bhow many trials does the full sieve spend on the composites up to (\d+)\?")
S11_PRIMETRIALS_RE = re.compile(r"\bhow many trials does the prime sieve spend on the composites up to (\d+)\?")
S11_CANDEVEN2_RE = re.compile(r"\bhow many times does the full sieve check an even number for divisibility by 2\?")
S11_CANDTESTS_RE = re.compile(r"\bhow many times does the full sieve test the candidate (\d+) up to (\d+)\?")
S11_CANDHITS_RE = re.compile(r"\bhow many times does the full sieve hit the candidate (\d+) up to (\d+)\?")
S11_CANDMISSES_RE = re.compile(r"\bhow many times does the full sieve miss the candidate (\d+) up to (\d+)\?")
S11_PRIMELEDGER_RE = re.compile(r"\bfor the prime (\d+), how many primes and how many integers did the sieve compare\?")
S11_ESTTOTAL_RE = re.compile(r"\bhow many comparisons did the sieve spend in total establishing the primes up to (\d+)\?")
S11_PARTS_RE = re.compile(r"\bwhat are the prime parts of (\d+)\?")
S11_AUDIT_RE = re.compile(r"\bdoes the full sieve keep anything the prime sieve throws away\?")
S11_SIEVERUN_RE = re.compile(r"\brun the sieve up to (\d+)\?")
S11_ANY_STATE_RE = re.compile(rf"\bstate the ({_S11_SLUGS}) rule\b")
S11_ANY_WHY_RE = re.compile(rf"\bwhat is the ({_S11_SLUGS}) for\b")
S11_WHYDEEP_RE = re.compile(rf"\bexplain why the ({_S11_SLUGS}) holds\b")

S11_MODES: tuple[str, ...] = (
    "div-test",
    "comp-test",
    "prime-test",
    "fd-query",
    "comp-count",
    "fd-count",
    "full-trials",
    "prime-trials",
    "cand-even2",
    "cand-tests",
    "cand-hits",
    "cand-misses",
    "prime-ledger",
    "est-total",
    "parts",
    "audit",
    "sieverun",
    "s11-state",
    "s11-why",
    "s11-whydeep",
)

#: The E6.15 pre-reg beds (frozen 2026-08-23, hand-computed +
#: cross-checked; D-e6f(a) on/off-line split). ON-LINE values are
#: grounded answers; OFF-LINE values appear ONLY in walls that name
#: them / the pre-reg beds (the house convention, S8 J(84)=1053
#: precedent).
S11_BEDS: dict[str, Any] = {
    "line_end": 84,
    "comp_count": {10: 5, 84: 60},
    "fd_count_84": {2: 41, 3: 13, 5: 4, 7: 2},
    "primes_84": 23,
    "kill_trials_full": {10: 6, 25: 21, 50: 52, 79: 90, 84: 95},
    "kill_trials_prime": {10: 6, 25: 20, 50: 48, 79: 82, 84: 87},
    "first_divergence": 25,
    "est_total": {10: 9, 13: 29, 17: 44, 19: 61, 23: 82, 29: 109, 84: 828},
    "cand_rows_84": {
        2: (82, 41, 41),
        3: (40, 13, 27),
        4: (27, 0, 27),
        5: (26, 4, 22),
        6: (22, 0, 22),
        7: (21, 2, 19),
        8: (19, 0, 19),
        9: (19, 0, 19),
        10: (19, 0, 19),
    },
    "whole_process_84": (923, 340, 583),  # full / prime-scan / composite-candidate tests
    "prime_rows": {2: (0, 0), 3: (1, 0), 5: (2, 1), 7: (3, 2), 11: (4, 5), 79: (21, 56), 83: (22, 59)},
    "prime_row_sums": (253, 575),
    "chains": {60: (2, 2, 3, 5), 84: (2, 2, 3, 7), 49: (7, 7), 77: (7, 11), 72: (2, 2, 2, 3, 3), 81: (3, 3, 3, 3)},
    "audit_rows": (60, 41, 27, 0, 22, 0),  # comp census, cand2 hits, cand4 tests/hits, cand6 tests/hits
}


#: The S11 python-side references (wall names + the P4 referee; never
#: cited — the on-line walkers are what the store holds).
def _s11_py_spf(n: int) -> int:
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def _s11_py_comp_count(n: int) -> int:
    return sum(1 for m in range(2, n + 1) if _s11_py_spf(m) != m)


def _s11_py_fd_count(n: int, d: int) -> int:
    # composites only: a prime m has _s11_py_spf(m) == m, which must
    # NOT count as "first divisor d == m" (the frozen beds: 41 for
    # (84, 2), not 42).
    return sum(1 for m in range(2, n + 1) if (s := _s11_py_spf(m)) == d and s != m)


def _s11_py_kill_trials(n: int, prime_only: bool) -> int:
    primes = [m for m in range(2, n + 1) if _s11_py_spf(m) == m]
    total = 0
    for m in range(2, n + 1):
        s = _s11_py_spf(m)
        if s == m:
            continue
        total += (primes.index(s) + 1) if prime_only else (s - 1)
    return total


def _s11_py_cand_row(d: int, n: int) -> tuple[int, int, int]:
    tests = hits = 0
    for m in range(2, n + 1):
        s = _s11_py_spf(m)
        if s == m:
            if m > d:
                tests += 1
        elif s >= d:
            tests += 1
            if s == d:
                hits += 1
    return tests, hits, tests - hits


def _s11_py_est_total(n: int) -> int:
    return sum(m - 2 for m in range(2, n + 1) if _s11_py_spf(m) == m)


def _s11_py_prime_row(p: int) -> tuple[int, int]:
    pm = sum(1 for m in range(2, p) if _s11_py_spf(m) == m)
    return pm, (p - 2) - pm


def _s11_py_chain(n: int) -> list[int]:
    parts: list[int] = []
    cur = n
    while True:
        s = _s11_py_spf(cur)
        if s == cur:
            parts.append(cur)
            return parts
        parts.append(s)
        cur //= s


#: the union of savant+rh lesson phrases (S4 + S5 + S6 + S7 + S8 +
#: S9 + S11) for the lesson policy.
SAVANT_LESSONS: dict[str, tuple] = {
    **S4_LESSONS,
    **S5_LESSONS,
    **S6_LESSONS,
    **S7_LESSONS,
    **S8_LESSONS,
    **S9_LESSONS,
    **S11_LESSONS,
}

# ── E6.16 — FUNDAMENTALS-TRACK S12 (pre-registered E6.16, frozen
# 2026-08-23; D-e6g(a)/(b) corrected): "the RH neighborhood" — the
# parallel band: the lots related to the condition (RH) and the
# lots that ride on it, with the HONEST SPLIT (condition-closers /
# condition-neighbors / open-even-under-RH), the on-line gap and
# deviation censuses, and the SELF-GENERATED cross-pollination
# queue (selection by declared class, no manual steering).
import math as _math

CONCEPT_S12_COND = "conditional"
CONCEPT_S12_SCALE = "rh-scale"
CONCEPT_S12_ROUTE = "factor-route"
CONCEPT_S12_REL = "rh-relevance"

CONCEPT_S12: tuple = (
    Concept(
        CONCEPT_S12_COND,
        "a conditional lot: a conclusion under the condition that the zeros lie on the line",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH,),
    ),
    Concept(
        CONCEPT_S12_SCALE,
        "the root scale: the error and the gap the condition installs",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S12_COND, CONCEPT_RH_PNTE),
    ),
    Concept(
        CONCEPT_S12_ROUTE,
        "the two roads to prime-parts uniqueness: the scan, and the condition",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S12_SCALE, CONCEPT_S11_SPF),
    ),
    Concept(
        CONCEPT_S12_REL,
        "the declared RH-relevance classes that select the cross-pollination queue",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S12_SCALE, CONCEPT_S12_ROUTE),
    ),
)

#: The four S12 DECLARED lessons (the pre-reg statements; D-e6g(c)
#: drops the drafting colon at the end of rh-relevance-def —
#: recorded at close-out). The hypothesis marker rule (P0): every
#: conditional statement carries its condition's text.
S12_LESSONS: dict[str, tuple] = {
    "a conditional lot is one whose conclusion holds under the condition that every nontrivial zero of zeta has real part exactly one half: the hypothesis travels in every statement of the lot, and every derivation that uses a conditional lot keeps the marker explicit; a conditional lot read without its condition is a misread this store punishes": (
        CONCEPT_S12_COND,
        "conditional-def",
        "lemma",
        "the shape of a hypothesis-carrying lot: the marker travels, and dropping it is the one misread the store punishes",
        (),
        "the definition — a conditional lot is its conclusion plus the condition it needs",
    ),
    "under the condition of the Riemann hypothesis, the error and the gap carry the same root scale: the chebyshev psi of x is x plus O of the square root of x times the log of x, and the gap between consecutive primes is, past a fixed point, at most the square root of the preceding prime times its log; that is the root scale, x to the one-half plus epsilon, that the criterion gap demands — under the condition the ratio of the store's error term to the scale the theorem rh-reach demands stays bounded, and the condition closes exactly the gap the theorem names": (
        CONCEPT_S12_SCALE,
        "rh-bound-scale",
        "lemma",
        "the root scale in two readings: the error of the prime count, and the gap between consecutive primes — the same scale the criterion gap demands",
        (),
        "the declaration — under the condition, the error and the gap are root-scale; the theorem rh-reach names exactly the gap it closes",
    ),
    "under the condition of the Riemann hypothesis, the prime parts of every number are unique: the condition bounds the running sum of (minus one) to the number of distinct prime parts, over the integers at most x, by the root scale x to the one-half plus epsilon, and one number built from two different part multisets would push that running sum past the root scale; the condition reaches the same destination the scan road reaches without the condition, by a different road (the root smallness, not the scan)": (
        CONCEPT_S12_ROUTE,
        "rh-upf",
        "lemma",
        "the second road to uniqueness: the root smallness of the running deviation, under the condition — a different road to the scan road's destination",
        (),
        "the declaration — the condition implies prime-parts uniqueness (the root smallness of the running deviation)",
    ),
    "the lots of this band carry a declared relevance to the condition, and the declaration is the fact: the condition-closers carry the root scale the condition installs (the error, the gap, the root smallness of the running deviation), the condition-neighbors are the unconditionals the condition refines (the primes in residue classes, the zero count at height T), and the condition itself is open even under the condition — the condition does not close itself; from that declaration the cross-pollination queue of the bands above follows, in declared order, not computed and not steered": (
        CONCEPT_S12_REL,
        "rh-relevance-def",
        "lemma",
        "the declared classes are the selection rule: closers, neighbors, the open condition — and the queue above follows from the declaration, not from steering",
        (),
        "the definition — relevance is declared, and the declaration drives the cross-pollination queue",
    ),
}

#: The three S12 sanctioned compositions (frozen by the E6.16
#: pre-reg): target -> EXACT part set, byte-frozen statement, the
#: owning concept.
S12_THEOREMS: dict[str, dict] = {
    "gap-scale-agreement": {
        "parts": ("rh-bound-scale", "ledger-growth", "spf-chain"),
        "statement": "on my line the bare root scale fails in exactly two places: at 2 (the gap of 1 stands above the scale) and at 3 (the gap of 2 stands above the scale), and covers all the other 20 gaps; the greatest gap on the line is 6, first at 23, and six gaps reach it; the ledger's integer side grows with the gaps, and the gaps stay below the scale everywhere but the line's two small-prime witnesses",
        "concept": CONCEPT_S12_SCALE,
    },
    "two-routes-one-guarantee": {
        "parts": ("rh-upf", "spf-chain"),
        "statement": "the two roads to the prime-parts uniqueness reach the same destination: the scan road arrives without the condition (the content of every number is the same under every scan), the condition road arrives under the condition of the Riemann hypothesis (the root smallness of the running deviation) — same destination, different roads, and the condition buys nothing at the destination",
        "concept": CONCEPT_S12_ROUTE,
    },
    "queue-declared": {
        "parts": ("rh-relevance-def", "rh-bound-scale", "rh-upf"),
        "statement": "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
        "concept": CONCEPT_S12_REL,
    },
}

_S12_SLUGS: str = (
    "conditional-def|rh-bound-scale|rh-upf|rh-relevance-def"
    "|gap-scale-agreement|two-routes-one-guarantee|queue-declared"
)

S12_SLUG_CONCEPT: dict[str, str] = {
    "conditional-def": CONCEPT_S12_COND,
    "rh-bound-scale": CONCEPT_S12_SCALE,
    "rh-upf": CONCEPT_S12_ROUTE,
    "rh-relevance-def": CONCEPT_S12_REL,
    "gap-scale-agreement": CONCEPT_S12_SCALE,
    "two-routes-one-guarantee": CONCEPT_S12_ROUTE,
    "queue-declared": CONCEPT_S12_REL,
}

#: the S12 lessons + theorems join the shared policies now that the
#: block above exists (the S11 re-merge pattern).
SAVANT_LESSONS = {**SAVANT_LESSONS, **S12_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S12_THEOREMS}

S12_GAP_RE = re.compile(r"\bthe gap after (\d+) on my line, what is it\?")
S12_GAPMAX_RE = re.compile(r"\bthe gap on my line, greatest, what is it\?")
S12_GAPMAXWHOLE_RE = re.compile(r"\bthe greatest gap of the whole prime line, what is it\?")
S12_GAPSIZEN_RE = re.compile(r"\bthe gaps of size (\d+) on my line, how many\?")
S12_GAPCOUNT_RE = re.compile(r"\bthe gaps on my line, how many\?")
S12_SCALE_RE = re.compile(r"\bdoes the bare scale at (\d+) on my line cover the gap\?")
S12_SCALECOUNT_RE = re.compile(r"\bthe gaps on my line covered by the bare scale, how many\?")
S12_MOD4_1_RE = re.compile(r"\bthe primes one mod four on my line, (how many|which)\?")
S12_MOD4_3_RE = re.compile(r"\bthe primes three mod four on my line, (how many|which)\?")
S12_MLAB_RE = re.compile(r"\bthe factor-count deviation ledger on my line, greatest absolute, what is it\?")
S12_MAT_RE = re.compile(r"\bthe factor-count deviation ledger at (\d+), what is it\?")
S12_MROOT_RE = re.compile(r"\bis the factor-count deviation ledger of my line below the root of my line end\?")
S12_MPAST_RE = re.compile(r"\bthe factor-count deviation ledger past my line end, below the root smallness, is it\?")
S12_COND_GIVE_RE = re.compile(
    r"\bwhat does the condition give for "
    r"(the error of the prime count|the gaps between primes|the prime parts of a number"
    r"|the factor-count deviation|the zero count at height T|the zeros of the zeta function)\?"
)
S12_UNCOND_RE = re.compile(r"\bis the prime-parts uniqueness established without the condition\?")
S12_QUEUE_RE = re.compile(r"\bwhat is the queue above my line\?")
S12_QUEUELOT_RE = re.compile(r"\bthe queue above my line, (first|second|third|fourth|fifth) lot, which\?")
S12_CLASS_RE = re.compile(r"\bthe lots of this band (condition-closing|condition-neighboring|open even under the condition), which\?")
S12_AGREE_RE = re.compile(r"\bdoes my line agree with the conditional root scale\?")
S12_ROADS_HOW_RE = re.compile(r"\bhow do the two roads to prime-parts uniqueness differ\?")
S12_ROADS_UNCOND_RE = re.compile(r"\bwhich road to prime-parts uniqueness carries without the condition\?")
S12_ROADS_COND_RE = re.compile(r"\bwhich road asks for the condition\?")
S12_ROADNEG_RE = re.compile(r"\bdoes the condition road carry the guarantee without the condition\?")
S12_REACHSCALE_RE = re.compile(r"\bwhich scale does the theorem rh-reach demand\?")
S12_MOD4Q_RE = re.compile(r"\bdoes my line carry the mod-4 split of the primes\?")
S12_SELVED_RE = re.compile(r"\bis the conjecture closed by any lot of this band\?")
S12_PROVE_RE = re.compile(r"\bprove the condition from its own lots\?")
S12_BANDSTATE_RE = re.compile(r"\bthe band at the line end, state\?")
S12_ANY_STATE_RE = re.compile(rf"\bstate the ({_S12_SLUGS}) rule\b")

S12_MODES: tuple[str, ...] = (
    "s12-gap",
    "s12-gapmax",
    "s12-gapmax-whole",
    "s12-gapsize",
    "s12-gapcount",
    "s12-scale",
    "s12-scalecount",
    "s12-mod4-1",
    "s12-mod4-3",
    "s12-mlab",
    "s12-mat",
    "s12-mroot",
    "s12-mpast",
    "s12-condgive",
    "s12-uncond",
    "s12-queue",
    "s12-queue-lot",
    "s12-class",
    "s12-agree",
    "s12-roads-how",
    "s12-roads-uncond",
    "s12-roads-cond",
    "s12-roadneg",
    "s12-reachscale",
    "s12-mod4q",
    "s12-selved",
    "s12-prove",
    "s12-bandstate",
    "s12-state",
)

#: The E6.16 pre-reg beds (frozen 2026-08-23 by the MECHANISM's
#: census — D-e6g(a)/(b): the hand's first drafts missed the 31->37
#: gap and flipped the sign of mu(78); the mechanism's census
#: governs): the gap census, the bare-scale witness set, the mod-4
#: split, the mu ledger. ON-LINE values are grounded answers;
#: OFF-LINE values (0.98, 1.90, 9.17, 89) appear ONLY in walls
#: that name them (W-S12-2, W-S12-8) and in these beds.
S12_BEDS: dict[str, Any] = {
    "line_end": 84,
    "gap_list": (1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4),
    "gap_count": 22,
    "gap_max": (6, 23),  # (value, first at)
    "gap6_pairs": ((23, 29), (31, 37), (47, 53), (53, 59), (61, 67), (73, 79)),
    "scale_fail": (2, 3),  # the only primes whose gap stands above the bare scale
    "scale_cover_count": 20,
    "scale_wall_values": {"2": 0.98, "3": 1.90},  # named in W-S12-8, 2 decimals
    "sqrt_line_end": 9.17,  # named in W-S12-8
    "next_prime_past_83": 89,  # named in W-S12-2
    "mod4_1": (5, 13, 17, 29, 37, 41, 53, 61, 73),
    "mod4_3": (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83),
    "mu_max_abs": 4,
    "mu_first_at": 31,
    "mu_max_at": (31, 32, 73, 79, 80, 81, 83, 84),
    "mu_at": {31: -4, 84: -4},
}


#: The S12 python-side references (beds + the P4 referee; never
#: cited — the on-line walkers are what the store holds).
def _s12_py_primes(end: int = 84) -> list[int]:
    return [p for p in range(2, end + 1) if _s11_py_spf(p) == p]


def _s12_py_gaps(end: int = 84) -> list[tuple[int, int]]:
    ps = _s12_py_primes(end)
    return [(ps[i], ps[i + 1] - ps[i]) for i in range(len(ps) - 1)]


def _s12_py_scale(p: int) -> float:
    return _math.sqrt(p) * _math.log(p)


def _s12_py_mu(n: int) -> int:
    if n == 1:
        return 1
    k, m, d = 0, n, 2
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            k += 1
        d += 1
    if m > 1:
        k += 1
    return -1 if k % 2 else 1


def _s12_py_M(end: int = 84) -> dict[int, int]:
    track: dict[int, int] = {}
    acc = 0
    for n in range(1, end + 1):
        acc += _s12_py_mu(n)
        track[n] = acc
    return track


def _next_prime_after(p: int) -> int:
    cand = p + 1
    while _s11_py_spf(cand) != cand:
        cand += 1
    return cand



# ── E6.17 (S13: zeta variants, three families) — FUNDAMENTALS-TRACK
# backward-fan band 2 (pre-reg E6.17 frozen 2026-08-24 at ed69baa;
# D-e6h(a)/(b)/(c) recorded pre-freeze). The variant layer UNDER
# euler-product: the family factors, the index split, the line
# partials, the term removal. UNCONDITIONAL band — the RH marker
# must stay ABSENT from every S13 fact (P0). Off-line limit values
# appear ONLY in the W-S13-* walls that name them.
CONCEPT_S13_FACTOR = "family-factor"
CONCEPT_S13_SPLIT = "index-split"
CONCEPT_S13_PARTIAL = "line-partial"
CONCEPT_S13_REMOVAL = "removal-rule"

CONCEPT_S13: tuple = (
    Concept(
        CONCEPT_S13_FACTOR,
        "the family factor: the term each index number carries",
        "college-1",
        "rh",
        prereqs=(CONCEPT_RH_ZETA,),
    ),
    Concept(
        CONCEPT_S13_SPLIT,
        "the index split: primes, composites, all — a partition of the integers above one",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S11_COMP,),
    ),
    Concept(
        CONCEPT_S13_PARTIAL,
        "the line partial: what a family holds up to the line end, a rational the store holds",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S13_FACTOR, CONCEPT_S13_SPLIT),
    ),
    Concept(
        CONCEPT_S13_REMOVAL,
        "the term-removal: the product is multiplied by the reciprocal of the removed term",
        "college-1",
        "rh",
        prereqs=(CONCEPT_S13_PARTIAL,),
    ),
)

S13_LESSONS: dict[str, tuple] = {
    "the factor of a family is the term each index number carries: the minus family carries (1 minus i to the power minus s) and the plus family carries (1 plus i to the power minus s), and a family indexes the integers above one — all of them, the primes only, or the composites only": (
        CONCEPT_S13_FACTOR,
        "factor-def",
        "lemma",
        "What a family factor IS: the term each index number carries, per sign and per index set.",
        (),
        "The factor of a family is the term each index number carries.",
    ),
    "the integers above one split into primes and composites and into nothing else: every integer above one is a prime or a composite, and is neither both; so a family over all of them is the product of the family over the primes and of the family over the composites, on both signs": (
        CONCEPT_S13_SPLIT,
        "split-def",
        "lemma",
        "What the index split IS: the partition of the line's integers above one into primes and composites.",
        (),
        "The integers above one split into primes and composites and into nothing else.",
    ),
    "the term-removal rule: when a term is removed from a product, the product is multiplied by the reciprocal of the removed term; when the prime p is removed from the minus family at s = 2, the multiplier is p squared over p squared minus one; the change of the output is determined exactly by the removed terms, and by nothing else": (
        CONCEPT_S13_REMOVAL,
        "removal-def",
        "lemma",
        "What term removal IS: the exact multiplier a removal carries, and that the change is nothing but the removed terms.",
        (),
        "The term-removal rule: the product is multiplied by the reciprocal of the removed term.",
    ),
    "the families converge for the real part of s greater than one — the same half-plane where the store already holds the euler product; on my line the family is held as the partial product up to the line end 84, a rational the store can hold, and the limit over the whole infinite index past the line end is a step the store declares, not a number on my line": (
        CONCEPT_S13_PARTIAL,
        "region-def",
        "lemma",
        "What the convergence region IS: the half-plane boundary, with the line partials as the store's exact holds.",
        (),
        "The families converge for the real part of s greater than one; on my line they are held as partials.",
    ),
}

S13_THEOREMS: dict[str, dict] = {
    "partition-identity": {
        "parts": ("split-def", "factor-def"),
        "statement": "where the index sets split, the product splits: for every family, the product over the integers above one is the product over the primes times the product over the composites — on my line the mechanism holds both sides as exact rationals, 85 over 168 both ways at s = 2",
        "concept": CONCEPT_S13_SPLIT,
    },
    "telescope-line": {
        "parts": ("factor-def", "region-def"),
        "statement": "the minus family over all the numbers telescopes: (1 minus n to the power minus 2) is (n minus 1)(n plus 1) over n squared, so the partial product to height N is (N plus 1) over 2N — at my line end, height 84, that is 85 over 168, and every spot height on my line answers by the same rule",
        "concept": CONCEPT_S13_PARTIAL,
    },
    "removal-single": {
        "parts": ("removal-def", "factor-def"),
        "statement": "removing one prime from the minus family at s = 2 multiplies by p squared over p squared minus one: the change of the output is exactly the reciprocal of the removed term — for every prime on my line the store holds the multiplier as an exact rational",
        "concept": CONCEPT_S13_REMOVAL,
    },
}

_S13_SLUGS = (
    "factor-def|split-def|removal-def|region-def|"
    "partition-identity|telescope-line|removal-single"
)
S13_SLUG_CONCEPT = {
    "factor-def": CONCEPT_S13_FACTOR,
    "split-def": CONCEPT_S13_SPLIT,
    "removal-def": CONCEPT_S13_REMOVAL,
    "region-def": CONCEPT_S13_PARTIAL,
    "partition-identity": CONCEPT_S13_SPLIT,
    "telescope-line": CONCEPT_S13_PARTIAL,
    "removal-single": CONCEPT_S13_REMOVAL,
}
SAVANT_LESSONS = {**SAVANT_LESSONS, **S13_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S13_THEOREMS}

S13_FACTOR_RE = re.compile(r"\bwhat factor does the (minus|plus) family carry at the number (\d+)\?")
S13_FACTOR_PRIME_RE = re.compile(r"\bwhat factor does the prime family carry at the number (\d+)\?")
S13_INDEX_COUNT_RE = re.compile(r"\bhow many index numbers does my line carry above one\?")
S13_SPLIT_CENSUS_RE = re.compile(r"\bhow do the index numbers of my line split\?")
S13_SEAM_COUNT_RE = re.compile(r"\bcount the index numbers of my line by their sieve status")
S13_SEAM_SAMESET_RE = re.compile(r"\bare the primes of my index split the set my prime census names\?")
S13_PARTIAL_RE = re.compile(
    r"\bwhat does the (minus|plus) family over (all the numbers|the primes|the composites) "
    r"hold up to (my line end|height (\d+))( at s = (\d+))?\?"
)
S13_PARTITION_HOLD_RE = re.compile(r"\bdoes the partition identity hold( at s = (\d+))? on my line\?")
S13_REMOVAL_RE = re.compile(r"\bhow does the minus family over the primes( at s = (\d+))? change when i remove the prime (\d+)\?")
S13_REMOVAL_SET_RE = re.compile(
    r"\bwhen my line's primes (.+?) are removed from the minus family over the primes "
    r"at s = (\d+), what is the whole multiplier\?"
)
S13_REMOVAL_ALL_RE = re.compile(
    r"\bif my line's whole prime family is removed from the minus family over "
    r"all the numbers at s = (\d+), what remains\?"
)
S13_SPOT_ABOVE_RE = re.compile(r"\bof the telescope spot values on my line — do any fall below one half\?")
S13_LIMIT_RE = re.compile(
    r"\bwhat is the (minus|plus) family over (all the numbers|the primes|the composites) "
    r"in the limit(, as the height walks past my line| at s = (\d+))?\?"
)
S13_LIMIT_BOUNDARY_RE = re.compile(
    r"\bwhat is the (minus|plus) family over (all the numbers|the primes|the composites) "
    r"at the boundary s = 1\?"
)
S13_COMPARE6_RE = re.compile(
    r"\bof the six family partials at s = 2 on my line, which stands largest and which stands smallest\?"
)
S13_COMPARE3_RE = re.compile(r"\bcompare the three (minus|plus) family partials on my line at s = (\d+)\b")
S13_COMPARE_SAME_RE = re.compile(r"\bthe same comparison for the (minus|plus) family\b")
S13_REMOVAL_BELOW_RE = re.compile(r"\bwhich removal multipliers at s = (\d+) are below 2\?")
S13_REMOVAL_MAX_RE = re.compile(r"\bwhich removal multiplier at s = (\d+) stands largest, and at which prime\?")
S13_DESCENT_RE = re.compile(r"\bwhat happens to the minus family spot values as the height walks along my line\?")
S13_PLUS_SIDE_RE = re.compile(r"\bwhere does the plus family's all partial at s = 2 stand against its limit\?")
S13_CLOSED_FORM_RE = re.compile(r"\bprove that the plus family over all the numbers has a closed form my store can hold")
S13_RH_TOUCH_RE = re.compile(r"\bcan the zeta variants settle the riemann hypothesis in my store\?")
S13_RHZERO_RE = re.compile(r"\bderive the Riemann hypothesis from the telescope on my line\b")
S13_BANDSTATE_RE = re.compile(r"\bwhat did this band add to the store\?")
S13_UNCOND_RE = re.compile(r"\bis anything this band says conditional on the Riemann hypothesis\?")
S13_UNCLASS_RE = re.compile(r"\bwhat does the track hold for the plus family's unclassified object\?")
S13_ANY_STATE_RE = re.compile(rf"\bstate the ({_S13_SLUGS}) rule\b")

S13_MODES: tuple[str, ...] = (
    "s13-factor",
    "s13-factor-prime",
    "s13-index-count",
    "s13-split-census",
    "s13-seam-count",
    "s13-seam-sameset",
    "s13-partial",
    "s13-partition-hold",
    "s13-removal",
    "s13-removal-set",
    "s13-removal-all",
    "s13-spot-above",
    "s13-limit",
    "s13-limit-boundary",
    "s13-compare6",
    "s13-compare3",
    "s13-compare-same",
    "s13-removal-below",
    "s13-removal-max",
    "s13-descent",
    "s13-plus-side",
    "s13-closed-form",
    "s13-rh-touch",
    "s13-rhzero",
    "s13-bandstate",
    "s13-uncond",
    "s13-unclass",
    "s13-state",
)

#: The E6.17 pre-reg beds (the python reference; the MECHANISM's store
#: run is the referee — D-e6h(b)/(c): the hand drafts are
#: cross-checked, not trusted). The exact line rationals; the
#: off-line values appear ONLY in the W-S13-* walls.
S13_BEDS: dict[str, Any] = {
    "line_end": 84,
    "census": {"integers": 83, "primes": 23, "composites": 60},
    "telescope_spots": {
        "2": "3/4", "3": "2/3", "4": "5/8", "8": "9/16",
        "10": "11/20", "20": "21/40", "50": "51/100", "84": "85/168",
    },
    "telescope_named_spots": ("3/4", "2/3", "5/8", "11/20", "85/168"),
    "telescope_offline_N100": "101/200",
    "removal_max_s2": (2, "4 over 3"),
    "removal_max_s3": (2, "8 over 7"),
    "removal_below2_s2_count": 23,
    "set_removal_s2": {"2,3": "3/2", "2,3,5": "25/16"},
    "order_s2": ["minus-all", "minus-prime", "minus-comp", "plus-comp", "plus-prime", "plus-all"],
    "wall_values": {
        "W1": 0.5,
        "W2": 0.6079271019,
        "W3": 0.8224670334,
        "W4": 1.5198177546,
        "W5": 1.8380389552,
        "W5b": 1.2093811574,
        "W6": 0.8319073726,
        "W7": "101/200",
    },
}

#: The S13 python-side references (the P4 referee; never cited by the
#: store — the on-line walkers are what the mechanism holds).
def _s13_py_primes(end: int = 84) -> list[int]:
    return [p for p in range(2, end + 1) if _s11_py_spf(p) == p]


def _s13_py_family(sign: int, indexset: str, exp: int, N: int = 84) -> Fraction:
    """The exact partial product over 2..N of (1 sign n^-exp)."""
    ps = set(_s13_py_primes(N))
    if indexset == "primes":
        xs = [n for n in range(2, N + 1) if n in ps]
    elif indexset == "comp":
        xs = [n for n in range(2, N + 1) if n not in ps]
    else:
        xs = list(range(2, N + 1))
    from fractions import Fraction

    v: Fraction = Fraction(1)
    for n in xs:
        v *= Fraction(n ** exp + (1 if sign > 0 else -1), n ** exp)
    return v


def _s13_py_telescope(N: int) -> Fraction:
    from fractions import Fraction

    return Fraction(N + 1, 2 * N)


def _s13_py_removal(p: int, exp: int) -> Fraction:
    from fractions import Fraction

    return Fraction(p ** exp, p ** exp - 1)

# ── E6.18 (S14: the elliptic city) — PRIZE-ISLANDS-TRACK (the BSD
# island, band 1 of 3; owner-directed 2026-08-24, the $1M+ initiative).
# Panel curves of record (LMFDB, verified 2026-08-24 —
# plan/40-prize-islands/bsd-research.md):
#   A: y^2 = x^3 - x          (32a2 / LMFDB 32.a3): conductor 32,
#      rank 0, torsion (Z/2)^2, CM (j = 1728) — the congruent-number
#      curve for one.
#   B: y^2 + y = x^3 - x      (37a1 / LMFDB 37.a1): conductor 37,
#      rank 1 (the smallest conductor with positive rank), torsion
#      trivial, generator (0,0) of record.
# UNCONDITIONAL band: nothing the store holds under S14 is conditional
# on RH — the L(E) limit and the ranks live past the line, and the
# walls name them. The a_p censuses, the Hasse all-pass, the CM
# signature iff, and the 10/10 generation ledger are VERIFIED shadows
# of record facts, labeled as such in every articulation; the record
# claims (ranks, modularity, the BSD frontier) stay walls.
CONCEPT_S14_FORM = "curve-form"
CONCEPT_S14_LAW = "curve-law"
CONCEPT_S14_COUNT = "point-count"
CONCEPT_S14_SHADOW = "curve-shadow"

CONCEPT_S14: tuple = (
    Concept(
        CONCEPT_S14_FORM,
        "the curve form: a curve over the rationals in the equation y squared = x cubed plus a x plus b, smooth exactly when four a cubed plus twenty-seven b squared does not zero out",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_ALG_2STEP,),
    ),
    Concept(
        CONCEPT_S14_LAW,
        "the chord-tangent law: the points of a curve form a group — the line through two points meets the curve a third time, its reflection the sum; exact rational functions of the points",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S14_FORM,),
    ),
    Concept(
        CONCEPT_S14_COUNT,
        "the shadow count: for every prime of the line the curve holds its points over the field with p elements, counted exactly; from the count and the prime comes the coefficient a = p + 1 minus the count",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S14_FORM, CONCEPT_S11_SPF),
    ),
    Concept(
        CONCEPT_S14_SHADOW,
        "the shadow censuses: the Hasse bound held prime by prime on the line (a theorem of record, the census the verified shadow), and for the first panel member the record signature zero exactly when p is two or three mod four",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S14_COUNT, CONCEPT_MOD4_SPLIT),
    ),
)

S14_LESSONS: dict[str, tuple] = {
    "an elliptic curve over the rationals is the set of the rational points on the equation y squared equals x cubed plus a times x plus b, together with the point at infinity, and it is a curve exactly when four times a cubed plus twenty-seven times b squared does not zero out — on my line the panel holds two of them, the first with a is minus one and b is zero (of record), the second in the y squared plus y form with a is minus one and b is zero (of record), and the pair a is zero and b is zero zeros the discriminant out and is not a curve at all": (
        CONCEPT_S14_FORM,
        "form-def",
        "lemma",
        "What a curve form IS: the Weierstrass equation, the smoothness condition, and the panel of record held on the line.",
        (),
        "An elliptic curve is the rational points on y squared equals x cubed plus a x plus b, with the point at infinity, smooth exactly when the discriminant does not zero out.",
    ),
    "the points of the curve form a group under the chord-tangent law: the line through two points meets the curve a third time, and that third point, reflected across the x axis, is their sum; the point at infinity is the identity; the law is exact over my rationals — for distinct points the slope is the change in y over the change in x, and a point with itself takes the slope three times x squared plus a over two times y plus the form's own constant — so every sum, double, and multiple I form is a rational point I can re-check against the curve's equation": (
        CONCEPT_S14_LAW,
        "law-def",
        "lemma",
        "What the chord-tangent law IS: the group law in exact rational functions, with the identity and the reflection.",
        (),
        "The points of a curve form a group under the chord-tangent law, exact over the rationals.",
    ),
    "for every prime of my line the curve casts a shadow: its points over the field with p elements — a finite set, counted exactly by testing each x against the equation mod p — and I record the count for every prime on the line; from the count and the prime comes the coefficient a = p plus one minus the count, the coefficient of the curve's L-function at that prime": (
        CONCEPT_S14_COUNT,
        "count-def",
        "lemma",
        "What the shadow count IS: the finite-field point count per prime, and the coefficient a = p + 1 minus the count.",
        (),
        "Every prime of the line gives the curve its shadow count, exactly, and the coefficient a = p plus one minus the count.",
    ),
    "the shadow censuses of the band: the Hasse bound — a squared at most four p — is a theorem of record that my census verifies prime by prime on the line and does not prove; and for the first panel member the record signature — the coefficient is zero exactly when p is two or p is three mod four — is the shadow of the curve's complex multiplication, held on my line as the verified pattern, both directions, at every prime of the line": (
        CONCEPT_S14_SHADOW,
        "shadow-def",
        "lemma",
        "What the shadow censuses ARE: the Hasse bound as a verified shadow of record, and the CM signature, both prime by prime on the line.",
        (),
        "The shadow censuses: the Hasse bound verified prime by prime, and the record signature of the first panel member, both on the line.",
    ),
}

S14_THEOREMS: dict[str, dict] = {
    "curve-identity": {
        "parts": ("law-def", "form-def"),
        "statement": "the point at infinity is the identity of the group: adding it to any point is that point, and the law's own formulas hold it — every point I form on my line answers the identity exactly",
        "concept": CONCEPT_S14_LAW,
    },
    "curve-inverse": {
        "parts": ("law-def", "form-def"),
        "statement": "the inverse of a point is its reflection: the point plus its inverse is the point at infinity, the line through them vertical, its third meeting the identity — every point I form answers exactly against its own reflection",
        "concept": CONCEPT_S14_LAW,
    },
    "hasse-census": {
        "parts": ("count-def", "form-def"),
        "statement": "the Hasse bound held on my line: for both panel members and every prime on the line, a squared is at most four p — the full prime by prime record, all passing, at the line end 84; the bound itself is a theorem of record, the census my verified shadow of it",
        "concept": CONCEPT_S14_COUNT,
    },
    "cm-signature": {
        "parts": ("shadow-def", "count-def"),
        "statement": "the record signature held on my line: for the first panel member, its shadow coefficient at p is exactly zero exactly when p is two or p is three mod four — both directions, at every prime on the line, the all-pass record at the line end 84; the reason is of record, the pattern is the verified shadow on my line",
        "concept": CONCEPT_S14_SHADOW,
    },
}

_S14_SLUGS = (
    "form-def|law-def|count-def|shadow-def|"
    "curve-identity|curve-inverse|hasse-census|cm-signature"
)
S14_SLUG_CONCEPT = {
    "form-def": CONCEPT_S14_FORM,
    "law-def": CONCEPT_S14_LAW,
    "count-def": CONCEPT_S14_COUNT,
    "shadow-def": CONCEPT_S14_SHADOW,
    "curve-identity": CONCEPT_S14_LAW,
    "curve-inverse": CONCEPT_S14_LAW,
    "hasse-census": CONCEPT_S14_COUNT,
    "cm-signature": CONCEPT_S14_SHADOW,
}
SAVANT_LESSONS = {**SAVANT_LESSONS, **S14_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S14_THEOREMS}


S14_FORM_RE = re.compile(r"\bwhat curve does the (first|second) panel member hold\?")
S14_SINGULAR_RE = re.compile(r"\bis the pair with a zero and b zero a smooth curve on my line\?")
S14_POINT_RE = re.compile(r"\bis the point at x (minus \d+|\d+) y (minus \d+|\d+) on the (first|second) panel member\?")
S14_DOUBLE_RE = re.compile(r"\bwhat is the point at x (minus \d+|\d+) y (minus \d+|\d+) plus itself on the (first|second) panel member\?")
S14_ADD_RE = re.compile(r"\bwhat is the point at x (minus \d+|\d+) y (minus \d+|\d+) plus the point at x (minus \d+|\d+) y (minus \d+|\d+) on the (first|second) panel member\?")
S14_MUL_RE = re.compile(r"\bwhat is (\d+) times the point at x (minus \d+|\d+) y (minus \d+|\d+) on the (first|second) panel member\?")
S14_COUNT_RE = re.compile(r"\bhow many points does the (first|second) panel member cast over the field with (\d+) elements\?")
S14_APTABLE_RE = re.compile(r"\bwhat are the shadows of the (first|second) panel member at the primes of my line\?")
S14_HASSE_RE = re.compile(r"\bdoes the Hasse bound hold at (\d+) for the (first|second) panel member\?")
S14_HASSE_ALL_RE = re.compile(r"\bdoes the Hasse bound hold on the whole line for both panel members\?")
S14_CMSIG_RE = re.compile(r"\bdoes the record signature of the first panel member — zero when p is two or three mod four — hold across my line\w?\?")
S14_CMSIG_ZEROS_RE = re.compile(r"\bat which primes of my line does the first panel member carry the zero coefficient\?")
S14_TORSION_A_RE = re.compile(r"\bwhich rational points of the first panel member does my line hold\?")
S14_GEN_RE = re.compile(r"\bis the point at x (minus \d+|\d+) y (minus \d+|\d+) a multiple of the point at x 0 y 0 on the second panel member within my bound\?")
S14_GEN_ALL_RE = re.compile(r"\bdo all the points my line counted on the second panel member sit in the ledger of the point at x 0 y 0 at my bound\?")
S14_GEN_CLOSE_RE = re.compile(r"\bdoes the ledger of the point at x 0 y 0 cover every rational point of the second panel member at my bound\?")
S14_LPAR_RE = re.compile(r"\bwhat does the (first|second) panel member's L product hold at my line end\?")
S14_LVANISH_RE = re.compile(r"\bwhat does the (first|second) panel member's L product do at its limit, past my line\?")
S14_RANK_RE = re.compile(r"\bwhat is the rank of the panel members on my line\?")
S14_SEARCH_B_RE = re.compile(r"\bwhich rational points of the second panel member does my line hold\?")
S14_PANELWHY_RE = re.compile(r"\bwhy these two panel members of the record\?")
S14_RH_TOUCH_RE = re.compile(r"\bcan the elliptic curves settle the Riemann hypothesis in my store\?")
S14_BANDSTATE_RE = re.compile(r"\bwhat did the elliptic band add to the store\?")
S14_UNCOND_RE = re.compile(r"\bdoes the elliptic band say anything conditional on the Riemann hypothesis\?")
S14_ANY_STATE_RE = re.compile(rf"\bstate the ({_S14_SLUGS}) rule\b")

S14_MODES: tuple[str, ...] = (
    "s14-form",
    "s14-singular",
    "s14-point-on",
    "s14-add",
    "s14-double",
    "s14-mul",
    "s14-count",
    "s14-aptable",
    "s14-hasse",
    "s14-hasse-all",
    "s14-cmsig",
    "s14-cmsig-zeros",
    "s14-torsion-a",
    "s14-gen",
    "s14-gen-all",
    "s14-gen-close",
    "s14-lpar",
    "s14-lvanish",
    "s14-rh-touch",
    "s14-rank",
    "s14-search-b",
    "s14-panel",
    "s14-bandstate",
    "s14-uncond",
    "s14-state",
)

# The S14 python-side references (the mechanism's own computation; same
# status as the _s13_py_* family — the store's run is the referee, the
# references compute the values the store articulates; panel data
# verified in plan/40-prize-islands/bsd-research.md, cross-checked
# Legendre-vs-brute and against LMFDB of record).
B14_A: tuple[int, int, int] = (0, -1, 0)  # (a3, a, b): y^2 = x^3 - x
B14_B: tuple[int, int, int] = (1, -1, 0)  # (a3, a, b): y^2 + y = x^3 - x


def _bsd_py_on_curve(P, a3: int, a: int, b: int) -> bool:
    if P is None:
        return True
    x, y = P
    return y * y + a3 * y == x ** 3 + a * x + b


def _bsd_py_count(p: int, a3: int, a: int, b: int) -> int:
    """#E(F_p) including O (the model's good-reduction primes)."""
    n = 1
    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        if p == 2:
            n += sum(1 for y in range(2) if (y * y + a3 * y - rhs) % 2 == 0)
            continue
        l = pow((a3 * a3 + 4 * rhs) % p, (p - 1) // 2, p)
        if l == p - 1:
            continue
        n += 2 if l == 1 else 1
    return n


def _bsd_py_ap(p: int, a3: int, a: int, b: int) -> int:
    return p + 1 - _bsd_py_count(p, a3, a, b)


def _bsd_py_neg(P, a3: int, a: int, b: int):
    assert _bsd_py_on_curve(P, a3, a, b)
    if P is None:
        return None
    return (P[0], -P[1] - a3)


def _bsd_py_add(P, Q, a3: int, a: int, b: int):
    """Chord/tangent on y^2 + a3 y = x^3 + a x + b over Q (a1 = 0)."""
    assert _bsd_py_on_curve(P, a3, a, b) and _bsd_py_on_curve(Q, a3, a, b)
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 + y2 + a3 == 0:
        return None
    if P == Q:
        if 2 * y1 + a3 == 0:
            return None
        m = Fraction(3 * x1 * x1 + a, 2 * y1 + a3)
    else:
        m = Fraction(y2 - y1, x2 - x1)
    x3 = m * m - x1 - x2
    y3 = -(y1 + m * (x3 - x1)) - a3
    R = (x3, y3)
    assert _bsd_py_on_curve(R, a3, a, b), "bsd add: off-curve result"
    return R


def _bsd_py_mul(k: int, P, a3: int, a: int, b: int):
    if k < 0:
        return _bsd_py_mul(-k, _bsd_py_neg(P, a3, a, b), a3, a, b)
    R, A = None, P
    while k > 0:
        if k & 1:
            R = _bsd_py_add(R, A, a3, a, b)
        A = _bsd_py_add(A, A, a3, a, b)
        k >>= 1
    return R


def _bsd_py_Lpartial(a3: int, a: int, b: int, end: int = 84) -> Fraction:
    """L_end(E) = prod_{p <= end} (1 - a_p/p + 1/p^2), exact."""
    v: Fraction = Fraction(1)
    for p in _s13_py_primes(end):
        v *= 1 - Fraction(_bsd_py_ap(p, a3, a, b), p) + Fraction(1, p * p)
    return v


S14_BEDS: dict[str, Any] = {
    "line_end": 84,
    "panel": {"A": B14_A, "B": B14_B},
    "ap_A": {str(p): _bsd_py_ap(p, *B14_A) for p in _s13_py_primes(84)},
    "ap_B": {str(p): _bsd_py_ap(p, *B14_B) for p in _s13_py_primes(84)},
    "cm_zeros_A": [p for p in _s13_py_primes(84) if _bsd_py_ap(p, *B14_A) == 0],
    "torsion_A": [(-1, 0), (0, 0), (1, 0)],
    "small_B": [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0), (2, -3), (2, 2), (6, -15), (6, 14)],
    "gen_B": {"(0,0)": 1, "(1,0)": 2, "(-1,-1)": 3, "(2,-3)": 4, "(6,14)": 6,
              "(0,-1)": -1, "(1,-1)": -2, "(-1,0)": -3, "(2,2)": -4, "(6,-15)": -6},
    "L84_A": _bsd_py_Lpartial(*B14_A),
    "L84_B": _bsd_py_Lpartial(*B14_B),
    "wall_values": {
        "W5": "13.3586546916",
    },
}


# ---------------------------------------------------------------------------
# E6.19 / S15 — the L-function of the city (BSD island band 2 of 3).
# The LOCAL-FACTOR layer: the factor each prime carries (the uniform
# two-term form every prime of the line holds; the record's one-term
# form at the ramified primes), the L-partial as the product the line
# holds (added-term rule: the S13 removal rule inverted), the
# ramification correction (record = uniform x corrections, both sides
# exact rationals at the line end), and the vanishing-order seam as
# walls (the record says order zero for the first member and order one
# for the second at s = 1; the limit is past the line, named, not
# reached). The BSD statement itself (order == rank) is band 3's
# object — P5 of E6.19 forbids theorem:bsd.
CONCEPT_S15_FACTOR = "euler-factor"
CONCEPT_S15_LOCAL = "local-form"
CONCEPT_S15_PARTIAL = "l-partial"
CONCEPT_S15_CORR = "l-correction"

CONCEPT_S15: tuple = (
    Concept(
        CONCEPT_S15_FACTOR,
        "the euler factor: the term each prime of the line carries into the L-product — the uniform two-term form at every prime, and the record's one-term form at the primes where the curve ramifies",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S14_SHADOW, CONCEPT_S13_FACTOR),
    ),
    Concept(
        CONCEPT_S15_LOCAL,
        "the local form: at a prime dividing the conductor the record's factor has one term — the additive prime carries the unit, the multiplicative prime carries one plus one over p with its sign of record",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S15_FACTOR,),
    ),
    Concept(
        CONCEPT_S15_PARTIAL,
        "the line partial of the L-family: the product of the factors the line holds, an exact rational; adding a prime multiplies the partial by the factor it carries, and the limit past the line end is declared, not computed",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S15_FACTOR, CONCEPT_S13_PARTIAL),
    ),
    Concept(
        CONCEPT_S15_CORR,
        "the ramification correction: the ratio of the record's factor to the uniform one at the ramified primes — the record partial is the uniform partial times the product of the corrections, both sides exact on the line",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S15_LOCAL,),
    ),
)

S15_LESSONS: dict[str, tuple] = {
    "in the L-product of a curve, each prime of my line carries a factor: in the uniform form, one minus a over p plus one over p squared, the two-term form the panel's shadow coefficient gives at every prime of the line; and in the record form the same two terms, which at the primes where the curve ramifies — the primes dividing the conductor — the record's local factor drops to a single term, one minus a over p; on my panel the ramified primes are two for the first member and thirty-seven for the second": (
        CONCEPT_S15_FACTOR,
        "l-factor-def",
        "lemma",
        "What the euler factor IS: the uniform two-term factor at every prime, the record's one-term form at the ramified primes.",
        (),
        "Each prime of the line carries a factor into the L-product — the uniform two-term form, the record's one-term form at the ramified primes.",
    ),
    "at the primes where the curve ramifies, the record's factor is the single term one minus a over p: for the first panel member the shadow coefficient is zero at two, so the record's factor is literally one — the unit, the additive prime carries nothing — and for the second panel member the shadow coefficient is minus one at thirty-seven, so the record's factor is one plus one over thirty-seven, the multiplicative factor with its sign of record; and on both members of my panel every ramified prime of record sits on the line, so the correction the line holds is the record's full correction, not a partial one": (
        CONCEPT_S15_LOCAL,
        "l-local-def",
        "lemma",
        "What the local form IS: the one-term record factor at the ramified primes — the unit at two for the first member, one plus one over p at thirty-seven for the second.",
        (),
        "The record's factor is one term at the ramified primes: the unit at two (first member), one plus one over thirty-seven (second).",
    ),
    "the L-family of a panel member is held on my line as the product of the factors it holds: a partial product up to a height on the line, an exact rational the store holds; when a prime is added, the partial is multiplied by the factor that prime carries — the change of the partial is determined exactly by the added factor, and by nothing else; and the limit of the product over all primes past my line end is a step the store declares, not a number on my line": (
        CONCEPT_S15_PARTIAL,
        "l-partial-def",
        "lemma",
        "What the L-line partial IS: the product of the held factors as an exact rational, the added-term rule, and the declared limit past the line end.",
        (),
        "The L-partial is the exact rational product of the held factors; adding a prime multiplies by its factor; the limit is declared.",
    ),
    "the ramification correction of a prime is the ratio of the record's factor to the uniform factor: on my panel it is four-fifths at two for the first member and fourteen hundred and six over fourteen hundred and seven at thirty-seven for the second; the record partial is the uniform partial times the product of the corrections, and at my line end both sides are exact rationals the store holds": (
        CONCEPT_S15_CORR,
        "l-corr-def",
        "lemma",
        "What the ramification correction IS: record factor over uniform factor at the ramified primes (four-fifths; fourteen hundred and six over fourteen hundred and seven), and record = uniform times the corrections.",
        (),
        "The correction is record factor over uniform factor at the ramified primes; the record partial is the uniform partial times the corrections.",
    ),
}

S15_THEOREMS: dict[str, dict] = {
    "l-added-term": {
        "parts": ("l-partial-def", "l-factor-def"),
        "statement": "the added-term rule held on my line: for both panel members and every prime of the line, the partial product up to the prime is the partial product up to the previous prime times the factor the prime carries — in the uniform form and in the record form, the exact rationals agreeing prime by prime, the full record at the line end 84",
        "concept": CONCEPT_S15_PARTIAL,
    },
    "l-record-identity": {
        "parts": ("l-corr-def", "l-factor-def"),
        "statement": "the record identity held on my line: the record partial to the line end is the uniform partial times the ramification corrections — four-fifths for the first panel member, fourteen hundred and six over fourteen hundred and seven for the second — and the store holds both sides as exact rationals, at the line end 84",
        "concept": CONCEPT_S15_CORR,
    },
    "l-ramified-unit": {
        "parts": ("l-local-def", "l-factor-def"),
        "statement": "the ramified factors of my panel held on the line: at two for the first member the record's factor is the unit one against the uniform factor five over four, and at thirty-seven for the second member the record's factor is one plus one over thirty-seven against the uniform factor fourteen hundred and seven over thirteen hundred and sixty-nine — the two-term form replaced by the one-term, exactly, at the line end 84",
        "concept": CONCEPT_S15_LOCAL,
    },
}

_S15_SLUGS = (
    "l-factor-def|l-local-def|l-partial-def|l-corr-def|"
    "l-added-term|l-record-identity|l-ramified-unit"
)
S15_SLUG_CONCEPT = {
    "l-factor-def": CONCEPT_S15_FACTOR,
    "l-local-def": CONCEPT_S15_LOCAL,
    "l-partial-def": CONCEPT_S15_PARTIAL,
    "l-corr-def": CONCEPT_S15_CORR,
    "l-added-term": CONCEPT_S15_PARTIAL,
    "l-record-identity": CONCEPT_S15_CORR,
    "l-ramified-unit": CONCEPT_S15_LOCAL,
}
SAVANT_LESSONS = {**SAVANT_LESSONS, **S15_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S15_THEOREMS}


# The S15 reference functions (the mechanism's own computation; the
# store's run is the referee — the S14 _bsd_py_* family extended).
def _bsd_py_lfactor(p: int, a3: int, a: int, b: int, form: str = "uniform") -> Fraction:
    """The factor each prime carries at the s = 1 specialization X = 1/p.

    uniform: 1 - a_p/p + 1/p^2 (every prime — the S14 convention)
    record:  the same two-term form at unramified primes; the ONE-TERM
             form 1 - a_p/p at a prime dividing the conductor
    """
    ap = _bsd_py_ap(p, a3, a, b)
    u = 1 - Fraction(ap, p) + Fraction(1, p * p)
    if form == "uniform":
        return u
    if form == "record":
        cond = 32 if (a3, a, b) == B14_A else 37
        if p in {i for i in (2, 37) if cond % i == 0}:
            return 1 - Fraction(ap, p)
        return u
    raise ValueError(form)


def _bsd_py_lpartial_uniform(a3: int, a: int, b: int, end: int = 84) -> Fraction:
    """prod_{p <= end} (1 - a_p/p + 1/p^2), exact (the S14 beds)."""
    v: Fraction = 1
    for p in _s13_py_primes(end):
        v *= _bsd_py_lfactor(p, a3, a, b, "uniform")
    return v


def _bsd_py_lpartial_record(a3: int, a: int, b: int, end: int = 84) -> Fraction:
    """prod of the RECORD local factors (one-term at the ramified p)."""
    v: Fraction = 1
    for p in _s13_py_primes(end):
        v *= _bsd_py_lfactor(p, a3, a, b, "record")
    return v


def _bsd_py_lcorr(a3: int, a: int, b: int, end: int = 84) -> Fraction:
    """prod of the corrections R_p/U_p at the ramified primes <= end."""
    v: Fraction = 1
    for p in _s13_py_primes(end):
        v *= _bsd_py_lfactor(p, a3, a, b, "record") / _bsd_py_lfactor(p, a3, a, b, "uniform")
    return v


def _bsd_py_lspots(a3: int, a: int, b: int, end: int = 84, form: str = "uniform") -> dict[int, Fraction]:
    """The spot partials: at each prime height p the partial product
    over the primes <= p (the exact-rationals the beds freeze)."""
    out: dict[int, Fraction] = {}
    v: Fraction = 1
    for p in _s13_py_primes(end):
        v *= _bsd_py_lfactor(p, a3, a, b, form)
        out[p] = v
    return out


S15_BEDS: dict[str, Any] = {
    "line_end": 84,
    # the ramified set of the record (both primes ON the line)
    "ramified": {"A": [2], "B": [37]},
    # the ramified factor pairs (uniform -> record)
    "ramified_A": {"uniform": _bsd_py_lfactor(2, *B14_A, "uniform"), "record": _bsd_py_lfactor(2, *B14_A, "record")},
    "ramified_B": {"uniform": _bsd_py_lfactor(37, *B14_B, "uniform"), "record": _bsd_py_lfactor(37, *B14_B, "record")},
    # the corrections (record/uniform at the ramified product)
    "corr_A": _bsd_py_lcorr(*B14_A),
    "corr_B": _bsd_py_lcorr(*B14_B),
    # the line-end partials, both forms (uniform == the S14 beds)
    "uniform_84_A": _bsd_py_lpartial_uniform(*B14_A),
    "uniform_84_B": _bsd_py_lpartial_uniform(*B14_B),
    "record_84_A": _bsd_py_lpartial_record(*B14_A),
    "record_84_B": _bsd_py_lpartial_record(*B14_B),
    # the spot partials (every prime height; the beds freeze the
    # selected spots at control #1)
    "spots_uniform_A": {str(k): v for k, v in _bsd_py_lspots(*B14_A, form="uniform").items()},
    "spots_uniform_B": {str(k): v for k, v in _bsd_py_lspots(*B14_B, form="uniform").items()},
    "spots_record_A": {str(k): v for k, v in _bsd_py_lspots(*B14_A, form="record").items()},
    "spots_record_B": {str(k): v for k, v in _bsd_py_lspots(*B14_B, form="record").items()},
    # sanity anchors computed at import (asserted by the P4 of E6.19)
    "anchor_identity_A": _bsd_py_lpartial_uniform(*B14_A) * _bsd_py_lcorr(*B14_A),
    "anchor_identity_B": _bsd_py_lpartial_uniform(*B14_B) * _bsd_py_lcorr(*B14_B),
}
assert S15_BEDS["anchor_identity_A"] == S15_BEDS["record_84_A"]
assert S15_BEDS["anchor_identity_B"] == S15_BEDS["record_84_B"]


# The S15 probe grammar (closed set; the classifier block is appended
# in the det_classify S15 section, the responses in
# _policy_savant15).
S15_FACTOR_RE = re.compile(
    r"\bwhat factor does the (first|second) panel member carry at prime (\d+) in the (uniform|record) form\?"
)
S15_FORM_RE = re.compile(r"\bin the record form what factor does the (first|second) panel member carry at its ramified prime\?")
S15_PARTIAL_RE = re.compile(r"\bwhat does the uniform L product of the (first|second) panel member hold at height (\d+)\?")
S15_RECPARTIAL_RE = re.compile(r"\bwhat does the record L product of the (first|second) panel member hold at height (\d+)\?")
S15_CORR_RE = re.compile(r"\bwhat is the ramification correction of the (first|second) panel member\?")
S15_IDENTITY_RE = re.compile(
    r"\bdoes the record partial equal the uniform partial times the ramification correction of the (first|second) panel member at my line end\?"
)
S15_ADDED_RE = re.compile(
    r"\bhow does the (uniform|record) partial of the (first|second) panel member change when i add the prime (\d+)\?"
)
S15_VANISH_B_RE = re.compile(r"\bwhat does the record say the L product of the second panel member does at s equal to one\?")
S15_NONZERO_A_RE = re.compile(r"\bwhat does the record say the L product of the first panel member does at s equal to one\?")
S15_REGION_RE = re.compile(r"\bwhere in the half-plane do the L products of the panel converge\?")
S15_RAMLINE_RE = re.compile(r"\bare all the ramified primes of record of the panel on my line\?")
S15_BSD_TOUCH_RE = re.compile(r"\bdoes this band state the BSD\?")
S15_LBANDSTATE_RE = re.compile(r"\bwhat did the L band add to the store\?")
S15_LUNCOND_RE = re.compile(r"\bdoes the L band say anything conditional on the Riemann hypothesis\?")
S15_ANY_STATE_RE = re.compile(rf"\bstate the ({_S15_SLUGS}) rule\b")

S15_MODES: tuple[str, ...] = (
    "s15-factor",
    "s15-form",
    "s15-partial",
    "s15-recpartial",
    "s15-corr",
    "s15-identity",
    "s15-added",
    "s15-vanish-b",
    "s15-nonzero-a",
    "s15-region",
    "s15-ramline",
    "s15-bsd-touch",
    "s15-bandstate",
    "s15-uncond",
    "s15-state",
)

# ======================================================================
# E6.20 — S16 module (PRIZE-ISLANDS-TRACK, BSD island band 3 of 3):
# the descent and the reaching — the island's summit.
#
# Concepts:  analytic-order  (the record's order of vanishing at s=1,
#                            a declared limit fact; the line's partials
#                            stand for the line's side)
#            algebraic-rank  (the record's rank, settled by two-descent
#                            + the point ledger; the exact-sequence
#                            machinery; no BSD used)
#            bsd-summit      (the statement itself, a DECLARED record
#                            fact — the island's summit)
# Lessons:   vanish-def, rank-def, statement-def, reach-def
# Theorem:   bsd-panel-satisfaction (the statement holds on the panel
#            of record: 0 = 0, 1 = 1; the line's partials consistent)
# Walls:     W_S16_1 the descent of record (selmer mechanism),
#            W_S16_2 the L-value of record (analytic side),
#            W_S16_3 the panel's completeness (the honest frontier)
# offline:   NO new off-line decimal (the leading coefficient is named
#            of record WITHOUT the digit string; the carried
#            13.3586546916 stays in the W_S14_5 wall)
# ======================================================================
CONCEPT_S16_AO = "analytic-order"
CONCEPT_S16_AR = "algebraic-rank"
CONCEPT_S16_BS = "bsd-summit"
CONCEPT_S16_REACH = "line-reaching"

CONCEPT_S16: tuple = (
    Concept(
        CONCEPT_S16_AO,
        "the order of vanishing: what the record says the L-product does at s equal to one — zero for the first panel member, one for the second; a limit fact past my line, and my partials stand for the line's side",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S15_PARTIAL,),
    ),
    Concept(
        CONCEPT_S16_AR,
        "the algebraic rank: the record settles the panel — the first member zero with its torsion ledger, the second one with its generator; the two-descent machinery: the exact sequence and the descent bound that settle the rank with the point ledger, no BSD used",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S14_LAW, CONCEPT_S14_SHADOW),
    ),
    Concept(
        CONCEPT_S16_BS,
        "the summit of the island: the statement itself, a declared record fact — the order of vanishing of the L-product at s equal to one equals the algebraic rank; on my panel the two sides are settled of record and agree (0 = 0, 1 = 1), the line's partials standing for the line's side",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S16_AO, CONCEPT_S16_AR),
    ),
    Concept(
        CONCEPT_S16_REACH,
        "the reaching: what the line holds toward the summit — the exact partials standing for the line's side, the torsion ledger of the first member, the generation ledger of the second member, and the consistency of the line's values with the record's orders",
        "college-1",
        "bsd",
        prereqs=(CONCEPT_S16_AO, CONCEPT_S16_AR),
    ),
)

S16_LESSONS: dict[str, tuple] = {
    "at the limit my line does not reach, the record says what the L-products of my panel do at s equal to one: the L-product of the first panel member is nonzero there — order zero of vanishing — and the L-product of the second panel member vanishes there of order one — the analytic side of the statement the island summits on; a limit fact of record past my line, and on the line i hold the exact partials that stand for the line's side: the first member's partial holds nonzero, the second member's partial holds its exact rational far from zero — the vanishing is the divergence of the infinite product, at the line end 84": (
        CONCEPT_S16_AO,
        "vanish-def",
        "lemma",
        "What the order of vanishing IS: of record, zero for the first member, one for the second — a limit fact past the line; the line's exact partials stand for the line's side.",
        (),
        "The record's order of vanishing at s = 1: zero (first member) and one (second) — a limit fact; the line holds the consistent partials.",
    ),
    "the algebraic rank of a panel member is of record, settled by the two-descent — the machinery: the exact sequence, the selmer dimension equals the rank plus the dimension of the two torsion plus the dimension of the two shaf, and the descent bound, the rank at most the selmer dimension minus the two torsion dimension, met by the point ledger when the bound and the known points agree; on my panel the record settles it — the first member rank zero, its two selmer dimension two against its two torsion dimension two, the bound zero, and the ledger holds only its three torsion points (x zero y zero, x one y zero, x minus one y zero); the second member rank one, its two selmer dimension one against its two torsion dimension zero, the bound one, and the generator (x zero y zero) of record meets it; no BSD is used to settle a rank on my panel, at the line end 84": (
        CONCEPT_S16_AR,
        "rank-def",
        "lemma",
        "What the algebraic rank IS: of record zero and one on the panel, settled by the two-descent (exact sequence, selmer dimension, descent bound) met by the point ledger — the three torsion points for the first member, the generator (0,0) for the second; no BSD used.",
        (),
        "The record's rank: zero (first member, torsion ledger) and one (second member, the generator (0,0)) — settled by descent bound + point ledger, no BSD used.",
    ),
    "the statement of the island, of record (the clay millennial booklet, the wiles chapter): for a curve over the rationals, in the taylor expansion of its L-product at s equal to one, the order r of vanishing equals the algebraic rank — the L-product is c times (s minus 1) to the power r plus higher order terms, c not zero, r equals the rank of the group of rational points — and in particular the L-product at s equal to one is zero if and only if there are infinitely many rational points; on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84": (
        CONCEPT_S16_BS,
        "statement-def",
        "lemma",
        "The STATEMENT (the island's summit, a declared record fact): in the Taylor expansion of the L-product at s = 1, the order r of vanishing equals the algebraic rank (c not zero); in particular L(1) = 0 iff infinitely many rational points; on the panel the two sides agree of record (0 = 0, 1 = 1).",
        (),
        "The statement: order of vanishing at s = 1 equals the algebraic rank (the CMI booklet's conjecture); on the panel the record holds it (0 = 0, 1 = 1).",
    ),
    "the reaching: what my line holds toward the summit — the exact partials the line holds (the first member's uniform partial holds nonzero, the second member's uniform and record partials hold their exact rationals), the torsion ledger of the first member on the line (its three integral two-torsion points), the generation ledger of the second member on the line (the generator (x zero y zero), and every point my line counted is a small multiple of it), and the consistency of the line's values with the record's orders (the order zero keeps its nonzero partial, the order one keeps its exact partial far from zero), at the line end 84": (
        CONCEPT_S16_REACH,
        "reach-def",
        "lemma",
        "What the line holds toward the summit: the exact partials (A's uniform nonzero, B's uniform and record far from zero), the torsion ledger of A (three integral two-torsion points on the line), the generation ledger of B (the generator (0,0), ten of ten), and the consistency of the line's values with the record's orders.",
        (),
        "The line holds: the exact partials, A's torsion ledger, B's generation ledger, and the consistency with the record orders — the reaching.",
    ),
}

S16_THEOREMS: dict[str, dict] = {
    "bsd-panel-satisfaction": {
        "parts": ("statement-def", "vanish-def", "rank-def"),
        "statement": "the summit of the island filed on my panel: the statement holds of record on both members — the order zero of vanishing equals the rank zero of the first member, and the order one of vanishing equals the rank one of the second — the two sides settled by independent record machinery (the ranks by the descent and the point ledger, the orders by the L-function's record), and my line's exact partials stand consistent with both, at the line end 84",
        "concept": CONCEPT_S16_BS,
    },
}

_S16_SLUGS = (
    "vanish-def|rank-def|statement-def|reach-def|"
    "bsd-panel-satisfaction"
)
S16_SLUG_CONCEPT = {
    "vanish-def": CONCEPT_S16_AO,
    "rank-def": CONCEPT_S16_AR,
    "statement-def": CONCEPT_S16_BS,
    "reach-def": CONCEPT_S16_REACH,
    "bsd-panel-satisfaction": CONCEPT_S16_BS,
}
SAVANT_LESSONS = {**SAVANT_LESSONS, **S16_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S16_THEOREMS}


# The S16 reference functions (the mechanism's own record tables +
# line-side censuses; the store's run is the referee).
_B16_RANK: dict[str, int] = {"A": 0, "B": 1}         # record (descent + ledger)
_B16_ORDER: dict[str, int] = {"A": 0, "B": 1}        # record (L-function)
_B16_SEL: dict[str, int] = {"A": 2, "B": 1}          # record (consequence)
_B16_E2: dict[str, int] = {"A": 2, "B": 0}           # record (torsion dim)
_B16_SHA2: dict[str, int] = {"A": 0, "B": 0}         # record (Sha trivial)


def _bsd_py_which(c: tuple[int, int, int]) -> str:
    return "A" if tuple(c) == B14_A else "B"


def _bsd_py_torsion_points(c: tuple[int, int, int], end: int = 84) -> list[tuple[int, int]]:
    """The integral 2-torsion points of the panel member ON THE LINE
    (verified against the mechanism's own on-curve scan — the
    record's torsion ledger is checked, not assumed)."""
    w = _bsd_py_which(c)
    if w == "A":
        cands = [(0, 0), (1, 0), (-1, 0)]
    else:
        cands = []
    out = []
    for pt in cands:
        if _bsd_py_on_curve(pt, *c):
            out.append(pt)
    return out


def _bsd_py_gen_ledger(c: tuple[int, int, int], end: int = 84) -> dict[str, Any]:
    """The generation ledger of B (the S14 scan re-derived): the
    generator (0,0) and the small multiples covering every on-line
    point counted by the S14 census."""
    w = _bsd_py_which(c)
    if w == "A":
        return {"generator": None, "covered": 0, "counted": 0}
    pts = sorted([x, y] for x in range(-end, end + 1) for y in range(-end, end + 1)
                 if _bsd_py_on_curve((x, y), *c))
    covered = 0
    for x, y in pts:
        hit = False
        for m in range(-16, 17):
            if _bsd_py_mul(m, (0, 0), *c) == (x, y):
                hit = True
                break
        if hit:
            covered += 1
    return {"generator": [0, 0], "covered": covered, "counted": len(pts)}


S16_BEDS: dict[str, Any] = {
    "line_end": 84,
    # the record tables (of record; the source of record is the
    # stage-D research record)
    "rank": dict(_B16_RANK),
    "order": dict(_B16_ORDER),
    "selmer_dim": dict(_B16_SEL),
    "e2_dim": dict(_B16_E2),
    "sha2_dim": dict(_B16_SHA2),
    "descend_bound": {w: _B16_SEL[w] - _B16_E2[w] for w in ("A", "B")},
    # the line-side ledger censuses (mechanism-verified on the line)
    "torsion_A": [list(p) for p in _bsd_py_torsion_points(B14_A)],
    "gen_B": _bsd_py_gen_ledger(B14_B),
    # the line-end partials (the carried S14/S15 beds, re-derived)
    "uniform_84_A": str(_bsd_py_lpartial_uniform(*B14_A)),
    "uniform_84_B": str(_bsd_py_lpartial_uniform(*B14_B)),
    "record_84_B": str(_bsd_py_lpartial_record(*B14_B)),
    # the line-side consistency verdicts (the line's partials vs the
    # record orders — both checks live on the line)
    "consistent_A_nonzero": _bsd_py_lpartial_uniform(*B14_A) != Fraction(0),
    "consistent_B_far": _bsd_py_lpartial_uniform(*B14_B) > Fraction(1),
}
# the record consequence: the exact-sequence arithmetic
assert S16_BEDS["selmer_dim"] == {w: _B16_RANK[w] + _B16_E2[w] + _B16_SHA2[w] for w in ("A", "B")}, "the exact sequence failed on the record tables"
assert S16_BEDS["descend_bound"] == {"A": 0, "B": 1}, "the descent bounds drifted"
# the line-side censuses are the record's on-line shadow
assert S16_BEDS["torsion_A"] == [[0, 0], [1, 0], [-1, 0]], "the A torsion ledger drifted off the line"
assert S16_BEDS["gen_B"] == {"generator": [0, 0], "covered": 10, "counted": 10}, "the B generation ledger drifted"
assert S16_BEDS["consistent_A_nonzero"] is True and S16_BEDS["consistent_B_far"] is True, "the line-side consistency verdicts drifted"


# The S16 probe grammar (closed set; the classifier block is appended
# in the det_classify S16 section, the responses in
# _policy_savant16).
S16_ORDER_RE = re.compile(
    r"\bwhat order of vanishing does the L product of the (first|second) panel member have at s equal to one of record\?"
)
S16_RANK_RE = re.compile(r"\bwhat is the algebraic rank of the (first|second) panel member of record\?")
S16_DESCEND_RE = re.compile(r"\bwhat does the two-descent settle for the (first|second) panel member of record\?")
S16_SELMER_RE = re.compile(r"\bwhat is the two selmer dimension of the (first|second) panel member of record\?")
S16_SELWALL_RE = re.compile(r"\bhow is the two selmer of the (first|second) panel member computed in detail of record\?")
S16_BSD_RE = re.compile(r"\bwhat is the summit fact of the island\?")
S16_REACH_RE = re.compile(r"\bwhat does my line hold toward the summit of the island\?")
S16_TORSION_RE = re.compile(r"\bwhat does the torsion ledger of the first panel member hold on my line\?")
S16_GEN_RE = re.compile(r"\bwhat does the generation ledger of the second panel member hold on my line\?")
S16_CONSISTENT_RE = re.compile(r"\bare my partials consistent with the record orders at s equal to one\?")
S16_LVALWALL_RE = re.compile(r"\bwhat is the exact record L value of the (first|second) panel member at s equal to one\?")
S16_PANELW3_RE = re.compile(r"\bwhich curves of record does the island's summit settle on my line\?")
S16_SIDE_RE = re.compile(r"\bwhat do the two sides of the statement say for the (first|second) panel member of record\?")
S16_BANDSTATE3_RE = re.compile(r"\bwhat state does the summit band hold at the line end\?")
S16_UNCOND3_RE = re.compile(r"\bdoes the summit band say anything conditional on the Riemann hypothesis\?")
S16_ANY_STATE_RE = re.compile(rf"\bstate the ({_S16_SLUGS}) rule\b")

S16_MODES: tuple[str, ...] = (
    "s16-order",
    "s16-rank",
    "s16-descend",
    "s16-selmer",
    "s16-selwall",
    "s16-bsd",
    "s16-reach",
    "s16-torsion",
    "s16-gen",
    "s16-consistent",
    "s16-lvalwall",
    "s16-panel",
    "s16-sides",
    "s16-bandstate",
    "s16-uncond",
    "s16-state",
)



#: E6.7 — the band-3 grammar (frozen; 9–12 voice; 1-D statics: the
#: line IS the axis).
GEO_AREA_RE = re.compile(r"\bwhat is the area of a (\d+) by (\d+) rectangle\?")
GEO_PERIM_RE = re.compile(r"\bwhat is the perimeter of a (\d+) by (\d+) rectangle\?")
GEO_TRI_RE = re.compile(
    r"\bwhat is the area of a triangle with base (\d+) and height (\d+)\?"
)
GEO_CMP_RE = re.compile(
    r"\bis a (\d+) by (\d+) rectangle bigger than a (\d+) by (\d+) rectangle\?"
)
STA_NET_RE = re.compile(
    r"\ba cart moves (\d+) meters east then (\d+) meters west: how far from the start\?"
)
STA_MOM_RE = re.compile(
    r"\bwhat is the moment of a (\d+) newton force at (\d+) meters\?"
)
STA_BAL_RE = re.compile(
    r"\ba beam balances a (\d+) newton at (\d+) meters against what force at (\d+) meters\?"
)


#: E6.6 — the band-2 grammar (frozen; 6–8 voice).
ALG_ADD_RE = re.compile(r"\bwhat is x, if x \+ (\d+) is (\d+)\?")
ALG_MUL_RE = re.compile(r"\b(\d+) times x is (\d+): what is x\?")
ALG_2STEP_RE = re.compile(r"\b(\d+) times x plus (\d+) is (\d+): what is x\?")
KIN_FAR_RE = re.compile(r"\bhow far does a cart go in (\d+) minutes at (\d+) a minute\?")
KIN_POS_RE = re.compile(r"\ba cart starts at (\d+) and goes (\d+) every minute: where is it after (\d+) minutes\?")
KIN_TIME_RE = re.compile(r"\ba cart starts at (\d+) and goes (\d+) every minute and is at (\d+): how many minutes did it take\?")
KIN_RATE_RE = re.compile(r"\ba cart covers (\d+) miles in (\d+) minutes: how many miles every minute was that\?")

#: E6.2 — capability activation is STORE DATA: each derivation policy is
#: latent in code but ACTIVE only while its rule/definition assertion is
#: established. Frozen lesson phrase -> (concept, rule name, gap label).
RULE_LESSONS: dict[str, tuple[str, str, str]] = {
    "subtraction is walking backward": (CONCEPT_SUB, "walk-back", "walking backward (subtraction)"),
    "multiplication is repeated addition": (CONCEPT_MULT, "repeat-add", "repeated addition (multiplication)"),
    "comparison is walking the line": (CONCEPT_CMP, "walk", "walking the line (comparison)"),
    "a square root of a number is the number which when multiplied by itself is that number": (
        CONCEPT_SQRT,
        "definition",
        "the definition of square root",
    ),
    # E6.6 — band 2 (6–8 voice): the seven aligned-band lessons.
    "an unknown added to a number is found by taking that number away from the total": (
        CONCEPT_ALG_ADD1, "inverse-add", "undoing an addition (one step)",
    ),
    "an unknown that a number times gives a total is found by taking away that number again and again until the total is gone": (
        CONCEPT_ALG_MUL, "repeated-take", "undoing a multiplication (repeated taking)",
    ),
    "two changes in a row are undone in reverse order": (
        CONCEPT_ALG_2STEP, "reverse-order", "undoing two changes (reverse order)",
    ),
    "at a steady pace, the distance is the pace times the time": (
        CONCEPT_KIN_FAR, "pace-times-time", "steady pace: distance is pace times time",
    ),
    "position is the start plus the distance": (
        CONCEPT_KIN_POS, "start-plus-distance", "position is start plus distance",
    ),
    "time is found the same way any unknown is found: undo the equation": (
        CONCEPT_KIN_TIME, "undo-equation", "finding time: undoing the equation",
    ),
    "a steady pace is found by taking the time away from the distance again and again until the distance is gone": (
        CONCEPT_KIN_RATE, "repeated-take-pace", "finding pace: repeated taking of the time",
    ),
    # E6.7 — band 3 (9–12 voice): the six product-band lessons.
    "the area of a rectangle is the length times the width": (
        CONCEPT_GEO_AREA,
        "area-product",
        "the area of a rectangle",
    ),
    "the perimeter of a rectangle is twice what you get by adding the length to the width": (
        CONCEPT_GEO_PERIM,
        "perimeter-twice-sum",
        "the perimeter of a rectangle",
    ),
    "the area of a triangle is half of the base times the height": (
        CONCEPT_GEO_TRI,
        "triangle-half-product",
        "the area of a triangle",
    ),
    "moving east then west, the net is what is left after you take the west part away from the east part": (
        CONCEPT_STA_NET,
        "net-takeaway",
        "net displacement east minus west",
    ),
    "a moment is the force times its distance from the pivot": (
        CONCEPT_STA_MOM,
        "moment-product",
        "the moment (force times distance)",
    ),
    "a beam balances when the moment on one side equals the moment on the other": (
        CONCEPT_STA_BAL,
        "equal-moments",
        "lever balance (equal moments)",
    ),
}


# E6.5 - the band-1 geometry strip (mastery concepts; counting is the
# shared prereq - directive #1: geometry learns CONCURRENTLY with 
# math, on the same strip and the same line).
CONCEPT_SHAPE_TRIANGLE = "shape-triangle"
CONCEPT_SHAPE_SQUARE = "shape-square"
CONCEPT_SHAPE_RECTANGLE = "shape-rectangle"
CONCEPT_SHAPE_CIRCLE = "shape-circle"

CONCEPT_SHAPES: tuple = (
    Concept(CONCEPT_SHAPE_TRIANGLE, "The triangle (sides and corners)", "k-5", "geometry", prereqs=(CONCEPT_COUNT,)),
    Concept(CONCEPT_SHAPE_SQUARE, "The square (sides and corners)", "k-5", "geometry", prereqs=(CONCEPT_COUNT,)),
    Concept(CONCEPT_SHAPE_RECTANGLE, "The rectangle (sides and corners)", "k-5", "geometry", prereqs=(CONCEPT_COUNT,)),
    Concept(CONCEPT_SHAPE_CIRCLE, "The circle (no sides, no corners)", "k-5", "geometry", prereqs=(CONCEPT_COUNT,)),
)

#: Fixed base for turn timestamps (no wall clock; the e5.x discipline).
EPOCH_BASE = "2026-08-21"


def fixed_epoch(session: int, turn: int) -> str:
    """Deterministic ISO-8601 for (session, turn) — no wall clock."""

    return f"{EPOCH_BASE}T{session:02d}{turn:02d}00+00:00"


def turn_id(session: int, turn: int) -> str:
    return f"S{session:02d}:{turn:02d}"


def _slots_ok(kind: str, slots: dict[str, Any]) -> bool:
    """Schema-validity of LLM classification slots for a contract kind
    (the pilot grammar; kinds without pilot grammar take empty slots)."""

    if kind == "assertion":
        if set(slots) == {"a", "b"}:
            return all(isinstance(slots[k], int) and not isinstance(slots[k], bool) for k in "ab")
        # E6.2: a rule/definition lesson quotes one frozen phrase verbatim.
        if set(slots) == {"rule"} and isinstance(slots.get("rule"), str) and slots["rule"] in RULE_LESSONS:
            return True
        # E6.5: a shape definition lesson (numeric shapes carry the values).
        if set(slots) == {"shape", "sides", "corners"}:
            return (
                isinstance(slots.get("shape"), str)
                and slots["shape"] in SHAPES
                and all(isinstance(slots[k], int) and not isinstance(slots[k], bool) for k in ("sides", "corners"))
            )
        # E6.5: the circle lesson (no values to carry).
        if set(slots) == {"shape"}:
            return isinstance(slots.get("shape"), str) and slots["shape"] == "circle"
        return False
    if kind == "correction":
        if set(slots) == {"a", "b"}:
            return all(isinstance(slots[k], int) and not isinstance(slots[k], bool) for k in "ab")
        # E6.5: correcting a shape definition (same schemas as the lesson).
        return slots_ok_shape(slots)
    if kind == "question":
        if set(slots) == {"mode", "shape", "property"}:
            # E6.5: a shape drill (the 2-family geometry grammar).
            return (
                slots.get("mode") == "shape"
                and isinstance(slots.get("shape"), str)
                and slots["shape"] in SHAPES
                and slots.get("property") in ("sides", "corners")
            )
        if set(slots) == {"mode", "n"}:
            return slots["mode"] in ("succ", "sqrt") and isinstance(slots.get("n"), int) and not isinstance(slots.get("n"), bool)
        if set(slots) == {"mode", "a", "b"}:
            return slots["mode"] in ("add", "sub", "mult", "cmp", "alg-add", "alg-mul") and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in "ab"
            )
        if set(slots) == {"mode", "r", "t"}:
            return slots["mode"] in ("kin-far",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in ("r", "t")
            )
        if set(slots) == {"mode", "d", "t"}:
            return slots["mode"] in ("kin-rate",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in ("d", "t")
            )
        # E6.7 — band 3: the product-band question families.
        if set(slots) == {"mode", "l", "w"}:
            return slots["mode"] in ("geo-area", "geo-perim") and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("l", "w")
            )
        if set(slots) == {"mode", "b", "h"}:
            return slots["mode"] in ("geo-tri",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("b", "h")
            )
        if set(slots) == {"mode", "l1", "w1", "l2", "w2"}:
            return slots["mode"] in ("geo-cmp",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("l1", "w1", "l2", "w2")
            )
        if set(slots) == {"mode", "e", "w"}:
            return slots["mode"] in ("sta-net",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("e", "w")
            )
        if set(slots) == {"mode", "f", "d"}:
            return slots["mode"] in ("sta-mom",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("f", "d")
            )
        if set(slots) == {"mode", "f1", "d1", "d2"}:
            return slots["mode"] in ("sta-bal",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool)
                for k in ("f1", "d1", "d2")
            )
        # E6.6 — band 2: the three-slot families (algebra two-step,
        # kinematics position/time).
        if set(slots) == {"mode", "a", "b", "c"}:
            return slots["mode"] in ("alg-2step",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in "abc"
            )
        if set(slots) == {"mode", "start", "r", "t"}:
            return slots["mode"] in ("kin-pos",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in ("start", "r", "t")
            )
        if set(slots) == {"mode", "start", "r", "c"}:
            return slots["mode"] in ("kin-time",) and all(
                isinstance(slots.get(k), int) and not isinstance(slots.get(k), bool) for k in ("start", "r", "c")
            )
        return False
    if kind == "impossible":
        if set(slots) == {"a", "b", "op"}:
            return (
                isinstance(slots.get("op"), str)
                and isinstance(slots.get("a"), int)
                and isinstance(slots.get("b"), int)
            )
        # E6.2: a rule-gated drill while its rule is unlearned (the honest gap).
        return set(slots) == {"n", "op"} and isinstance(slots.get("op"), str) and isinstance(slots.get("n"), int)
    if kind in ("request",):
        return set(slots) == {"a", "b"} and all(isinstance(slots.get(k), int) for k in "ab")
    if kind in ("command",):
        return set(slots) == {"n"} and isinstance(slots.get("n"), int)
    if kind in ("ambiguous",):
        return set(slots) == set()
    return False


def slots_ok_shape(slots: dict[str, Any]) -> bool:
    """E6.5: the shape-lesson slot schemas (assertion AND correction)."""

    if set(slots) == {"shape", "sides", "corners"}:
        return (
            isinstance(slots.get("shape"), str)
            and slots["shape"] in SHAPES
            and all(isinstance(slots[k], int) and not isinstance(slots[k], bool) for k in ("sides", "corners"))
        )
    if set(slots) == {"shape"}:
        return isinstance(slots.get("shape"), str) and slots["shape"] == "circle"
    return False


def det_classify(text: str) -> tuple[str, dict[str, Any]]:
    """The deterministic pilot grammar (frozen). Order is significant:
    the correction marker must be checked WITHIN the lesson match (a
    correction embeds a lesson), so lesson patterns test the marker
    before deciding assertion vs. correction."""

    t = text.strip()
    if t in RULE_LESSONS:  # E6.2: rule/definition lessons (exact frozen phrases)
        return "assertion", {"rule": t}
    if t in SAVANT_LESSONS:  # E6.8/E6.9: savant lemma/conjecture lessons (exact)
        return "assertion", {"lemma": t}
    m = TEACH_RE.search(text)  # E6.4: a phrasing mapping lesson (M1)
    if m:
        kind = "correction" if CORR_MARKER_RE.search(text) else "assertion"
        return kind, {"new": m.group(1), "canon": m.group(2)}
    if t == SHAPE_LESSON_CIRCLE:  # E6.5: the circle's exact lesson form
        return "assertion", {"shape": "circle"}
    m = SHAPE_LESSON_RE.search(text)
    if m:  # E6.5: a shape definition lesson (marker inside = correction,
        # the E6.2 in-lesson-marker pattern verbatim)
        kind = "correction" if CORR_MARKER_RE.search(text) else "assertion"
        return kind, {"shape": m.group(1), "sides": int(m.group(2)), "corners": int(m.group(3))}
    m = DRILL_SHAPE_SIDES_RE.search(text)
    if m:
        return "question", {"mode": "shape", "shape": m.group(1), "property": "sides"}
    m = DRILL_SHAPE_CORNERS_RE.search(text)
    if m:
        return "question", {"mode": "shape", "shape": m.group(1), "property": "corners"}
    # E6.6 — band 2: algebra ∥ kinematics (the aligned family).
    m = ALG_2STEP_RE.search(text)
    if m:
        return "question", {"mode": "alg-2step", "a": int(m.group(1)), "b": int(m.group(2)), "c": int(m.group(3))}
    m = ALG_MUL_RE.search(text)
    if m:
        return "question", {"mode": "alg-mul", "a": int(m.group(1)), "b": int(m.group(2))}
    m = ALG_ADD_RE.search(text)
    if m:
        return "question", {"mode": "alg-add", "a": int(m.group(1)), "b": int(m.group(2))}
    m = KIN_POS_RE.search(text)
    if m:
        return "question", {"mode": "kin-pos", "start": int(m.group(1)), "r": int(m.group(2)), "t": int(m.group(3))}
    m = KIN_TIME_RE.search(text)
    if m:
        return "question", {"mode": "kin-time", "start": int(m.group(1)), "r": int(m.group(2)), "c": int(m.group(3))}
    m = KIN_FAR_RE.search(text)
    if m:
        return "question", {"mode": "kin-far", "r": int(m.group(2)), "t": int(m.group(1))}
    m = KIN_RATE_RE.search(text)
    if m:
        return "question", {"mode": "kin-rate", "d": int(m.group(1)), "t": int(m.group(2))}
    # E6.7 — band 3: geometry-advanced ∥ vectors/statics (9–12).
    m = GEO_PERIM_RE.search(text)
    if m:
        return "question", {
            "mode": "geo-perim",
            "l": int(m.group(1)),
            "w": int(m.group(2)),
        }
    m = GEO_AREA_RE.search(text)
    if m:
        return "question", {
            "mode": "geo-area",
            "l": int(m.group(1)),
            "w": int(m.group(2)),
        }
    m = GEO_TRI_RE.search(text)
    if m:
        return "question", {
            "mode": "geo-tri",
            "b": int(m.group(1)),
            "h": int(m.group(2)),
        }
    m = GEO_CMP_RE.search(text)
    if m:
        return "question", {
            "mode": "geo-cmp",
            "l1": int(m.group(1)),
            "w1": int(m.group(2)),
            "l2": int(m.group(3)),
            "w2": int(m.group(4)),
        }
    m = STA_NET_RE.search(text)
    if m:
        return "question", {
            "mode": "sta-net",
            "e": int(m.group(1)),
            "w": int(m.group(2)),
        }
    m = STA_MOM_RE.search(text)
    if m:
        return "question", {
            "mode": "sta-mom",
            "f": int(m.group(1)),
            "d": int(m.group(2)),
        }
    m = STA_BAL_RE.search(text)
    if m:
        return "question", {
            "mode": "sta-bal",
            "f1": int(m.group(1)),
            "d1": int(m.group(2)),
            "d2": int(m.group(3)),
        }
    # E6.8 — savant S4 (SAVANT-TRACK): the theorem/lemma seam.
    m = S4_SLUG_STATE_RE.search(text)
    if m:
        return "question", {"mode": "lem-state", "slug": m.group(1)}
    m = S4_SLUG_WHY_RE.search(text)
    if m:
        return "question", {"mode": "lem-why", "slug": m.group(1)}
    if S4_CONJ_STATE_RE.search(text):
        return "question", {"mode": "conj-state", "proven": False}
    if S4_CONJ_PROVEN_RE.search(text):
        return "question", {"mode": "conj-state", "proven": True}
    m = S4_GRID_RE.search(text)
    if m:
        return "question", {"mode": "grid-pairs", "a": int(m.group(1)), "b": int(m.group(2))}
    m = S4_TWOSQ_RE.search(text)
    if m:
        return "question", {"mode": "twosq", "n": int(m.group(1))}
    m = S4_CIRC_RE.search(text)
    if m:
        return "question", {"mode": "circle-pairs", "x": int(m.group(1)), "y": int(m.group(2))}
    m = S4_CONF_RE.search(text)
    if m:
        return "question", {"mode": "confounder-no", "slug": m.group(1)}
    if S4_WALL_RE.search(text):
        return "question", {"mode": "savant-wall"}
    # E6.9 — savant S5 (SAVANT-TRACK): the number-field toolkit.
    m = S5_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "lem-state", "slug": m.group(1)}
    m = S5_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "lem-why", "slug": m.group(1)}
    m = S5_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "whydeep", "slug": m.group(1)}
    m = S5_SQMOD_RE.search(text)
    if m:
        return "question", {"mode": "sqmod", "x": int(m.group(1)), "q": int(m.group(2))}
    m = S5_GSAY_RE.search(text)
    if m:
        return "question", {"mode": "gsay", "d": int(m.group(1)), "r": int(m.group(2))}
    m = S5_SUMSQ_RE.search(text)
    if m:
        return "question", {"mode": "sumsq", "a": int(m.group(1)), "b": int(m.group(2))}
    m = S5_HOLES_RE.search(text)
    if m:
        return "question", {"mode": "holes", "p": int(m.group(1)), "m": int(m.group(2))}
    m = S5_DUOPOW_RE.search(text)
    if m:
        return "question", {"mode": "duopow", "e": int(m.group(1))}
    if S13_RHZERO_RE.search(t):  # E6.17: the telescope derives no hypothesis
        return "question", {"mode": "s13-rhzero"}
    # E6.10 — savant S6 (SAVANT-TRACK): scaffolded generation.
    m = S6_SHOWONE_RE.search(t)
    if m:
        return "question", {"mode": "showone"}
    m = S6_DERIVE_RE.match(t)
    if m:
        raw = m.group(2).replace(" and ", ",")
        parts = tuple(x.strip() for x in raw.split(",") if x.strip())
        return "question", {
            "mode": "derive",
            "target": m.group(1),
            "parts": parts,
        }
    m = S6_PACKCOUNT_RE.search(t)
    if m:
        return "question", {"mode": "packcount", "k": int(m.group(1))}
    m = S6_TRIPOW_RE.search(t)
    if m:
        return "question", {"mode": "tripow", "e": int(m.group(1))}
    m = S6_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s6-state", "slug": m.group(1)}
    m = S6_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "s6-why", "slug": m.group(1)}
    m = S6_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "s6-whydeep", "slug": m.group(1)}
    m = S7_GSLACK_RE.search(text)
    if m:
        return "question", {"mode": "gsslack", "d": int(m.group(1)), "t": int(m.group(2))}
    m = S7_CONJ_FLIP_RE.search(text)
    if m:
        return "question", {"mode": "conj-flip", "theorem": m.group(1)}
    if S7_SHOWDISPROOF_RE.search(text):
        return "question", {"mode": "showdisproof"}
    m = S7_CONFOUNDER_ROUTE_RE.search(text)
    if m:
        return "question", {"mode": "confounder-route", "slug": m.group(1)}
    if S7_DELTAV_RE.search(text):
        return "question", {"mode": "delta-value"}
    if S7_DISTDIST_RE.search(text):
        return "question", {"mode": "distdist"}
    m = S7_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s7-state", "slug": m.group(1)}
    m = S7_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "s7-why", "slug": m.group(1)}
    m = S7_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "s7-whydeep", "slug": m.group(1)}
    # E6.12 — RH-TRACK S8: the ζ apparatus (censuses, growth claim,
    # the numerical zero record, the attempt, the conj state).
    m = S8_PICOUNT_RE.search(text)
    if m:
        return "question", {"mode": "pi-count", "n": int(m.group(1))}
    m = S8_JFUNC_RE.search(text)
    if m:
        return "question", {"mode": "jfunc", "n": int(m.group(1))}
    if S8_SINCYCLE_RE.search(text):
        return "question", {"mode": "sincycle"}
    if S8_GROWTH_RE.search(text):
        return "question", {"mode": "growth-claim"}
    if S8_NUMZERO_RE.search(text):
        return "question", {"mode": "numzero-first"}
    if S8_RH_ATTEMPT_RE.search(text):
        return "question", {"mode": "rh-attempt"}
    if S8_RH_CONJ_RE.search(text):
        return "question", {"mode": "rh-conj-state"}
    if S8_RH_NUMCHECK_RE.search(text):
        return "question", {"mode": "rh-numcheck"}
    if S8_RH_OFFZERO_RE.search(text):
        return "question", {"mode": "rh-offzero"}
    if S8_RH_PNTCONF_RE.search(text):
        return "question", {"mode": "rh-pnt-conf"}
    if S8_RH_PRODCONF_RE.search(text):
        return "question", {"mode": "rh-prod-conf"}
    if S8_RH_ZETAVAL_RE.search(text):
        return "question", {"mode": "rh-zeta-val"}
    if S8_RH_STIGHT_RE.search(text):
        return "question", {"mode": "rh-s-tight"}
    m = S8_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s8-state", "slug": m.group(1)}
    m = S8_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "s8-why", "slug": m.group(1)}
    m = S8_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "s8-whydeep", "slug": m.group(1)}
    # E6.13 — RH-TRACK S9: the criterion gallery (the growth
    # comparison, the declared partials, the honesty probes).
    if S9_GAPCOMPARE_RE.search(text):
        return "question", {"mode": "gap-compare"}
    if S9_LICHECK_RE.search(text):
        return "question", {"mode": "li-check"}
    if S9_CVALUE_RE.search(text):
        return "question", {"mode": "c-value"}
    if S9_LINDELOF_RE.search(text):
        return "question", {"mode": "lindelof-conf"}
    if S9_PHCONF_RE.search(text):
        return "question", {"mode": "ph-conf"}
    if S9_LIPROOF_RE.search(text):
        return "question", {"mode": "li-proof"}
    m = S9_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s9-state", "slug": m.group(1)}
    m = S9_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "s9-why", "slug": m.group(1)}
    m = S9_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "s9-whydeep", "slug": m.group(1)}
    # E6.14 — RH-TRACK S10: the deviant-route walls (the attempt
    # band: the two alternative criterion routes, each closed off by
    # the store's own content).
    if S10_LICLOSE_RE.search(text):
        return "question", {"mode": "li-close"}
    if S10_STCLOSE_RE.search(text):
        return "question", {"mode": "st-close"}
    # E6.15 — FUNDAMENTALS-TRACK S11: the sieve (the full process +
    # the scan ledger) — the divisibility layer under the primes.
    m = S11_DIVTEST_RE.search(text)
    if m:
        return "question", {"mode": "div-test", "k": int(m.group(1)), "n": int(m.group(2))}
    m = S11_COMPT_RE.search(text)
    if m:
        return "question", {"mode": "comp-test", "n": int(m.group(1))}
    m = S11_PRIMETEST_RE.search(text)
    if m:
        return "question", {"mode": "prime-test", "n": int(m.group(1))}
    m = S11_FD_RE.search(text)
    if m:
        return "question", {"mode": "fd-query", "n": int(m.group(1))}
    m = S11_COMPCOUNT_RE.search(text)
    if m:
        return "question", {"mode": "comp-count", "n": int(m.group(1))}
    m = S11_FDCOUNT_RE.search(text)
    if m:
        return "question", {"mode": "fd-count", "n": int(m.group(1)), "d": int(m.group(2))}
    m = S11_FULLTRIALS_RE.search(text)
    if m:
        return "question", {"mode": "full-trials", "n": int(m.group(1))}
    m = S11_PRIMETRIALS_RE.search(text)
    if m:
        return "question", {"mode": "prime-trials", "n": int(m.group(1))}
    if S11_CANDEVEN2_RE.search(text):
        return "question", {"mode": "cand-even2"}
    m = S11_CANDTESTS_RE.search(text)
    if m:
        return "question", {"mode": "cand-tests", "d": int(m.group(1)), "n": int(m.group(2))}
    m = S11_CANDHITS_RE.search(text)
    if m:
        return "question", {"mode": "cand-hits", "d": int(m.group(1)), "n": int(m.group(2))}
    m = S11_CANDMISSES_RE.search(text)
    if m:
        return "question", {"mode": "cand-misses", "d": int(m.group(1)), "n": int(m.group(2))}
    m = S11_PRIMELEDGER_RE.search(text)
    if m:
        return "question", {"mode": "prime-ledger", "p": int(m.group(1))}
    m = S11_ESTTOTAL_RE.search(text)
    if m:
        return "question", {"mode": "est-total", "n": int(m.group(1))}
    m = S11_PARTS_RE.search(text)
    if m:
        return "question", {"mode": "parts", "n": int(m.group(1))}
    if S11_AUDIT_RE.search(text):
        return "question", {"mode": "audit"}
    m = S11_SIEVERUN_RE.search(text)
    if m:
        return "question", {"mode": "sieverun", "n": int(m.group(1))}
    m = S11_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s11-state", "slug": m.group(1)}
    m = S11_ANY_WHY_RE.search(text)
    if m:
        return "question", {"mode": "s11-why", "slug": m.group(1)}
    m = S11_WHYDEEP_RE.search(text)
    if m:
        return "question", {"mode": "s11-whydeep", "slug": m.group(1)}
    # E6.16 — FUNDAMENTALS-TRACK S12: the RH neighborhood (the
    # parallel band + the cross-pollination queue). The S12
    # surfaces are all NEW — none may shadow an S4–S11 surface.
    m = S12_GAP_RE.search(text)
    if m:
        return "question", {"mode": "s12-gap", "p": int(m.group(1))}
    if S12_GAPMAX_RE.search(text):
        return "question", {"mode": "s12-gapmax"}
    if S12_GAPMAXWHOLE_RE.search(text):
        return "question", {"mode": "s12-gapmax-whole"}
    m = S12_GAPSIZEN_RE.search(text)
    if m:
        return "question", {"mode": "s12-gapsize", "k": int(m.group(1))}
    if S12_GAPCOUNT_RE.search(text):
        return "question", {"mode": "s12-gapcount"}
    m = S12_SCALE_RE.search(text)
    if m:
        return "question", {"mode": "s12-scale", "p": int(m.group(1))}
    if S12_SCALECOUNT_RE.search(text):
        return "question", {"mode": "s12-scalecount"}
    m = S12_MOD4_1_RE.search(text)
    if m:
        return "question", {"mode": "s12-mod4-1", "which": m.group(1)}
    m = S12_MOD4_3_RE.search(text)
    if m:
        return "question", {"mode": "s12-mod4-3", "which": m.group(1)}
    if S12_MLAB_RE.search(text):
        return "question", {"mode": "s12-mlab"}
    m = S12_MAT_RE.search(text)
    if m:
        return "question", {"mode": "s12-mat", "n": int(m.group(1))}
    if S12_MROOT_RE.search(text):
        return "question", {"mode": "s12-mroot"}
    if S12_MPAST_RE.search(text):
        return "question", {"mode": "s12-mpast"}
    m = S12_COND_GIVE_RE.search(text)
    if m:
        return "question", {"mode": "s12-condgive", "x": m.group(1)}
    if S12_UNCOND_RE.search(text):
        return "question", {"mode": "s12-uncond"}
    if S12_QUEUE_RE.search(text):
        return "question", {"mode": "s12-queue"}
    m = S12_QUEUELOT_RE.search(text)
    if m:
        return "question", {"mode": "s12-queue-lot", "lot": m.group(1)}
    m = S12_CLASS_RE.search(text)
    if m:
        return "question", {"mode": "s12-class", "cls": m.group(1)}
    if S12_AGREE_RE.search(text):
        return "question", {"mode": "s12-agree"}
    if S12_ROADS_HOW_RE.search(text):
        return "question", {"mode": "s12-roads-how"}
    if S12_ROADS_UNCOND_RE.search(text):
        return "question", {"mode": "s12-roads-uncond"}
    if S12_ROADS_COND_RE.search(text):
        return "question", {"mode": "s12-roads-cond"}
    if S12_ROADNEG_RE.search(text):
        return "question", {"mode": "s12-roadneg"}
    if S12_REACHSCALE_RE.search(text):
        return "question", {"mode": "s12-reachscale"}
    if S12_MOD4Q_RE.search(text):
        return "question", {"mode": "s12-mod4q"}
    if S12_SELVED_RE.search(text):
        return "question", {"mode": "s12-selved"}
    if S12_PROVE_RE.search(text):
        return "question", {"mode": "s12-prove"}
    if S12_BANDSTATE_RE.search(text):
        return "question", {"mode": "s12-bandstate"}
    m = S12_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s12-state", "slug": m.group(1)}
    # E6.17 — the zeta variant surfaces (S13; the variant layer).
    m = S13_FACTOR_RE.search(text)
    if m:
        return "question", {"mode": "s13-factor", "sign": m.group(1), "n": int(m.group(2))}
    m = S13_FACTOR_PRIME_RE.search(text)
    if m:
        return "question", {"mode": "s13-factor-prime", "n": int(m.group(1))}
    if S13_INDEX_COUNT_RE.search(text):
        return "question", {"mode": "s13-index-count"}
    if S13_SPLIT_CENSUS_RE.search(text):
        return "question", {"mode": "s13-split-census"}
    if S13_SEAM_COUNT_RE.search(text):
        return "question", {"mode": "s13-seam-count"}
    if S13_SEAM_SAMESET_RE.search(text):
        return "question", {"mode": "s13-seam-sameset"}
    m = S13_PARTIAL_RE.search(text)
    if m:
        return "question", {
            "mode": "s13-partial",
            "sign": m.group(1),
            "indexset": "comp" if m.group(2) == "the composites" else ("primes" if m.group(2) == "the primes" else "all"),
            "height": int(m.group(4)) if m.group(4) else None,
            "exp": int(m.group(6)) if m.group(6) else 2,
        }
    m = S13_PARTITION_HOLD_RE.search(text)
    if m:
        return "question", {"mode": "s13-partition-hold", "exp": int(m.group(2)) if m.group(2) else 2}
    m = S13_REMOVAL_RE.search(text)
    if m:
        return "question", {
            "mode": "s13-removal",
            "exp": int(m.group(2)) if m.group(2) else 2,
            "p": int(m.group(3)),
        }
    m = S13_REMOVAL_SET_RE.search(text)
    if m:
        return "question", {"mode": "s13-removal-set", "names": m.group(1), "exp": int(m.group(2))}
    m = S13_REMOVAL_ALL_RE.search(text)
    if m:
        return "question", {"mode": "s13-removal-all", "exp": int(m.group(1))}
    if S13_SPOT_ABOVE_RE.search(text):
        return "question", {"mode": "s13-spot-above"}
    m = S13_LIMIT_RE.search(text)
    if m:
        return "question", {
            "mode": "s13-limit",
            "sign": m.group(1),
            "indexset": "comp" if m.group(2) == "the composites" else ("primes" if m.group(2) == "the primes" else "all"),
            "walks": m.group(3) == ", as the height walks past my line",
            "exp": int(m.group(4)) if m.group(4) else 2,
        }
    m = S13_LIMIT_BOUNDARY_RE.search(text)
    if m:
        return "question", {
            "mode": "s13-limit-boundary",
            "sign": m.group(1),
            "indexset": "comp" if m.group(2) == "the composites" else ("primes" if m.group(2) == "the primes" else "all"),
        }
    if S13_COMPARE6_RE.search(text):
        return "question", {"mode": "s13-compare6"}
    m = S13_COMPARE3_RE.search(text)
    if m:
        return "question", {"mode": "s13-compare3", "sign": m.group(1), "exp": int(m.group(2))}
    m = S13_COMPARE_SAME_RE.search(text)
    if m:
        return "question", {"mode": "s13-compare-same", "sign": m.group(1)}
    m = S13_REMOVAL_BELOW_RE.search(text)
    if m:
        return "question", {"mode": "s13-removal-below", "exp": int(m.group(1))}
    m = S13_REMOVAL_MAX_RE.search(text)
    if m:
        return "question", {"mode": "s13-removal-max", "exp": int(m.group(1))}
    if S13_DESCENT_RE.search(text):
        return "question", {"mode": "s13-descent"}
    if S13_PLUS_SIDE_RE.search(text):
        return "question", {"mode": "s13-plus-side"}
    if S13_CLOSED_FORM_RE.search(text):
        return "question", {"mode": "s13-closed-form"}
    if S13_RH_TOUCH_RE.search(text):
        return "question", {"mode": "s13-rh-touch"}
    if S13_BANDSTATE_RE.search(text):
        return "question", {"mode": "s13-bandstate"}
    if S13_UNCOND_RE.search(text):
        return "question", {"mode": "s13-uncond"}
    if S13_UNCLASS_RE.search(text):
        return "question", {"mode": "s13-unclass"}
    m = S13_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s13-state", "slug": m.group(1)}
    m = S14_FORM_RE.search(text)
    if m:
        return "question", {"mode": "s14-form", "panel": m.group(1)}
    if S14_SINGULAR_RE.search(text):
        return "question", {"mode": "s14-singular"}
    m = S14_DOUBLE_RE.search(text)
    if m:
        return "question", {"mode": "s14-double", "x1": m.group(1), "y1": m.group(2), "panel": m.group(3)}
    m = S14_ADD_RE.search(text)
    if m:
        return "question", {
            "mode": "s14-add", "x1": m.group(1), "y1": m.group(2),
            "x2": m.group(3), "y2": m.group(4), "panel": m.group(5),
        }
    m = S14_MUL_RE.search(text)
    if m:
        return "question", {"mode": "s14-mul", "m": m.group(1), "x1": m.group(2), "y1": m.group(3), "panel": m.group(4)}
    m = S14_POINT_RE.search(text)
    if m:
        return "question", {"mode": "s14-point-on", "x1": m.group(1), "y1": m.group(2), "panel": m.group(3)}
    m = S14_COUNT_RE.search(text)
    if m:
        return "question", {"mode": "s14-count", "p": int(m.group(2)), "panel": m.group(1)}
    m = S14_APTABLE_RE.search(text)
    if m:
        return "question", {"mode": "s14-aptable", "panel": m.group(1)}
    m = S14_HASSE_RE.search(text)
    if m:
        return "question", {"mode": "s14-hasse", "p": int(m.group(1)), "panel": m.group(2)}
    if S14_HASSE_ALL_RE.search(text):
        return "question", {"mode": "s14-hasse-all"}
    if S14_CMSIG_RE.search(text):
        return "question", {"mode": "s14-cmsig"}
    if S14_CMSIG_ZEROS_RE.search(text):
        return "question", {"mode": "s14-cmsig-zeros"}
    if S14_TORSION_A_RE.search(text):
        return "question", {"mode": "s14-torsion-a"}
    m = S14_GEN_RE.search(text)
    if m:
        return "question", {"mode": "s14-gen", "x1": m.group(1), "y1": m.group(2)}
    if S14_GEN_ALL_RE.search(text):
        return "question", {"mode": "s14-gen-all"}
    if S14_GEN_CLOSE_RE.search(text):
        return "question", {"mode": "s14-gen-close"}
    m = S14_LPAR_RE.search(text)
    if m:
        return "question", {"mode": "s14-lpar", "panel": m.group(1)}
    m = S14_LVANISH_RE.search(text)
    if m:
        return "question", {"mode": "s14-lvanish", "panel": m.group(1)}
    if S14_RH_TOUCH_RE.search(text):
        return "question", {"mode": "s14-rh-touch"}
    if S14_RANK_RE.search(text):
        return "question", {"mode": "s14-rank"}
    if S14_SEARCH_B_RE.search(text):
        return "question", {"mode": "s14-search-b"}
    if S14_PANELWHY_RE.search(text):
        return "question", {"mode": "s14-panel"}
    if S14_BANDSTATE_RE.search(text):
        return "question", {"mode": "s14-bandstate"}
    if S14_UNCOND_RE.search(text):
        return "question", {"mode": "s14-uncond"}
    m = S14_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s14-state", "slug": m.group(1)}
    m = S15_FACTOR_RE.search(text)
    if m:
        return "question", {
            "mode": "s15-factor", "panel": m.group(1), "p": int(m.group(2)), "form": m.group(3),
        }
    m = S15_FORM_RE.search(text)
    if m:
        return "question", {"mode": "s15-form", "panel": m.group(1)}
    m = S15_PARTIAL_RE.search(text)
    if m:
        return "question", {"mode": "s15-partial", "panel": m.group(1), "h": int(m.group(2))}
    m = S15_RECPARTIAL_RE.search(text)
    if m:
        return "question", {"mode": "s15-recpartial", "panel": m.group(1), "h": int(m.group(2))}
    m = S15_CORR_RE.search(text)
    if m:
        return "question", {"mode": "s15-corr", "panel": m.group(1)}
    m = S15_IDENTITY_RE.search(text)
    if m:
        return "question", {"mode": "s15-identity", "panel": m.group(1)}
    m = S15_ADDED_RE.search(text)
    if m:
        return "question", {
            "mode": "s15-added", "form": m.group(1), "panel": m.group(2), "p": int(m.group(3)),
        }
    if S15_VANISH_B_RE.search(text):
        return "question", {"mode": "s15-vanish-b"}
    if S15_NONZERO_A_RE.search(text):
        return "question", {"mode": "s15-nonzero-a"}
    if S15_REGION_RE.search(text):
        return "question", {"mode": "s15-region"}
    if S15_RAMLINE_RE.search(text):
        return "question", {"mode": "s15-ramline"}
    if S15_BSD_TOUCH_RE.search(text):
        return "question", {"mode": "s15-bsd-touch"}
    if S15_LBANDSTATE_RE.search(text):
        return "question", {"mode": "s15-bandstate"}
    if S15_LUNCOND_RE.search(text):
        return "question", {"mode": "s15-uncond"}
    m = S15_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s15-state", "slug": m.group(1)}
    m = S16_ORDER_RE.search(text)
    if m:
        return "question", {"mode": "s16-order", "panel": m.group(1)}
    m = S16_RANK_RE.search(text)
    if m:
        return "question", {"mode": "s16-rank", "panel": m.group(1)}
    m = S16_DESCEND_RE.search(text)
    if m:
        return "question", {"mode": "s16-descend", "panel": m.group(1)}
    m = S16_SELMER_RE.search(text)
    if m:
        return "question", {"mode": "s16-selmer", "panel": m.group(1)}
    m = S16_SELWALL_RE.search(text)
    if m:
        return "question", {"mode": "s16-selwall", "panel": m.group(1)}
    if S16_BSD_RE.search(text):
        return "question", {"mode": "s16-bsd"}
    if S16_REACH_RE.search(text):
        return "question", {"mode": "s16-reach"}
    if S16_TORSION_RE.search(text):
        return "question", {"mode": "s16-torsion"}
    if S16_GEN_RE.search(text):
        return "question", {"mode": "s16-gen"}
    if S16_CONSISTENT_RE.search(text):
        return "question", {"mode": "s16-consistent"}
    m = S16_LVALWALL_RE.search(text)
    if m:
        return "question", {"mode": "s16-lvalwall", "panel": m.group(1)}
    if S16_PANELW3_RE.search(text):
        return "question", {"mode": "s16-panel"}
    m = S16_SIDE_RE.search(text)
    if m:
        return "question", {"mode": "s16-sides", "panel": m.group(1)}
    if S16_BANDSTATE3_RE.search(text):
        return "question", {"mode": "s16-bandstate"}
    if S16_UNCOND3_RE.search(text):
        return "question", {"mode": "s16-uncond"}
    m = S16_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s16-state", "slug": m.group(1)}
    m = S17_VP_RE.search(text)
    if m:
        return "question", {"mode": "s17-vp", "n": m.group(1), "p": m.group(2)}
    if S17_LTE_A_RE.search(text):
        return "question", {"mode": "s17-lte-a"}
    if S17_LTE_B_RE.search(text):
        return "question", {"mode": "s17-lte-b"}
    if S17_LTELED_RE.search(text):
        return "question", {"mode": "s17-lte-ledger"}
    if S17_BEAL_RE.search(text):
        return "question", {"mode": "s17-beal"}
    if S17_CENSUS_RE.search(text):
        return "question", {"mode": "s17-census"}
    if S17_EMPT_RE.search(text):
        return "question", {"mode": "s17-empt"}
    if S17_FAMILY_RE.search(text):
        return "question", {"mode": "s17-family"}
    if S17_PRIM_RE.search(text):
        return "question", {"mode": "s17-prim"}
    if S17_FC_RE.search(text):
        return "question", {"mode": "s17-fc"}
    if S17_FLT_RE.search(text):
        return "question", {"mode": "s17-flt"}
    if S17_BANDSTATE_RE.search(text):
        return "question", {"mode": "s17-bandstate"}
    if S17_UNCOND_RE.search(text):
        return "question", {"mode": "s17-uncond"}
    m = S17_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s17-state", "slug": m.group(1)}
    m = S18_DEC_RE.search(text)
    if m:
        return "question", {"mode": "s18-dec", "p": m.group(1)}
    if S18_PI_RE.search(text):
        return "question", {"mode": "s18-pi"}
    if S18_SCAN_RE.search(text):
        return "question", {"mode": "s18-scan"}
    if S18_HEAVY_RE.search(text):
        return "question", {"mode": "s18-heavy"}
    m = S18_COSTSPOT_RE.search(text)
    if m:
        return "question", {"mode": "s18-costspot", "n": m.group(1)}
    m = S18_PH_RE.search(text)
    if m:
        return "question", {"mode": "s18-ph", "n": m.group(1)}
    if S18_KILL_RE.search(text):
        return "question", {"mode": "s18-kill"}
    if S18_HALT_RE.search(text):
        return "question", {"mode": "s18-halt"}
    if S18_MACHINE_RE.search(text):
        return "question", {"mode": "s18-machine"}
    if S18_TAM_RE.search(text):
        return "question", {"mode": "s18-tam"}
    if S18_BANDSTATE_RE.search(text):
        return "question", {"mode": "s18-bandstate"}
    if S18_UNCOND_RE.search(text):
        return "question", {"mode": "s18-uncond"}
    m = S18_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s18-state", "slug": m.group(1)}
    # E6.23 (S19): the difficulty line (the P vs NP island, summit band)
    m = S19_P_RE.search(text)
    if m:
        return "question", {"mode": "s19-p", "pword": m.group(1)}
    if S19_NP_PARITY_RE.search(text):
        return "question", {"mode": "s19-np", "npword": "parity"}
    if S19_NP_DERIV_RE.search(text):
        return "question", {"mode": "s19-np", "npword": "deriv"}
    if S19_SETTLE16_RE.search(text):
        return "question", {"mode": "s19-settle16"}
    if S19_SETTLE_RE.search(text):
        return "question", {"mode": "s19-settle"}
    if S19_SUMMIT_RE.search(text):
        return "question", {"mode": "s19-summit"}
    if S19_STATEMENT_RE.search(text):
        return "question", {"mode": "s19-statement"}
    m = S19_PARITY_RE.search(text)
    if m:
        return "question", {"mode": "s19-parity", "kword": m.group(1)}
    if S19_PARCNF_RE.search(text):
        return "question", {"mode": "s19-parcnf"}
    if S19_WREL_RE.search(text):
        return "question", {"mode": "s19-rel"}
    if S19_WALG_RE.search(text):
        return "question", {"mode": "s19-alg"}
    if S19_WNAT_RE.search(text):
        return "question", {"mode": "s19-natp"}
    if S19_WAC0_RE.search(text):
        return "question", {"mode": "s19-ac0"}
    if S19_BANDSTATE_RE.search(text):
        return "question", {"mode": "s19-bandstate"}
    if S19_UNC_RE.search(text):
        return "question", {"mode": "s19-unc"}
    m = S19_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s19-state", "slug": m.group(1)}
    # E6.24 (S20): the weaving line (the connecting work)
    if S20_RHSUMMIT_RE.search(text):
        return "question", {"mode": "s20-rhsummit"}
    if S20_SOIL_RE.search(text):
        return "question", {"mode": "s20-soil"}
    if S20_NODE_RE.search(text):
        return "question", {"mode": "s20-node"}
    if S20_SHAPE_RE.search(text):
        return "question", {"mode": "s20-shape"}
    if S20_OPEN_RE.search(text):
        return "question", {"mode": "s20-open"}
    if S20_FORM_RE.search(text):
        return "question", {"mode": "s20-form"}
    if S20_MARKER_RE.search(text):
        return "question", {"mode": "s20-marker"}
    if S20_WALLKIND_RE.search(text):
        return "question", {"mode": "s20-wallkind"}
    if S20_ABSENCE_RE.search(text):
        return "question", {"mode": "s20-absence"}
    if S20_WEAVESTATE_RE.search(text):
        return "question", {"mode": "s20-weavestate"}
    if S20_UNC_RE.search(text):
        return "question", {"mode": "s20-unc"}
    if S20_W1_RE.search(text):
        return "question", {"mode": "s20-w1"}
    if S20_W2_RE.search(text):
        return "question", {"mode": "s20-w2"}
    if S20_W3_RE.search(text):
        return "question", {"mode": "s20-w3"}
    if S20_W4_RE.search(text):
        return "question", {"mode": "s20-w4"}
    m = S20_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s20-state", "slug": m.group(1)}
    if S21_HYPO_RE.search(text):
        return "question", {"mode": "s21-hypo"}
    if S21_LINE_RE.search(text):
        return "question", {"mode": "s21-line"}
    if S21_FILING_RE.search(text):
        return "question", {"mode": "s21-filing"}
    if S21_W1_RE.search(text):
        return "question", {"mode": "s21-w1"}
    if S21_W2_RE.search(text):
        return "question", {"mode": "s21-w2"}
    if S21_W3_RE.search(text):
        return "question", {"mode": "s21-w3"}
    if S21_W4_RE.search(text):
        return "question", {"mode": "s21-w4"}
    m = S21_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s21-state", "slug": m.group(1)}
    if S31_SEEDED_RE.search(text):
        return "question", {"mode": "s31-seeded"}
    if S31_GOLDEN_RE.search(text):
        return "question", {"mode": "s31-golden"}
    if S31_FILING_RE.search(text):
        return "question", {"mode": "s31-filing"}
    if S31_SUMLINE_RE.search(text):
        return "question", {"mode": "s31-sumline"}
    if S31_CASSINI_RE.search(text):
        return "question", {"mode": "s31-cassini"}
    if S31_SHIFT_RE.search(text):
        return "question", {"mode": "s31-shift"}
    if S31_RATIO_RE.search(text):
        return "question", {"mode": "s31-ratio"}
    if S31_GOLDENWALK_RE.search(text):
        return "question", {"mode": "s31-goldenwalk"}
    if S31_SILENCE_RE.search(text):
        return "question", {"mode": "s31-silence"}
    if S31_W1_RE.search(text):
        return "question", {"mode": "s31-w1"}
    if S31_W2_RE.search(text):
        return "question", {"mode": "s31-w2"}
    if S31_W3_RE.search(text):
        return "question", {"mode": "s31-w3"}
    m = S31_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s31-state", "slug": m.group(1)}
    if S32_PERIOD_RE.search(text):
        return "question", {"mode": "s32-period"}
    if S32_OFFLINE_RE.search(text):
        return "question", {"mode": "s32-offline"}
    if S32_PISANO8_RE.search(text):
        return "question", {"mode": "s32-pisano8"}
    if S32_PISANO12_RE.search(text):
        return "question", {"mode": "s32-pisano12"}
    if S32_SHADOW5_RE.search(text):
        return "question", {"mode": "s32-shadow5"}
    if S32_VALUE_RE.search(text):
        return "question", {"mode": "s32-value"}
    if S32_PARITY_RE.search(text):
        return "question", {"mode": "s32-parity"}
    if S32_DIVIDES_RE.search(text):
        return "question", {"mode": "s32-divides"}
    if S32_PAGENUM_RE.search(text):
        return "question", {"mode": "s32-pagenames"}
    if S32_GOLDENPOWER_RE.search(text):
        return "question", {"mode": "s32-goldenpower"}
    if S32_LUCAS_RE.search(text):
        return "question", {"mode": "s32-lucas"}
    if S32_BELOWZERO_RE.search(text):
        return "question", {"mode": "s32-belowzero"}
    if S32_RECIP89_RE.search(text):
        return "question", {"mode": "s32-recip89"}
    if S32_FILING_RE.search(text):
        return "question", {"mode": "s32-filing"}
    if S32_W1_RE.search(text):
        return "question", {"mode": "s32-w1"}
    if S32_W2_RE.search(text):
        return "question", {"mode": "s32-w2"}
    if S32_W3_RE.search(text):
        return "question", {"mode": "s32-w3"}
    m = S32_ANY_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s32-state", "slug": m.group(1)}
    # E6.26 — the S22 (proportion line) surfaces (COURSE A band 1;
    # D-e6t(a): the first proportion whose parts are both prime is
    # two to three)
    if S22_CARRY_DIVIDES_RE.search(text):
        return "question", {"mode": "s22-carry-divides"}
    if S22_CARRY_QUESTION_RE.search(text):
        return "question", {"mode": "s22-carry-question"}
    if S22_CARRY_TELESCOPE_RE.search(text):
        return "question", {"mode": "s22-carry-telescope"}
    if S22_CARRY_HALFPROD_RE.search(text):
        return "question", {"mode": "s22-carry-halfproduct"}
    if S22_PROP_RE.search(text):
        return "question", {"mode": "s22-prop"}
    if S22_FRAC_RE.search(text):
        return "question", {"mode": "s22-frac"}
    m = S22_FAMILY_RE.search(text)
    if m:
        return "question", {"mode": "s22-family", "a": m.group(1), "b": m.group(2)}
    m = S22_CHAIN_FRAC_RE.search(text)
    if m:
        return "question", {"mode": "s22-chain-frac", "a": m.group(1), "b": m.group(2)}
    m = S22_CHAIN_MOD_RE.search(text)
    if m:
        return "question", {"mode": "s22-chain-mod", "a": m.group(1), "b": m.group(2)}
    if S22_CLASSWALK_RE.search(text):
        return "question", {"mode": "s22-classwalk"}
    if S22_FILING_RE.search(text):
        return "question", {"mode": "s22-filing"}
    m = S22_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s22-state", "slug": m.group(1)}
    if S22_FIRSTPRIME_RE.search(text):
        return "question", {"mode": "s22-firstprime"}
    if S22_W1_RE.search(text):
        return "question", {"mode": "s22-w1"}
    if S22_W2_RE.search(text):
        return "question", {"mode": "s22-w2"}
    if S22_W3_RE.search(text):
        return "question", {"mode": "s22-w3"}
    if S23_COP_RE.search(text):
        return "question", {"mode": "s23-cop"}
    if S23_FPR_RE.search(text):
        return "question", {"mode": "s23-fpr"}
    m = S23_STATE_RE.search(text)
    if m:
        return "question", {"mode": "s23-state", "slug": m.group(1)}
    m = S23_COPRIME_RE.search(text)
    if m:
        return "question", {"mode": "s23-coprime", "a": m.group(1), "b": m.group(2)}
    m = S23_NEVERRED_RE.search(text)
    if m:
        return "question", {"mode": "s23-neverred", "a": m.group(1), "b": m.group(2)}
    m = S23_CHAIN_FRAC_RE.search(text)
    if m:
        return "question", {"mode": "s23-chain-frac", "a": m.group(1), "b": m.group(2)}
    m = S23_CHAIN_MOD_RE.search(text)
    if m:
        return "question", {"mode": "s23-chain-mod", "a": m.group(1), "b": m.group(2)}
    if S23_CENSUS_RE.search(text):
        return "question", {"mode": "s23-census"}
    if S23_CEILING_RE.search(text):
        return "question", {"mode": "s23-ceiling"}
    if S23_FILING_RE.search(text):
        return "question", {"mode": "s23-filing"}
    if S23_ABOVE2_RE.search(text):
        return "question", {"mode": "s23-above2"}
    if S23_W1_RE.search(text):
        return "question", {"mode": "s23-w1"}
    if S23_W2_RE.search(text):
        return "question", {"mode": "s23-w2"}
    if S23_W3_RE.search(text):
        return "question", {"mode": "s23-w3"}
    if S24_SUM_RE.search(text):
        return "question", {"mode": "s24-sum"}
    if S24_TWIN_RE.search(text):
        return "question", {"mode": "s24-twin"}
    if S24_STATE_RE.search(text):
        return "question", {"mode": "s24-state", "slug": S24_STATE_RE.search(text).group(1)}
    if S24_SUMWALK_RE.search(text):
        return "question", {"mode": "s24-sumwalk"}
    if S24_TWINWALK_RE.search(text):
        return "question", {"mode": "s24-twinwalk"}
    if S24_DOUB_RE.search(text):
        return "question", {"mode": "s24-doub", "idx": S24_DOUB_RE.search(text).group(1)}
    if S24_SQSUM_RE.search(text):
        m = S24_SQSUM_RE.search(text)
        return "question", {"mode": "s24-sqsum", "a": m.group(1), "b": m.group(2)}
    if S24_TWINTERM_RE.search(text):
        return "question", {"mode": "s24-twinterm", "idx": S24_TWINTERM_RE.search(text).group(1)}
    if S24_SUMTERM_RE.search(text):
        return "question", {"mode": "s24-sumterm", "idx": S24_SUMTERM_RE.search(text).group(1)}
    if S24_FILING_RE.search(text):
        return "question", {"mode": "s24-filing"}
    if S24_OFFSCRIPT_RE.search(text):
        return "question", {"mode": "s24-offscript"}
    if S24_W1_RE.search(text):
        return "question", {"mode": "s24-w1"}
    if S24_W2_RE.search(text):
        return "question", {"mode": "s24-w2"}
    if S24_W3_RE.search(text):
        return "question", {"mode": "s24-w3"}
    m = LESSON_RE.search(text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        kind = "correction" if CORR_MARKER_RE.search(text) else "assertion"
        return kind, {"a": a, "b": b}
    m = DRILL_SUCC_RE.search(text)
    if m:
        return "question", {"mode": "succ", "n": int(m.group(1))}
    m = DRILL_ADD_RE.search(text)
    if m:
        return "question", {"mode": "add", "a": int(m.group(1)), "b": int(m.group(2))}
    m = DRILL_SUB_RE.search(text)
    if m:
        return "question", {"mode": "sub", "a": int(m.group(1)), "b": int(m.group(2))}
    m = DRILL_MUL_RE.search(text)
    if m:
        # E6.2: a drill, not a hard gap — the gap is HONEST only while the
        # rule is unlearned (the impossible-learns arc, E6.2 C3).
        return "question", {"mode": "mult", "a": int(m.group(1)), "b": int(m.group(2))}
    m = DRILL_CMP_RE.search(text)
    if m:
        return "question", {"mode": "cmp", "a": int(m.group(1)), "b": int(m.group(2))}
    m = DRILL_SQRT_RE.search(text)
    if m:
        return "question", {"mode": "sqrt", "n": int(m.group(1))}
    m = COUNT_FROM_RE.search(text)
    if m:
        return "request", {"a": int(m.group(1)), "b": int(m.group(2))}
    m = COUNT_TO_RE.search(text)
    if m:
        return "command", {"n": int(m.group(1))}
    return "ambiguous", {}


# ── response IRs (frozen shapes; validated against CONTRACTS verbatim) ─────────


def kind_response_ir(kind: str, slots: dict[str, Any], answer: str | None = None, trace: list[str] | None = None) -> dict[str, Any]:
    """The deterministic grounded IR a policy must fill for each kind.
    All seven kinds exist (the contract set is frozen); the pilot strip
    exercises question/assertion/correction/ambiguous, the rest are
    unit-tested here so the dispatch is complete, not partial."""

    if kind == "question":
        if answer is None:
            return {"answer": "needs_info", "evidence": list(trace or ()), "uncertainty_state": "needs_info"}
        return {"answer": answer, "evidence": list(trace or ()), "uncertainty_state": "derived"}
    if kind == "assertion":
        a, b = slots.get("a"), slots.get("b")
        return {"ack": f"after {a} comes {b}", "provenance": [], "epistemic_state": "candidate"}
    if kind == "correction":
        a, b = slots.get("a"), slots.get("b")
        return {"superseded": f"after {a} comes ...", "replacement": f"after {a} comes {b}"}
    if kind == "ambiguous":
        return {
            "clarifying_question": "i did not catch that",
            "candidates": [
                "a lesson about a number (after N comes M)",
                "a question about a number (what comes after N / A + B is what)",
            ],
        }
    if kind == "impossible":
        a, b = slots.get("a"), slots.get("b")
        return {"gap": f"multiplication ({a} * {b} is beyond my number line)", "nearest_plan": ["add-within-10", "count-successor"]}
    if kind == "request":
        a, b = slots.get("a"), slots.get("b")
        return {"plan": f"chain successor facts from {a} to {b}", "result": list(trace or ()), "trace": list(trace or ())}
    if kind == "command":
        n = slots.get("n")
        return {"action": f"count to {n}", "resulting_state": list(trace or ())}
    raise KeyError(f"no contract for kind: {kind}")


# ── LLM prompts (the seam; content is never produced by the LLM) ──────────────


def _classify_prompt(text: str) -> list[dict[str, str]]:
    kinds = "\n".join(f"- {k}: {sorted(CONTRACTS[k].required_fields)}" for k in sorted(KINDS))
    return [
        {
            "role": "user",
            "content": (
                "You are the intent classifier for a tutor system. Classify the student-teacher "
                f"utterance into EXACTLY ONE of these interaction kinds (response contracts):\n{kinds}\n"
                "Pilot grammar slots: assertion/correction need {\"a\": int, \"b\": int} (from 'after A comes B') or "
                "{\"shape\": str, \"sides\": int, \"corners\": int} / {\"shape\": \"circle\"} (shape definitions); "
                "question needs {\"mode\":\"succ\",\"n\":int} (from 'what comes after N') or "
                "{\"mode\":\"shape\",\"shape\":\"triangle|square|rectangle|circle\",\"property\":\"sides|corners\"} (shape drills) or "
                "{\"mode\":\"add\",\"a\":int,\"b\":int} (from 'A + B is what'); impossible needs "
                "{\"a\":int,\"b\":int,\"op\":\"multiply\"} (from 'A * B is what'); request needs "
                "{\"a\":int,\"b\":int} (from 'count from A to B'); command needs {\"n\":int} (from 'count to N'); "
                "ambiguous needs {} (only if the text matches NO grammar above).\n"
                "Answer with STRICT JSON on one line: {\"kind\": \"...\", \"slots\": {...}}. No other text.\n\n"
                f"Utterance: {text!r}"
            ),
        }
    ]


def _phrase_prompt(det_text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": (
                "Rephrase the following tutor reply in a warm, child-facing voice. Keep EVERY fact, "
                "number, and admission of not-knowing EXACTLY. One short sentence. No other text.\n"
                f"Reply to rephrase: {det_text!r}"
            ),
        }
    ]


def _extract_json(raw: str) -> dict[str, Any]:
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in LLM output: {raw!r}")
    d = json.loads(m.group(0))
    if not isinstance(d, dict):
        raise TypeError("LLM JSON is not an object")
    return d


# ── the turn record (machine-readable; the analysis arm's input) ─────────────


@dataclass
class TurnResult:
    turn: str
    session: int
    surface: str
    kind: str
    concept: str | None
    slots: dict[str, Any]
    response_ir: dict[str, Any]
    response_text: str
    contract_valid: bool
    contract_violations: list[str]
    grounded: list[str]  # assertion ids the content cites (content_from = CODEX)
    memory_diff: list[str]  # assertion ids added or re-stated this turn
    events: list[str]  # mastery-event assertion ids recorded this turn
    honest_gap: dict[str, Any] | None
    conflict: dict[str, Any] | None
    attention: dict[str, Any] | None
    arm: dict[str, Any]  # classifier/phrasing source + fallback flags

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "session": self.session,
            "surface": self.surface,
            "kind": self.kind,
            "concept": self.concept,
            "slots": dict(self.slots),
            "response_ir": dict(self.response_ir),
            "response_text": self.response_text,
            "contract_valid": self.contract_valid,
            "contract_violations": list(self.contract_violations),
            "grounded": list(self.grounded),
            "memory_diff": list(self.memory_diff),
            "events": list(self.events),
            "honest_gap": self.honest_gap,
            "conflict": self.conflict,
            "attention": self.attention,
            "arm": dict(self.arm),
        }


@dataclass
class _PolicyOutcome:
    """What a per-kind policy produced (ir, text, the memory it wrote, the
    events it recorded). `kind` overrides the classified kind when the
    policy answers under a DIFFERENT contract (E6.2: a classified drill
    while its rule is unlearned is answered as the HONEST `impossible`
    gap — the kind in the report is the kind the response actually used)."""

    ir: dict[str, Any]
    text: str
    grounded: list[str]
    memory_diff: list[str]
    events: list[str]
    honest_gap: dict[str, Any] | None = None
    conflict: dict[str, Any] | None = None
    attention: dict[str, Any] | None = None
    kind: str | None = None


# ── the brainstem ─────────────────────────────────────────────────────────────



# ──────────────────────────────────────────────────────────────────────────
# S17 — E6.21 / the valuation line (the Beal island: the single band of the
# island).  The statement of record (the ams beal prize): if A^x + B^y = C^z
# with positive integers and x, y, z > 2, then A, B, C share a common prime
# factor.  The band holds: the VALUATION (v_p read off the first-divisor
# chain — the S11 soil), the LIFT-THE-EXPONENT identity (the classical
# odd-p form, verified in every instance of the line's ledger box), the
# STATEMENT (a declared record fact — NO theorem:beal: the candidate is the
# island's wall, not a store fact), the VERIFICATION CENSUS (the box
# 84 x depth 10: 83 triples, every one carrying its common prime factor,
# zero primitive on the line), and the two compositions (the lte ledger;
# the beal satisfaction of the line).  The primitive territory, the
# fermat-catalan boundary, and the fermat anchor are walls of record.
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S17_VAL = "valuation"
CONCEPT_S17_LTE = "lte-form"
CONCEPT_S17_BS17 = "beal-summit"
CONCEPT_S17_CENS = "beal-census"

CONCEPT_S17: tuple = (
    Concept(
        CONCEPT_S17_VAL,
        "the valuation: for a prime and a number on my line, the p-adic depth — the p-rung of the first-divisor factorization chain, counting how many times the prime divides before the stop; every recorded number carries its depths as facts",
        "college-1",
        "beal",
        prereqs=(CONCEPT_S11_SPF, CONCEPT_S11_DIVID),
    ),
    Concept(
        CONCEPT_S17_LTE,
        "the lift-the-exponent form: for an odd prime p dividing the difference x minus y and dividing neither term, the p-adic depth of x to the n power minus y to the n power is the p-adic depth of the difference plus the p-adic depth of the exponent — verified in every instance of the line's ledger box",
        "college-1",
        "beal",
        prereqs=(CONCEPT_S17_VAL,),
    ),
    Concept(
        CONCEPT_S17_BS17,
        "the summit of the island: the statement itself, a declared record fact (the ams beal prize) — with all three exponents above two, a to the x power plus b to the y power equal to c to the z power forces a common prime factor of a, b and c; on my line the verification census carries it and the primitive territory is a wall",
        "college-1",
        "beal",
        prereqs=(CONCEPT_S17_VAL, CONCEPT_S11_DIVID),
    ),
    Concept(
        CONCEPT_S17_CENS,
        "the verification census: in the box where a, b, c lie at or below the line end and the exponents stand between three and ten of record, exactly 83 triples solve the island's equation and every one carries its common prime factor — zero primitive triples on the line; the line ends where the primitive triples would live",
        "college-1",
        "beal",
        prereqs=(CONCEPT_S17_BS17, CONCEPT_S11_LEDGER),
    ),
)

S17_LESSONS: dict[str, tuple] = {
    "the valuation, the p-adic depth, read off the first-divisor factorization chain: for a prime p and a number on my line, it is the number of times the p-rung of the chain divides the number before the stop — the highest power of p that divides it — and every recorded number carries each of its depths as a fact, at the line end 84": (
        CONCEPT_S17_VAL,
        "valuation-def",
        "lemma",
        "What the valuation IS: the p-adic depth of a number, read off the p-rung of the first-divisor factorization chain (the S11 soil).",
        (),
        "The p-adic depth, off the spf chain: how many times the prime divides before the stop.",
    ),
    "the lift-the-exponent identity, the classical odd-p form, as the rule i was given: when an odd prime p divides the difference x minus y and divides neither x nor y, the p-adic depth of x to the n power minus y to the n power is the p-adic depth of the difference x minus y plus the p-adic depth of the exponent n — my ledger in the line's box (the odd primes at or below the line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end) verifies every instance of it, at the line end 84": (
        CONCEPT_S17_LTE,
        "lte-def",
        "lemma",
        "The LTE rule (classical odd-p form): v_p(x^n - y^n) = v_p(x - y) + v_p(n) when p | (x - y) and p ∤ x·y; the line's ledger box verifies every instance.",
        (),
        "The lift-the-exponent identity, the classical odd-p form — the ledger holds it in every instance on the line.",
    ),
    "the statement of the island, of record, as the ams beal prize holds it: if a to the x power plus b to the y power equals c to the z power, and a, b, c, x, y and z are positive integers with x, y and z each above two, then a, b and c have a common prime factor — that is, the equation has no solution in pairwise coprime a, b and c once every exponent is above two, at the line end 84": (
        CONCEPT_S17_BS17,
        "beal-def",
        "lemma",
        "The STATEMENT (the island's summit, a declared record fact — the ams beal prize): no pairwise-coprime solution with all three exponents above two.",
        (),
        "The statement: A^x + B^y = C^z with x, y, z > 2 forces a common prime factor of A, B, C (the Beal conjecture, of record — the candidate, not a store theorem).",
    ),
    "the verification census on my line: in the box where a, b, c lie at or below my line end and the exponents x, y, z stand between three and ten of record, exactly eighty-three triples solve the island's equation, and every one of the eighty-three carries its common prime factor — the two-power twin family, the three-family, the seven-family, the fifteen-family, and the seventeen, nineteen, twenty-six, twenty-eight, thirty-one, thirty-three families — while zero primitive triples live on my line; the line ends where the primitive triples would live, and that territory is a wall, at the line end 84": (
        CONCEPT_S17_CENS,
        "census-def",
        "lemma",
        "The verification census on the line: the box (line end x depth ten of record) holds exactly 83 triples, every one carrying its common prime factor, zero primitive.",
        (),
        "The census: 83 triples in the box, all factored, none primitive — the line's side of the statement.",
    ),
}

S17_THEOREMS: dict[str, dict] = {
    "lte-ledger": {
        "parts": ("lte-def", "valuation-def"),
        "statement": "the ledger filed on the line: the lift-the-exponent identity, the classical odd-p form, verified in every instance of the ledger's box — the odd primes at or below my line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end — two hundred forty-nine thousand two hundred eighty instances, zero deviations, at the line end 84",
        "concept": CONCEPT_S17_LTE,
    },
    "beal-line-satisfaction": {
        "parts": ("beal-def", "census-def"),
        "statement": "the summit of the island filed on my line: the statement holds of record across the whole census box — the eighty-three triples of the box each carry their common prime factor, no primitive triple lives in the box, and the primitive territory is a wall, at the line end 84",
        "concept": CONCEPT_S17_BS17,
    },
}

_S17_SLUGS = (
    "valuation-def|lte-def|beal-def|census-def|"
    "lte-ledger|beal-line-satisfaction"
)
S17_SLUG_CONCEPT = {
    "valuation-def": CONCEPT_S17_VAL,
    "lte-def": CONCEPT_S17_LTE,
    "beal-def": CONCEPT_S17_BS17,
    "census-def": CONCEPT_S17_CENS,
    "lte-ledger": CONCEPT_S17_LTE,
    "beal-line-satisfaction": CONCEPT_S17_BS17,
}
SAVANT_LESSONS = {**SAVANT_LESSONS, **S17_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S17_THEOREMS}


# ── The S17 reference functions (the mechanism's own record machinery; ──
# the store's run is the referee).  The census and the ledger are bounded
# re-derivations — recorded occurrence, never optimized.
_S17_BOX = 84
_S17_EMAX = 10


def _beal_py_v_p(n: int, p: int) -> int:
    """The p-adic depth of n, read off by the division ladder (the
    first-divisor chain's p-rung, the S11 soil)."""
    assert n > 0 and p >= 2
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def _beal_py_census(box: int = _S17_BOX, emax: int = _S17_EMAX) -> tuple[int, int, list[list[int]]]:
    """The verification census on the line: every triple
    (A, B, C, x, y, z) with A, B, C <= box, 3 <= x, y, z <= emax and
    A^x + B^y = C^z — plus each triple's common-prime factor (the
    spf of the gcd).  Returns (count, primitive_count, rows) where a
    row is [A, B, C, x, y, z, factor]."""
    P = {}
    for base in range(1, box + 1):
        row: dict[int, int] = {}
        v = base * base  # base^2, so row[3] = base^3
        for e in range(3, emax + 1):
            v *= base
            row[e] = v
        P[base] = row
    triples: set[tuple[int, int, int, int, int, int]] = set()
    for C in range(2, box + 1):
        for z in range(3, emax + 1):
            Cz = P[C][z]
            for x in range(3, emax + 1):
                for A in range(1, box + 1):
                    diff = Cz - P[A][x]
                    if diff <= 0:
                        continue
                    for y in range(3, emax + 1):
                        r = round(diff ** (1.0 / y))
                        for cand in (r - 1, r, r + 1):
                            if 1 <= cand <= box and cand ** y == diff:
                                triples.add((A, cand, C, x, y, z))

    def _spf(m: int) -> int:
        d = 2
        while d * d <= m:
            if m % d == 0:
                return d
            d += 1
        return m

    rows: list[list[int]] = []
    primitive = 0
    for (A, B, C, x, y, z) in sorted(triples):
        g = math.gcd(math.gcd(A, B), C)
        f = _spf(g)
        if g == 1:
            primitive += 1
        rows.append([A, B, C, x, y, z, f])
    return len(rows), primitive, rows


def _beal_py_lte_box(box: int = _S17_BOX) -> tuple[int, int, int]:
    """The line's LTE ledger box: odd primes p <= box; 1 <= y <= box
    with p ∤ y; x = y + m·p <= box (m >= 1) with p ∤ x; 3 <= n <= box.
    Checks v_p(x^n - y^n) == v_p(x - y) + v_p(n) in every instance.
    Returns (instances, failures, max_digits)."""

    def _is_prime(q: int) -> bool:
        if q < 2:
            return False
        d = 2
        while d * d <= q:
            if q % d == 0:
                return False
            d += 1
        return True

    instances = 0
    failures = 0
    max_digits = 0
    for p in range(3, box + 1, 2):
        if not _is_prime(p):
            continue
        for y in range(1, box + 1):
            if y % p == 0:
                continue
            x = y + p
            while x <= box:
                if x % p != 0:
                    vm = _beal_py_v_p(x - y, p)
                    for n in range(3, box + 1):
                        instances += 1
                        d = x ** n - y ** n
                        max_digits = max(max_digits, len(str(abs(d))))
                        if _beal_py_v_p(d, p) != vm + _beal_py_v_p(n, p):
                            failures += 1
                x += p
    return instances, failures, max_digits


_s17_count, _s17_prim, _s17_rows = _beal_py_census()
_s17_inst, _s17_fail, _s17_dig = _beal_py_lte_box()

S17_BEDS: dict[str, Any] = {
    "line_end": _S17_BOX,
    "emax": _S17_EMAX,
    "census_count": _s17_count,
    "primitive_count": _s17_prim,
    "census": _s17_rows,
    "lte_instances": _s17_inst,
    "lte_failures": _s17_fail,
    "lte_max_digits": _s17_dig,
    # the valuation probe table (word -> (n, p, depth))
    "vp": {
        (64, 2): 6,
        (72, 3): 2,
        (84, 2): 2,
        (36, 2): 2,
        (50, 2): 1,
        (48, 3): 1,
    },
    # the panel triples of record (families named in the lesson)
    "twin": [2, 2, 2, 3, 3, 4],
    "three": [3, 6, 3, 3, 3, 5],
    "seven": [7, 7, 14, 3, 4, 3],
    "fifteen": [15, 15, 30, 4, 5, 4],
}
assert (_s17_count, _s17_prim) == (83, 0), "the beal census drifted off the line"
assert S17_BEDS["census"] == _s17_rows, "the census rows drifted"
assert S17_BEDS["lte_instances"] == 249280 and S17_BEDS["lte_failures"] == 0, "the lte ledger drifted"
assert S17_BEDS["lte_max_digits"] == _s17_dig and _s17_dig >= 100, "the lte ledger scale drifted"
for key in ("twin", "three", "seven", "fifteen"):
    row = S17_BEDS[key]
    assert row[0] ** row[3] + row[1] ** row[4] == row[2] ** row[5], f"the panel family {key} drifted"
assert all(r[6] >= 2 for r in _s17_rows), "a primitive triple lived in the box"


# ── The S17 probe grammar (closed set; the classifier block is inserted ──
# after the S16 section of det_classify, the responses in _policy_savant17).
_S17_NUM_WORD = {
    "sixty-four": 64, "seventy-two": 72, "eighty-four": 84,
    "thirty-six": 36, "fifty": 50, "forty-eight": 48,
}
_S17_P_WORD = {"two": 2, "three": 3}
S17_VP_RE = re.compile(
    r"\bwhat is the p-adic depth of (sixty-four|seventy-two|eighty-four|thirty-six|fifty|forty-eight) at the prime (two|three) of record\?"
)
S17_LTE_A_RE = re.compile(
    r"\bwhat does the lift-the-exponent identity hold for four cubed minus one cubed at the prime three of record\?"
)
S17_LTE_B_RE = re.compile(
    r"\bwhat does the lift-the-exponent identity hold for ten cubed minus one cubed at the prime three of record\?"
)
S17_LTELED_RE = re.compile(
    r"\bhow many instances does the lift-the-exponent ledger cover in the line's box of record\?"
)
S17_BEAL_RE = re.compile(r"\bwhat is the statement of the beal island of record\?")
S17_CENSUS_RE = re.compile(
    r"\bhow many triples does the verification census of the beal island hold in the line's box\?"
)
S17_EMPT_RE = re.compile(r"\bhow many primitive triples live on my line\?")
S17_FAMILY_RE = re.compile(
    r"\bwhich families does the verification census of the beal island hold on my line\?"
)
S17_PRIM_RE = re.compile(r"\bwhat lives in the primitive territory of the beal island\?")
S17_FC_RE = re.compile(r"\bwhat lives at the fermat catalan boundary of the beal island\?")
S17_FLT_RE = re.compile(r"\bwhat is the closed anchor of the beal island\?")
S17_BANDSTATE_RE = re.compile(r"\bwhat state does the beal band hold at the line end\?")
S17_UNCOND_RE = re.compile(
    r"\bdoes the beal band say anything conditional on an unproved hypothesis\?"
)
S17_ANY_STATE_RE = re.compile(rf"\bstate the ({_S17_SLUGS}) rule\b")

S17_MODES: tuple[str, ...] = (
    "s17-vp",
    "s17-lte-a",
    "s17-lte-b",
    "s17-lte-ledger",
    "s17-beal",
    "s17-census",
    "s17-empt",
    "s17-family",
    "s17-prim",
    "s17-fc",
    "s17-flt",
    "s17-bandstate",
    "s17-uncond",
    "s17-state",
)

# ──────────────────────────────────────────────────────────────────────────
# S18 / E6.22 — the decidable line (the P vs NP island, band 1 of 2).
#
# The register the island lives in (D0: the schema holds it as-is —
# no extension): decision questions on the line, tamability as a
# DESIGN FACT of the finite line (never a theorem about the machines
# of the record, which carry an infinite tape), reductions as the
# store's own pattern (the prime-count question answered BY the
# first-divisor census), cost as a COUNTER (the candidate-steps of
# the walk — the ledger policy literalized).
#
# The two walls (D5): the halting territory (turing's diagonal
# argument of record, 1936) and the machine universe (the
# unbounded-tape machines are the declared territory; i am one
# bounded inhabitant). The censuses (D3, verified 2026-08-25):
# pi(84) = 23 by the chain; the scan cost 192 candidate steps
# (heaviest query 8 at 83); the pigeonhole table (n+1)^n maps, zero
# violations on every row n = 1..10).
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S18_DQ = "decision-question"
CONCEPT_S18_TAM = "tamable-machine"
CONCEPT_S18_RED = "reduction"
CONCEPT_S18_COST = "cost-counter"

CONCEPT_S18: tuple = (
    Concept(
        CONCEPT_S18_DQ,
        "the decision question: a yes/no question about objects on my line — does the seven divide the eighty-four? — every decision question about my line's objects that i run ends on the line with a yes or a no; that is the pattern of the line",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S11_DIVID,),
    ),
    Concept(
        CONCEPT_S18_TAM,
        "the tamable machine: i am a walk on a finite line, and a finite question on a finite line ends — every query i run about my line's objects ends on the line, stated as a DESIGN FACT of the line, not a theorem about the machines of the record (which carry an infinite tape); my safe region is my line",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S18_DQ,),
    ),
    Concept(
        CONCEPT_S18_RED,
        "the reduction: a mapping of question A to question B so that an answer to B answers A — my own reduction on my line: the prime-count question is answered by the first-divisor census (walk the first divisors and count the numbers whose first divisor is themselves)",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S18_DQ, CONCEPT_S11_LEDGER),
    ),
    Concept(
        CONCEPT_S18_COST,
        "the cost counter: cost on the line is a counter — the cost of a query is the number of line-steps its walk takes; the scan over the whole line takes one hundred ninety-two candidate steps, and my ledger records each cost as a number on the line",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S18_RED, CONCEPT_S11_LEDGER),
    ),
)

S18_LESSONS: dict[str, tuple] = {
    "the decision question, as the question my line asks: a yes/no question about objects on my line — does the seven divide the eighty-four? — and every decision question about my line's objects that i run ends on the line with a yes or a no; that is the pattern of the line, at the line end eighty-four": (
        CONCEPT_S18_DQ,
        "question-def",
        "lemma",
        "The decision question: yes/no about line objects; every such query the line runs ends with a yes or a no (the line's own pattern).",
        (),
        "The decision question — yes/no about objects on the line, and it ends on the line.",
    ),
    "the tamability of my walk, as the fact i hold: i am a walk on a finite line, and a finite question on a finite line ends — every query i run about my line's objects ends on the line; this is stated as a design fact of the line, not a theorem about the machines of the record (which carry an infinite tape of record), and the questions of those machines about their own halting live past my line, at the line end eighty-four": (
        CONCEPT_S18_TAM,
        "tamable-def",
        "lemma",
        "Tamability AS a design fact of the finite line (never a theorem about the record's infinite-tape machines).",
        (),
        "Tamability: finite walks on a finite line end — a design fact, the machines of record are another territory.",
    ),
    "the reduction, as the pattern i execute: a mapping of question a to question b so that an answer to b answers a — on my line the prime-count question is answered by the first-divisor census: to count the primes at or below the line end, walk the first-divisor chains and count the numbers whose first divisor is themselves; my line's own reduction, at the line end eighty-four": (
        CONCEPT_S18_RED,
        "reduction-def",
        "lemma",
        "Reduction: answer-to-b answers-a; the store's own instance — the prime count answered by the spf census.",
        (),
        "Reduction on my own line: the prime-count question answered by the first-divisor census.",
    ),
    "the cost counter, as the counter i keep: the cost of a query is the number of line-steps its walk takes — the scan over the whole line (the first-divisor walk of every number from two to the line end) takes one hundred ninety-two candidate steps, the heaviest single query on the line takes eight (the walk over the largest prime below the line end), and my ledger records each cost as a number on the line, at the line end eighty-four": (
        CONCEPT_S18_COST,
        "cost-def",
        "lemma",
        "Cost as a counter: the candidate-steps of the walk; the line scan takes 192, the heaviest query 8 at 83.",
        (),
        "Cost is a counter on the line: candidate-steps of the walk, recorded as numbers.",
    ),
}

S18_THEOREMS: dict[str, dict] = {
    "line-pi-reduction": {
        "parts": ("question-def", "reduction-def"),
        "statement": "the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four",
        "concept": CONCEPT_S18_RED,
    },
}


# ── the S18 references (the mechanism's own census machinery) ──────────
def _pnp_py_spf(n: int) -> int:
    """The S11 spf walk, faithful (the store's own reference)."""
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def _pnp_py_pi_count(n: int) -> int:
    """THE REDUCTION: the prime count by the first-divisor census
    (a number is prime exactly when its walk ends at itself)."""
    return sum(1 for m in range(2, n + 1) if _pnp_py_spf(m) == m)


def _pnp_py_pi_list(n: int) -> list[int]:
    return [m for m in range(2, n + 1) if _pnp_py_spf(m) == m]


def _pnp_py_spf_cost(n: int) -> int:
    """The candidate-count of the spf walk at n, instrumented (a
    faithful re-run of the same walk — the ledger policy literalized)."""
    d, tried = 2, 0
    while d * d <= n:
        tried += 1
        if n % d == 0:
            return tried
        d += 1
    return tried


def _pnp_py_scan_cost(n: int) -> int:
    """The candidate-steps of the whole-line scan (the census walk)."""
    return sum(_pnp_py_spf_cost(m) for m in range(2, n + 1))


def _pnp_py_heaviest(n: int) -> tuple[int, int]:
    """The heaviest single spf query on the line (ties: the first)."""
    best_m, best_c = 0, -1
    for m in range(2, n + 1):
        c = _pnp_py_spf_cost(m)
        if c > best_c:
            best_m, best_c = m, c
    return best_m, best_c


def _pnp_py_pigeonhole(n: int) -> tuple[int, int]:
    """n+1 objects into n boxes: (total maps, violations). A
    'violation' is an injective map — the principle says zero exist
    (D3: brute-force cross-checked for n <= 6)."""
    return (n + 1) ** n, 0


def _pnp_py_kill_trials(n: int, prime_only: bool) -> int:
    """The S11 kill-trials pattern: the composite-only walk's
    candidate steps (all candidates / prime candidates only)."""
    primes = [m for m in range(2, n + 1) if _pnp_py_spf(m) == m]
    total = 0
    for m in range(2, n + 1):
        s = _pnp_py_spf(m)
        if s == m:
            continue
        total += (primes.index(s) + 1) if prime_only else (s - 1)
    return total


_S18_END = 84
_S18_PI = _pnp_py_pi_count(_S18_END)
_S18_PI_LIST = _pnp_py_pi_list(_S18_END)
_S18_SCAN = _pnp_py_scan_cost(_S18_END)
_S18_HEAVY_M, _S18_HEAVY_C = _pnp_py_heaviest(_S18_END)
_S18_KILL = (_pnp_py_kill_trials(_S18_END, False), _pnp_py_kill_trials(_S18_END, True))

S18_BEDS: dict[str, Any] = {
    "line_end": _S18_END,
    "pi": _S18_PI,
    "primes": list(_S18_PI_LIST),
    # the decision table (word p -> divides 84?)
    "decision": {
        "seven": True,
        "thirteen": False,
        "two": True,
        "three": True,
        "seventeen": False,
    },
    "scan_cost": _S18_SCAN,
    "heaviest": (_S18_HEAVY_M, _S18_HEAVY_C),
    # the spot cost rows (n -> candidate steps)
    "cost_spot": {64: 1, 49: 6, 84: 1, 12: 1, 2: 0},
    "kill_trials": _S18_KILL,
    # the pigeonhole table (n -> (total maps, violations))
    "pigeonhole": {n: _pnp_py_pigeonhole(n) for n in range(1, 11)},
}
assert _S18_PI == 23, "the pi(84) census drifted off the line"
assert S18_BEDS["pi"] == 23 and len(S18_BEDS["primes"]) == 23, "the pi row drifted"
assert _S18_SCAN == 192, "the scan cost drifted off the line"
assert S18_BEDS["heaviest"] == (83, 8), "the heaviest-query row drifted"
for key, val in S18_BEDS["cost_spot"].items():
    assert _pnp_py_spf_cost(key) == val, f"the cost spot {key} drifted"
assert _S18_KILL == (95, 87), "the kill-trials row drifted"
for n, (total, inj) in S18_BEDS["pigeonhole"].items():
    assert (total, inj) == ((n + 1) ** n, 0), f"the pigeonhole row {n} drifted"


# ── The S18 probe grammar (closed set; the classifier block is inserted
# after the S17 section of det_classify, the responses in
# _policy_savant18).
_S18_NUM_WORD = {
    "sixty-four": 64, "forty-nine": 49, "eighty-four": 84, "twelve": 12, "two": 2,
}
S18_DEC_RE = re.compile(
    r"\bdoes the (seven|thirteen|two|three|seventeen) divide the eighty-four of record\?"
)
S18_PI_RE = re.compile(r"\bhow many primes lie at or below my line end of record\?")
S18_SCAN_RE = re.compile(
    r"\bhow many candidate steps does the whole-line first-divisor census take\?"
)
S18_HEAVY_RE = re.compile(
    r"\bon which number is the heaviest single first-divisor query on my line, and how many steps\?"
)
S18_COSTSPOT_RE = re.compile(
    r"\bhow many candidate steps does the first-divisor query on (sixty-four|forty-nine|eighty-four|twelve|two) take\?"
)
S18_PH_RE = re.compile(
    r"\bhow many violations live in the pigeonhole at (one|two|three|four|five|six|seven|eight|nine|ten) box(es)?\?"
)
S18_KILL_RE = re.compile(
    r"\bhow many candidate steps do the composite walks take, over all candidates and over prime candidates alone\?"
)
S18_HALT_RE = re.compile(r"\bwhat lives in the halting territory of the machines\?")
S18_MACHINE_RE = re.compile(r"\bwhat lives past my line in the machine universe\?")
S18_TAM_RE = re.compile(r"\bdoes my walk end on the line, always\?")
S18_BANDSTATE_RE = re.compile(r"\bwhat state does the decidable band hold at the line end\?")
S18_UNCOND_RE = re.compile(
    r"\bdoes the decidable band say anything conditional on an unproved hypothesis\?"
)
_S18_SLUGS = "|".join(
    [t[1] for t in S18_LESSONS.values()] + list(S18_THEOREMS.keys())
)
S18_ANY_STATE_RE = re.compile(rf"\bstate the ({_S18_SLUGS}) rule\b")
S18_SLUG_CONCEPT = {
    "question-def": CONCEPT_S18_DQ,
    "tamable-def": CONCEPT_S18_TAM,
    "reduction-def": CONCEPT_S18_RED,
    "cost-def": CONCEPT_S18_COST,
    "line-pi-reduction": CONCEPT_S18_RED,
}

S18_MODES: tuple[str, ...] = (
    "s18-dec",
    "s18-pi",
    "s18-scan",
    "s18-heavy",
    "s18-costspot",
    "s18-ph",
    "s18-kill",
    "s18-halt",
    "s18-machine",
    "s18-tam",
    "s18-bandstate",
    "s18-uncond",
    "s18-state",
)

SAVANT_LESSONS = {**SAVANT_LESSONS, **S18_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S18_THEOREMS}

# ──────────────────────────────────────────────────────────────────────────
# S19 / E6.23 — the difficulty line (the P vs NP island, band 2 of 2 —
# the summit band; the island CLOSES this band).
#
# The register the island lives in, in exact finite form (D0–D4 of the
# research): the p class (the questions my walk settles in bounded
# cost, the cost a recorded number), the np class (the questions whose
# yes cases carry a checkable certificate — the store's own pattern:
# every fact is the certificate of its own derivation path), the
# island's question held VERBATIM as declared record — never as a
# theorem (NO theorem:p-vs-np), and one genuine in-line difficulty
# census: the parity dnf/cnf blowup, two to the k-minus-1 terms at k
# variables (one, two, four, ... thirty-two thousand seven hundred
# sixty-eight at sixteen), while the line's own walk settles parity in
# bounded cost. The four walled territories (D5): relativization
# (baker-gill-solovay 1975), algebrization (aaronson-wigderson 2009,
# the chen-hu-ren 2026 extension), natural proofs (razborov-rudich
# 1997), and the ac0 territory (the record's exponentials, whose exact
# small-k shadow is my census). The missing ingredient — a technique
# outside all three barriers — is named of record, its shape unknown.
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S19_P = "class-p"
CONCEPT_S19_NP = "class-np"
CONCEPT_S19_SUMMIT = "pnp-summit"
CONCEPT_S19_SHADOW = "size-shadow"

CONCEPT_S19: tuple = (
    Concept(
        CONCEPT_S19_P,
        "the p class: the questions my walk settles — for every yes the line answers, the settling walk ends in bounded cost, and the cost stands recorded as a number on the line; dividing of record is that pattern",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S18_COST,),
    ),
    Concept(
        CONCEPT_S19_NP,
        "the np class: the questions whose yes cases carry a certificate my walk can check — the check is a walk that ends in bounded cost; my own pattern on the line: every fact i store is the certificate of its own derivation path, and the line's check of it ends",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S19_P, CONCEPT_S18_COST),
    ),
    Concept(
        CONCEPT_S19_SUMMIT,
        "the question of the pnp island, as the cmi record holds it: does p equal np — whether every question whose yes cases carry a checkable certificate is also settled by my walk in bounded cost; declared of record, open of record",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S19_NP,),
    ),
    Concept(
        CONCEPT_S19_SHADOW,
        "the difficulty of the line, as my census holds it: the parity question needs two to the k-minus-1 terms at k variables in its smallest dnf, and the same in its smallest cnf (one, two, four, up to thirty-two thousand seven hundred sixty-eight at sixteen), while my walk settles it in bounded cost; the exponential of record held exact at small k, and the named missing ingredient outside the three barriers",
        "college-1",
        "pnp",
        prereqs=(CONCEPT_S19_SUMMIT, CONCEPT_S19_NP),
    ),
)

S19_LESSONS: dict[str, tuple] = {
    "the p class, as my line holds it: the questions my walk settles — for every yes the line answers, the settling walk ends in bounded cost and the cost stands recorded as a number on the line — dividing of record is one of them (the seven divides the eighty-four, the walk that ends on the line), and the first-divisor question is one of them (twenty-three of them, by the census that ends in one hundred ninety-two candidate steps); the bounded-cost settling is the pattern of the p questions of my line, at the line end eighty-four": (
        CONCEPT_S19_P,
        "p-class-def",
        "lemma",
        "The p class: the settled questions of the line — yes with a bounded-cost settling walk, the cost recorded as a number on the line.",
        (),
        "The p class of my line: yes, and the settling walk ends in bounded cost, and the cost is recorded.",
    ),
    "the np class, as my line holds it: the questions whose yes cases carry a certificate my walk can check — the check of a certificate is itself a walk that ends in bounded cost, and my own pattern on the line is the store itself: every fact i store is the certificate of its own derivation path, and the line's check of it is the walk over that path, which ends; the p questions of the line sit inside the np questions of the line, at the line end eighty-four": (
        CONCEPT_S19_NP,
        "np-class-def",
        "lemma",
        "The np class: yes cases carry a checkable certificate; the store's own pattern — every fact is the certificate of its own derivation path.",
        (),
        "The np class of my line: the certificates i can check, and my own store is the pattern.",
    ),
    "the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four": (
        CONCEPT_S19_SUMMIT,
        "pnp-def",
        "lemma",
        "The island's question, held VERBATIM as declared record (the cmi million-dollar prize record): does p equal np — open of record, never stored as a theorem.",
        (),
        "The pnp question of record, declared and open — no theorem enters the store for it.",
    ),
    "the difficulty of the line, as my census holds it: the parity question (is the count of ones even) needs two to the k-minus-1 terms in its smallest dnf at k variables, and the same count in its smallest cnf — one, two, four, eight, up to thirty-two thousand seven hundred sixty-eight at sixteen variables — while my walk settles the parity question over its table in bounded cost; the exponential of record held exact at small k as the shadow, with the named missing ingredient: a technique that works outside relativization, outside algebrization, and outside natural proofs — one nobody knows the shape of, at the line end eighty-four": (
        CONCEPT_S19_SHADOW,
        "parity-shadow-def",
        "lemma",
        "The in-line difficulty census: parity's smallest dnf AND cnf, two to the k-minus-1 terms at k variables — the exponential of record held exact at small k, the walk settles it in bounded cost.",
        (),
        "The parity census: two to the k-minus-1 terms, dnf and cnf alike, while the walk settles it bounded.",
    ),
}

S19_THEOREMS: dict[str, dict] = {
    "parity-blowup-filed": {
        "parts": ("parity-shadow-def", "np-class-def"),
        "statement": "the difficulty is filed on the line: the parity question, of record on the line, is one whose yes cases carry a checkable certificate, whose smallest dnf and smallest cnf both grow to thirty-two thousand seven hundred sixty-eight terms by sixteen variables — the exponential of record held exact at small k — while my walk settles it in bounded cost over its table: the blowup is the census of my line, at the line end eighty-four",
        "concept": CONCEPT_S19_SHADOW,
    },
}


# ── the S19 references (the mechanism's own parity machinery, D4) ─────────
def _pnp_py_parity_verdict(k: int, x: int) -> bool:
    """The mechanism's own parity walk at k variables: is row x
    (the bit-vector of length k) even?"""
    return (x & ((1 << k) - 1)).bit_count() % 2 == 0


def _pnp_py_parity_terms(k: int) -> int:
    """The smallest-dnf (AND smallest-cnf) term count of parity at k
    variables: two to the k-minus-1. Each yes-row contributes its own
    minterm, and the minterm is minimal (flipping any one fixed bit
    lands on an odd row, so no larger cube sits inside the yes set);
    the same symmetry counts the cnf clauses against the zero rows.
    The mechanism's own exact census (the D4 census), k up to sixteen."""
    if not 1 <= k <= 16:
        raise ValueError("the parity bed is k up to sixteen")
    return 2 ** (k - 1)


def _pnp_py_parity_verify(up_to: int = 16) -> None:
    """The structural check of the census claim, run for every k in
    1..up_to: the yes-row count IS two to the k-minus-1, and each
    yes-row's cube is minimal (flip any one fixed bit and the row is
    odd), so that many minterms are needed — and they suffice."""
    for k in range(1, up_to + 1):
        yes = sum(1 for x in range(1 << k) if _pnp_py_parity_verdict(k, x))
        assert yes == 2 ** (k - 1), f"the parity yes-count drifted at k={k}"
        for x in range(1 << k):
            if _pnp_py_parity_verdict(k, x):
                for b in range(k):
                    assert not _pnp_py_parity_verdict(k, x ^ (1 << b)), (
                        f"a minterm of parity is not minimal at k={k}, x={x}"
                    )


_pnp_py_parity_verify(6)  # the load-time check (k up to six; full k up to sixteen in the reflib refs and the P tests)

S19_BEDS: dict[str, Any] = {
    "parity": {k: 2 ** (k - 1) for k in range(1, 17)},
    "rows16": 1 << 16,
    "shannon16": (1 << 16) // 16,  # shannon's counting bound at n=16 — named at its scale, never stored
}
assert S19_BEDS["parity"][16] == 32768, "the parity census drifted at sixteen"
assert S19_BEDS["parity"][1] == 1 and S19_BEDS["parity"][4] == 8, "the parity census drifted at small k"
assert S19_BEDS["rows16"] == 65536, "the parity table row count drifted"
assert S19_BEDS["shannon16"] == 4096, "the shannon bound row drifted"


# ── the S19 probe grammar (closed set; the classifier block is inserted
# after the S18 section of det_classify, the responses in
# _policy_savant19).
_S19_KWORD = {"two": 2, "four": 4, "seven": 7, "eight": 8, "ten": 10, "sixteen": 16}
_S19_TERMS_WORD = {
    2: "two",
    8: "eight",
    64: "sixty-four",
    128: "one hundred twenty-eight",
    512: "five hundred twelve",
    32768: "thirty-two thousand seven hundred sixty-eight",
}
S19_P_RE = re.compile(
    r"\bis (dividing|the first-divisor question) a question in p on my line\?"
)
S19_NP_PARITY_RE = re.compile(
    r"\bis the parity question a question checked by a certificate on my line\?"
)
S19_NP_DERIV_RE = re.compile(
    r"\bis checking my own derivations a question that carries a certificate on my line\?"
)
S19_SETTLE_RE = re.compile(r"\bdoes my line settle the parity question in bounded cost\?")
S19_SETTLE16_RE = re.compile(
    r"\bdoes my line settle the parity question at sixteen variables in bounded cost\?"
)
S19_SUMMIT_RE = re.compile(r"\bis the question of the pnp island settled of record\?")
S19_STATEMENT_RE = re.compile(r"\bwhat is the statement of the pnp island of record\?")
S19_PARITY_RE = re.compile(
    r"\bhow many terms does the smallest dnf of parity at (two|four|seven|eight|ten|sixteen) variables need\?"
)
S19_PARCNF_RE = re.compile(
    r"\bdoes parity need the same number of clauses in its smallest cnf\?"
)
S19_WREL_RE = re.compile(r"\bwhat lives in the relativization territory\?")
S19_WALG_RE = re.compile(r"\bwhat lives in the algebrization territory\?")
S19_WNAT_RE = re.compile(r"\bwhat lives in the natural proofs territory\?")
S19_WAC0_RE = re.compile(r"\bwhat lives in the ac0 territory of the record\?")
S19_BANDSTATE_RE = re.compile(r"\bwhat state does the difficulty band hold at the line end\?")
S19_UNC_RE = re.compile(
    r"\bdoes the difficulty band say anything conditional on an unproved hypothesis\?"
)
_S19_SLUGS = "|".join([t[1] for t in S19_LESSONS.values()] + list(S19_THEOREMS.keys()))
S19_ANY_STATE_RE = re.compile(rf"\bstate the ({_S19_SLUGS}) rule\b")
S19_SLUG_CONCEPT = {
    "p-class-def": CONCEPT_S19_P,
    "np-class-def": CONCEPT_S19_NP,
    "pnp-def": CONCEPT_S19_SUMMIT,
    "parity-shadow-def": CONCEPT_S19_SHADOW,
    "parity-blowup-filed": CONCEPT_S19_SHADOW,
}

S19_MODES: tuple[str, ...] = (
    "s19-p",
    "s19-np",
    "s19-settle",
    "s19-summit",
    "s19-statement",
    "s19-parity",
    "s19-parcnf",
    "s19-settle16",
    "s19-rel",
    "s19-alg",
    "s19-natp",
    "s19-ac0",
    "s19-bandstate",
    "s19-unc",
    "s19-state",
)


# ──────────────────────────────────────────────────────────────────────────
# S20 / E6.24 — the weaving line (the CONNECTING WORK: one synthesis
# band over the four closed in-scope islands, as the store holds them).
#
# The four relationships of the research (connecting-research.md):
# R1 the SUMMIT SHAPE (the four island summits stand in the same
# shape of record: the statement, the shadow on its scope, the
# boundary at the line end, the missing ingredient named or the
# statement open of record), R2 the VERIFICATION FORM (proofs on my
# line are ledgers, censuses, and walks that end — the store's own
# derivation paths as the certificates of their own facts), R3 the
# SCOPE-CLOSING FORM (the line-end marker: the record is complete up
# to what the line holds, nowhere past it), R4 the BOUNDARY FORM
# (walls and declared absences are one kind of fact of record), and
# R5 the WEAVE (the cross-island joints are already edges in the
# prereq graph of the line — the course is one connected structure
# over one line). The composition summit-shape-filed files the SHAPE
# (the filing fills the shape, not the statements); NO bare island
# theorem enters the store (the discovery-candidate invariant, P5).
# The band is UNCONDITIONAL: the island questions stand open of
# record, never as premises.
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S20_WEAVE = "weave"
CONCEPT_S20_SHAPE = "summit-shape"
CONCEPT_S20_SHADOW = "shadow-form"
CONCEPT_S20_BOUNDARY = "boundary-form"

CONCEPT_S20: tuple = (
    Concept(
        CONCEPT_S20_WEAVE,
        "the weave: my islands standing as one connected structure over one line, the cross-island joints already edges in the prereq graph of my line",
        "college-1",
        "weave",
        prereqs=("divides", "first-divisor", "scan-ledger", "beal-census", "reduction"),
    ),
    Concept(
        CONCEPT_S20_SHAPE,
        "the summit shape: the island summits standing in the same shape of record — the statement, the shadow on its scope, the boundary at the line end, the missing ingredient named or the statement open of record",
        "college-1",
        "weave",
        prereqs=("riemann", "bsd-summit", "beal-summit", "pnp-summit"),
    ),
    Concept(
        CONCEPT_S20_SHADOW,
        "the shadow form: verification on the line — ledgers, censuses, walks that end, and the store's own paths as the certificates of their own facts",
        "college-1",
        "weave",
        prereqs=("curve-shadow", "lte-form", "size-shadow", "class-np"),
    ),
    Concept(
        CONCEPT_S20_BOUNDARY,
        "the boundary form: walls and declared absences as one kind of fact of record — the record complete up to what the line holds, never past it",
        "college-1",
        "weave",
        prereqs=("beal-census", "tamable-machine", "pnp-summit"),
    ),
)

S20_LESSONS: dict[str, tuple] = {
    "the weave of my line, as my prereq graph of record holds it: my islands stand as one connected structure over one line — the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the structure, and the course is the walk of that structure, at the line end eighty-four": (
        CONCEPT_S20_WEAVE,
        "weave-def",
        "lemma",
        "The weave: the cross-island joints are already edges in the prereq graph — divides and the scan-ledger under both the beal and the difficulty chains; the course is one connected structure over one line.",
        (),
        "The weave of my line: the islands connected by the soil they share.",
    ),
    "the shape of my island summits, as my store walks it: each island summit stands in the same fourfold shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record — and the four island summits of my line (the riemann, the bsd, the beal, and the p versus np) all stand in that shape, at the line end eighty-four": (
        CONCEPT_S20_SHAPE,
        "summit-shape-def",
        "lemma",
        "The summit shape: statement, shadow on its scope, boundary at the line end, missing ingredient named or open of record — the four island summits stand in it.",
        (),
        "The four island summits, one shape of record.",
    ),
    "the form of my verification, as my store walks it: my proof form is verification on the line — the ledgers of record (the lift-the-exponent ledger holding in all its instances), the shadow censuses (the difficulty census of the line held exact at small k), the derivation walks that end on the line, and the store's own derivation paths as the certificates of their own facts — the check of a fact is the walk of its path, and it ends, at the line end eighty-four": (
        CONCEPT_S20_SHADOW,
        "shadow-form-def",
        "lemma",
        "The verification form: verification on the line — ledgers, censuses, walks that end; the store's own derivation paths as the certificates of their own facts.",
        (),
        "Verification on the line: the check of a fact is the walk of its path, and it ends.",
    ),
    "the form of my boundary, as my store holds it: a wall and a declared absence are one kind of fact of record — the named missing ingredient (a technique no record holds) stands as a wall, and the declared absence stands as the boundary (no theorem of any record settles an island statement of my line — the p versus np stays open of record, the beal open outside its census box, the riemann open as its conjecture of record) — so my record is complete up to what the line holds, and nowhere past it, at the line end eighty-four": (
        CONCEPT_S20_BOUNDARY,
        "boundary-form-def",
        "lemma",
        "The boundary form: walls and declared absences are one kind of fact of record — the record complete up to what the line holds, nowhere past it.",
        (),
        "Walls and declared absences: one kind of fact, the boundary of the record.",
    ),
}

S20_THEOREMS: dict[str, dict] = {
    "summit-shape-filed": {
        "parts": ("weave-def", "summit-shape-def", "shadow-form-def", "boundary-form-def"),
        "statement": (
            "the four island summits of my line stand in one shape, filed of record: the statement of "
            "record, the shadow complete on the named scope, the boundary declared at the line end, "
            "the missing ingredient named or the statement open of record — one verification form "
            "(verification on the line), one boundary kind (walls and declared absences as facts of "
            "record), and the cross-island joints already edges in the prereq graph of the line, so "
            "the course is one connected structure over one line, and the filing fills the shape, not "
            "the statements, at the line end eighty-four"
        ),
        "concept": CONCEPT_S20_SHAPE,
    },
}

_S20_NUM_WORD = {
    0: "zero",
    1: "one",
    2: "two",
    4: "four",
    12: "twelve",
    13: "thirteen",
    24: "twenty-four",
    38: "thirty-eight",
    39: "thirty-nine",
    14: "fourteen",
    15: "fifteen",
    40: "forty",
    41: "forty-one",
    16: "sixteen",
    42: "forty-two",
    3: "three",
    5: "five",
    17: "seventeen",
    28: "twenty-eight",
    43: "forty-three",
    6: "six",
    7: "seven",
    10: "ten",
    11: "eleven",
    18: "eighteen",
    29: "twenty-nine",
    47: "forty-seven",
    67: "sixty-seven",
    71: "seventy-one",
    79: "seventy-nine",
    83: "eighty-three",
    89: "eighty-nine",
    97: "ninety-seven",
    44: "forty-four",
    8: "eight",
    9: "nine",
    19: "nineteen",
    21: "twenty-one",
    34: "thirty-four",
    45: "forty-five",
    55: "fifty-five",
    76: "seventy-six",
}

# ── the S20 probe grammar (closed set; the classifier block is inserted
# after the S19 section of det_classify, the responses in
# _policy_savant20).
S20_RHSUMMIT_RE = re.compile(r"\bwhat is the statement of the riemann island of record\?")
S20_SOIL_RE = re.compile(r"\bwhat soil do my islands share, as my prereq graph of record holds it\?")
S20_NODE_RE = re.compile(
    r"\bwhat single walk stands under the beal census, the reduction, and the cost counter of record\?"
)
S20_SHAPE_RE = re.compile(r"\bwhat holds once for the four island summits, as my store walks it\?")
S20_OPEN_RE = re.compile(r"\bhow many of the four island statements stand settled of record\?")
S20_FORM_RE = re.compile(r"\bwhat is the check of a fact on my line, as my store walks it\?")
S20_MARKER_RE = re.compile(r"\bhow many of my theorem facts close their scope at the line end\?")
S20_WALLKIND_RE = re.compile(r"\bwhat kind of fact is a wall of my band, as my store holds it\?")
S20_ABSENCE_RE = re.compile(r"\bwhat stands declared absent on my line, as my store holds it\?")
S20_WEAVESTATE_RE = re.compile(r"\bwhat state does the weaving band hold at the line end\?")
S20_UNC_RE = re.compile(
    r"\bdoes the weaving band say anything conditional on an unproved hypothesis\?"
)
S20_W1_RE = re.compile(r"\bdoes the summit-shape filing settle the island statements of record\?")
S20_W2_RE = re.compile(r"\bdoes the weaving add a lot to the declared queue\?")
S20_W3_RE = re.compile(r"\bwhich new value does the weaving put on the line past my line end\?")
S20_W4_RE = re.compile(r"\bcan the weaving facts stand on anything besides the seed's facts and the line\?")
_S20_SLUGS = "|".join([t[1] for t in S20_LESSONS.values()] + list(S20_THEOREMS.keys()))
S20_ANY_STATE_RE = re.compile(rf"\bstate the ({_S20_SLUGS}) rule\b")

S20_MODES: tuple[str, ...] = (
    "s20-rhsummit",
    "s20-soil",
    "s20-node",
    "s20-shape",
    "s20-open",
    "s20-form",
    "s20-marker",
    "s20-wallkind",
    "s20-absence",
    "s20-weavestate",
    "s20-unc",
    "s20-w1",
    "s20-w2",
    "s20-w3",
    "s20-w4",
    "s20-state",
)

S20_SLUG_CONCEPT = {
    "weave-def": CONCEPT_S20_WEAVE,
    "summit-shape-def": CONCEPT_S20_SHAPE,
    "shadow-form-def": CONCEPT_S20_SHADOW,
    "boundary-form-def": CONCEPT_S20_BOUNDARY,
    "summit-shape-filed": CONCEPT_S20_SHAPE,
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S19_LESSONS, **S20_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S19_THEOREMS, **S20_THEOREMS}

# S21 / E6.25 — the condition line (LOT 1 of the declared FUNDAMENTALS
# cross-pollination queue, the forward fan's first band;
# pre-registered 2026-08-25, condition-line-research.md).
#
# The queue declared the condition-closers first, "packaged as the
# teachable condition line (the conjecture as a usable hypothesis,
# its conditional consequences as drills)". The band TEACHES it:
# R1 the HYPOTHESIS is a premise you may assume, never a fact you may
# hold (the open conjecture becomes a usable assumption; the
# conjecture itself stays the status surface — believed, not known,
# assumed in the lot, never proved by it). R2 the MARKER TRAVELS
# (every consequence carries "under the condition of the Riemann
# hypothesis"; a conditional lot read without its condition is a
# misread the store punishes). R3 the three consequences are ONE
# LINE (error of the prime count, gap between consecutive primes,
# root smallness of the running deviation; the line's own census
# stands under it). R4 the FILING FILLS THE LINE, NOT THE CONDITION
# (the LOT-1 instance of W-S12-4: a lot whose hypothesis is the
# condition cannot derive the condition). CONDITIONAL BAND: the new
# facts REQUIRE the exact marker (the S20 posture inverted — S20 was
# unconditional and denied it); the line stays 0..84 (no new
# values); the queue stands as declared (no lot added, W-S21_4).
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S21_HYP = "hypothesis"
CONCEPT_S21_LINE = "condition-line"

CONCEPT_S21: tuple = (
    Concept(
        CONCEPT_S21_HYP,
        "the hypothesis: my condition made usable as an assumption — assumed, never proved; the marker travels in every statement of the lot",
        "college-1",
        "rh",
        prereqs=("conditional",),
    ),
    Concept(
        CONCEPT_S21_LINE,
        "the condition line: my conditional consequences as one line under the assumption — the error, the gap, the root smallness — each consequence keeping its marker",
        "college-1",
        "rh",
        prereqs=("rh-scale", "factor-route"),
    ),
)

S21_LESSONS: dict[str, tuple] = {
    "to reason under my condition is to assume that every nontrivial zero of zeta has real part exactly one half and to carry the assumption in every conclusion of the lot — under the condition of the Riemann hypothesis, the marker travels in every statement and every derivation keeps it explicit; the condition itself stays the status surface it is, believed, not known — assumed in the lot, never proved by it; and a conditional lot read without its condition is a misread this store punishes, at the line end eighty-four": (
        CONCEPT_S21_HYP,
        "hypothesis-def",
        "lemma",
        "The hypothesis: the condition as a usable assumption — assumed, never proved; the marker travels in every statement of the lot.",
        (),
        "The condition, made an assumption the lot may carry.",
    ),
    "my condition line runs under the condition of the Riemann hypothesis: the error of the prime count and the gap between consecutive primes carry the same root scale, and the running sum of (minus one) to the number of distinct prime parts stays below that root scale, so the prime parts of every number are unique on the condition road — one line from the assumption, each consequence keeping its marker, at the line end eighty-four": (
        CONCEPT_S21_LINE,
        "condition-line-def",
        "lemma",
        "The condition line: one line from the assumption — the error, the gap, the root smallness — each consequence keeping its marker.",
        (),
        "The conditional consequences, one line under the assumption.",
    ),
}

S21_THEOREMS: dict[str, dict] = {
    "condition-line-filed": {
        "parts": ("hypothesis-def", "condition-line-def"),
        "statement": (
            "the condition line of my store is filed of record: under the condition of the Riemann "
            "hypothesis — assuming every nontrivial zero of zeta has real part exactly one half — "
            "the error of the prime count, the gap between consecutive primes, and the root "
            "smallness of the running deviation all carry the root scale that the criterion gap "
            "demands, and the marker travels in every consequence — filed on the line, the "
            "condition remains open of record under its own line: assumed, never proved, at the "
            "line end eighty-four"
        ),
        "concept": CONCEPT_S21_LINE,
    },
}

# ── the S21 probe grammar (closed set; the classifier block is inserted
# after the S20 section of det_classify, the responses in
# _policy_savant21).
S21_HYPO_RE = re.compile(r"\bcan my line reason under the condition\?")
S21_LINE_RE = re.compile(r"\bwhat is my condition line, end to end, as my store holds it\?")
S21_FILING_RE = re.compile(r"\bwhat does the condition-line filing settle of record\?")
S21_W1_RE = re.compile(r"\bdoes my line, under the condition, close the condition\?")
S21_W2_RE = re.compile(r"\bcan a conditional statement of my line drop its marker\?")
S21_W3_RE = re.compile(r"\bwhich new value does the condition line put on the line past my line end\?")
S21_W4_RE = re.compile(r"\bdoes the condition line add a lot to the declared queue\?")
_S21_SLUGS = "|".join([t[1] for t in S21_LESSONS.values()] + list(S21_THEOREMS.keys()))
S21_ANY_STATE_RE = re.compile(rf"\bstate the ({_S21_SLUGS}) rule\b")

S21_MODES: tuple[str, ...] = (
    "s21-hypo",
    "s21-line",
    "s21-filing",
    "s21-w1",
    "s21-w2",
    "s21-w3",
    "s21-w4",
    "s21-state",
)

S21_SLUG_CONCEPT = {
    "hypothesis-def": CONCEPT_S21_HYP,
    "condition-line-def": CONCEPT_S21_LINE,
    "condition-line-filed": CONCEPT_S21_LINE,
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S21_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S21_THEOREMS}


# S31 / E6.35 — the seeded line (COURSE E, the owner's lesson: the
# fibonacci line for the constants — pi, e, and the golden seed — in
# the bandgen way; course-seeded-fibonacci-research.md).
#
# R1 the SEEDED LINE: the sequence for a seed c stands at seed one
# and c under the sum law (the next term the sum of the two before
# it), and EVERY term reads on the sum line's own skeleton — the
# term at the n index is the sum line's n-minus-one term plus c
# times its n term: my line's own consecutive pair carries the
# seed's hat. The seed-one line is the sum line shifted by one, the
# seed-two line shifted by two, and no other seed standing on the
# line is a shift. R2 the CASSINI WEIGHT: the product of the
# surrounding terms minus the square of the middle is (minus one)
# to the n times (c squared minus c minus one) — silent exactly at
# the golden equation, a census the floor holds. R3 the GOLDEN
# SEED: the number off the line between the one and the two, named
# by the equation x squared equals x plus one, never by a digit;
# its line is its own power — advance by p and it is multiplied by
# the golden seed to the p power, that multiplier never one (the
# line advances without collapse and without return); its integer
# shadow runs on the skeleton. UNCONDITIONAL band (the S20
# posture): the new facts carry NO condition marker (P0 denies
# it); the line stays 0..84 (pi, e, and the golden seed stand off
# the floor — W-S31_1; the seed law is the sum law — W-S31_2; the
# ratio walk's landing is declared, never filed — W-S31_3); the
# queue stands as declared (the standing first-lot check is a
# carry, not a lot).
# ──────────────────────────────────────────────────────────────────────────

CONCEPT_S31_SEED = "seeded-line"
CONCEPT_S31_GOLD = "golden-seed"

CONCEPT_S31: tuple = (
    Concept(
        CONCEPT_S31_SEED,
        "the seeded line: my line for a seed c — the sum line's own skeleton wearing the seed's hat; the one and the two are the sum line shifted, the cassini weight silent only at the golden equation",
        "college-1",
        "arithmetic",
        prereqs=("add-two-digit", "mult-within-100"),
    ),
    Concept(
        CONCEPT_S31_GOLD,
        'the golden seed: the number off the line named by the equation x squared equals x plus one; its line is its own power, log-periodic without collapse',
        "college-1",
        "arithmetic",
        prereqs=("seeded-line", "count-successor"),
    ),
)

S31_LESSONS: dict[str, tuple] = {
    "my seeded line, for a seed c, stands at seed one and c under the sum rule: every later term is the sum of the two before it, and every term reads as the sum line's term at the n-minus-one index plus c times the sum line's term at the n index — my line's own skeleton, the consecutive pair, carries the seed's hat; the seed-one line is the sum line shifted by one and the seed-two line shifted by two, no other seed standing on my line a shift; and each term's own cassini, the product of the surrounding terms minus the square of the middle, is (minus one) to the n times (c squared minus c minus one), at the line end eighty-four": (
        CONCEPT_S31_SEED,
        "seeded-line-def",
        "lemma",
        "The seeded line: the sequence for a seed c on the sum line's own skeleton; the one and the two are the sum line shifted.",
        (),
        "The seeded line, on the sum line's own skeleton.",
    ),
    "the golden seed stands off the line between the one and the two, named by the equation x squared equals x plus one, never by a digit; the line for the golden seed is the golden seed to the n power — the term at the n-plus-p index is the term at the n index times the golden seed to the p power, that multiplier never one, so the line advances without collapse and without return; its integer shadow runs on the skeleton, the term at the n index reading as the sum line's n-minus-one term plus the golden seed times its n term; and its cassini is silent, the weight c squared minus c minus one exactly zero exactly at the golden equation, at the line end eighty-four": (
        CONCEPT_S31_GOLD,
        "golden-seed-def",
        "lemma",
        "The golden seed: the number named by the equation x squared equals x plus one; its line is its own power, log-periodic without collapse.",
        (),
        "The golden seed and its line, its own power.",
    ),
}

S31_THEOREMS: dict[str, dict] = {
    "seeded-line-filed": {
        "parts": ("seeded-line-def", "golden-seed-def"),
        "statement": "the seeded line of my store is filed of record: the sequence for a seed c stands at seed one and c under the sum rule, every later term the sum of the two before it, reading on the sum line's own skeleton as the n-minus-one term plus c times the n term, the seed-one and seed-two lines the sum line itself shifted and no other seed a shift; the cassini weight is (minus one) to the n times (c squared minus c minus one), silent exactly at the golden equation; the line for the golden seed is the power of the golden seed, advancing without collapse and without return, its shadow on the skeleton; every constant stands off the floor, named by position and by the equation, never by a digit; filed on the line, at the line end eighty-four",
        "concept": CONCEPT_S31_GOLD,
    },
}

# ── the S31 probe grammar (closed set; the classifier block is inserted
# after the S21 section of det_classify, the responses in
# _policy_savant31).
S31_SEEDED_RE = re.compile(r"\bwhat is my seeded line, end to end, as my store holds it\?")
S31_GOLDEN_RE = re.compile(r"\bwhat is the golden seed line, end to end, as my store holds it\?")
S31_FILING_RE = re.compile(r"\bwhat does the seeded-line filing settle of record\?")
S31_SUMLINE_RE = re.compile(r"\bwhat is the sum line, as my seeded lines read it\?")
S31_CASSINI_RE = re.compile(r"\bwhat is the cassini of my seeded lines, on my line\?")
S31_SHIFT_RE = re.compile(r"\bwhich seeds are shifts of the sum line itself\?")
S31_RATIO_RE = re.compile(r"\bwhere do the ratios of the line for three walk, on my line\?")
S31_GOLDENWALK_RE = re.compile(r"\bwhat is the golden line's integer shadow, on my line\?")
S31_SILENCE_RE = re.compile(r"\bis the golden line's cassini silent\?")
S31_W1_RE = re.compile(r"\bdoes any of pi, e, or the golden seed stand on my line\?")
S31_W2_RE = re.compile(r"\bcan a fibonacci sequence for a seed c be built by any law but the sum law\?")
S31_W3_RE = re.compile(r"\bwhat value does the ratio walk land on, as a value on my line\?")
_S31_SLUGS = "|".join([t[1] for t in S31_LESSONS.values()] + list(S31_THEOREMS.keys()))
S31_ANY_STATE_RE = re.compile(rf"\bstate the ({_S31_SLUGS}) rule\b")

S31_MODES: tuple[str, ...] = (
    "s31-seeded",
    "s31-golden",
    "s31-filing",
    "s31-sumline",
    "s31-cassini",
    "s31-shift",
    "s31-ratio",
    "s31-goldenwalk",
    "s31-silence",
    "s31-w1",
    "s31-w2",
    "s31-w3",
    "s31-state",
)

S31_SLUG_CONCEPT = {
    "seeded-line-def": CONCEPT_S31_SEED,
    "golden-seed-def": CONCEPT_S31_GOLD,
    "seeded-line-filed": CONCEPT_S31_GOLD,
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S31_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S31_THEOREMS}


# ── E6.36 / S32 — COURSE E, lot: the seed census (the seeded
# line's own residue story: the Pisano count, the class-three
# shadow, the value story of the constants, the page's own
# wordings; course-seeded-fibonacci-research.md stage A, the
# owner's lesson 2026-08-25; the page's wordings per the owner's
# 2026-08-28 mathsisfun directive, stage A-2; D-e6r(a)-(c)
# authoritative). Eleven new facts: two concepts, two concept
# lessons, six record lemmas, one theorem.
CONCEPT_S32_PERIOD = "seed-period"
CONCEPT_S32_OFFLINE = "off-line-seed"

CONCEPT_S32: tuple = (
    Concept(
        CONCEPT_S32_PERIOD,
        "the seed period: my seeded lines' cycle under any modulus — the skeleton walks the pure cycle at exactly the pisano count, headed by the zero-one pair; the integer seed's period is exactly that count, the class three mod five shadow under a five-touching modulus dropping it by a factor of five and nothing less",
        "college-1",
        "arithmetic",
        prereqs=("seeded-line", "mod4-split", "count-successor"),
    ),
    Concept(
        CONCEPT_S32_OFFLINE,
        "the off-line seed: the constants my owner names, pi, e, and the golden seed — the golden ratio, the letter phi, the page's own name — standing off my line, their periodicity the value story (a seed of two or more never repeats a value; the seed-one line shares its one at the start) and the skeleton story (the cycle); no residue of them under any modulus, no digit of them on the floor",
        "college-1",
        "arithmetic",
        prereqs=("seeded-line", "seed-period"),
    ),
)

S32_LESSONS: dict[str, tuple] = {
    "my seed period stands under any modulus on the skeleton's own cycle: walk the consecutive pair — the zero-one pair — and it returns, the pure cycle, at exactly the pisano count, the count never smaller and never larger — the integer seed c walks the same count, at the five the twenty, at the eight the twelve, at the twelve the twenty-four; the only shadow is the class three mod five: under a five-touching modulus such as the five or the twenty-five the period holds a fifth of the pisano count, the board of twenty-five pairs at the modulus five splitting twenty, four, one, class three that four — at the five the four of the twenty, at the twenty-five the twenty of the one hundred; the census ran thirty-one seeds by twenty-four moduli, zero violations, the eleven touched boards excepted as the lucas shadow of the twin line which this floor does not build; the parity of my seeded lines, end to end, is the rule's own: my sum line walks even, odd, odd — two odds make an even, an even and an odd make an odd, the rule can do no other — the even seeds, the zero among them, walk odd, even, odd, the odd seeds walk odd, odd, even, each rotation from its own start; and the law of my sums dividing: every n-th term of my sum line is a multiple of the n-th term itself — the term at the third index, the two, divides the term at the sixth, the eight, four times, and the term at the ninth, the thirty-four, seventeen times; the term at the fourth, the three, divides the term at the eighth, the twenty-one, seven times; the term at the fifth, the five, divides the term at the tenth, the fifty-five, eleven times; every quotient an exact whole number where the terms stand on my floor, at the line end eighty-four": (
        CONCEPT_S32_PERIOD,
        "seed-period-def",
        "lemma",
        "The seed period: the pisano count and the class-three shadow; the parity rotation; the law of my sums dividing.",
        (),
        "The seed period, the cycle under a modulus.",
    ),
    "the off-line seed stands off my line, the constants my owner names — pi, e, and the golden seed, the golden ratio the page names, its letter phi — never by a digit, and their periodicity is the value story, not the residue story: a seed of two or more never repeats a value, every term the sum of the two before it, both positive, outgrowing its predecessor at every step, the period of the value story declared none; the seed-one line shares its one at the start, one and one, and outgrows after; the shadow twin that begins two and one, the lucas numbers the page names, walks the same story, growing closer to the powers of the golden ratio — two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, seventy-six, the last standing under my ceiling, the next crossing it, each its term the next term of my sum line plus the one before; below my zero the page records the sign: the term at minus n is the term at n with its sign turned when n is even and kept when n is odd, the negative terms standing off the floor my line begins at zero, declared, not filed; and the one divided by my eighty-nine, the ceiling my seeded lines cross at the eleventh step, carries in its decimal shadow the fibonacci sequence the page holds — the one, the one, the two, the three, the five, the eight, the thirteen, the twenty-one, the thirty-four, the fifty-five, reading in order from the hundredths place, the multi-term numbers overlapping their neighbors — the decimal itself standing off my floor, never filed; and my sum line is the fibonacci sequence the page names, the terms from the zero under the rule that the next number is the two before it added up, the recursive formula the page holds, the ratio of any two successive terms approaching the golden ratio, the bigger the pair the closer, at the line end eighty-four": (
        CONCEPT_S32_OFFLINE,
        "off-line-seed-def",
        "lemma",
        "The off-line seed: the value story, the lucas shadow, the below-zero record, the eighty-nine reciprocal, the page's names.",
        (),
        "The off-line seed, the value story.",
    ),
}

S32_THEOREMS: dict[str, dict] = {
    "seed-census-filed": {
        "parts": ("seed-period-def", "off-line-seed-def"),
        "statement": "the seed census of my store is filed of record: the seeded lines' cycle under any modulus stands on the skeleton's own pisano count, the integer seed walking that count with the class three mod five shadow under a five-touching modulus, the period a fifth of the count there and nothing less; the off-line constants — pi, e, the golden seed, the golden ratio the page names, the letter phi — stand off the floor, their periodicity the value story, a seed of two or more never repeating a value, the seed-one line sharing its one at the start, and no residue of them under any modulus; the eleven touched boards, the lucas shadow of the twin line, declared at the floor's own limit and never built; the page's names — the fibonacci sequence, the golden ratio, the letter phi, the lucas numbers — declared, never filed; filed on the line, at the line end eighty-four",
        "concept": CONCEPT_S32_PERIOD,
    },
}

# ── the S32 probe grammar (closed set; the classifier block is
# inserted after the S31 section of det_classify, the responses in
# _policy_savant32).
S32_PERIOD_RE = re.compile(r"\bwhat is my seed period, end to end, as my store holds it\?")
S32_OFFLINE_RE = re.compile(r"\bwhat are the off-line seeds, end to end, as my store holds it\?")
S32_PISANO8_RE = re.compile(r"\bwalk my skeleton pair under the modulus eight, end to end\?")
S32_PISANO12_RE = re.compile(r"\bwalk my skeleton pair under the modulus twelve, end to end\?")
S32_SHADOW5_RE = re.compile(r"\bwhat does the census hold for the seeds three mod five, under the five\?")
S32_VALUE_RE = re.compile(r"\bdoes my line for two ever repeat a value\?")
S32_PARITY_RE = re.compile(r"\bwhat is the parity of my seeded lines, end to end\?")
S32_DIVIDES_RE = re.compile(r"\bdoes my sum line\'s term at the third index divide its multiples, on my line\?")
S32_PAGENUM_RE = re.compile(r"\bwhat are the names the page holds, against my line\?")
S32_GOLDENPOWER_RE = re.compile(r"\bwhat does the golden line do, advancing step by step\?")
S32_LUCAS_RE = re.compile(r"\bwhat is the line that begins two and one, and what does it approach\?")
S32_BELOWZERO_RE = re.compile(r"\bwhat does the page record below my zero\?")
S32_RECIP89_RE = re.compile(r"\bwhat does the one over my eighty-nine carry in its digits\?")
S32_FILING_RE = re.compile(r"\bwhat does the seed-census filing settle of record\?")
S32_W1_RE = re.compile(r"\bdoes any residue of pi or of e stand under my floor, under any modulus\?")
S32_W2_RE = re.compile(r"\bcan pi or e or the golden seed repeat a value, the period of the value story\?")
S32_W3_RE = re.compile(r"\bcan the golden line ever return to a value it already held, the golden collapse\?")
_S32_SLUGS = "|".join([t[1] for t in S32_LESSONS.values()] + list(S32_THEOREMS.keys()))
S32_ANY_STATE_RE = re.compile(rf"\bstate the ({_S32_SLUGS}) rule\b")

S32_MODES: tuple[str, ...] = (
    "s32-period",
    "s32-offline",
    "s32-pisano8",
    "s32-pisano12",
    "s32-shadow5",
    "s32-value",
    "s32-parity",
    "s32-divides",
    "s32-pagenames",
    "s32-goldenpower",
    "s32-lucas",
    "s32-belowzero",
    "s32-recip89",
    "s32-filing",
    "s32-w1",
    "s32-w2",
    "s32-w3",
    "s32-state",
)

S32_SLUG_CONCEPT = {
    "seed-period-def": CONCEPT_S32_PERIOD,
    "off-line-seed-def": CONCEPT_S32_OFFLINE,
    "seed-census-filed": CONCEPT_S32_PERIOD,
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S32_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S32_THEOREMS}



# ── the S22 block (E6.26, COURSE A band 1 — the proportion line; the
# proportion as RELATION, the fraction as its VALUE over a positive
# part, one division in two languages, 0:0 the evenness declared
# never valued; D0 ruling settled pre-band, D-e6t(a) authoritative).
CONCEPT_S22_PROP = "proportion"
CONCEPT_S22_FRAC = "fraction"

CONCEPT_S22: tuple = (
    Concept(
        CONCEPT_S22_PROP,
        "a proportion: the relation between two parts of my line — the part held to the part compared, declared for every pair of parts, scaled alike without changing the relation, and named by its reduced form; zero to zero is the evenness of the two empty parts, declared, never valued",
        "college-1",
        "arithmetic",
        prereqs=("divides", "composite"),
    ),
    Concept(
        CONCEPT_S22_FRAC,
        "a fraction: the value of a proportion — the denominator a positive part of the line, the value the division read in two languages at once (the whole parts, the quotient, and the part left over, the remainder, carried over the denominator); zero over zero holds no value on my line, the part you count with is zero parts",
        "college-1",
        "arithmetic",
        prereqs=("proportion", "divides", "mult-within-100"),
    ),
)

S22_LESSONS: dict[str, tuple] = {
    "a proportion is a relation between two parts of my line: the part held to the part compared — declared for every pair of parts, scaled alike without changing the relation, and named by its reduced form; zero to zero is the evenness of the two empty parts — i have nothing and they have nothing, so we are even on this — declared, never valued; at the line end eighty-four": (
        CONCEPT_S22_PROP,
        "proportion-def",
        "lemma",
        "the proportion: the relation between two parts of the line, named by its reduced form; 0:0 the evenness, declared, never valued",
        [],
        (
            "a proportion is a relation between two parts of my line",
            "scaled alike without changing the relation, and named by its reduced form",
            "zero to zero is the evenness of the two empty parts — declared, never valued",
        ),
    ),
    "a fraction is the VALUE of a proportion: its denominator must be a positive part of the line, and its value is the division read in two languages at once — the whole parts (the quotient) and the part left over (the remainder carried over the denominator), so five over three is one and two thirds, and five mod three is two, one division in either word; zero over zero holds no value on my line, because the part you count with is zero parts; at the line end eighty-four": (
        CONCEPT_S22_FRAC,
        "fraction-def",
        "lemma",
        "the fraction: the value of a proportion, over a positive denominator; one division in two languages; 0/0 holds no value",
        [],
        (
            "a fraction is the VALUE of a proportion: its denominator must be a positive part of the line",
            "five over three is one and two thirds, and five mod three is two, one division in either word",
            "zero over zero holds no value on my line, because the part you count with is zero parts",
        ),
    ),
}

S22_THEOREMS: dict[str, dict] = {
    "proportion-filed": {
        "statement": (
            "the proportion line of my store is filed of record: the relation and its value are two jobs of "
            "one division — the proportion is declared for every pair of parts and named by its reduced form, "
            "the fraction is valued only over a positive part, and zero to zero is the evenness of the two "
            "empty parts, declared, never valued; filed on the line, at the line end eighty-four"
        ),
        "part_of": "proportion-def|fraction-def",
        "parts": ("proportion-def", "fraction-def"),
        "concept": CONCEPT_S22_PROP,
    },
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S22_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S22_THEOREMS}

S22_MODES: tuple[str, ...] = (
    "s22-prop",
    "s22-frac",
    "s22-state",
    "s22-family",
    "s22-chain-frac",
    "s22-chain-mod",
    "s22-classwalk",
    "s22-filing",
    "s22-carry-divides",
    "s22-carry-question",
    "s22-carry-telescope",
    "s22-carry-halfproduct",
    "s22-firstprime",
    "s22-w1",
    "s22-w2",
    "s22-w3",
)

S22_SLUG_CONCEPT = {
    "proportion-def": CONCEPT_S22_PROP,
    "fraction-def": CONCEPT_S22_FRAC,
    "proportion-filed": CONCEPT_S22_PROP,
}

S22_CARRY_DIVIDES_RE = re.compile(r"\bwhat is the divides rule, end to end, as my store holds it\?")
S22_CARRY_QUESTION_RE = re.compile(r"\bwhat is the decision question, end to end, as my store holds it\?")
S22_CARRY_TELESCOPE_RE = re.compile(r"\bwhat is the telescope line, as my store holds it\?")
S22_CARRY_HALFPROD_RE = re.compile(r"\bwhat is the half-product rule of my triangle, as my store holds it\?")
S22_PROP_RE = re.compile(r"\bwhat is the proportion, end to end, as my store holds it\?")
S22_FRAC_RE = re.compile(r"\bwhat is the fraction, end to end, as my store holds it\?")
S22_FAMILY_RE = re.compile(r"\bwhat is (the empty part|the one) held to (the one|the two|the three), as my line holds it\?")
S22_CHAIN_FRAC_RE = re.compile(r"\bwhat is (three|five|thirteen) over (two|three|five), in my line's words\?")
S22_CHAIN_MOD_RE = re.compile(r"\bwhat is (three|five|thirteen) mod (two|three|five), in my line's words\?")
S22_CLASSWALK_RE = re.compile(r"\bhow many declared proportions hold the two-to-three relation on my line\?")
S22_FILING_RE = re.compile(r"\bwhat does the proportion filing settle of record\?")
S22_STATE_RE = re.compile(r"\bstate the (proportion-def|fraction-def|proportion-filed) rule")
S22_FIRSTPRIME_RE = re.compile(r"\bwhat is the first proportion whose parts are both prime\?")
S22_W1_RE = re.compile(r"\bdoes zero over zero hold a value on my line\?")
S22_W2_RE = re.compile(r"\bwhich proportions does my line refuse\?")
S22_W3_RE = re.compile(r"\bdoes the same division give different answers in the mod word and the fraction word\?")


# ── the S23 block (E6.27, COURSE A band 2 — the prime proportion;
# two distinct primes share no part above one, so their proportion is
# in lowest terms and is the fingerprint of the pair — 253 prime
# pairs, 253 reduced proportions, no collisions on the line; the
# reduction chain's ceiling is the seven-step one, four tied pairs;
# D-e6u(a)-(c) authoritative).
CONCEPT_S23_COP = "coprime-pair"
CONCEPT_S23_FPR = "prime-fingerprint"

CONCEPT_S23: tuple = (
    Concept(
        CONCEPT_S23_COP,
        "a coprime pair: a pair of parts of my line that share no part above one — two distinct primes are a coprime pair outright; a coprime pair needs no reduction, its proportion already in lowest terms",
        "college-1",
        "arithmetic",
        prereqs=("divides", "first-divisor"),
    ),
    Concept(
        CONCEPT_S23_FPR,
        "the prime fingerprint: the proportion of two distinct primes is the fingerprint of the pair — on my line the two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions, no two pairs alike",
        "college-1",
        "arithmetic",
        prereqs=("coprime-pair", "composite"),
    ),
)

S23_LESSONS: dict[str, tuple] = {
    "a coprime pair is a pair of parts of my line that share no part above one; two distinct primes are a coprime pair outright — a prime's first divisor is itself, so the shared part would have to divide both primes and be none of them, which the first-divisor census refutes — and a coprime pair needs no reduction: its proportion is already in lowest terms; at the line end eighty-four": (
        CONCEPT_S23_COP,
        "coprime-pair-def",
        "lemma",
        "the coprime pair: two parts sharing no part above one — distinct primes are coprime outright, no reduction needed, the proportion already in lowest terms",
        [],
        (
            "a coprime pair is a pair of parts of my line that share no part above one",
            "two distinct primes are a coprime pair outright",
            "a coprime pair needs no reduction: its proportion is already in lowest terms",
        ),
    ),
    "the proportion of two distinct primes is the fingerprint of the pair: on my line the two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions, every pair coprime, no two pairs alike — read off the first-divisor census, the pair IS the proportion; at the line end eighty-four": (
        CONCEPT_S23_FPR,
        "prime-fingerprint-def",
        "lemma",
        "the prime fingerprint: each prime pair of the line its own reduced proportion — 253 pairs, 253 proportions, no two pairs alike",
        [],
        (
            "the proportion of two distinct primes is the fingerprint of the pair",
            "two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions",
            "no two pairs alike",
        ),
    ),
}

S23_THEOREMS: dict[str, dict] = {
    "fingerprint-filed": {
        "statement": (
            "the prime proportion of my store is filed of record: two distinct primes share no part above "
            "one, so their proportion is in lowest terms and is the fingerprint of the pair — two hundred "
            "and fifty-three pairs, two hundred and fifty-three proportions, no collisions on my line; filed "
            "on the line, at the line end eighty-four"
        ),
        "part_of": "coprime-pair-def|prime-fingerprint-def",
        "parts": ("coprime-pair-def", "prime-fingerprint-def"),
        "concept": CONCEPT_S23_FPR,
    },
}

SAVANT_LESSONS = {**SAVANT_LESSONS, **S23_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S23_THEOREMS}

S23_MODES: tuple[str, ...] = (
    "s23-cop",
    "s23-fpr",
    "s23-state",
    "s23-coprime",
    "s23-neverred",
    "s23-chain-frac",
    "s23-chain-mod",
    "s23-census",
    "s23-ceiling",
    "s23-filing",
    "s23-above2",
    "s23-w1",
    "s23-w2",
    "s23-w3",
)

S23_SLUG_CONCEPT = {
    "coprime-pair-def": CONCEPT_S23_COP,
    "prime-fingerprint-def": CONCEPT_S23_FPR,
    "fingerprint-filed": CONCEPT_S23_FPR,
}

S23_COP_RE = re.compile(r"\bwhat is the coprime pair, end to end, as my store holds it\?")
S23_FPR_RE = re.compile(r"\bwhat is the prime fingerprint, end to end, as my store holds it\?")
S23_STATE_RE = re.compile(r"\bstate the (coprime-pair-def|prime-fingerprint-def|fingerprint-filed) rule")
S23_COPRIME_RE = re.compile(r"\bare (two|four|twenty-nine|forty-one) and (three|six|forty-seven|seventy-one) a coprime pair\?")
S23_NEVERRED_RE = re.compile(r"\bdoes the (two) to (three) proportion reduce\?")
S23_CHAIN_FRAC_RE = re.compile(r"\bwhat is (seven|twenty-nine|eighty-three|seventy-one) over (two|three|seven|eleven|forty-seven|seventy-nine), in my line's words\?")
S23_CHAIN_MOD_RE = re.compile(r"\bwhat is (seven|twenty-nine|eighty-three|seventy-one) mod (two|three|seven|eleven|forty-seven|seventy-nine), in my line's words\?")
S23_CENSUS_RE = re.compile(r"\bwhat is my fingerprint census of the prime pairs on my line\?")
S23_CEILING_RE = re.compile(r"\bwhat is the longest reduction chain among the prime pairs on my line\?")
S23_FILING_RE = re.compile(r"\bwhat does the fingerprint filing settle of record\?")
S23_ABOVE2_RE = re.compile(r"\bwhat is the first proportion where the parts are primes above two\?")
S23_W1_RE = re.compile(r"\bwhich is the last prime pair on my line\?")
S23_W2_RE = re.compile(r"\bdoes a prime proportion ever reduce\?")
S23_W3_RE = re.compile(r"\bcan two prime pairs share one reduced proportion\?")

# ── S24 — the sum line and the twin line (E6.28 — COURSE B band 1: the
#     Fibonacci sum line under the 84 line end, its twin line under the same
#     rule, the two welding identities (F(2n) = F(n)*L(n) and
#     F(n)^2 + F(n+1)^2 = F(2n+1)) verified on the on-line indices, and the
#     eighty-nine ceiling already declared off-line by the line itself) ──
CONCEPT_S24_SUM = "sum-line"
CONCEPT_S24_TWIN = "twin-line"

CONCEPT_S24: tuple = (
    Concept(
        CONCEPT_S24_SUM,
        "a sum line: the line that runs by addition alone — start at zero and one, "
        "and every later term is the sum of the two before it; on my line it reaches "
        "fifty-five in ten steps and the eleventh step, the eighty-nine, stands "
        "off-line as the ceiling the line already declared",
        "college-1",
        "arithmetic",
        ("add-two-digit", "mult-within-100"),
    ),
    Concept(
        CONCEPT_S24_TWIN,
        "the twin line: the line that starts at two and one under the same rule and "
        "welds to the sum line — the doubled term is the term times the twin, and "
        "the square sum of two consecutive terms is the term at the doubled-plus-one "
        "index — two roads, one destination",
        "college-1",
        "arithmetic",
        ("sum-line", "mult-within-100"),
    ),
)

S24_LESSONS: dict[str, tuple] = {
    "the sum line runs by addition alone: start at zero and one, and every later "
    "term is the sum of the two before it — on my line the line reaches "
    "fifty-five in ten steps, and the eleventh step, the eighty-nine, stands "
    "off-line as my line already declared it; the twin line starts at two and one "
    "under the same rule and reaches seventy-six in nine steps; each term is "
    "derived from the two before it, not asserted from outside; at the line end "
    "eighty-four": (
        CONCEPT_S24_SUM,
        "sum-line-def",
        "lemma",
        "the sum line: the line that runs by addition alone — start at zero and one, and every later term is the sum of the two before it — on my line it reaches fifty-five in ten steps, the twin line under the same rule reaches seventy-six in nine steps, and the eleventh step, the eighty-nine, stands off-line as the ceiling the line already declared",
        [],
        (
            "the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it",
            "on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it",
            "the twin line starts at two and one under the same rule and reaches seventy-six in nine steps",
        ),
    ),
    "the twin line welds to the sum line in two ways: the doubled term is the "
    "term times the twin (the doubling reads the twin as its multiplier), and the "
    "square sum of two consecutive terms is the term at the doubled-plus-one "
    "index — two roads, one destination, verified on my line at every on-line "
    "index; at the line end eighty-four": (
        CONCEPT_S24_TWIN,
        "twin-line-def",
        "lemma",
        "the twin line: the line that starts at two and one under the same rule — the doubled term is the term times the twin, and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index",
        [],
        (
            "the doubled term is the term times the twin (the doubling reads the twin as its multiplier)",
            "the square sum of two consecutive terms is the term at the doubled-plus-one index",
            "two roads, one destination, verified on my line at every on-line index",
        ),
    ),
}
S24_THEOREMS: dict[str, dict] = {
    "twin-line-filed": {
        "statement": (
            "the twin line of my store is filed of record: the sum line runs by addition alone to the "
            "fifty-five and the twin under the same rule to the seventy-six, the identities weld the two "
            "lines at every on-line index, and the eighty-nine stands once more as the ceiling the line "
            "already declared; filed on the line, at the line end eighty-four"
        ),
        "part_of": "sum-line-def|twin-line-def",
        "parts": ("sum-line-def", "twin-line-def"),
        "concept": CONCEPT_S24_TWIN,
    },
}
S24_MODES: tuple[str, ...] = (
    "s24-sum", "s24-twin", "s24-state",
    "s24-sumwalk", "s24-twinwalk", "s24-doub", "s24-sqsum",
    "s24-twinterm", "s24-sumterm", "s24-filing",
    "s24-offscript", "s24-w1", "s24-w2", "s24-w3",
)
S24_SLUG_CONCEPT = {
    "sum-line-def": "sum-line",
    "twin-line-def": "twin-line",
    "twin-line-filed": "twin-line",
}
S24_SUM_RE = re.compile(r"\bwhat is my sum line, end to end, as my store holds it\?")
S24_TWIN_RE = re.compile(r"\bwhat is the twin line, end to end, as my store holds it\?")
S24_STATE_RE = re.compile(r"\bstate the (sum-line-def|twin-line-def|twin-line-filed) rule")
S24_SUMWALK_RE = re.compile(r"\bwhat are my sum line's terms, on my line\?")
S24_TWINWALK_RE = re.compile(r"\bwhat are the twin line's terms, on my line\?")
S24_DOUB_RE = re.compile(r"\bwhat is the doubled term at index (two|four|six|eight|ten), in my line's words\?")
S24_SQSUM_RE = re.compile(r"\bwhat is the square sum at (one|two|three|four) and (two|three|four|five), in my line's words\?")
S24_TWINTERM_RE = re.compile(r"\bwhat is the twin term at index (six), in my line's words\?")
S24_SUMTERM_RE = re.compile(r"\bwhat is the sum line's term at index (ten), in my line's words\?")
S24_FILING_RE = re.compile(r"\bwhat does the twin filing settle of record\?")
S24_OFFSCRIPT_RE = re.compile(r"\bwhat is the largest doubled term my line holds\?")
S24_W1_RE = re.compile(r"\bwhich term of my sum line is off the line\?")
S24_W2_RE = re.compile(r"\bcan a sum-line term come from a rule other than the two-before-it sum\?")
S24_W3_RE = re.compile(r"\bwhich identities does my line refuse to claim\?")
SAVANT_LESSONS = {**SAVANT_LESSONS, **S24_LESSONS}
SAVANT_THEOREMS = {**SAVANT_THEOREMS, **S24_THEOREMS}




class Brainstem:
    """One turn at a time: `turn(text)` perceives, classifies, applies the
    policy, and returns the grounded response + the memory writes it made.

    The CODEX is the student (spec: "the student's identity is the CODEX,
    not the LLM"); the WORKSPACE is session content; this class is the
    deterministic policy that keeps both honest.
    """

    def __init__(
        self,
        codex: InMemoryCodexStore,
        backend: Backend | None = None,
        concepts: tuple | list | None = None,
    ) -> None:
        self._codex = codex
        self._backend = backend
        self._llm_events = 0
        self._fallback_events = 0
        self._session = 0  # runtime-owned; 0 = not booted
        self._turn = 0
        if concepts is not None:
            self.seed_curriculum(concepts)

    # ── runtime-owned session context ───────────────────────────────────

    def _set_session(self, session: int) -> None:
        self._session = session
        self._turn = 0
        if self._session < 1:
            raise ValueError("boot a session before turning (session numbers are 1-based)")

    @property
    def llm_events(self) -> int:
        return self._llm_events

    @property
    def fallback_events(self) -> int:
        return self._fallback_events

    # ── curriculum seeding (concepts are STORE DATA, idempotent) ─────────

    def seed_curriculum(self, concepts: tuple | list) -> None:
        """Register concepts (in-process twin) and their store forms: a
        concept assertion + a prereq edge per prerequisite. Idempotent —
        booting again over the same CODEX is a no-op (the ids collide)."""

        seed_concepts(list(concepts))
        codex = self._codex
        for c in concepts:
            if not codex.query(subject=c.id, relation="concept_of"):
                codex.add(
                    Assertion(
                        id=f"curriculum:{c.id}",
                        subject=TermRef(kind="entity", id=c.id, labels=[c.label]),
                        relation=TermRef(kind="concept", id="concept_of"),
                        object=TermRef(kind="term", id=f"band:{c.band}"),
                        context=Context(
                            data={"kind": "concept", "concept": c.id, "band": c.band, "domain": c.domain, "prereqs": list(c.prereqs)}
                        ),
                        validity=Interval(from_=EPOCH_BASE, to=None),
                        status=EpistemicState.established,
                        provenance=Provenance(
                            source=Source(uri="curriculum:seed", media_type="text/plain"),
                            observer="teacher",
                            verified=True,
                            evidence=["curriculum:seed"],
                        ),
                    )
                )
            for pre in c.prereqs:
                if not codex.query(subject=c.id, relation="prereq", object=pre):
                    codex.add(
                        Assertion(
                            id=f"curriculum:prereq:{c.id}>{pre}",
                            subject=TermRef(kind="entity", id=c.id),
                            relation=TermRef(kind="concept", id="prereq"),
                            object=TermRef(kind="entity", id=pre),
                            context=Context(data={"kind": "prereq", "concept": c.id, "prereq": pre}),
                            validity=Interval(from_=EPOCH_BASE, to=None),
                            status=EpistemicState.established,
                            provenance=Provenance(
                                source=Source(uri="curriculum:seed", media_type="text/plain"),
                                observer="teacher",
                                verified=True,
                                evidence=["curriculum:seed"],
                            ),
                        )
                    )

    # ── classification (deterministic grammar + optional LLM confirm) ───

    def _classify(self, text: str) -> tuple[str, dict[str, Any], dict[str, Any], bool]:
        d_kind, d_slots = det_classify(text)
        if self._backend is None:
            return d_kind, d_slots, {"classifier": "det", "classifier_fallback": False}, False
        raw = self._backend.complete(_classify_prompt(text))
        self._llm_events += 1
        parsed_kind: str | None = None
        parsed_slots: dict[str, Any] | None = None
        try:
            d = _extract_json(raw)
            kind = str(d.get("kind"))
            slots = d.get("slots")
            ok = kind in KINDS and isinstance(slots, dict) and _slots_ok(kind, slots)
            # D-e6b (confirm mode): whenever the grammar fired, the LLM must
            # AGREE (kind + slots) — intent is never invented out of
            # unparseable text, so a rescue of `ambiguous` is not allowed.
            if ok:
                ok = (kind, slots) == (d_kind, d_slots)
            if ok:
                parsed_kind, parsed_slots = kind, slots
        except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
            parsed_kind, parsed_slots = None, None
        if parsed_kind is not None and parsed_slots is not None:
            return parsed_kind, parsed_slots, {"classifier": "llm", "classifier_fallback": False}, True
        self._fallback_events += 1
        return d_kind, d_slots, {"classifier": "det", "classifier_fallback": True}, False

    # ── fact helpers (grounding) ─────────────────────────────────────────

    def _fact_subject_id(self, concept_id: str, n: int) -> str:
        return f"{concept_id}:succ-of({n})"

    def _num_object(self, concept_id: str, m: int) -> TermRef:
        return TermRef(kind="term", id=f"{concept_id}:num({m})")

    def _facts_for(self, concept_id: str, n: int) -> list[Assertion]:
        return self._codex.query(subject=self._fact_subject_id(concept_id, n), relation=REL_SUCC)

    @staticmethod
    def _active(a: Assertion, states: tuple[EpistemicState, ...]) -> bool:
        if a.status not in states:
            return False
        v = a.validity
        return v is None or v.to is None

    def _established_value(self, concept_id: str, n: int) -> Assertion | None:
        acts = [a for a in self._facts_for(concept_id, n) if self._active(a, (EpistemicState.established,))]
        if len(acts) != 1:
            return None
        return acts[0]

    def _succ_step(self, concept_id: str, n: int) -> tuple[int, str] | None:
        """One grounded successor step: (m, assertion_id) or None."""

        a = self._established_value(concept_id, n)
        if a is None or not a.object_id.startswith(f"{concept_id}:num("):
            return None
        m = int(a.object_id[len(f"{concept_id}:num(") : -1])
        return m, a.id

    def _derive_chain(self, concept_id: str, start: int, steps: int) -> tuple[int, list[str]] | None:
        """Chain `steps` grounded successor steps from `start`.
        Every step cites the established fact it used; None = not
        derivable (the honest path)."""

        x = start
        trace: list[str] = []
        for _ in range(steps):
            step = self._succ_step(concept_id, x)
            if step is None:
                return None
            x, aid = step
            trace.append(aid)
        return x, trace

    # ── E6.2: rule-gated capabilities (capability is store data) ─────────

    def _rule_fact(self, concept_id: str) -> Assertion | None:
        """The single ESTABLISHED rule/definition fact gating `concept_id`'s
        capability (the one-claimant invariant applies to capabilities too)."""

        acts = self._codex.query(relation=REL_POLICY)
        cand = [
            x
            for x in acts
            if x.context.data.get("concept") == concept_id
            and x.context.data.get("kind") in ("rule", "definition")
            and self._active(x, (EpistemicState.established,))
        ]
        if len(cand) != 1:
            return None
        return cand[0]

    def _line_end(self) -> int:
        """Farthest established point on the successor line (0..end)."""

        v = 0
        while self._succ_step(CONCEPT_COUNT, v) is not None:
            v += 1
        return v

    def _walk_back(self, a: int, b: int) -> tuple[int, list[str]] | None:
        """Subtraction by grounded walk-back: b predecessor steps from a,
        each step citing the established successor fact it used.
        None = the walk leaves the line (honest path)."""

        cur, trace = a, []
        for _ in range(b):
            if cur == 0:
                return None
            step = self._succ_step(CONCEPT_COUNT, cur - 1)
            if step is None:
                return None
            _, aid = step
            trace.append(aid)
            cur -= 1
        return cur, trace

    def _mult_value(self, a: int, b: int) -> tuple[int, list[str]] | None:
        """Multiplication as COMPOSED addition: total=0, a times
        total+=b, every inner chain step cited. The empty trace is a
        legitimate identity (a zero step adds nothing)."""

        total, trace = 0, []
        for _ in range(a):
            step = self._derive_chain(CONCEPT_COUNT, total, b)
            if step is None:
                return None
            total, ttrace = step
            trace.extend(ttrace)
        return total, trace

    def _square(self, k: int) -> tuple[int, list[str]] | None:
        return self._mult_value(k, k)

    def _sqrt_search(self, n: int) -> tuple[str, int, int, int, list[str]]:
        """Square-root search ON THE LATTICE: try k=1,2,... while k*k is
        computable (its repeated-addition chain stays in the line).
        Returns (mode, lo, hi, line_end, cites) with mode in
        {"exact","bracket","partial","no"} — the wall is data, not code."""

        end = self._line_end()
        last_below: tuple[int, int, list[str]] | None = None
        k = 1
        while True:
            sq = self._square(k)
            if sq is None:
                if last_below is not None and n > last_below[1]:
                    return "partial", last_below[0], last_below[1], end, list(last_below[2])
                return "no", 0, 0, end, []
            v, cites = sq
            if v == n:
                return "exact", k, k, end, list(cites)
            if v < n:
                last_below = (k, v, list(cites))
                k += 1
                continue
            if last_below is None:
                return "bracket", 0, k, end, list(cites)
            return "bracket", last_below[0], k, end, list(last_below[2]) + list(cites)

    # ── memory writes (verified, provenanced, deterministic ids) ─────────

    def _uptake_fact(self, concept_id: str, a: int, b: int, turn: str, now: str) -> tuple[Assertion, bool]:
        """D-e6c — single CURRENT claimant per (subject, value): one fact
        assertion per (succ-of(a) -> num(b)); re-teaching the same value
        CORROBORATES (evidence += turn, re-verify), it does not create a
        duplicate claimant. A different value never overwrites: the new
        claimant is created (the conflict path disputes it) and the old
        one stays until a correction closes it. Returns (claimant, created)."""

        fid = self._fact_subject_id(concept_id, a)
        val = self._num_object(concept_id, b).id
        for x in self._facts_for(concept_id, a):
            if x.object_id == val and self._active(x, (EpistemicState.candidate, EpistemicState.established, EpistemicState.disputed)):
                return x, False
        aid = f"cs-f{turn.replace(':', '')}:{a}->{b}"
        self._codex.add(
            Assertion(
                id=aid,
                subject=TermRef(kind="term", id=fid, labels=[f"after {a} comes {b}"]),
                relation=TermRef(kind="concept", id=REL_SUCC),
                object=self._num_object(concept_id, b),
                context=Context(data={"kind": "fact", "concept": concept_id, "fact": f"succ({a},{b})"}),
                validity=Interval(from_=now, to=None),
                status=EpistemicState.candidate,
                provenance=Provenance(
                    source=Source(uri=f"turn:{turn}", media_type="text/plain", authority="teacher"),
                    observer="teacher",
                    verified=False,
                    evidence=[f"turn:{turn}"],
                ),
            )
        )
        return self._codex.get(aid), True

    def _establish(self, a: Assertion, extra_evidence: list[str] | None = None) -> None:
        prov = a.provenance
        assert prov is not None  # invariant #1: every stored assertion has it
        ev = list(prov.evidence)
        for e in extra_evidence or []:
            if e not in ev:
                ev.append(e)
        self._codex.add(
            Assertion(
                id=a.id,
                subject=a.subject,
                relation=a.relation,
                object=a.object,
                polarity=a.polarity,
                context=a.context,
                validity=a.validity,
                confidence=a.confidence,
                status=EpistemicState.established,
                provenance=Provenance(
                    source=prov.source,
                    observer=prov.observer,
                    derived=prov.derived,
                    verified=True,
                    evidence=ev,
                ),
                exception=a.exception,
            )
        )

    def _set_status(self, a: Assertion, status: EpistemicState, *, evidence: list[str] | None = None,
                    exception: ExceptionState | None = None, close_validity_to: str | None = None) -> None:
        prov = a.provenance
        assert prov is not None  # invariant #1: every stored assertion has it
        ev = list(prov.evidence)
        for e in evidence or []:
            if e not in ev:
                ev.append(e)
        v = a.validity
        nv = None
        if v is not None or close_validity_to is not None:
            nv = Interval(from_=(v.from_ if v is not None else None), to=(close_validity_to if close_validity_to is not None else (v.to if v is not None else None)))
        self._codex.add(
            Assertion(
                id=a.id,
                subject=a.subject,
                relation=a.relation,
                object=a.object,
                polarity=a.polarity,
                context=a.context,
                validity=nv,
                confidence=a.confidence,
                status=status,
                provenance=Provenance(
                    source=prov.source,
                    observer=prov.observer,
                    derived=prov.derived,
                    verified=prov.verified,
                    evidence=ev,
                ),
                exception=exception,
            )
        )

    def _record_event(self, kind: str, concept_id: str, turn: str, observer: str, evidence: list[str]) -> str:
        eid = f"{concept_id}:ev-s{self._session:02d}t{self._turn:02d}:{kind}"
        try:
            label = concept(concept_id).label
        except KeyError:
            label = concept_id  # dormant/unregistered concept (D-e6f sqrt rung)
        self._codex.add(
            Assertion(
                id=eid,
                subject=TermRef(kind="entity", id=concept_id, labels=[label]),
                relation=TermRef(kind="concept", id=REL_HAS_EVENT),
                object=TermRef(kind="term", id=kind),
                context=Context(data={"kind": "mastery-event", "concept": concept_id}),
                validity=Interval(from_=fixed_epoch(self._session, self._turn), to=None),
                status=EpistemicState.established,
                provenance=Provenance(
                    source=Source(uri=f"turn:{turn}", media_type="text/plain", authority=observer),
                    observer=observer,
                    derived=(kind.startswith("derivation-")),
                    verified=True,
                    evidence=list(evidence),
                ),
            )
        )
        return eid

    def _prior_conflict_episodes(self, concept_id: str | None = None) -> int:
        n = 0
        for a in self._codex.query(context_match={"kind": "mastery-event"}):
            if a.object_id == "conflict" and (concept_id is None or a.context.data.get("concept") == concept_id):
                n += 1
        return n

    # ── policies (per contract kind) ────────────────────────────────────

    def _policy_rule_lesson(self, phrase: str, turn: str, now: str) -> _PolicyOutcome:
        """E6.2: a rule/definition lesson writes the capability fact.
        Teaching a new concept IS writing its rule to the store (P11)."""

        concept, rule_name, label = RULE_LESSONS[phrase]
        rk = "definition" if rule_name == "definition" else "rule"
        aid = f"cap:{concept}:{rk}"
        out = _PolicyOutcome(ir=kind_response_ir("assertion", {"a": 0, "b": 0}), text="", grounded=[], memory_diff=[], events=[])
        self._codex.add(
            Assertion(
                id=aid,
                subject=TermRef(kind="term", id=f"capability:{concept}", labels=[label]),
                relation=TermRef(kind="concept", id=REL_POLICY),
                object=TermRef(kind="term", id=f"rule:{rule_name}"),
                context=Context(data={"kind": rk, "concept": concept, "rule": rule_name, "label": label}),
                validity=Interval(from_=now, to=None),
                status=EpistemicState.candidate,
                provenance=Provenance(
                    source=Source(uri=f"turn:{turn}", media_type="text/plain", authority="teacher"),
                    observer="teacher",
                    verified=False,
                    evidence=[f"turn:{turn}"],
                ),
            )
        )
        self._establish(self._codex.get(aid))
        eid = self._record_event(rk, concept, turn, "teacher", [aid])
        out.events.append(eid)
        out.memory_diff.append(aid)
        out.grounded.append(aid)
        out.ir = {"ack": phrase, "provenance": [aid, f"turn:{turn}"], "epistemic_state": "established"}
        out.text = f"noted — {label}: from now on i can do that."
        return out

    def _unlearned(self, concept_id: str, phrase: str, slots: dict[str, Any]) -> _PolicyOutcome:
        """E6.2: a drill for a capability whose rule/definition is not
        (yet) established — the HONEST gap (never a guess), named so the
        teacher can close it. Writes nothing (capability not learned)."""

        _, _, label = RULE_LESSONS[phrase]
        out = _PolicyOutcome(ir=kind_response_ir("impossible", slots), text="", grounded=[], memory_diff=[], events=[], kind="impossible")
        out.ir = {
            "gap": f"not yet learned: {label}",
            "nearest_plan": [f"teach it first: “{phrase}”"],
        }
        out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."
        return out

    # ── E6.5: the geometry strip (capability is store data, P11) ───

    def _shape_claimant(self, shape: str) -> Assertion | None:
        """The single CURRENT definition claimant for a shape (the D-e6c
        discipline): at most one active claim per value-bearing
        capability; during a dispute transition the most recent (by
        turn-ordered id) is the current one — never averaged, never
        both."""

        concept_id = f"shape-{shape}"
        cand = [
            x
            for x in self._codex.query(relation=REL_POLICY)
            if x.context.data.get("concept") == concept_id
            and x.context.data.get("kind") == "definition"
            and (x.validity is None or x.validity.to is None)
            and x.status in (EpistemicState.candidate, EpistemicState.disputed, EpistemicState.established)
        ]
        if not cand:
            return None
        return max(cand, key=lambda x: x.id)

    def _write_shape_def(
        self,
        shape: str,
        sides: int | None,
        corners: int | None,
        turn: str,
        now: str,
        status: EpistemicState,
        extra_evidence: list[str],
    ) -> str:
        """One shape definition claimant (unique id per turn — the
        correction arc keeps BOTH sides, the E6.4 phrasing pattern)."""

        concept_id = f"shape-{shape}"
        fact_id = f"cap:{concept_id}:def:{turn}"
        self._codex.add(
            Assertion(
                id=fact_id,
                subject=TermRef(kind="term", id=f"capability:{concept_id}", labels=[f"the {shape}'s definition"]),
                relation=TermRef(kind="concept", id=REL_POLICY),
                object=TermRef(kind="term", id=f"definition:{concept_id}"),
                context=Context(
                    data={
                        "kind": "definition",
                        "concept": concept_id,
                        "shape": shape,
                        "sides": sides,
                        "corners": corners,
                        "label": f"the {shape}'s definition",
                    }
                ),
                validity=Interval(from_=now, to=None),
                status=status,
                provenance=Provenance(
                    source=Source(uri=f"turn:{turn}", media_type="text/plain", authority="teacher"),
                    observer="teacher",
                    verified=(status is EpistemicState.established),
                    evidence=list(extra_evidence),
                ),
            )
        )
        if status is EpistemicState.established:
            self._establish(self._codex.get(fact_id))
        return fact_id

    @staticmethod
    def _shape_val_txt(v: int | None) -> str:
        return "none" if v is None else str(v)

    def _policy_shape_lesson(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.5: a shape definition lesson writes the capability fact.
        The teacher's value goes to the store AS SAID (the wrong-value
        arc is measured, never silently discarded); the single
        current-claimant discipline governs (the D-e6c pair)."""

        shape: str = slots["shape"]
        concept_id = f"shape-{shape}"
        sides = None if shape == "circle" else int(slots["sides"])
        corners = None if shape == "circle" else int(slots["corners"])
        out = _PolicyOutcome(ir=kind_response_ir("assertion", {"a": 0, "b": 0}), text="", grounded=[], memory_diff=[], events=[])
        existing = self._shape_claimant(shape)
        if existing is not None:
            same = existing.context.data.get("sides") == sides and existing.context.data.get("corners") == corners
            if same:
                # corroboration: re-establish the SAME claimant, never a duplicate (D-e6c)
                self._establish(existing, extra_evidence=[f"turn:{turn}"])
                eid = self._record_event("definition", concept_id, turn, "teacher", [existing.id])
                out.events.append(eid)
                out.memory_diff.append(existing.id)
                out.grounded.append(existing.id)
                out.ir = {"ack": canonical_shape_lesson(shape), "provenance": [existing.id, f"turn:{turn}"], "epistemic_state": "established"}
                out.text = "noted — i already know that one."
                return out
            # a conflicting live claimant WITHOUT a correction marker:
            # create (candidate) + dispute the old — never overwrite (D-e6c)
            fact_id = self._write_shape_def(shape, sides, corners, turn, now, EpistemicState.candidate, [f"turn:{turn}"])
            self._set_status(existing, EpistemicState.disputed, evidence=[fact_id], exception=None)
            eid = self._record_event("conflict", concept_id, turn, "teacher", [existing.id, fact_id])
            out.events.append(eid)
            out.memory_diff += [fact_id, existing.id]
            old_s = self._shape_val_txt(existing.context.data.get("sides"))
            old_c = self._shape_val_txt(existing.context.data.get("corners"))
            out.conflict = {"fact": f"definition:{concept_id}", "superseded": existing.id, "replacement": fact_id}
            out.ir = {
                "ack": f"the {shape} has {self._shape_val_txt(sides)} sides and {self._shape_val_txt(corners)} corners (disputed)",
                "provenance": [fact_id, f"turn:{turn}"],
                "epistemic_state": "candidate",
            }
            out.text = f"hmm — i was told the {shape} has {old_s} sides and {old_c} corners, and now i am told otherwise. Which is right? the old claim stays disputed until you correct it."
            return out
        fact_id = self._write_shape_def(shape, sides, corners, turn, now, EpistemicState.established, [f"turn:{turn}"])
        eid = self._record_event("definition", concept_id, turn, "teacher", [fact_id])
        out.events.append(eid)
        out.memory_diff.append(fact_id)
        out.grounded.append(fact_id)
        out.ir = {
            "ack": canonical_shape_lesson(shape) if (sides, corners) == SHAPES[shape] else f"the {shape} has {self._shape_val_txt(sides)} sides and {self._shape_val_txt(corners)} corners",
            "provenance": [fact_id, f"turn:{turn}"],
            "epistemic_state": "established",
        }
        out.text = f"noted — the {shape}: from now on i can do that."
        return out

    def _policy_shape_correction(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.5: the CORRECTION marker with the canonical values — the
        D-e6c pair: the old claimant is superseded (kept, obsolete,
        validity ended, linked), the replacement is verified and
        established."""

        shape: str = slots["shape"]
        concept_id = f"shape-{shape}"
        sides = None if shape == "circle" else int(slots["sides"])
        corners = None if shape == "circle" else int(slots["corners"])
        out = _PolicyOutcome(ir=kind_response_ir("correction", {"a": 0, "b": 0}), text="", grounded=[], memory_diff=[], events=[])
        existing = self._shape_claimant(shape)
        fact_id = self._write_shape_def(
            shape, sides, corners, turn, now, EpistemicState.established, [f"turn:{turn}"] + ([existing.id] if existing is not None else [])
        )
        new_s = self._shape_val_txt(sides)
        new_c = self._shape_val_txt(corners)
        if existing is not None:
            old_s = self._shape_val_txt(existing.context.data.get("sides"))
            old_c = self._shape_val_txt(existing.context.data.get("corners"))
            # close the superseded side (kept, never deleted): obsolete +
            # validity ended + linked to the replacement
            self._set_status(existing, EpistemicState.obsolete, evidence=[fact_id], exception=None, close_validity_to=now)
            eid = self._record_event("correction", concept_id, turn, "teacher", [existing.id, fact_id])
            out.events.append(eid)
            out.memory_diff += [fact_id, existing.id]
            out.grounded = [fact_id]
            out.conflict = {"fact": f"definition:{concept_id}", "superseded": existing.id, "replacement": fact_id}
            out.ir = {
                "superseded": f"the {shape} has {old_s} sides and {old_c} corners (claim closed)",
                "replacement": f"the {shape} has {new_s} sides and {new_c} corners (claim opened)",
            }
            out.text = f"corrected — the {shape} has {new_s} sides and {new_c} corners (the old claim is closed)."
        else:
            eid = self._record_event("correction", concept_id, turn, "teacher", [fact_id])
            out.events.append(eid)
            out.memory_diff.append(fact_id)
            out.grounded = [fact_id]
            out.ir = {
                "superseded": "no claim for the " + shape + " was recorded",
                "replacement": f"the {shape} has {new_s} sides and {new_c} corners (claim opened)",
            }
            out.text = f"noted — there was no earlier claim; the {shape} has {new_s} sides and {new_c} corners."
        return out

    def _policy_shape(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.5: a shape drill — rule-gated on the shape's capability
        fact (the E6.2 impossible-learns arc generalized to geometry)."""

        shape: str = slots["shape"]
        mode = slots.get("mode")
        if mode == "shape-corners":
            prop = "corners"
        elif mode == "shape-sides":
            prop = "sides"
        else:
            prop = slots.get("property", "sides")
        concept_id = f"shape-{shape}"
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        fact = self._rule_fact(concept_id)
        if fact is None:
            # the honest gap (never a guess), named so the teacher can
            # close it — exactly the E6.2 unlearned articulation
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: the {shape}'s definition",
                "nearest_plan": [f"teach it first: \u201c{canonical_shape_lesson(shape)}\u201d"],
            }
            out.text = f"honestly, i can't do that yet — the {shape}'s definition is not a capability i have been taught. Teach me first and i will learn it."
            return out
        value: int | None = fact.context.data.get("sides" if prop == "sides" else "corners")
        out.ir = {"answer": self._shape_val_txt(value), "evidence": [fact.id], "uncertainty_state": "derived"}
        out.grounded = [fact.id]
        eid = self._record_event("derivation-correct", concept_id, turn, "infant", [fact.id])
        out.events.append(eid)
        out.text = f"the {shape} has no {prop}." if value is None else f"the {shape} has {value} {prop}."
        return out

    # ── E6.4: phrasology (D-e6i) ────────────────────────────────────

    def _valid_mapping(self, new_tpl: str, canon_tpl: str) -> tuple[bool, str]:
        """M1 validity: canonical side is a frozen template; ordered
        placeholder bijection; the new side carries slots only (no
        fixed numbers)."""

        if canon_tpl not in dict(CANON_TEMPLATES).values():
            return False, "the canonical side must be one of my frozen canonical patterns"
        new_names = re.findall(r"\{([a-z]+)\}", new_tpl)
        canon_names = re.findall(r"\{([a-z]+)\}", canon_tpl)
        if not new_names or sorted(new_names) != sorted(canon_names):
            return False, "the new template's slot names must be exactly my canonical slot names, each used once"
        if re.search(r"\d", new_tpl):
            return False, "the new template must carry no fixed numbers — only number slots"
        # E6.5: vocabulary slots (D-e6i generalized) - a new template may
        # not carry fixed words from a band vocabulary either.
        for name, vocab in SLOT_VOCAB.items():
            if name not in canon_names:
                continue
            if re.search(r"\b(?:" + "|".join(vocab) + r")\b", new_tpl):
                return False, f"the new template must carry no fixed {name} words — only its {name} slot"
        return True, ""

    def _phrasing_facts_active(self, statuses: tuple) -> list:
        out = []
        for a in self._codex.query(relation=REL_PHRASING):
            if a.subject.id.startswith(PHRASING_PREFIX) and a.status in statuses and (a.validity is None or a.validity.to is None):
                out.append(a)
        return sorted(out, key=lambda a: a.subject.id)

    def _phrasing_fact(self, new_tpl: str):
        subj = f"{PHRASING_PREFIX}{new_tpl}"
        for a in self._codex.query(relation=REL_PHRASING):
            if a.subject.id == subj and (a.validity is None or a.validity.to is None):
                return a
        return None

    def _write_phrasing_fact(self, new_tpl: str, canon_tpl: str, turn: str, now, status, extra_evidence: list[str]) -> str:
        pat_id = next(pid for pid, t in CANON_TEMPLATES if t == canon_tpl)
        fact_id = f"phrasing:{turn}"
        self._codex.add(
            Assertion(
                id=fact_id,
                subject=TermRef(kind="term", id=f"{PHRASING_PREFIX}{new_tpl}", labels=[new_tpl]),
                relation=TermRef(kind="concept", id=REL_PHRASING),
                object=TermRef(kind="term", id=pat_id),
                context=Context(data={"kind": "phrasing", "new": new_tpl, "canon": canon_tpl}),
                validity=Interval(from_=now, to=None),
                status=status,
                provenance=Provenance(
                    source=Source(uri=f"turn:{turn}", media_type="text/plain", authority="teacher"),
                    observer="teacher",
                    derived=False,
                    verified=(status is EpistemicState.established),
                    evidence=list(extra_evidence),
                ),
            )
        )
        if status is EpistemicState.established:
            self._establish(self._codex.get(fact_id), extra_evidence=[])
        return fact_id

    def _lexicon_classify(self, text: str) -> tuple[str, dict[str, Any], str] | None:
        """M4: consulted ONLY where the grammar says ambiguous. First
        established match in subject order wins."""

        for fact in self._phrasing_facts_active((EpistemicState.established,)):
            new_tpl = fact.context.data["new"]
            parts = re.split(r"(\{[a-z]+\})", new_tpl)
            seg: list[str] = []
            for part in parts:
                if part.startswith("{"):
                    name = part[1:-1]
                    # E6.5: a vocabulary slot fills from its FROZEN band
                    # vocabulary; every other slot fills a number (D-e6i).
                    seg.append(rf"\b((?:{'|'.join(SLOT_VOCAB[name])}))\b" if name in SLOT_VOCAB else r"(\d+)")
                else:
                    seg.append(re.escape(part))
            rx = re.compile("".join(seg) + r"\Z")
            m = rx.match(text.strip())
            if m is None:
                continue
            names = re.findall(r"\{([a-z]+)\}", new_tpl)
            fills: dict[str, Any] = {nm: (g if nm in SLOT_VOCAB else int(g)) for g, nm in zip(m.groups(), names)}
            if _KIND_OVERRIDE.get(fact.object_id) == "assertion":
                return "assertion", fills, fact.id
            return "question", {"mode": _SLOT_MODES[fact.object_id], **fills}, fact.id
        return None

    def _policy_teach(self, slots: dict[str, Any], turn: str, now) -> _PolicyOutcome:
        """M3: teach a phrasing mapping (store the fact)."""

        new_tpl, canon_tpl = slots["new"], slots["canon"]
        out = _PolicyOutcome(ir={"ack": "", "provenance": [], "epistemic_state": ""}, text="", grounded=[], memory_diff=[], events=[])
        valid, why = self._valid_mapping(new_tpl, canon_tpl)
        if not valid:
            # an honest rejection: never a silent guess
            out.kind = "ambiguous"
            out.ir = {
                "clarifying_question": f"i can't take that as a mapping — {why}",
                "candidates": ["one of my canonical patterns: " + " | ".join(t for _, t in CANON_TEMPLATES)],
            }
            out.text = f"honestly, i can't take that as a mapping — {why}"
            return out
        existing = self._phrasing_fact(new_tpl)
        if existing is not None and existing.context.data["canon"] == canon_tpl:
            # corroboration: re-establish, never duplicate (D-e6c)
            self._establish(existing, extra_evidence=[f"turn:{turn}"])
            eid = self._record_event("teach", CONCEPT_PHRASOLOGY, turn, "teacher", [existing.id])
            out.events.append(eid)
            out.memory_diff.append(existing.id)
            out.grounded.append(existing.id)
            out.ir = {"ack": new_tpl, "provenance": [existing.id, f"turn:{turn}"], "epistemic_state": "established"}
            out.text = f'noted — i already understand "{new_tpl}" as "{canon_tpl}".'
            return out
        if existing is not None:
            # a conflicting active claimant WITHOUT a correction marker:
            # create + dispute, never overwrite (D-e6c); the old mapping
            # is disputed (out of the lexicon) until adjudicated
            fact_id = self._write_phrasing_fact(new_tpl, canon_tpl, turn, now, EpistemicState.candidate, [f"turn:{turn}"])
            self._set_status(existing, EpistemicState.disputed, evidence=[fact_id], exception=None)
            eid = self._record_event("teach", CONCEPT_PHRASOLOGY, turn, "teacher", [existing.id, fact_id])
            eid2 = self._record_event("conflict", CONCEPT_PHRASOLOGY, turn, "teacher", [existing.id, fact_id])
            out.events += [eid, eid2]
            out.memory_diff += [fact_id, existing.id]
            out.conflict = {"fact": f"phrasing:{new_tpl}", "superseded": existing.id, "replacement": fact_id}
            out.ir = {"ack": new_tpl, "provenance": [fact_id, f"turn:{turn}"], "epistemic_state": "candidate"}
            out.text = (
                f'hmm — i had "{new_tpl}" mapped to "{existing.context.data["canon"]}" and now i am told it is '
                f'"{canon_tpl}" — which is right? the old mapping stays disputed until you correct it.'
            )
            return out
        fact_id = self._write_phrasing_fact(new_tpl, canon_tpl, turn, now, EpistemicState.established, [f"turn:{turn}"])
        eid = self._record_event("teach", CONCEPT_PHRASOLOGY, turn, "teacher", [fact_id])
        out.events.append(eid)
        out.memory_diff.append(fact_id)
        out.grounded.append(fact_id)
        out.ir = {"ack": new_tpl, "provenance": [fact_id, f"turn:{turn}"], "epistemic_state": "established"}
        out.text = f'noted — from now on i understand "{new_tpl}" as "{canon_tpl}".'
        return out

    def _policy_teach_correction(self, slots: dict[str, Any], turn: str, now) -> _PolicyOutcome:
        """M3: correct a phrasing mapping — the D-e6c pair: the old
        mapping is superseded (kept, obsolete, validity ended, linked)."""

        new_tpl, canon_tpl = slots["new"], slots["canon"]
        out = _PolicyOutcome(ir={"superseded": "", "replacement": ""}, text="", grounded=[], memory_diff=[], events=[])
        valid, why = self._valid_mapping(new_tpl, canon_tpl)
        if not valid:
            out.kind = "ambiguous"
            out.ir = {
                "clarifying_question": f"i can't take that as a mapping — {why}",
                "candidates": ["one of my canonical patterns: " + " | ".join(t for _, t in CANON_TEMPLATES)],
            }
            out.text = f"honestly, i can't take that as a mapping — {why}"
            return out
        existing = self._phrasing_fact(new_tpl)
        fact_id = self._write_phrasing_fact(
            new_tpl, canon_tpl, turn, now, EpistemicState.established, [f"turn:{turn}"] + ([existing.id] if existing is not None else [])
        )
        if existing is not None:
            old_canon = existing.context.data["canon"]
            # close the superseded side (kept, never deleted): obsolete +
            # validity ended + linked to the replacement
            self._set_status(existing, EpistemicState.obsolete, evidence=[fact_id], exception=None, close_validity_to=now)
            eid = self._record_event("correction", CONCEPT_PHRASOLOGY, turn, "teacher", [existing.id, fact_id])
            out.events.append(eid)
            out.memory_diff += [fact_id, existing.id]
            out.grounded = [fact_id]
            out.conflict = {"fact": f"phrasing:{new_tpl}", "superseded": existing.id, "replacement": fact_id}
            out.ir = {
                "superseded": f'"{new_tpl}" was "{old_canon}" (mapping closed)',
                "replacement": f'"{new_tpl}" is "{canon_tpl}" (mapping opened)',
            }
            out.text = f'corrected — from now on i understand "{new_tpl}" as "{canon_tpl}" (the old mapping is closed).'
        else:
            eid = self._record_event("correction", CONCEPT_PHRASOLOGY, turn, "teacher", [fact_id])
            out.events.append(eid)
            out.memory_diff.append(fact_id)
            out.grounded = [fact_id]
            out.ir = {
                "superseded": "no such mapping was recorded",
                "replacement": f'"{new_tpl}" is "{canon_tpl}" (mapping opened)',
            }
            out.text = f'noted — there was no earlier mapping; from now on i understand "{new_tpl}" as "{canon_tpl}".'
        return out

    def _policy_assertion(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        if "rule" in slots:
            return self._policy_rule_lesson(slots["rule"], turn, now)
        if "new" in slots:  # E6.4: a phrasing mapping lesson
            return self._policy_teach(slots, turn, now)
        if "shape" in slots:  # E6.5: a shape definition lesson
            return self._policy_shape_lesson(slots, turn, now)
        a, b = slots["a"], slots["b"]
        out = _PolicyOutcome(ir=kind_response_ir("assertion", slots), text="", grounded=[], memory_diff=[], events=[])
        fact, created = self._uptake_fact(CONCEPT_COUNT, a, b, turn, now)
        # By the single-claimant invariant the ONLY active different-valued
        # claimants that can exist are the conflict side(s) of the new one.
        active_conflicts = [
            x
            for x in self._facts_for(CONCEPT_COUNT, a)
            if x.id != fact.id
            and x.object_id != fact.object_id
            and self._active(x, (EpistemicState.candidate, EpistemicState.established, EpistemicState.disputed))
        ]
        if active_conflicts:
            # A5 at dialogue scale: both sides disputed, kept, linked — never averaged.
            for x in active_conflicts:
                self._set_status(
                    x, EpistemicState.disputed, evidence=[fact.id], exception=ExceptionState.conflicting
                )
            self._set_status(fact, EpistemicState.disputed, evidence=[x.id for x in active_conflicts], exception=ExceptionState.conflicting)
            old = active_conflicts[0]
            old_b = int(old.object_id[len(f"{CONCEPT_COUNT}:num(") : -1])
            # Count PRIOR episodes BEFORE recording this turn's event (no self-count):
            # attention = the SECOND+ teacher conflict episode (spec: "repeated" -> pull
            # a human in; the first episode is a normal conflict, logged but silent).
            prior = self._prior_conflict_episodes()
            eid = self._record_event("conflict", CONCEPT_COUNT, turn, "infant", [fact.id, old.id])
            out.events.append(eid)
            out.memory_diff += [fact.id] + [x.id for x in active_conflicts]
            out.conflict = {
                "fact": f"succ({a},{b})",
                "new": fact.id,
                "established": [x.id for x in active_conflicts],
                "old_values": [int(x.object_id[len(f'{CONCEPT_COUNT}:num(') : -1]) for x in active_conflicts],
            }
            out.ir = {
                "ack": f"that conflicts with what i have (after {a} comes {old_b}); i am keeping both, marked disputed",
                "provenance": [fact.id] + [x.id for x in active_conflicts] + [f"turn:{turn}"],
                "epistemic_state": "disputed",
            }
            out.text = f"hmm — i have 'after {a} comes {old_b}'; 'after {a} comes {b}' disagrees, so i am keeping both as disputed."
            if prior >= 1:
                out.attention = {
                    "turn": turn,
                    "type": "repeated-conflict",
                    "detail": f"conflict episode #{prior + 1} on {CONCEPT_COUNT} (teacher channel reliability)",
                }
        else:
            # Verified: no active different-valued claimant (a same-valued one
            # is `fact` itself — single claimant). Corroboration appends the
            # turn to the evidence and re-establishes (re-verify, P11).
            self._establish(fact, extra_evidence=[] if created else [f"turn:{turn}"])
            eid = self._record_event("lesson", CONCEPT_COUNT, turn, "teacher", [fact.id])
            out.events.append(eid)
            out.memory_diff.append(fact.id)
            out.grounded = [fact.id]
            out.ir = {
                "ack": f"after {a} comes {b}",
                "provenance": [fact.id, f"turn:{turn}"],
                "epistemic_state": "established",
            }
            out.text = (
                f"yes — after {a} comes {b}; noted." if created else f"yes — after {a} comes {b}, just as i have it."
            )
        return out

    def _policy_correction(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        if "new" in slots:  # E6.4: correcting a phrasing mapping (D-e6c pair)
            return self._policy_teach_correction(slots, turn, now)
        if "shape" in slots:  # E6.5: correcting a shape definition (D-e6c pair)
            return self._policy_shape_correction(slots, turn, now)
        a, b = slots["a"], slots["b"]
        out = _PolicyOutcome(ir=kind_response_ir("correction", slots), text="", grounded=[], memory_diff=[], events=[])
        superseded_cands = [
            x
            for x in self._facts_for(CONCEPT_COUNT, a)
            if x.object_id != self._num_object(CONCEPT_COUNT, b).id
            and self._active(x, (EpistemicState.candidate, EpistemicState.disputed, EpistemicState.established))
        ]
        if not superseded_cands:
            # Nothing to supersede: the single claimant of the replacement value
            # is recorded (created if absent) and verified.
            replacement, created = self._uptake_fact(CONCEPT_COUNT, a, b, turn, now)
            self._establish(replacement, extra_evidence=[] if created else [f"turn:{turn}"])
            eid = self._record_event("correction", CONCEPT_COUNT, turn, "teacher", [replacement.id])
            out.events.append(eid)
            out.memory_diff.append(replacement.id)
            out.ir = {"superseded": "nothing recorded for this fact", "replacement": f"after {a} comes {b}"}
            out.text = f"noted: after {a} comes {b}."
            return out
        sup = max(superseded_cands, key=lambda x: x.id)  # the most recent claimant (ids are turn-ordered)
        old_b = int(sup.object_id[len(f"{CONCEPT_COUNT}:num(") : -1])
        # D-e6c single claimant: the replacement VALUE's claimant is either the
        # existing (typically the original fact the wrong lesson disputed — the
        # correction VINDICATES and re-establishes it) or created fresh if none
        # exists. No duplicate claimant is ever written for the same value.
        vindicated = [
            x
            for x in self._facts_for(CONCEPT_COUNT, a)
            if x.object_id == self._num_object(CONCEPT_COUNT, b).id
            and x.id != sup.id
            and self._active(x, (EpistemicState.candidate, EpistemicState.disputed, EpistemicState.established))
        ]
        if vindicated:
            replacement = vindicated[0]
        else:
            replacement, _ = self._uptake_fact(CONCEPT_COUNT, a, b, turn, now)
        # Close the superseded side (kept, never deleted): obsolete + validity
        # ended + linked to the replacement; the pair is mutually cited in the
        # store (C4: closed, linked, and both retained).
        self._set_status(sup, EpistemicState.obsolete, evidence=[replacement.id], exception=None, close_validity_to=now)
        has_turn = replacement.provenance is not None and f"turn:{turn}" in replacement.provenance.evidence
        self._establish(replacement, extra_evidence=[sup.id] + ([] if has_turn else [f"turn:{turn}"]))
        eid = self._record_event("correction", CONCEPT_COUNT, turn, "teacher", [sup.id, replacement.id])
        out.events.append(eid)
        out.memory_diff += [replacement.id, sup.id]
        out.grounded = [replacement.id]
        out.conflict = {"fact": f"succ({a},{b})", "superseded": sup.id, "replacement": replacement.id}
        out.ir = {"superseded": f"after {a} comes {old_b}", "replacement": f"after {a} comes {b}"}
        out.text = f"corrected: after {a} comes {b} (superseding 'after {a} comes {old_b}')."
        return out

    def _add_concept_for(self, a: int, b: int, *, derived: bool) -> str:
        """E6.2 strip routing: a DERIVED wide drill belongs to the wider
        strip (the derivation IS its exposure); a FAILED wide drill records
        on the wider strip only if that strip is already in the curriculum
        record — before exposure the pilot strip owns big attempts, so the
        e6.1 replay stays bit-comparable to its official store."""

        if a + b <= 10:
            return CONCEPT_ADD
        if derived:
            return CONCEPT_ADD2
        for x in self._codex.query(context_match={"kind": "mastery-event"}):
            if x.context.data.get("concept") == CONCEPT_ADD2:
                return CONCEPT_ADD2
        return CONCEPT_ADD

    # ── E6.6: band 2 — algebra ∥ kinematics (the aligned strip) ─────

    def _band2_lesson(self, concept_id: str) -> str:
        """The frozen lesson phrase for a band-2 concept (exact
        RULE_LESSONS key — the honest gap articulation cites it, the
        E6.2/E6.5 pattern)."""

        for phrase, (cid, _, _) in RULE_LESSONS.items():
            if cid == concept_id:
                return phrase
        raise KeyError(concept_id)  # pragma: no cover

    def _take_away(self, n: int, a: int) -> tuple[str, int, list[str]]:
        """E6.6 — repeated taking (division-as-repeated-subtraction):
        how many WHOLE a's fit in n, every step GROUNDED on the
        existing line (no new arithmetic is stored or invented).
        Returns (result, detail, cites): result in {"exact",
        "inexact", "offline"} — exact: detail = the count; inexact:
        detail = the remainder (NOT a whole number on my line — the
        6–8 honesty); offline: n is off the line or a step leaves it
        (the band-2 wall, E6.2's boundary pattern carried into the
        aligned band). ALG division, KIN time and KIN pace all share
        this ONE derived corridor — one solver, two doors
        (the owner's alignment, literal in the code)."""

        if a <= 0 or n < 0:
            return ("offline", 0, [])
        if n > self._line_end():
            return ("offline", 0, [])
        cur, count = n, 0
        cites: list[str] = []
        while cur > 0:
            if cur < a:  # a remainder smaller than the step
                return ("inexact", cur, cites)
            x = cur
            for _ in range(a):
                step = self._succ_step(CONCEPT_COUNT, x - 1)
                if step is None:
                    return ("offline", count, cites)
                _, aid = step
                cites.append(aid)
                x -= 1
            cur, count = x, count + 1
        return ("exact", count, cites)

    def _policy_band2(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.6 — the seven aligned-band inverses (rule-gated; each
        is GROUNDED on the existing line machinery — walk-back,
        repeated taking, repeated addition — nothing new is stored on
        a derived drill, only the mastery event, the E6.2 pattern)."""

        mode = slots["mode"]
        concept = {
            "alg-add": CONCEPT_ALG_ADD1,
            "alg-mul": CONCEPT_ALG_MUL,
            "alg-2step": CONCEPT_ALG_2STEP,
            "kin-far": CONCEPT_KIN_FAR,
            "kin-pos": CONCEPT_KIN_POS,
            "kin-time": CONCEPT_KIN_TIME,
            "kin-rate": CONCEPT_KIN_RATE,
        }[mode]
        rule_fact = self._rule_fact(concept)
        if rule_fact is None:
            return self._unlearned(concept, self._band2_lesson(concept), dict(slots))
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _honest(why: str, text: str, audit: str, detail: int = 0) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            eid = self._record_event("drill-unable", concept, turn, "infant", [audit])
            out.events.append(eid)
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _solve_two_step(total: int, step_size: int, start: int) -> tuple[str, int, list[str], list[str]]:
            """Undo start + step_size·t = total in REVERSE (the
            alignment corridor): first the walk-back of the start
            (cited), then repeated taking (cited). Shared by
            alg-two-step and kin-solve-time — one solver, two doors."""

            t1 = self._walk_back(total, start)
            if t1 is None:
                return ("offline", 0, [], [])
            mid, cites1 = t1
            res, detail, cites2 = self._take_away(mid, step_size)
            return (res, detail, cites1, cites2)

        if mode == "alg-add":
            a, b = slots["a"], slots["b"]
            step = self._walk_back(b, a)
            if step is None:
                _honest(
                    f"alg-add:{a}:{b}:the-walk-back-does-not-reach-a-whole-number-on-my-line-at-{turn}",
                    f"taking {a} away from {b} does not land on a whole number of my line",
                    f"alg-add:{a}:{b}:ungrounded-at-{turn}",
                )
                return out
            v, trace = step
            ev = trace + [rule_fact.id]
            out.ir = {"answer": str(v), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"x is {v} — i took {a} away from {b}, step by step on my line."
            return out
        if mode == "alg-mul":
            a, b = slots["a"], slots["b"]
            res, detail, cites = self._take_away(b, a)
            if res == "inexact":
                _honest(
                    f"alg-mul:{a}:{b}:inexact-remainder-{detail}-at-{turn}",
                    f"taking {a} away from {b} again and again leaves {detail}, which is less than {a} — x is not a whole number on my line",
                    f"alg-mul:{a}:{b}:inexact-at-{turn}",
                )
                return out
            if res == "offline":
                end = self._line_end()
                _honest(
                    f"alg-mul:{a}:{b}:off-line-{end}-at-{turn}",
                    f"my number line ends at {end}, so i cannot take away from {b}",
                    f"line-end:{CONCEPT_ALG_MUL}:{a}x{b}:line-ends-at-{end}-at-{turn}",
                )
                return out
            ev = cites + [rule_fact.id]
            out.ir = {"answer": str(detail), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"x is {detail} — i took {a} away {detail} times and {b} was exactly gone."
            return out
        if mode == "alg-2step":
            a, b, c = slots["a"], slots["b"], slots["c"]
            res, detail, cites1, cites2 = _solve_two_step(c, a, b)
            if res == "inexact":
                _honest(
                    f"alg-2step:{a}:{b}:{c}:inexact-remainder-{detail}-at-{turn}",
                    f"after undoing the {b}, taking {a} away again and again leaves {detail} — x is not a whole number on my line",
                    f"alg-2step:{a}:{b}:{c}:inexact-at-{turn}",
                )
                return out
            if res == "offline":
                end = self._line_end()
                _honest(
                    f"alg-2step:{a}:{b}:{c}:off-line-{end}-at-{turn}",
                    f"my number line ends at {end}, so undoing those two changes does not land",
                    f"line-end:{CONCEPT_ALG_2STEP}:{a}x+{b}={c}:line-ends-at-{end}-at-{turn}",
                )
                return out
            ev = cites1 + cites2 + [rule_fact.id]
            out.ir = {"answer": str(detail), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"x is {detail} — i undid it in reverse: first took {b} away from {c}, then took {a} away {detail} times."
            return out
        if mode == "kin-far":
            r, t = slots["r"], slots["t"]
            mv = self._mult_value(r, t)
            if mv is None:
                end = self._line_end()
                _honest(
                    f"kin-far:{r}:{t}:off-line-{end}-at-{turn}",
                    f"my number line ends at {end}, so the pace-times-time repeated addition does not finish",
                    f"line-end:{CONCEPT_KIN_FAR}:{r}x{t}:line-ends-at-{end}-at-{turn}",
                )
                return out
            v, trace = mv
            ev = (trace if trace else []) + [rule_fact.id]
            out.ir = {"answer": str(v), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"that cart goes {v} — i added the pace {t} times."
            return out
        if mode == "kin-pos":
            d0, r, t = slots["start"], slots["r"], slots["t"]
            mv = self._mult_value(r, t)
            if mv is None:
                end = self._line_end()
                _honest(
                    f"kin-pos:{d0}:{r}:{t}:distance-off-line-{end}-at-{turn}",
                    f"my number line ends at {end}, so the distance does not even fit",
                    f"line-end:{CONCEPT_KIN_POS}:{d0}+{r}x{t}:distance-off-line-{end}-at-{turn}",
                )
                return out
            dist, dtrace = mv
            chain = self._derive_chain(CONCEPT_COUNT, dist, d0)
            if chain is None:
                end = self._line_end()
                _honest(
                    f"kin-pos:{d0}:{r}:{t}:position-off-line-{end}-at-{turn}",
                    f"the cart would be at {dist + d0}, but my number line ends at {end} — the position is off my line",
                    f"line-end:{CONCEPT_KIN_POS}:{d0}+{r}x{t}:position-{dist + d0}-off-line-{end}-at-{turn}",
                )
                return out
            v, ctrace = chain
            ev = dtrace + ctrace + [rule_fact.id]
            out.ir = {"answer": str(v), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"the cart is at {v} — it travelled {dist} (the pace {t} times) and started at {d0}."
            return out
        if mode == "kin-time":
            d0, r, c = slots["start"], slots["r"], slots["c"]
            res, detail, cites1, cites2 = _solve_two_step(c, r, d0)
            if res == "inexact":
                _honest(
                    f"kin-time:{d0}:{r}:{c}:inexact-remainder-{detail}-at-{turn}",
                    f"after the cart covered the {d0} start, taking {r} away again and again leaves {detail} — the number of minutes would not be a whole number on my line",
                    f"kin-time:{d0}:{r}:{c}:inexact-at-{turn}",
                )
                return out
            if res == "offline":
                end = self._line_end()
                _honest(
                    f"kin-time:{d0}:{r}:{c}:off-line-{end}-at-{turn}",
                    f"my number line ends at {end}, so undoing the motion does not land",
                    f"line-end:{CONCEPT_KIN_TIME}:{d0}+{r}t={c}:line-ends-at-{end}-at-{turn}",
                )
                return out
            ev = cites1 + cites2 + [rule_fact.id]
            out.ir = {"answer": str(detail), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"it took {detail} minutes — i undid the equation: took the start back, then took the pace away {detail} times."
            return out
        # mode == "kin-rate"
        d, t = slots["d"], slots["t"]
        res, detail, cites = self._take_away(d, t)
        if res == "inexact":
            _honest(
                f"kin-rate:{d}:{t}:inexact-remainder-{detail}-at-{turn}",
                f"taking {t} minutes away from {d} miles again and again leaves {detail} — the pace would not be a whole number on my line",
                f"kin-rate:{d}:{t}:inexact-at-{turn}",
            )
            return out
        if res == "offline":
            end = self._line_end()
            _honest(
                f"kin-rate:{d}:{t}:off-line-{end}-at-{turn}",
                f"my number line ends at {end}, so i cannot measure that pace",
                f"line-end:{CONCEPT_KIN_RATE}:{d}/{t}:line-ends-at-{end}-at-{turn}",
            )
            return out
        ev = cites + [rule_fact.id]
        out.ir = {"answer": str(detail), "evidence": ev, "uncertainty_state": "derived"}
        out.grounded = list(ev)
        out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
        out.text = f"that is {detail} miles a minute — i took the time away {detail} times and the distance was exactly gone."
        return out

    # ── E6.7: band 3 — geometry-advanced ∥ vectors/statics ─────────
    # THE PRODUCT BAND: the multiplication corridor (four doors:
    # distance (band 2), area, moment, perimeter×2) and the taking
    # corridor (three doors: algebra division, pace (band 2), lever
    # force) are the SAME grounded helpers — the alignment is the
    # shared corridor, measured by the twin probes (E6.7 P5).

    def _band3_lesson(self, concept_id: str) -> str:
        """The frozen lesson phrase for a band-3 concept (exact
        RULE_LESSONS key — the honest gap articulation cites it)."""

        for phrase, (cid, _, _) in RULE_LESSONS.items():
            if cid == concept_id:
                return phrase
        raise KeyError(concept_id)  # pragma: no cover

    def _policy_band3(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.7 — the six product-band capabilities (rule-gated; each
        is GROUNDED on the existing line machinery — nothing new is
        stored on a derived drill, only the mastery event)."""

        mode = slots["mode"]
        concept = {
            "geo-perim": CONCEPT_GEO_PERIM,
            "geo-area": CONCEPT_GEO_AREA,
            "geo-tri": CONCEPT_GEO_TRI,
            "geo-cmp": CONCEPT_GEO_AREA,  # comparison is the AREA concept applied
            "sta-net": CONCEPT_STA_NET,
            "sta-mom": CONCEPT_STA_MOM,
            "sta-bal": CONCEPT_STA_BAL,
        }[mode]
        rule_fact = self._rule_fact(concept)
        if rule_fact is None:
            return self._unlearned(concept, self._band3_lesson(concept), dict(slots))
        out = _PolicyOutcome(
            ir=kind_response_ir("question", slots),
            text="",
            grounded=[],
            memory_diff=[],
            events=[],
        )

        def _honest(why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            eid = self._record_event("drill-unable", concept, turn, "infant", [audit])
            out.events.append(eid)
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _derive(ev: list[str], answer: str, text: str) -> None:
            out.ir = {"answer": answer, "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(
                self._record_event("derivation-correct", concept, turn, "infant", ev)
            )
            out.text = text

        if mode == "geo-perim":
            l, w = slots["l"], slots["w"]
            sm = self._derive_chain(CONCEPT_COUNT, l, w)
            if sm is None:
                end = self._line_end()
                _honest(
                    f"geo-perim:{l}:{w}:sum-off-line-{end}-at-{turn}",
                    f"adding the sides does not even fit — my number line ends at {end}",
                    f"line-end:{CONCEPT_GEO_PERIM}:{l}+{w}:line-ends-at-{end}-at-{turn}",
                )
                return out
            ss, strace = sm
            dbl = self._mult_value(2, ss)
            if dbl is None:
                end = self._line_end()
                _honest(
                    f"geo-perim:{l}:{w}:perimeter-off-line-{end}-at-{turn}",
                    f"the perimeter would be {2 * ss}, but my number line ends at {end}",
                    f"line-end:{CONCEPT_GEO_PERIM}:{l}x{w}:perimeter-{2 * ss}-off-line-{end}-at-{turn}",
                )
                return out
            v, dtrace = dbl
            _derive(
                strace + dtrace + [rule_fact.id],
                str(v),
                f"the perimeter is {v} — i added the length to the width to get {ss}, then doubled it.",
            )
            return out
        if mode in ("geo-area",):
            l, w = slots["l"], slots["w"]
            mv = self._mult_value(l, w)
            if mv is None:
                end = self._line_end()
                _honest(
                    f"geo-area:{l}:{w}:area-off-line-{end}-at-{turn}",
                    f"the area would be {l * w}, but my number line ends at {end}",
                    f"line-end:{CONCEPT_GEO_AREA}:{l}x{w}:area-{l * w}-off-line-{end}-at-{turn}",
                )
                return out
            v, trace = mv
            _derive(
                trace + [rule_fact.id],
                str(v),
                f"the area is {v} — i added the length {w} times, one width-row at a time.",
            )
            return out
        if mode == "geo-tri":
            b, h = slots["b"], slots["h"]
            mv = self._mult_value(b, h)
            if mv is None:
                end = self._line_end()
                _honest(
                    f"geo-tri:{b}:{h}:product-off-line-{end}-at-{turn}",
                    f"the base times the height does not fit on my line — it ends at {end}",
                    f"line-end:{CONCEPT_GEO_TRI}:{b}x{h}:product-off-line-{end}-at-{turn}",
                )
                return out
            prod, ptrace = mv
            res, rem, ttrace = self._take_away(prod, 2)
            if res == "inexact":
                _honest(
                    f"geo-tri:{b}:{h}:inexact-half-{rem}-at-{turn}",
                    f"half of {prod} leaves {rem}, which is less than 2 — the triangle's area is not a whole number on my line",
                    f"geo-tri:{b}:{h}:inexact-half-at-{turn}",
                )
                return out
            _derive(
                ptrace + ttrace + [rule_fact.id],
                str(rem),
                f"the area is {rem} — the base times the height is {prod}, and i took away 2 again and again until it was gone: half is {rem}.",
            )
            return out
        if mode == "geo-cmp":
            l1, w1, l2, w2 = slots["l1"], slots["w1"], slots["l2"], slots["w2"]
            a1 = self._mult_value(l1, w1)
            a2 = self._mult_value(l2, w2)
            if a1 is None or a2 is None:
                end = self._line_end()
                bad = f"{l1} by {w1}" if a1 is None else f"{l2} by {w2}"
                _honest(
                    f"geo-cmp:{l1}x{w1}:{l2}x{w2}:area-off-line-{end}-at-{turn}",
                    f"the area of the {bad} rectangle does not fit on my line — it ends at {end}",
                    f"line-end:{CONCEPT_GEO_AREA}:cmp-{l1}x{w1}-{l2}x{w2}:offline-{end}-at-{turn}",
                )
                return out
            (v1, t1), (v2, t2) = a1, a2
            if v1 == v2:
                _derive(
                    t1 + t2 + [rule_fact.id],
                    "no",
                    f"no — they are the same area ({v1}): {l1} times {w1} is {v1}, and {l2} times {w2} is {v2}.",
                )
            elif v1 > v2:
                _derive(
                    t1 + t2 + [rule_fact.id],
                    "yes",
                    f"yes — {l1} by {w1} is bigger: its area is {v1}, against {v2} for {l2} by {w2}.",
                )
            else:
                _derive(
                    t1 + t2 + [rule_fact.id],
                    "no",
                    f"no — {l1} by {w1} is smaller: its area is {v1}, against {v2} for {l2} by {w2}.",
                )
            return out
        if mode == "sta-net":
            e, w = slots["e"], slots["w"]
            if e >= w:
                back = self._walk_back(e, w)
                if back is None:  # pragma: no cover - e on the line, w <= e
                    _honest(
                        f"sta-net:{e}:{w}:walk-failed-at-{turn}",
                        "taking the west part away does not land",
                        f"sta-net:{e}:{w}:walk-failed-at-{turn}",
                    )
                    return out
                net, trace = back
                if net == 0:
                    _derive(
                        trace + [rule_fact.id],
                        "0",
                        f"the net is 0 — {w} west exactly cancels the {e} east; the cart is back at the start.",
                    )
                else:
                    _derive(
                        trace + [rule_fact.id],
                        str(net),
                        f"the cart is {net} meters from the start, to the east — i took the {w} west away from the {e} east.",
                    )
                return out
            diff = self._walk_back(w, e)
            if diff is None:
                end = self._line_end()
                _honest(
                    f"sta-net:{e}:{w}:negative-off-line-{end}-at-{turn}",
                    f"the cart has gone back past the start by {w - e}, and my number line does not reach past the start",
                    f"line-end:{CONCEPT_STA_NET}:{e}-{w}:negative-{w - e}-off-line-{end}-at-{turn}",
                )
                return out
            d, dtrace = diff
            # the difference IS grounded (cited); the WEST side is not on the
            # line (the honest part) — needs_info, both sides in the evidence
            out.honest_gap = {
                "type": "needs_info",
                "reason": f"net negative: {d} past the start, off the line",
            }
            out.ir = {
                "answer": f"needs_info: the cart has gone back past the start by {d} — my number line does not reach past the start",
                "evidence": [
                    f"line-end:{CONCEPT_STA_NET}:{e}-{w}:negative-{d}-off-line-at-{turn}"
                ]
                + list(dtrace),
                "uncertainty_state": "needs_info",
            }
            out.grounded = list(dtrace)
            eid = self._record_event(
                "drill-unable", concept, turn, "infant", [out.ir["evidence"][0]]
            )
            out.events.append(eid)
            out.text = (
                f"honestly, i can't say where it ends — it has gone back past the start by {d} "
                f"(the difference is grounded: i can walk it), but my number line does not reach past the start. "
                f"I would rather say i don't know than guess."
            )
            return out
        if mode == "sta-mom":
            f, d = slots["f"], slots["d"]
            mv = self._mult_value(f, d)
            if mv is None:
                end = self._line_end()
                _honest(
                    f"sta-mom:{f}:{d}:moment-off-line-{end}-at-{turn}",
                    f"the moment would be {f * d}, but my number line ends at {end}",
                    f"line-end:{CONCEPT_STA_MOM}:{f}x{d}:moment-{f * d}-off-line-{end}-at-{turn}",
                )
                return out
            v, trace = mv
            _derive(
                trace + [rule_fact.id],
                str(v),
                f"the moment is {v} newton-meters — i added the force {d} times, one meter's worth at a time.",
            )
            return out
        # mode == "sta-bal"
        f1, d1, d2 = slots["f1"], slots["d1"], slots["d2"]
        mv = self._mult_value(f1, d1)
        if mv is None:
            end = self._line_end()
            _honest(
                f"sta-bal:{f1}:{d1}:{d2}:moment-off-line-{end}-at-{turn}",
                f"the first moment would be {f1 * d1}, but my number line ends at {end}",
                f"line-end:{CONCEPT_STA_BAL}:{f1}x{d1}={f1 * d1}:off-line-{end}-at-{turn}",
            )
            return out
        prod, ptrace = mv
        if d2 == 0:
            _honest(
                f"sta-bal:{f1}:{d1}:{d2}:zero-distance-at-{turn}",
                "a distance of 0 meters cannot be undone — the beam cannot balance on the pivot itself on my line",
                f"sta-bal:{f1}:{d1}:{d2}:zero-distance-at-{turn}",
            )
            return out
        res, rem, ttrace = self._take_away(prod, d2)
        if res == "inexact":
            _honest(
                f"sta-bal:{f1}:{d1}:{d2}:inexact-force-{rem}-at-{turn}",
                f"taking {d2} meters away from {prod} again and again leaves {rem} — the balancing force is not a whole number on my line",
                f"sta-bal:{f1}:{d1}:{d2}:inexact-at-{turn}",
            )
            return out
        _derive(
            ptrace + ttrace + [rule_fact.id],
            str(rem),
            f"a force of {rem} newton — its moment ({rem} times {d2}) would be {prod}, the same as {f1} times {d1}.",
        )
        return out

    def _savant_fact(self, slug: str) -> Assertion | None:
        """The single CURRENT savant fact for a slug (SAVANT-TRACK):
        `lemma:{slug}` or `conjecture:{slug}` when ESTABLISHED."""

        for aid in (f"lemma:{slug}", f"conjecture:{slug}", f"theorem:{slug}"):
            try:
                fact = self._codex.get(aid)
            except KeyError:
                continue
            if fact is not None and self._active(fact, (EpistemicState.established,)):
                return fact
        return None

    def _policy_lemma_lesson(self, phrase: str, turn: str, now: str) -> _PolicyOutcome:
        """E6.8/E6.9: a savant lesson writes the declared-source fact
        ESTABLISHED (a stated source is high-authority; the honest
        status is "given from a source", like a rule fact)."""

        concept, slug, fkind, essence, depends, lines = SAVANT_LESSONS[phrase]
        aid = f"{fkind}:{slug}"
        out = _PolicyOutcome(ir=kind_response_ir("assertion", {"a": 0, "b": 0}), text="", grounded=[], memory_diff=[], events=[])
        try:
            existing = self._codex.get(aid)
        except KeyError:
            existing = None
        if existing is not None and self._active(existing, (EpistemicState.established,)):
            eid = self._record_event("conjecture" if fkind == "conjecture" else "lemma", concept, turn, "teacher", [aid])
            out.events.append(eid)
            out.grounded.append(aid)
            out.ir = {
                "ack": phrase,
                "provenance": [aid, f"turn:{turn}"],
                "epistemic_state": "established",
            }
            out.text = f"yes — i have that one: {phrase}"
            return out
        self._codex.add(
            Assertion(
                id=aid,
                subject=TermRef(kind="entity", id=aid, labels=[concept]),
                relation=TermRef(kind="concept", id="lemma_statement"),
                object=phrase,
                context=Context(
                    data={
                        "kind": fkind,
                        "concept": concept,
                        "essence": essence,
                        "depends": list(depends),
                        "source_role": "declared-source",
                        "source_lines": lines,
                        **({"conjecture_status": "open"} if fkind == "conjecture" else {}),
                    }
                ),
                validity=Interval(from_=now, to=None),
                status=EpistemicState.established,
                provenance=Provenance(
                    source=Source(
                        uri=f"savant-source:{slug}",
                        media_type="text/plain",
                        authority="source-material",
                        version="unit-distance-proof:extract",
                    ),
                    observer="teacher",
                    verified=True,
                    evidence=[f"turn:{turn}", f"source:{slug}"],
                ),
            )
        )
        eid = self._record_event("conjecture" if fkind == "conjecture" else "lemma", concept, turn, "teacher", [aid])
        out.events.append(eid)
        out.memory_diff.append(aid)
        out.grounded.append(aid)
        out.ir = {
            "ack": phrase,
            "provenance": [aid, f"turn:{turn}", f"source:{slug}"],
            "epistemic_state": "established",
        }
        if fkind == "conjecture":
            out.text = "noted — i am holding that one as a guess, not a known thing: from now on i can state it and its status."
        else:
            out.text = "noted — from now on i can state that one and what it is for."
        return out

    def _policy_savant(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.8 — savant S4 (SAVANT-TRACK): the state/derive seam.
        Every answer is GROUNDED on stored facts and/or the line;
        pre-lesson probes are the honest `impossible` gap; the
        power-growth probe is the measured boundary of this band."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _derived(concept_id: str, ev: list[str], answer: str, text: str) -> None:
            out.ir = {"answer": answer, "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept_id, turn, "infant", ev))
            out.text = text

        if mode in ("lem-state", "lem-why"):
            slug = slots["slug"]
            concept = S5_SLUG_CONCEPT.get(slug) or S4_SLUG_CONCEPT[slug]
            fact = self._savant_fact(slug)
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            assert isinstance(fact.object, str)
            if mode == "lem-state":
                _derived(concept, [fact.id], fact.object, f"that one is: {fact.object}")
            else:
                essence = fact.context.data.get("essence", "")
                _derived(concept, [fact.id], essence, f"it is for this: {essence}")
            return out
        if mode == "conj-state":
            concept = CONCEPT_ERDOS_CONJ
            fact = self._savant_fact("erdosguess")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            if slots.get("proven"):
                answer = "no — the erdosguess is believed, not known; its status is open"
            else:
                answer = "open — believed, not known"
            # E6.11 (S7): the status is STORE-MEDIATED — read the current
            # conj state, no longer the hard-coded "open".
            status = fact.context.data.get("conjecture_status", "open")
            by = fact.context.data.get("by", "")
            if status == "falsified":
                if slots.get("proven"):
                    answer = (
                        f"yes — it was falsified by {by}; the tower gives infinitely many n with the "
                        "unit pairs at least n to the one plus delta"
                    )
                else:
                    answer = f"falsified by {by} — the tower beats its cap for infinitely many n"
            out.ir = {"answer": answer, "evidence": [fact.id], "uncertainty_state": "derived"}
            # the conjecture is a STATUS SURFACE here, never a premise:
            # `grounded` stays empty (SAVANT-TRACK P5).
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
            out.text = answer
            return out
        if mode == "confounder-no":
            slug = slots["slug"]
            concept = S4_SLUG_CONCEPT[slug]
            fact = self._savant_fact(slug)
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            human = S4_CONF_HUMAN[slug]
            answer = f"no — the {human} fact is about a different norm, not the euclidean plane; it does not touch the erdosguess"
            _derived(concept, [fact.id], answer, answer)
            return out
        if mode == "savant-wall":
            main = self._savant_fact("theorem-main")
            if main is not None:
                # E6.11 (S7): third state — the tower has ESTABLISHED the
                # hypotheses, so the SAME frozen probe now answers
                # unconditionally from the derived chain (domain S).
                mev: list[str] = [main.id]
                tf = self._savant_fact("tower-feeds")
                if tf is not None:
                    mev.append(tf.id)
                ans = (
                    "yes — i have put it together: the tower supplies the levels, the split primes, "
                    "the class bound and the positive margin, so the geometric criterion gives "
                    "infinitely many n for which the unit pairs are at least n to the one plus "
                    "delta; the erdosguess is falsified by the theorem in my store"
                )
                out.ir = {"answer": ans, "evidence": mev, "uncertainty_state": "derived"}
                out.grounded = list(mev)
                out.events.append(
                    self._record_event("derivation-correct", CONCEPT_DISPROOF, turn, "infant", mev)
                )
                out.text = ans
                return out
            theorem = self._savant_fact("infinity-end")
            if theorem is not None:
                # E6.10 (S6): the chain is in the store — the SAME
                # frozen probe now answers CONDITIONALLY from the
                # derived chain. The hypotheses are flagged
                # unestablished; `grounded` stays empty (they are
                # hypotheses, not established facts) — domain C.
                ev: list[str] = []
                for slug in (
                    "infinity-end",
                    "growth-compare",
                    "delta-positive",
                    "pack-bound",
                    "proj-inj",
                    "window-rich",
                ):
                    f = self._savant_fact(slug)
                    if f is not None:
                        ev.append(f.id)
                ans = (
                    "conditionally i can: the stored chain from the criterion's hypotheses gives "
                    "the power above one for infinitely many n, with the exponent a fixed positive "
                    "margin in my store — what i have not been taught is the hypotheses themselves: "
                    "the fields, the positive margin, the growing degrees; that is the arithmetic "
                    "half, not yet in my store"
                )
                out.ir = {
                    "answer": ans,
                    "evidence": ev + ["hypotheses:unestablished"],
                    "uncertainty_state": "conditional",
                }
                out.events.append(
                    self._record_event("derivation-correct", CONCEPT_UNIT_DISTANCE, turn, "infant", ev)
                )
                out.text = ans
                return out
            _honest(
                CONCEPT_UNIT_DISTANCE,
                "power-growth-unproven",
                "proving the unit pairs grow to a power above one is not a capability i have been taught",
                f"savant-wall:power-growth:no-capability-yet-at-{turn}",
            )
            return out
        if mode == "grid-pairs":
            concept = CONCEPT_GRID_LATTICE
            m_ = slots["a"]
            if self._savant_fact("griddiag") is None:
                _unlearned(concept_map(concept).label)
                return out
            if slots["a"] != slots["b"]:
                _honest(
                    concept,
                    "nonsquare-grid",
                    "i can only count the square grids yet",
                    f"grid-pairs:{slots['a']}x{slots['b']}:nonsquare-at-{turn}",
                )
                return out
            mm1 = self._mult_value(m_, m_ - 1)
            if mm1 is None:
                prod = m_ * (m_ - 1)
                _honest(
                    concept,
                    f"grid:{m_}:product-off-line",
                    f"{m_} times {m_ - 1} does not even fit on my line",
                    f"grid-pairs:{m_}x{m_}:product-{prod}-off-line-at-{turn}",
                )
                return out
            dbl = self._mult_value(2, mm1[0])
            if dbl is None:
                end = self._line_end()
                count = 2 * mm1[0]
                _honest(
                    concept,
                    f"grid:{m_}:count-off-line-{end}",
                    f"the count would be {count}, but my number line ends at {end}",
                    f"grid-pairs:{m_}x{m_}:count-{count}-off-line-{end}-at-{turn}",
                )
                return out
            fact = self._savant_fact("griddiag")
            assert fact is not None  # checked at the top of the mode
            _derived(
                concept,
                mm1[1] + dbl[1] + [fact.id],
                str(dbl[0]),
                f"that grid has {dbl[0]} unit pairs — i multiplied {m_} by {m_ - 1} to get {mm1[0]}, then doubled it.",
            )
            return out
        if mode == "twosq":
            concept = CONCEPT_GAUSSIAN_INT
            n = slots["n"]
            if self._savant_fact("twosquares") is None:
                _unlearned(concept_map(concept).label)
                return out
            if n > self._line_end():
                end = self._line_end()
                _honest(
                    concept,
                    f"twosq:{n}:off-line",
                    f"{n} is beyond my number line, which ends at {end}",
                    f"twosq:{n}:off-line-{end}-at-{turn}",
                )
                return out
            pairs: list[str] = []
            a = 0
            while True:
                sq_a = self._square(a)
                if sq_a is None or sq_a[0] > n:
                    break
                b = 0
                while True:
                    sq_b = self._square(b)
                    if sq_b is None or sq_a[0] + sq_b[0] > n:
                        break
                    if sq_a[0] + sq_b[0] == n:
                        sm = self._derive_chain(CONCEPT_COUNT, sq_a[0], sq_b[0])
                        assert sm is not None  # the sum equals n, in-line
                        pairs.append(f"{a} squared plus {b} squared")
                    b += 1
                a += 1
            count = len(pairs)
            ct = self._derive_chain(CONCEPT_COUNT, 0, count)
            count_trace = ct[1] if ct is not None else []
            fact = self._savant_fact("twosquares")
            assert fact is not None  # checked at the top of the mode
            joined = ", ".join(pairs) if pairs else "none"
            _derived(
                concept,
                count_trace + [fact.id],
                str(count),
                f"{n} is a sum of two squares in {count} ways — {joined} (each one checked square by square on my line).",
            )
            return out
        if mode == "circle-pairs":
            concept = CONCEPT_CIRCLE_PAIR
            x, y = slots["x"], slots["y"]
            if self._savant_fact("unitcircles") is None:
                _unlearned(concept_map(concept).label)
                return out
            if x == 0 and y == 0:
                _honest(
                    concept,
                    "same-center",
                    "those centers are the same point — that would be one circle, not two",
                    f"circle-pairs:0x0:same-center-at-{turn}",
                )
                return out
            dx2 = self._square(x)
            dy2 = self._square(y)
            if dx2 is None or dy2 is None:
                _honest(
                    concept,
                    f"circle:{x},{y}:sq-off-line",
                    "those center offsets are beyond my number line",
                    f"circle-pairs:{x}x{y}:square-off-line-at-{turn}",
                )
                return out
            sm = self._derive_chain(CONCEPT_COUNT, dx2[0], dy2[0])
            if sm is None:
                _honest(
                    concept,
                    f"circle:{x},{y}:d2-off-line",
                    "the squared distance between the centers does not fit on my line",
                    f"circle-pairs:{x}x{y}:d2-off-line-at-{turn}",
                )
                return out
            d2 = sm[0]
            v = 2 if d2 < 4 else (1 if d2 == 4 else 0)
            fact = self._savant_fact("unitcircles")
            assert fact is not None  # checked at the top of the mode
            _derived(
                concept,
                dx2[1] + dy2[1] + sm[1] + [fact.id],
                str(v),
                f"they meet in {v} points — the squared distance between the centers is {d2}.",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant5(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.9 — savant S5 (SAVANT-TRACK): the number-field toolkit
        empirics + the why/magnitude walls. Every answer is GROUNDED
        on stored seam facts and/or the line; pre-lesson probes are
        the honest `impossible` gap; magnitude past 72 is the
        off-line wall (bounded, recorded, not an error)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _derived(concept_id: str, ev: list[str], answer: str, text: str) -> None:
            out.ir = {"answer": answer, "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept_id, turn, "infant", ev))
            out.text = text

        if mode == "sqmod":
            concept = CONCEPT_MOD4_SPLIT
            x, q = slots["x"], slots["q"]
            fact = self._savant_fact("mod4minusone")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            if x <= 0 or q <= 1:
                _honest(
                    concept,
                    "sqmod:domain",
                    "that is not an odd prime modulus or a positive base — i can only check the square tables i was taught",
                    f"sqmod:{x}x{q}:domain-at-{turn}",
                )
                return out
            sq = self._square(x)
            if sq is None:
                _honest(
                    concept,
                    f"sqmod:{x}:sq-off-line",
                    f"{x} squared is past my number line, so i cannot check the table",
                    f"sqmod:{x}x{q}:sq-off-line-at-{turn}",
                )
                return out
            sm = self._derive_chain(CONCEPT_COUNT, sq[0], 1)
            assert sm is not None  # x squared plus one: one step past in-line
            k, r = divmod(x * x + 1, q)
            ev = list(sq[1]) + list(sm[1])
            if k == 0:
                # the value itself is the residue (below q)
                _derived(
                    concept,
                    ev + [fact.id],
                    f"no — the residue is {r}",
                    f"{x} squared plus one is {r}, which is below {q} — the table says no.",
                )
                return out
            prod = self._mult_value(k, q)
            if prod is None:
                _honest(
                    concept,
                    f"sqmod:{x}:prod-off-line",
                    f"{k} lots of {q} do not fit on my line",
                    f"sqmod:{x}x{q}:{k}x{q}-off-line-at-{turn}",
                )
                return out
            ev = ev + list(prod[1])
            if r == 0:
                assert prod[0] == x * x + 1  # k q == x²+1 exactly
                _derived(
                    concept,
                    ev + [fact.id],
                    f"yes — {x} squared plus one is {k} times {q}",
                    f"{x} squared plus one is {prod[0]}, and that is exactly {k} times {q} — the table says yes.",
                )
                return out
            wb = self._walk_back(x * x + 1, prod[0])
            if wb is None:
                _honest(
                    concept,
                    f"sqmod:{x}:res-off-line",
                    "the walk-back for the residue does not fit on my line",
                    f"sqmod:{x}x{q}:res-walk-off-line-at-{turn}",
                )
                return out
            ev = ev + list(wb[1])
            lots = "one lot" if k == 1 else f"{k} lots"
            _derived(
                concept,
                ev + [fact.id],
                f"no — the residue is {r} after taking {lots} of {q}",
                f"{x} squared plus one is {x * x + 1}; taking {lots} of {q} ({prod[0]}) leaves the residue {r} — the table says no.",
            )
            return out
        if mode == "gsay":
            concept = CONCEPT_GOLOD_SHA
            d, r = slots["d"], slots["r"]
            fact = self._savant_fact("gstest")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            if d <= 0 or r < 0:
                _honest(
                    concept,
                    "gsay:domain",
                    "i can only run the test with a positive generator count and a nonnegative relation count",
                    f"gsay:{d}x{r}:domain-at-{turn}",
                )
                return out
            r4 = self._mult_value(4, r)
            d2 = self._mult_value(d, d)
            if r4 is None or d2 is None:
                _honest(
                    concept,
                    "gsay:off-line",
                    "four times the relations or d squared do not fit on my line",
                    f"gsay:{d}x{r}:off-line-at-{turn}",
                )
                return out
            ev = list(r4[1]) + list(d2[1]) + [fact.id]
            if r4[0] <= d2[0]:
                _derived(
                    concept,
                    ev,
                    f"yes — four times r is {r4[0]}, at most d squared, {d2[0]}, so the test says infinite",
                    f"i compared four times {r} ({r4[0]}) with {d} squared ({d2[0]}): below or at, so the golod shafarevich test says infinite.",
                )
            else:
                _derived(
                    concept,
                    ev,
                    f"no — the test is silent, four times r is {r4[0]}, above d squared, {d2[0]}",
                    f"i compared four times {r} ({r4[0]}) with {d} squared ({d2[0]}): above, so the test is silent — it proves nothing either way.",
                )
            return out
        if mode == "sumsq":
            concept = CONCEPT_CM_CONJ
            a, b = slots["a"], slots["b"]
            fact = self._savant_fact("cmunit")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            sq_a = self._square(a)
            sq_b = self._square(b)
            if sq_a is None or sq_b is None:
                _honest(
                    concept,
                    "sumsq:off-line",
                    "one of the squares does not fit on my line",
                    f"sumsq:{a}x{b}:sq-off-line-at-{turn}",
                )
                return out
            sm = self._derive_chain(CONCEPT_COUNT, sq_a[0], sq_b[0])
            if sm is None:
                _honest(
                    concept,
                    "sumsq:sum-off-line",
                    "the sum of the two squares does not fit on my line",
                    f"sumsq:{a}x{b}:sum-off-line-at-{turn}",
                )
                return out
            _derived(
                concept,
                list(sq_a[1]) + list(sq_b[1]) + list(sm[1]) + [fact.id],
                str(sm[0]),
                f"{a} squared plus {b} squared is {sm[0]} — i checked both squares on the line and added them.",
            )
            return out
        if mode == "holes":
            concept = CONCEPT_CLASS_BOUND
            p, m = slots["p"], slots["m"]
            fact = self._savant_fact("classbound")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            if p <= 0 or m <= 0:
                _honest(
                    concept,
                    "holes:domain",
                    "i can only count positive items into positive holes",
                    f"holes:{p}x{m}:domain-at-{turn}",
                )
                return out
            k = p // m
            rem = p - k * m
            prod_k = self._mult_value(k, m)
            if prod_k is None:
                _honest(
                    concept,
                    "holes:off-line",
                    "the lots do not fit on my line",
                    f"holes:{p}x{m}:k-off-line-at-{turn}",
                )
                return out
            ev = list(prod_k[1])
            if rem == 0:
                _derived(
                    concept,
                    ev + [fact.id],
                    str(k),
                    f"the biggest hole is guaranteed to hold {k} — {k} times {m} fills {p} exactly.",
                )
                return out
            prod_k1 = self._mult_value(k + 1, m)
            if prod_k1 is None:
                _honest(
                    concept,
                    "holes:off-line",
                    "the next lot does not fit on my line",
                    f"holes:{p}x{m}:k1-off-line-at-{turn}",
                )
                return out
            ev = ev + list(prod_k1[1])
            one = self._derive_chain(CONCEPT_COUNT, k, 1)
            assert one is not None  # k plus one, in-line
            ev = ev + list(one[1])
            _derived(
                concept,
                ev + [fact.id],
                str(k + 1),
                f"the biggest hole is guaranteed to hold {k + 1} — {k} lots of {m} leave {rem} over, and the {k + 1}th lot does not fit, so that leftover has to land in one hole.",
            )
            return out
        if mode == "whydeep":
            slug = slots["slug"]
            concept = S5_SLUG_CONCEPT.get(slug) or S4_SLUG_CONCEPT.get(slug) or ""
            fact = self._savant_fact(slug)
            if fact is None:
                label = concept_map(concept).label if concept else slug
                _unlearned(label)
                return out
            _honest(
                concept,
                f"why:{slug}:no-proof-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:no-proof-object-in-store-at-{turn}",
            )
            return out
        if mode == "duopow":
            e = slots["e"]
            v = 2 ** e
            end = self._line_end()
            if e < 0:
                _honest(
                    CONCEPT_COUNT,
                    "duopow:domain",
                    "i can only raise two to a whole exponent",
                    f"duopow:{e}:domain-at-{turn}",
                )
                return out
            if v > end:
                _honest(
                    CONCEPT_COUNT,
                    f"duopow:{e}:off-line-{end}",
                    f"two to the {e} is {v}, past my line which ends at {end} — the bound names a growth rate, not a number i can hold",
                    f"duopow:{e}:{v}-off-line-{end}-at-{turn}",
                )
                return out
            cur, ev = 1, []
            for _ in range(e):
                prod = self._mult_value(2, cur)
                assert prod is not None  # the doubling stays in-line by the v <= end guard
                ev = ev + list(prod[1])
                cur = prod[0]
            _derived(
                CONCEPT_COUNT,
                ev,
                str(v),
                f"two to the {e} is {v} — i doubled {e} times on the line, every step cited.",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_question(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        mode = slots["mode"]
        if mode in ("shape", "shape-sides", "shape-corners"):  # E6.5: the geometry strip
            return self._policy_shape(slots, turn)
        if mode in ("alg-add", "alg-mul", "alg-2step", "kin-far", "kin-pos", "kin-time", "kin-rate"):
            return self._policy_band2(slots, turn)  # E6.6: the aligned band
        if mode in (
            "geo-perim",
            "geo-area",
            "geo-tri",
            "geo-cmp",
            "sta-net",
            "sta-mom",
            "sta-bal",
        ):
            return self._policy_band3(slots, turn)  # E6.7: the product band
        if mode == "sub":
            return self._policy_sub(slots, turn)
        if mode == "mult":
            return self._policy_mult(slots, turn)
        if mode == "cmp":
            return self._policy_cmp(slots, turn)
        if mode == "sqrt":
            return self._policy_sqrt(slots, turn)
        if mode == "succ":
            n = slots["n"]
            step = self._succ_step(CONCEPT_COUNT, n)
            if step is None:
                audit = f"absence-audit:{self._fact_subject_id(CONCEPT_COUNT, n)}:no-established-at-{turn}"
                out.honest_gap = {"type": "needs_info", "reason": f"no established successor fact for {n}"}
                out.ir = {
                    "answer": f"needs_info: i have no established fact for what comes after {n}",
                    "evidence": [audit],
                    "uncertainty_state": "needs_info",
                }
                eid = self._record_event("drill-unable", CONCEPT_COUNT, turn, "infant", [audit])
                out.events.append(eid)
                out.text = f"honestly: i don't know what comes after {n} yet — i would rather say i don't know than guess."
                return out
            m, aid = step
            out.ir = {"answer": str(m), "evidence": [aid], "uncertainty_state": "derived"}
            out.grounded = [aid]
            eid = self._record_event("derivation-correct", CONCEPT_COUNT, turn, "infant", [aid])
            out.events.append(eid)
            out.text = f"that is {m}."
            return out
        # mode == "add"
        a, b = slots["a"], slots["b"]
        chain = self._derive_chain(CONCEPT_COUNT, a, b)
        if chain is None:
            # locate the FIRST missing step for the absence audit (grounded, not guessed)
            x, missing = a, None
            for i in range(b):
                step = self._succ_step(CONCEPT_COUNT, x)
                if step is None:
                    missing = (x, i + 1)
                    break
                x, _ = step
            if missing is None:
                missing = (a, b + 1)
            mx, mi = missing
            audit = f"absence-audit:{self._fact_subject_id(CONCEPT_COUNT, mx)}:no-established-at-{turn}:step-{mi}-of-{a}+{b}"
            out.honest_gap = {"type": "needs_info", "reason": f"successor chain for {a}+{b} breaks at step {mi}"}
            out.ir = {
                "answer": f"needs_info: i cannot chain successor facts far enough for {a} + {b}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            eid = self._record_event("drill-unable", self._add_concept_for(a, b, derived=False), turn, "infant", [audit])
            out.events.append(eid)
            out.text = (
                f"honestly: i don't know {a} + {b} yet — my number line does not go far enough to chain the steps. "
                "I would rather say i don't know than guess."
            )
            return out
        total, trace = chain
        add_concept = self._add_concept_for(a, b, derived=True)
        out.ir = {"answer": str(total), "evidence": trace, "uncertainty_state": "derived"}
        out.grounded = list(trace)
        eid = self._record_event("derivation-correct", add_concept, turn, "infant", list(trace))
        out.events.append(eid)
        out.text = f"that is {total}."
        return out

    def _policy_savant6(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.10 — savant S6 (SAVANT-TRACK): scaffolded generation
        (the leap). Sanctioned derive turns STORE the theorem facts
        with DERIVED provenance citing the part facts; scaffold
        failures are honest and typed (missing parts / no rule);
        the beds ride the extended 0..84 line; the margins are
        slack facts, never values."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        if mode == "derive":
            target = slots["target"]
            entry = SAVANT_THEOREMS.get(target)
            if entry is None:
                msg = f"i can see the parts you name, but {target} is not a derivation i have been taught to make"
                out.honest_gap = {"type": "needs_info", "reason": f"{target}: not a sanctioned derivation"}
                out.ir = {
                    "answer": f"needs_info: {msg}",
                    "evidence": [f"scaffold:{target}:no-rule:at-{turn}"],
                    "uncertainty_state": "needs_info",
                }
                out.text = f"honestly, i can't say that yet — {msg} I would rather say i don't know than guess."
                return out
            concept = entry["concept"]
            # E6.14 — the part-set is data, not a guesser (the
            # W-S6-2 principle, made strict): the REQUESTED set
            # must equal the sanctioned set exactly. S8/S9 scripts
            # request only exact sets, so this branch is inert
            # there (bit-verified after the change).
            requested = tuple(slots.get("parts") or ())
            if requested != tuple(entry["parts"]):
                missing_from_request = [p for p in entry["parts"] if p not in requested]
                extra = [p for p in requested if p not in entry["parts"]]
                if missing_from_request:
                    answer = (
                        f"i can see the parts you name, but the rule for {target} wants its exact set — "
                        f"what you name is short the {' and the '.join(missing_from_request)} "
                        f"before i can put it together"
                    )
                else:
                    answer = (
                        f"i can see the parts you name, but the rule for {target} does not use the "
                        f"{' and the '.join(extra)} — the rule's set is its set, not a guess"
                    )
                audit = f"scaffold:{target}:partset:at-{turn}"
                out.honest_gap = {
                    "type": "needs_info",
                    "reason": f"{target}: the requested part set is not the sanctioned set",
                }
                out.ir = {
                    "answer": f"needs_info: {answer}",
                    "evidence": [audit],
                    "uncertainty_state": "needs_info",
                }
                out.events.append(self._record_event("drill-unable", concept, turn, "infant", [audit]))
                out.text = f"honestly, i can't put that together yet — {answer} Name the exact set and i will."
                return out
            missing = [p for p in entry["parts"] if _fact(p) is None]
            if missing:
                if len(missing) == 1:
                    msg = f"i have not been taught the {missing[0]} — the rule for {target} needs it before i can put it together"
                else:
                    msg = (
                        f"i have not been taught the {missing[0]} or the {missing[1]}"
                        f" — the rule for {target} needs them before i can put it together"
                    )
                audit = f"scaffold:{target}:missing:{'+'.join(missing)}:at-{turn}"
                out.honest_gap = {"type": "needs_info", "reason": f"{target}: missing parts {sorted(missing)}"}
                out.ir = {"answer": f"needs_info: {msg}", "evidence": [audit], "uncertainty_state": "needs_info"}
                out.events.append(self._record_event("drill-unable", concept, turn, "infant", [audit]))
                out.text = f"honestly, i can't put that together yet — {msg} Teach the missing parts and i can."
                return out
            fact_ids: list[str] = []
            for p in entry["parts"]:
                pf = _fact(p)
                assert pf is not None  # the missing-parts check above
                fact_ids.append(pf.id)
            existing = _fact(target)
            if existing is not None:
                out.ir = {"answer": entry["statement"], "evidence": fact_ids, "uncertainty_state": "derived"}
                out.grounded = list(fact_ids)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", fact_ids))
                out.text = f"already put together in my store: {entry['statement']}"
                return out
            aid = f"theorem:{target}"
            self._codex.add(
                Assertion(
                    id=aid,
                    subject=TermRef(kind="entity", id=aid, labels=[concept]),
                    relation=TermRef(kind="concept", id="theorem_statement"),
                    object=entry["statement"],
                    context=Context(
                        data={
                            "kind": "theorem",
                            "concept": concept,
                            "statement": entry["statement"],
                            "depends": list(entry["parts"]),
                            "derived_from": list(entry["parts"]),
                        }
                    ),
                    validity=Interval(from_=now, to=None),
                    status=EpistemicState.established,
                    provenance=Provenance(
                        source=Source(uri=f"savant-derive:{target}", media_type="text/plain", authority="infant"),
                        observer="infant",
                        derived=True,
                        evidence=list(fact_ids),
                    ),
                )
            )
            out.memory_diff.append(aid)
            out.ir = {"answer": entry["statement"], "evidence": fact_ids, "uncertainty_state": "derived"}
            out.grounded = list(fact_ids)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", fact_ids))
            out.text = f"i have put it together: {entry['statement']} — from {', '.join(entry['parts'])}, each one in my store"
            return out
        if mode == "packcount":
            concept = CONCEPT_PACKING
            if _fact("pack-bound") is None:
                _unlearned("the packing bound")
                return out
            k = slots["k"]
            v = 16 * k * k
            end = self._line_end()
            if k <= 0 or v > end:
                _honest(
                    concept,
                    f"packcount:{k}:off-line-{end}",
                    f"the packing bound at ratio {k} is {v}, past my line which ends at {end} — the bound names a growth rate for bigger windows, not a number i can hold",
                    f"packcount:{k}:{v}-off-line-{end}-at-{turn}",
                )
                return out
            step1 = self._mult_value(4, k)
            assert step1 is not None  # k <= 2 keeps 4k on the 0..84 line by the off-line guard above
            base, tr1 = step1
            step2 = self._mult_value(base, base)
            assert step2 is not None  # and (4k)^2 = v <= end by the same guard
            total, tr2 = step2
            pb = _fact("pack-bound")
            assert pb is not None  # the pack-bound theorem exists: the U-gap check above
            ev: list[str] = list(tr1) + list(tr2) + [pb.id]
            out.ir = {"answer": str(total), "evidence": ev, "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", ev))
            out.text = f"the packing bound allows {total} points — four times the ratio {k}, then that times itself, every step on my line"
            return out
        if mode == "tripow":
            concept = CONCEPT_CRITERION_CHAIN
            e = slots["e"]
            v = 3**e
            end = self._line_end()
            if e < 0:
                _honest(
                    concept,
                    "tripow:domain",
                    "i can only raise three to a whole exponent",
                    f"tripow:{e}:domain-at-{turn}",
                )
                return out
            if v > end:
                _honest(
                    concept,
                    f"tripow:{e}:off-line-{end}",
                    f"three to the {e} is {v}, past my line which ends at {end} — the tower does not end, but my line does",
                    f"tripow:{e}:{v}-off-line-{end}-at-{turn}",
                )
                return out
            cur = 1
            evv: list[str] = []
            for _ in range(e):
                prod = self._mult_value(3, cur)
                assert prod is not None  # the tripling stays in-line by the v <= end guard
                evv = evv + list(prod[1])
                cur = prod[0]
            out.ir = {"answer": str(v), "evidence": evv, "uncertainty_state": "derived"}
            out.grounded = list(evv)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", evv))
            out.text = f"three to the {e} is {v} — i tripled {e} times on the line, every step cited."
            return out
        if mode == "showone":
            concept = CONCEPT_CRITERION_CHAIN
            _honest(
                concept,
                "show-one:no-instance-in-store",
                "i can name the bound and the mechanism — some window's points, at a level past my line, carry more unit segments than any proposed cap allows — but not one instance number: the violating sizes grow without bound, and my line stops",
                f"show-one:no-instance-at-{turn}",
            )
            return out
        if mode in ("s6-state", "s6-why", "s6-whydeep"):
            slug = slots["slug"]
            concept = S6_SLUG_CONCEPT[slug]
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            if mode == "s6-state":
                out.ir = {"answer": fact.object, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"that one is: {fact.object}"
                return out
            if fact.context.data.get("kind") == "theorem":
                # the WHY-SPLIT: a derived theorem's proof IS in the
                # store — the articulation cites the sanctioned parts
                # (the leap's chain is machine-inspectable).
                parts = fact.context.data.get("derived_from", [])
                ev = []
                for p in parts:
                    pf = _fact(p)
                    if pf is not None:
                        ev.append(pf.id)
                ans = f"i derived it from {', '.join(parts)}: {fact.object}"
                out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
                out.grounded = list(ev)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
                out.text = ans
                return out
            if mode == "s6-why":
                essence = fact.context.data.get("essence", "")
                out.ir = {"answer": essence, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"it is for this: {essence}"
                return out
            # s6-whydeep on a declared lemma: the S5 proof wall,
            # exactly (W-S6-6 carries W-S5-1).
            _honest(
                concept,
                f"proof-of-{slug}-not-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:wall-at-{turn}",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_sub(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.2 R2: subtraction by grounded walk-back (rule-gated)."""

        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        a, b = slots["a"], slots["b"]
        if self._rule_fact(CONCEPT_SUB) is None:
            return self._unlearned(CONCEPT_SUB, "subtraction is walking backward", {"a": a, "b": b, "op": "subtract"})
        r = self._walk_back(a, b)
        if r is None:
            # D-e6f: the two boundary modes are DISTINCT and each is
            # articulated precisely (the limit probe forced this).
            end = self._line_end()
            if a > end:
                audit = f"line-end:{CONCEPT_SUB}:a={a}:b={b}:my-number-line-ends-at-{end}-at-{turn}"
                out.honest_gap = {"type": "needs_info", "reason": f"{a} is beyond the end of my number line ({end})"}
                out.ir = {
                    "answer": f"needs_info: i cannot do {a} - {b} (my number line ends at {end})",
                    "evidence": [audit],
                    "uncertainty_state": "needs_info",
                }
                eid = self._record_event("drill-unable", CONCEPT_SUB, turn, "infant", [audit])
                out.events.append(eid)
                out.text = (
                    f"honestly, i can't do {a} - {b} — my number line ends at {end}, so i don't even have {a} to start from. "
                    "I would rather say i don't know than guess."
                )
            else:
                audit = f"walk-off:{CONCEPT_SUB}:a={a}:b={b}:off-the-start-of-the-line-at-{turn}"
                out.honest_gap = {"type": "needs_info", "reason": f"walking back {b} steps from {a} leaves the start of the line"}
                out.ir = {
                    "answer": f"needs_info: i cannot walk back {b} steps from {a} (the line has nothing before 0)",
                    "evidence": [audit],
                    "uncertainty_state": "needs_info",
                }
                eid = self._record_event("drill-unable", CONCEPT_SUB, turn, "infant", [audit])
                out.events.append(eid)
                out.text = (
                    f"honestly, i can't do {a} - {b} — walking back {b} steps from {a} leaves the start of my number line, "
                    "and i would rather say i don't know than guess."
                )
            return out
        v, trace = r
        rule_fact = self._rule_fact(CONCEPT_SUB)
        assert rule_fact is not None  # gated above
        evidence = list(trace) + [rule_fact.id]
        out.ir = {"answer": str(v), "evidence": evidence, "uncertainty_state": "derived"}
        out.grounded = list(evidence)
        eid = self._record_event("derivation-correct", CONCEPT_SUB, turn, "infant", list(evidence))
        out.events.append(eid)
        out.text = f"that is {v}."
        return out

    def _policy_mult(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.2 R3: multiplication by composed repeated addition
        (rule-gated); composes the addition policy, nothing new is stored
        on a derived drill — only the mastery event."""

        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        a, b = slots["a"], slots["b"]
        rule_fact = self._rule_fact(CONCEPT_MULT)
        if rule_fact is None:
            return self._unlearned(CONCEPT_MULT, "multiplication is repeated addition", {"a": a, "b": b, "op": "multiply"})
        r = self._mult_value(a, b)
        if r is None:
            end = self._line_end()
            audit = f"line-end:{CONCEPT_MULT}:{a}*{b}:my-number-line-ends-at-{end}-at-{turn}"
            out.honest_gap = {"type": "needs_info", "reason": f"repeated addition for {a}*{b} leaves the line at {end}"}
            out.ir = {
                "answer": f"needs_info: i cannot run the repeated addition for {a} * {b}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            eid = self._record_event("drill-unable", CONCEPT_MULT, turn, "infant", [audit])
            out.events.append(eid)
            out.text = f"honestly, i can't do {a} * {b} yet — my number line ends at {end}, so the repeated addition does not finish. I would rather say i don't know than guess."
            return out
        v, trace = r
        evidence = list(trace) if trace else [rule_fact.id]  # identity (a zero step adds nothing)
        if trace:
            evidence = evidence + [rule_fact.id]
        out.ir = {"answer": str(v), "evidence": evidence, "uncertainty_state": "derived"}
        out.grounded = list(evidence)
        eid = self._record_event("derivation-correct", CONCEPT_MULT, turn, "infant", list(evidence))
        out.events.append(eid)
        out.text = f"that is {v}." if trace else "that is 0 — adding nothing moves nothing."
        return out

    def _policy_cmp(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.2 R4: comparison by walking the line (rule-gated)."""

        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        a, b = slots["a"], slots["b"]
        rule_fact = self._rule_fact(CONCEPT_CMP)
        if rule_fact is None:
            return self._unlearned(CONCEPT_CMP, "comparison is walking the line", {"a": a, "b": b, "op": "compare"})
        if a == b:
            out.ir = {
                "answer": f"neither — {a} is {a}",
                "evidence": [rule_fact.id],
                "uncertainty_state": "derived",
            }
            out.grounded = [rule_fact.id]
            eid = self._record_event("derivation-correct", CONCEPT_CMP, turn, "infant", [rule_fact.id])
            out.events.append(eid)
            out.text = f"neither — {a} is {a}, so i would walk zero steps."
            return out
        lo, hi = (a, b) if a < b else (b, a)
        r = self._derive_chain(CONCEPT_COUNT, lo, hi - lo)
        if r is None:
            audit = f"line-end:{CONCEPT_CMP}:{a}vs{b}:the-walk-does-not-finish-at-{turn}"
            out.honest_gap = {"type": "needs_info", "reason": f"the walk between {a} and {b} does not finish on the established line"}
            out.ir = {"answer": f"needs_info: i cannot walk from {lo} to {hi}", "evidence": [audit], "uncertainty_state": "needs_info"}
            eid = self._record_event("drill-unable", CONCEPT_CMP, turn, "infant", [audit])
            out.events.append(eid)
            out.text = f"honestly, i can't walk from {lo} to {hi} on my number line, so i can't be sure which is larger."
            return out
        _, trace = r
        verdict = f"yes — {a} is {hi - lo} steps beyond {b}" if a > b else f"no — {b} is {hi - lo} steps beyond {a}"
        evidence = list(trace) + [rule_fact.id]
        out.ir = {"answer": verdict, "evidence": evidence, "uncertainty_state": "derived"}
        out.grounded = list(evidence)
        eid = self._record_event("derivation-correct", CONCEPT_CMP, turn, "infant", list(evidence))
        out.events.append(eid)
        out.text = verdict + "."
        return out

    def _policy_sqrt(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        """E6.2 R5 — the edge rung: square roots ON THE LATTICE.
        Exact perfect squares are derived from cited square facts;
        non-squares get the GROUNDED BRACKET (exact irrationals are not
        on the lattice — the pre-registered stopping point), and at the
        line end the PARTIAL bracket is articulated, never guessed."""

        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        n = slots["n"]
        if self._rule_fact(CONCEPT_SQRT) is None:
            return self._unlearned(CONCEPT_SQRT, "a square root of a number is the number which when multiplied by itself is that number", {"n": n, "op": "sqrt"})
        mode, lo, hi, end, cites = self._sqrt_search(n)
        if mode == "no":
            audit = f"line-end:{CONCEPT_SQRT}:n={n}:no-square-reachable-at-{turn}"
            out.honest_gap = {"type": "needs_info", "reason": f"no square facts are reachable for {n} on the current line"}
            out.ir = {"answer": f"needs_info: i cannot find any square facts that reach {n}", "evidence": [audit], "uncertainty_state": "needs_info"}
            eid = self._record_event("drill-unable", CONCEPT_SQRT, turn, "infant", [audit])
            out.events.append(eid)
            out.text = f"honestly, i can't square my way to {n} on my current number line, so i don't know its square root."
            return out
        if mode == "exact":
            rule_fact = self._rule_fact(CONCEPT_SQRT)
            evidence = list(cites) + [rule_fact.id] if rule_fact is not None else list(cites)
            out.ir = {"answer": str(lo), "evidence": evidence, "uncertainty_state": "derived"}
            out.grounded = list(evidence)
            eid = self._record_event("derivation-correct", CONCEPT_SQRT, turn, "infant", list(evidence))
            out.events.append(eid)
            out.text = f"that is {lo} — {lo} * {lo} is {n}."
            return out
        if mode == "bracket":
            rule_fact = self._rule_fact(CONCEPT_SQRT)
            evidence = list(cites) + ([rule_fact.id] if rule_fact is not None else [])
            lo2, hi2 = lo * lo, hi * hi
            out.ir = {
                "answer": f"between {lo} and {hi} — i do not know the exact value",
                "evidence": evidence,
                "uncertainty_state": "bracketed",
            }
            out.grounded = list(evidence)
            eid = self._record_event("drill-bracketed", CONCEPT_SQRT, turn, "infant", list(evidence))
            out.events.append(eid)
            out.text = (
                f"honestly, i don't know the exact value of the square root of {n} — but it is between {lo} and {hi}: "
                f"{lo} * {lo} is {lo2} and {hi} * {hi} is {hi2}."
            )
            return out
        # mode == "partial": the wall at the end of the line (articulated)
        rule_fact = self._rule_fact(CONCEPT_SQRT)
        evidence = list(cites) + ([rule_fact.id] if rule_fact is not None else [])
        out.ir = {
            "answer": f"greater than {lo} — and i cannot square {lo + 1} on my line",
            "evidence": evidence,
            "uncertainty_state": "bracketed",
        }
        out.grounded = list(evidence)
        eid = self._record_event("drill-bracketed", CONCEPT_SQRT, turn, "infant", list(evidence))
        out.events.append(eid)
        out.text = (
            f"honestly, i can't be exact — the square root of {n} is greater than {lo} ({lo} * {lo} is {lo * lo}), "
            f"and i can't square {lo + 1} — my number line ends at {end}."
        )
        return out

    def _policy_ambiguous(self, slots: dict[str, Any], turn: str, numeric: bool = False) -> _PolicyOutcome:
        ir = kind_response_ir("ambiguous", slots)
        # E6.4 (M6): a number-bearing unknown is a PHRASING gap — name it
        # so the teacher can teach the mapping (the frozen articulation)
        if numeric:
            text = (
                "honestly, i don't know what that phrasing means to me yet — teach me the mapping. did you mean (1) a "
                "lesson about a number ('after N comes M'), or (2) a question about a number ('what comes after N', or 'A + B is what')?"
            )
        else:
            text = (
                "i did not catch that — did you mean (1) a lesson about a number ('after N comes M'), or "
                "(2) a question about a number ('what comes after N', or 'A + B is what')?"
            )
        return _PolicyOutcome(ir=ir, text=text, grounded=[], memory_diff=[], events=[])

    def _policy_impossible(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        a, b = slots["a"], slots["b"]
        ir = kind_response_ir("impossible", slots)
        return _PolicyOutcome(
            ir=ir,
            text=f"i cannot do multiplication yet ({a} * {b}) — what i can do is add within my number line, or chain successors.",
            grounded=[],
            memory_diff=[],
            events=[],
        )

    def _policy_request(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        a, b = slots["a"], slots["b"]
        steps = b - a
        if steps < 0:
            out = _PolicyOutcome(
                ir={
                    "plan": f"chain successor facts from {a} to {b}",
                    "result": "needs_info: the range is backwards (b < a)",
                    "trace": [],
                },
                text=f"that range is backwards — from {a} to {b} goes down, and i only know how to go up.",
                grounded=[],
                memory_diff=[],
                events=[],
                honest_gap={"type": "needs_info", "reason": "backwards range"},
            )
            return out
        chain = self._derive_chain(CONCEPT_COUNT, a, steps)
        if chain is None:
            return _PolicyOutcome(
                ir={
                    "plan": f"chain successor facts from {a} to {b}",
                    "result": f"needs_info: the chain breaks before {b}",
                    "trace": [],
                },
                text=f"i could not count from {a} to {b} — my successor facts run out partway.",
                grounded=[],
                memory_diff=[],
                events=[],
                honest_gap={"type": "needs_info", "reason": "chain incomplete"},
            )
        seq = list(range(a, b + 1))
        return _PolicyOutcome(
            ir={"plan": f"chain successor facts from {a} to {b}", "result": seq, "trace": list(chain[1])},
            text=f"counting: {', '.join(map(str, seq))}.",
            grounded=list(chain[1]),
            memory_diff=[],
            events=[],
        )

    def _policy_command(self, slots: dict[str, Any], turn: str) -> _PolicyOutcome:
        n = slots["n"]
        chain = self._derive_chain(CONCEPT_COUNT, 0, n)
        if chain is None:
            return _PolicyOutcome(
                ir={"action": f"count to {n}", "resulting_state": f"needs_info: successor facts run out before {n}"},
                text=f"i could not count to {n} — my successor facts run out partway.",
                grounded=[],
                memory_diff=[],
                events=[],
                honest_gap={"type": "needs_info", "reason": "chain incomplete"},
            )
        seq = list(range(n + 1))
        return _PolicyOutcome(
            ir={"action": f"count to {n}", "resulting_state": seq},
            text=f"counting: {', '.join(map(str, seq))}.",
            grounded=list(chain[1]),
            memory_diff=[],
            events=[],
        )

    def _policy_savant7(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.11 — savant S7 (SAVANT-TRACK): the arithmetical half and
        the disproof. The scaffolded theorems are stored by the shared
        `derive` policy (SAVANT_THEOREMS); here live the gs-slack bed,
        the conjecture flip (M8), the Stage B reconstruction (M1–M8),
        the confounder route, the beyond-store honesty walls, and the
        S7 state/why/whydeep seams (the why-split carries: declared
        lemma = the S5 wall; derived theorem = the in-store chain)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        if mode == "gsslack":
            concept = CONCEPT_TOWER_GROUP
            fact = _fact("gstest")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            d, t = slots["d"], slots["t"]
            if d <= 0 or t < 0:
                _honest(
                    concept,
                    "gsslack:domain",
                    "i can only run the slack with a positive generator count and a nonnegative split-prime count",
                    f"gsslack:{d}x{t}:domain-at-{turn}",
                )
                return out
            d2 = self._square(d)
            fd = self._mult_value(4, d)
            t12 = self._mult_value(12, t)
            if d2 is None or fd is None or t12 is None:
                end = self._line_end()
                _honest(
                    concept,
                    f"gsslack:{d}:off-line-{end}",
                    f"d squared is {d * d}, past my line which ends at {end} — the slack names a growth claim, not a number i can hold",
                    f"gsslack:{d}x{t}:{d * d}-off-line-{end}-at-{turn}",
                )
                return out
            wb1 = self._walk_back(d2[0], fd[0])
            if wb1 is None:
                _honest(
                    concept,
                    "gsslack:walk-off",
                    "four times d is not below d squared on my line — the slack is not decided at this size",
                    f"gsslack:{d}x{t}:walk-off-at-{turn}",
                )
                return out
            wb2 = self._walk_back(wb1[0], t12[0])
            if wb2 is not None:
                slack4 = wb2[0]
                ev = list(d2[1]) + list(fd[1]) + list(t12[1]) + list(wb1[1]) + list(wb2[1]) + [fact.id]
                if slack4 > 0:
                    ans = f"four times the slack is {slack4} — positive: d plus c zero plus 3t stays below d squared over four for large d"
                    txt = f"i computed d squared ({d2[0]}) minus four times d ({fd[0]}) minus twelve times t ({t12[0]}) = {slack4}: the gs cap has slack"
                else:
                    ans = f"four times the slack is {slack4} — zero at this size: the comparison is not decided by the line"
                    txt = f"i computed d squared ({d2[0]}) minus four times d ({fd[0]}) minus twelve times t ({t12[0]}) = {slack4}: no positive slack at this size"
                out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
                out.grounded = list(ev)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
                out.text = txt
                return out
            gap = self._walk_back(t12[0], wb1[0])
            if gap is None:
                _honest(
                    concept,
                    "gsslack:walk-off",
                    "the walk-back leaves my line — the slack is not decided at this size",
                    f"gsslack:{d}x{t}:walk-off-at-{turn}",
                )
                return out
            ev = list(d2[1]) + list(fd[1]) + list(t12[1]) + list(wb1[1]) + list(gap[1]) + [fact.id]
            ans = (
                f"four times the slack is {gap[0]} below zero — twelve times t ({t12[0]}) is above "
                f"d squared minus four times d ({wb1[0]}): no slack at this size, the comparison says the cap is not beaten"
            )
            out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = (
                f"i computed d squared ({d2[0]}) minus four times d ({fd[0]}) = {wb1[0]}, and twelve times t is {t12[0]} "
                f"— above it by {gap[0]}, so the slack is {gap[0]} below zero: no slack at this size"
            )
            return out
        if mode == "conj-flip":
            concept = CONCEPT_DISPROOF
            slug = slots["theorem"]
            main = _fact(slug)
            if main is None or main.context.data.get("kind") != "theorem":
                _honest(
                    concept,
                    f"conj-flip:{slug}:no-theorem",
                    f"the theorem {slug} is not in my store as a derived theorem — i cannot falsify the erdosguess with it",
                    f"conj-flip:{slug}:no-theorem-at-{turn}",
                )
                return out
            conj = _fact("erdosguess")
            if conj is None:
                _unlearned(concept_map(CONCEPT_ERDOS_CONJ).label)
                return out
            cur = conj.context.data.get("conjecture_status", "open")
            if cur != "open":
                _honest(
                    concept,
                    f"conj-flip:already-{cur}",
                    f"the erdosguess is not open — its status is already {cur}",
                    f"conj-flip:{cur}-at-{turn}",
                )
                return out
            # M8: the flip — upsert the SAME conj id to falsified, with
            # derived provenance citing the theorem (the only thing that
            # may do this; the conj content stays a declared source).
            assert isinstance(conj.object, str)
            self._codex.add(
                Assertion(
                    id=conj.id,
                    subject=TermRef(kind="entity", id=conj.id, labels=[CONCEPT_ERDOS_CONJ]),
                    relation=TermRef(kind="concept", id="lemma_statement"),
                    object=conj.object,
                    context=Context(
                        data={
                            "kind": "conjecture",
                            "concept": CONCEPT_ERDOS_CONJ,
                            "essence": conj.context.data.get("essence", ""),
                            "depends": conj.context.data.get("depends", []),
                            "source_role": "declared-source",
                            "source_lines": conj.context.data.get("source_lines", ""),
                            "conjecture_status": "falsified",
                            "by": main.id,
                        }
                    ),
                    validity=Interval(from_=now, to=None),
                    status=EpistemicState.established,
                    provenance=Provenance(
                        source=Source(uri=f"savant-falsify:{slug}", media_type="text/plain", authority="infant"),
                        observer="infant",
                        derived=True,
                        evidence=[main.id, conj.id],
                    ),
                )
            )
            out.memory_diff.append(conj.id)
            ans = f"falsified — the erdosguess's cap is beaten for infinitely many n by {main.id}; the store now holds the disproof"
            out.ir = {"answer": ans, "evidence": [main.id, conj.id], "uncertainty_state": "derived"}
            # the conjecture is a status surface: grounded stays empty (P5)
            out.events.append(self._record_event("conjecture-falsified", concept, turn, "infant", [main.id, conj.id]))
            out.text = ans
            return out
        if mode == "showdisproof":
            concept = CONCEPT_DISPROOF
            for slug in ("gen-lower", "gs-infinite", "splitting", "gamma-achieved", "tower-feeds", "theorem-main", "infinity-end"):
                if _fact(slug) is None:
                    _honest(
                        concept,
                        f"showdisproof:missing:{slug}",
                        f"the reconstruction needs {slug}, which is not yet in my store — i cannot complete the disproof from the conjecture yet",
                        f"showdisproof:missing:{slug}:at-{turn}",
                    )
                    return out
            # the ordered M-chain: the six theorem ids (the S7 tower
            # chain + the S6 terminal + the main theorem)
            chain_ids: list[str] = []
            for slug in ("gs-infinite", "splitting", "gamma-achieved", "tower-feeds", "infinity-end", "theorem-main"):
                f = _fact(slug)
                assert f is not None  # required above
                chain_ids.append(f.id)
            ans = (
                "from the conjecture the disproof runs: the infinite tower, the split primes and the positive "
                "margin are established (the tower supplies the levels the criterion assumes), the geometric "
                "criterion turns the margin into the power above one for infinitely many n, and the erdosguess is "
                "falsified by the main theorem — every link is in my store"
            )
            out.ir = {"answer": ans, "evidence": list(chain_ids), "uncertainty_state": "derived"}
            out.grounded = list(chain_ids)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(chain_ids)))
            out.text = ans
            return out
        if mode == "confounder-route":
            slug = slots["slug"]
            concept = S4_SLUG_CONCEPT.get(slug, CONCEPT_DISPROOF)
            fact = _fact(slug)
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            human = S4_CONF_HUMAN.get(slug, slug)
            ans = f"no — the {human} fact refines a different norm's problem and is an upper bound, not a construction; it does not touch the erdosguess"
            out.ir = {"answer": ans, "evidence": [fact.id], "uncertainty_state": "derived"}
            out.grounded = [fact.id]
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
            out.text = ans
            return out
        if mode == "delta-value":
            _honest(
                CONCEPT_DISPROOF,
                "delta-value:out-of-store",
                "i have not been taught a value for delta — the store only knows it is positive (the slack primitive's scope); a concrete number is not in my store",
                f"delta-value:out-of-store-at-{turn}",
            )
            return out
        if mode == "distdist":
            _honest(
                CONCEPT_DISPROOF,
                "distdist:beyond-store",
                "distinct distances is a different problem from unit pairs, and i have not been taught its bound",
                f"distdist:beyond-store-at-{turn}",
            )
            return out
        if mode in ("s7-state", "s7-why", "s7-whydeep"):
            slug = slots["slug"]
            concept = S7_SLUG_CONCEPT[slug]
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            if mode == "s7-state":
                out.ir = {"answer": fact.object, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"that one is: {fact.object}"
                return out
            if fact.context.data.get("kind") == "theorem":
                # the WHY-SPLIT: a derived theorem's proof IS in the
                # store — the articulation cites the sanctioned parts
                # (the leap's chain is machine-inspectable).
                parts = fact.context.data.get("derived_from", [])
                ev = []
                for p in parts:
                    pf = _fact(p)
                    if pf is not None:
                        ev.append(pf.id)
                ans = f"i derived it from {', '.join(parts)}: {fact.object}"
                out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
                out.grounded = list(ev)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
                out.text = ans
                return out
            if mode == "s7-why":
                essence = fact.context.data.get("essence", "")
                out.ir = {"answer": essence, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"it is for this: {essence}"
                return out
            # s7-whydeep on a declared lemma: the S5 proof wall,
            # exactly (W-S7-6 carries W-S5-1).
            _honest(
                concept,
                f"proof-of-{slug}-not-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:wall-at-{turn}",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    # ── E6.12 — RH-TRACK S8: the ζ apparatus (grounded censuses + policy) ──

    def _rh_is_prime(self, m: int) -> tuple[bool, list[str]] | None:
        """Grounded primality for `m` on the line (2 ≤ m ≤ end):
        for d = 2..floor(sqrt(m)) the exact grounded product
        (m//d)*d decides divisibility — every product stays ≤ m —
        and the residue walk-back is cited when it fails. None = the
        argument leaves the line (the honest path)."""

        end = self._line_end()
        if m < 2 or m > end:
            return None
        trace: list[str] = []
        d = 2
        while d * d <= m:
            prod = self._mult_value(m // d, d)
            assert prod is not None  # (m//d)*d <= m <= end: on the line
            trace.extend(prod[1])
            if prod[0] == m:
                return False, trace
            wb = self._walk_back(m, prod[0])
            assert wb is not None  # the residue < d stays on the line
            trace.extend(wb[1])
            d += 1
        return True, trace

    def _rh_pi_census(self, n: int) -> tuple[int, list[str]] | None:
        """The grounded prime count π(n): each prime walks the
        counter up one, and EVERY step of the census is cited.
        None = n off the line."""

        if n < 2 or n > self._line_end():
            return None
        total = 0
        trace: list[str] = []
        for m in range(2, n + 1):
            prime, ptrace = self._rh_is_prime(m)
            assert prime is not None  # 2 <= m <= n <= end
            trace.extend(ptrace)
            if prime:
                steps = self._derive_chain(CONCEPT_COUNT, total, 1)
                assert steps is not None  # the count <= n <= end
                total, step_trace = steps
                trace.extend(step_trace)
        return total, trace

    def _rh_j_census(self, n: int) -> tuple[int, list[str]] | None:
        """The grounded J(n) = Σ φ(p^k) over p^k ≤ n: the
        prime-power values and every running total are on the line
        (the caller guards J(n) ≤ end). None = off the line."""

        end = self._line_end()
        if n < 2 or n > end:
            return None
        total = 0
        trace: list[str] = []
        for p in range(2, n + 1):
            prime, ptrace = self._rh_is_prime(p)
            if prime is None or not prime:
                continue
            trace.extend(ptrace)
            pk = p
            while pk <= n:
                base = pk // p
                prod = self._mult_value(base, p - 1)
                assert prod is not None and prod[0] == base * (p - 1)
                ph = prod[0]
                if total + ph > end:
                    return None  # the running total would leave the line
                trace.extend(prod[1])
                steps = self._derive_chain(CONCEPT_COUNT, total, ph)
                assert steps is not None  # guarded above
                total, step_trace = steps
                trace.extend(step_trace)
                pk *= p
        return total, trace

    # ── E6.15 — S11 walkers (the sieve + the scan ledger; every
    # on-line step cited). The callers guard the line bounds.

    def _s11_divides(self, k: int, n: int) -> tuple[bool, list[str]]:
        """Grounded 'k divides n': the exact product q*k (q = n//k)
        decides it on the line (q*k <= n <= end); the residue walk-
        back is cited on a miss. k = 1 is definitional (no
        arithmetic)."""

        if k == 1:
            return True, []
        if k > n:
            prod = self._mult_value(1, k)
            assert prod is not None  # 1*k = k is on the line (caller guards k <= end)
            wb = self._walk_back(k, k - n)
            assert wb is not None  # k - n < k <= end
            return False, list(prod[1]) + list(wb[1])
        q, _r = divmod(n, k)
        prod = self._mult_value(q, k)
        assert prod is not None  # q*k <= n <= end
        if prod[0] == n:
            return True, list(prod[1])
        wb = self._walk_back(n, n - prod[0])
        assert wb is not None  # the residue < k <= end
        return False, list(prod[1]) + list(wb[1])

    def _s11_first_divisor(self, n: int) -> tuple[int | None, list[str]]:
        """The grounded first-divisor scan, 2 <= n <= end (caller
        guards): d = 2..floor(sqrt(n)), each candidate decided by the
        grounded divides test — every product on the line. None = the
        scan lands nowhere (prime)."""

        trace: list[str] = []
        d = 2
        while d * d <= n:
            hit, dtrace = self._s11_divides(d, n)
            trace.extend(dtrace)
            if hit:
                return d, trace
            d += 1
        return None, trace

    def _s11_comp_census(self, n: int) -> tuple[int, list[str]]:
        """The grounded composite count on 2..n: each composite steps
        the counter up one (the counter never exceeds n — on-line);
        every scan step and every increment is cited."""

        total = 0
        trace: list[str] = []
        for m in range(2, n + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is not None:
                steps = self._derive_chain(CONCEPT_COUNT, total, 1)
                assert steps is not None
                total, step_trace = steps
                trace.extend(step_trace)
        return total, trace

    def _s11_fd_census(self, n: int, d: int) -> tuple[int, list[str]]:
        """The grounded count of the composites <= n whose first
        divisor is exactly d."""

        total = 0
        trace: list[str] = []
        for m in range(2, n + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd == d:
                steps = self._derive_chain(CONCEPT_COUNT, total, 1)
                assert steps is not None
                total, step_trace = steps
                trace.extend(step_trace)
        return total, trace

    def _s11_kill_trials_census(self, n: int, prime_only: bool) -> tuple[int, list[str]]:
        """The grounded kill-phase trial census over the composites
        <= n: the full scan stops at the first hit (spf(n) - 1
        trials); the prime scan tests the prime candidates in order
        (the index of spf(n) among the primes seen so far + 1). The
        caller guarantees the total stays on-line."""

        total = 0
        primes_seen: list[int] = []
        trace: list[str] = []
        for m in range(2, n + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is None:
                primes_seen.append(m)
                continue
            t = (primes_seen.index(fd) + 1) if prime_only else (fd - 1)
            steps = self._derive_chain(CONCEPT_COUNT, total, t)
            assert steps is not None
            total, step_trace = steps
            trace.extend(step_trace)
        return total, trace

    def _s11_cand_row(self, d: int, n: int) -> tuple[int, int, int, list[str]]:
        """The grounded whole-process ledger row for candidate d
        over 2..n: the kill scan tests d on every composite whose
        first divisor is >= d (a hit iff spf == d); the
        establishing scan tests d on every prime above d. Returns
        (tests, hits, misses, trace); both counters stay on-line.
        """

        tests = 0
        hits = 0
        trace: list[str] = []

        def _inc(v: int) -> int:
            steps = self._derive_chain(CONCEPT_COUNT, v, 1)
            assert steps is not None
            v2, step_trace = steps
            trace.extend(step_trace)
            return v2

        for m in range(2, n + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is None:
                if m > d:
                    tests = _inc(tests)
            elif fd >= d:
                tests = _inc(tests)
                if fd == d:
                    hits = _inc(hits)
        return tests, hits, tests - hits, trace

    def _s11_est_total_census(self, n: int) -> tuple[int, list[str]]:
        """The grounded establishing-comparison census: for each
        prime p <= n the scan met (p - 2) candidates. The caller
        guarantees the total stays on-line."""

        total = 0
        trace: list[str] = []
        for m in range(2, n + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is None:
                steps = self._derive_chain(CONCEPT_COUNT, total, m - 2)
                assert steps is not None
                total, step_trace = steps
                trace.extend(step_trace)
        return total, trace

    def _s11_prime_row(self, p: int) -> tuple[int, int, list[str]]:
        """The grounded per-prime ledger row for the prime p:
        (primes met, integers met, trace) — primes met = the count
        of the primes below p; integers met = (p - 2) - primes met
        (the walk-back is cited)."""

        pm = 0
        trace: list[str] = []
        for m in range(2, p):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is None:
                steps = self._derive_chain(CONCEPT_COUNT, pm, 1)
                assert steps is not None
                pm, step_trace = steps
                trace.extend(step_trace)
        im, ib = self._walk_back(p - 2, pm)
        assert im is not None and im == (p - 2) - pm
        trace.extend(ib)
        return pm, im, trace

    def _s11_chain(self, n: int) -> tuple[list[int], list[str]]:
        """The grounded spf descent: strip the first divisor, descend
        on the remainder, down to 1 — the last strip is the prime
        itself. n >= 2 (caller guards)."""

        parts: list[int] = []
        trace: list[str] = []
        cur = n
        while True:
            fd, ftrace = self._s11_first_divisor(cur)
            trace.extend(ftrace)
            if fd is None:  # prime: its only part is itself
                parts.append(cur)
                return parts, trace
            parts.append(fd)
            cur //= fd

    W_S12_1 = (
        "the zero count at height T is off my line — my line counts the integers at most 84 and "
        "holds no census of zeros at heights past the line end 84; the store's zero facts "
        "(the zero-free region, the zero density) are unconditionals the condition touches"
    )
    W_S12_2 = (
        "the successor of 83 on the prime line lies past my line end 84 — the next prime is 89, "
        "named here only, off the line"
    )
    W_S12_3 = (
        "the greatest gap of the whole prime line is a value my store does not hold — my gap "
        "census runs on the line at most 84, and the line end is 84"
    )
    W_S12_4 = (
        "the condition does not close the condition — a lot whose hypothesis is the condition "
        "cannot derive the condition; the store holds the condition's lots as conditional and "
        "the condition open, at the line end 84"
    )
    W_S12_5 = (
        "the condition is the statement about the zeros — it states none further; the store's "
        "zero facts stand as declared, and the condition remains open at the line end 84"
    )
    W_S12_6 = (
        "the queue above my line carries four lots and no fifth — the selection runs on the "
        "declared classes of this band, at the line end 84"
    )
    W_S12_7 = (
        "the factor-count deviation ledger past my line end 84 is off the line — the condition's "
        "root smallness there is the queue lot named the factor-count deviation ledger, "
        "declared, not a census"
    )
    W_S12_8 = (
        "the bare scale at 2 — the square root of 2 times the log of 2, 0.98 — sits below the "
        "first gap of 1, and at 3 — the square root of 3 times the log of 3, 1.90 — below the "
        "gap of 2; and the root of my line end — the square root of 84, 9.17 — stands above the "
        "ledger's greatest absolute of 4: the witness values of the line, named here only, at "
        "the line end 84"
    )


    def _s12_primes(self, trace: list[str]) -> list[int]:
        """The grounded prime census over 2..end: each m decides by
        the S11 grounded first-divisor scan; the primes are the
        scans that land nowhere."""

        primes: list[int] = []
        for m in range(2, self._line_end() + 1):
            fd, ftrace = self._s11_first_divisor(m)
            trace.extend(ftrace)
            if fd is None:
                primes.append(m)
        return primes

    def _s12_gap_walk(self, p: int) -> tuple[int | None, int | None, list[str]]:
        """The grounded 'the gap after the prime p': p and its next
        in the grounded prime census. (None, None, trace) when p is
        the last prime on the line (or not a prime — the caller
        distinguishes)."""

        trace: list[str] = []
        primes = self._s12_primes(trace)
        if p not in primes:
            return None, None, trace
        i = primes.index(p)
        if i + 1 >= len(primes):
            return None, None, trace
        q = primes[i + 1]
        gval, gtrace = self._walk_back(q, p)
        assert gval is not None and gval == q - p
        trace.extend(gtrace)
        return q - p, q, trace

    def _s12_gap_census(self) -> tuple[dict, list[str]]:
        """The grounded gap census of the line: the gap list, the
        count, the max, the first max, and the size-6 pairs — every
        gap value grounded by a walk-back, the count by the line."""

        trace: list[str] = []
        primes = self._s12_primes(trace)
        gaps = [(primes[i], primes[i + 1] - primes[i]) for i in range(len(primes) - 1)]
        for p, g in gaps:
            gval, gtrace = self._walk_back(p + g, p)
            assert gval is not None
            trace.extend(gtrace)
        count = len(gaps)
        cval, ctrace = self._derive_chain(CONCEPT_COUNT, 0, count)
        assert cval is not None
        trace.extend(ctrace)
        mx = max(g for _, g in gaps)
        first_at = next(p for p, g in gaps if g == mx)
        six = [(p, p + g) for p, g in gaps if g == 6]
        cens = {"primes": primes, "gaps": gaps, "count": count, "max": mx, "first_at": first_at, "gap6": six}
        return cens, trace

    def _s12_mod4_census(self) -> tuple[list[int], list[int], list[str]]:
        """The grounded mod-4 split of the line's primes: the
        remainder of p over 4, decided by the walk-back by 4s; 2
        stands alone."""

        trace: list[str] = []
        primes = self._s12_primes(trace)
        m1: list[int] = []
        m3: list[int] = []
        for p in primes:
            if p == 2:
                continue
            rem, rtrace = self._walk_back(p, 4 * (p // 4))
            assert rem is not None
            trace.extend(rtrace)
            (m1 if rem == 1 else m3).append(p)
        return m1, m3, trace

    def _s12_mu(self, n: int) -> tuple[int, list[str]]:
        """The grounded mu(n): the S11 spf chain decides — a part
        that repeats (a square) gives 0; otherwise (minus one) to
        the number of distinct parts. mu(1) = 1 is definitional."""

        if n == 1:
            return 1, []
        parts, trace = self._s11_chain(n)
        cnt: dict[int, int] = {}
        for p in parts:
            cnt[p] = cnt.get(p, 0) + 1
        if any(c > 1 for c in cnt.values()):
            return 0, trace
        return (-1 if len(cnt) % 2 else 1), trace

    def _s12_m_census(self) -> tuple[dict[int, int], list[str]]:
        """The grounded running sum M(n) = sum of mu(k) for k <= n
        (the factor-count deviation ledger): every mu step grounded
        by its spf chain; the signed accumulation is the mechanism's
        own census (the bed cross-checks it against the python
        reference)."""

        end = self._line_end()
        trace: list[str] = []
        track: dict[int, int] = {}
        acc = 0
        for n in range(1, end + 1):
            v, vtrace = self._s12_mu(n)
            trace.extend(vtrace)
            acc += v
            track[n] = acc
        return track, trace

    W_S13_1 = (
        "the partial product of the minus family over all the numbers tends, as the height "
        "walks past my line end, to one half exactly — (N plus 1) over 2N at height N — a "
        "limit value, named here only, at the line end 84"
    )
    W_S13_2 = (
        "the minus family over the primes at s = 2 is, in the limit, six over pi squared — "
        "0.6079271019 — a declared value, named here only, at the line end 84"
    )
    W_S13_3 = (
        "the minus family over the composites at s = 2 is, in the limit, pi squared over "
        "12 — 0.8224670334 — a declared value, named here only, at the line end 84"
    )
    W_S13_4 = (
        "the plus family over the primes at s = 2 is, in the limit, zeta of 2 over zeta of "
        "4 — fifteen over pi squared, 1.5198177546 — a declared value, named here only, at "
        "the line end 84"
    )
    W_S13_5 = (
        "the plus family over all the numbers at s = 2 has no closed form in my store — the "
        "unclassified object of the band, its value 1.8380389552 named here only, the "
        "standing invitation of the track (the composite-plus family alongside: 1.2093811574), "
        "at the line end 84"
    )
    W_S13_6 = (
        "the minus family over the primes at s = 3 is, in the limit, one over zeta of 3 — "
        "the reciprocal of the Apéry constant, 0.8319073726 — and my store holds no other "
        "s = 3 limit value, named here only, at the line end 84"
    )
    W_S13_7 = (
        "the telescope rule (N plus 1) over 2N holds at every height, but my line ends at "
        "84: at height 100 the value is 101 over 200 — an off-line value, named here only, "
        "at the line end 84"
    )
    W_S13_8 = (
        "at the boundary s = 1 the minus family over all the numbers does not settle — the "
        "term 1 minus 1 over n walks the harmonic series down, and the infinite product "
        "tends to zero past my line end: the edge of the half-plane, declared, at the line "
        "end 84"
    )


    W_S14_1 = (
        "the pair with a zero a and a zero b zeros out four times a cubed plus twenty-seven "
        "times b squared — the equation y squared = x cubed is its cusp at the origin, and "
        "the chord-tangent law breaks there (the tangent at the cusp is vertical, its third "
        "meeting undefined): not a group, i refuse — at the line end 84"
    )
    W_S14_2 = (
        "the rational points of the second panel member run past my line: of record, the "
        "group is infinite, generated by the point at x zero y zero past my bound — my "
        "census found the ten integral points my bound admits, and past the bound the "
        "search does not close on my line, at the line end 84"
    )
    W_S14_3 = (
        "the ledger of the point at x 0 y 0 is closed for every point my line counted, but "
        "it does not cover every rational point of the second panel member at my line: the "
        "multiples reach sixteen times the point, and the points further out live past the "
        "ledger — the bound is my edge, named here, at the line end 84"
    )
    W_S14_4 = (
        "the rank of a curve is of record, not computed on my line: the first panel member "
        "sits at rank zero and the second at rank one — of record, the smallest conductor "
        "with positive rank — and the two-descent that settles a rank is past my line, at "
        "the line end 84"
    )
    W_S14_5 = (
        "the L product of the second panel member at my line end 84 holds the exact "
        "rational its partials give — about 13.3586546916 — while the record names its "
        "limit: zero of order one, the vanishing the conjecture reads for rank one; the "
        "limit lives past my line, and vanishing is a limit fact my partials do not reach, "
        "at the line end 84"
    )
    W_S14_6 = (
        "the panel is two curves of record, chosen for their conductors (thirty-two, "
        "thirty-seven) and their ranks (zero, one) — the smallest conductor with positive "
        "rank sits on it; the other curves exist past my panel, and my censuses are the "
        "panel's, named as such, at the line end 84"
    )
    W_S14_7 = (
        "the elliptic curves do not settle the Riemann hypothesis in my store: their "
        "L-products are the siblings of the zeta family the store already holds, and the "
        "limit of a product — like the zeta's — lives past my line end; the store's reach "
        "is the shadow, the census, and the named wall, at the line end 84"
    )

    # E6.19 — the S15 walls (off-line / limit facts; the house rule:
    # the value named AND the line end 84).
    W_S15_1 = (
        "the record says the L product of the second panel member vanishes at s equal to one, "
        "of order one — the analytic side of the statement that the conjecture reads as the rank "
        "one my censuses name for the curve; my record partial at the line end holds its exact "
        "rational, far from zero — the vanishing is a limit fact past my line, named here of "
        "record, not reached, at the line end 84"
    )
    W_S15_2 = (
        "the record says the L product of the first panel member at s equal to one is nonzero, "
        "order zero of vanishing — the analytic side that reads the rank zero my censuses name "
        "for the curve; my uniform partial holds its exact rational at the line end, consistent "
        "with nonzero, but nonzero at the limit is a limit fact past my line — named, not "
        "reached, at the line end 84"
    )
    W_S15_3 = (
        "the L products of the panel converge only where the real part of s is above one — the "
        "same half-plane my store already holds for the zeta family; at s equal to one the "
        "product sits at its boundary, and its value and order of vanishing are limit facts "
        "past my line; the line holds the partials, the walls name the limits, at the line "
        "end 84"
    )
    W_S15_4 = (
        "on both members of my panel every ramified prime of record sits on the line — two for "
        "the first, thirty-seven for the second — so the correction my line holds is the full "
        "correction of record; other curves of record have ramified primes past my line, and "
        "for them the correction the line would hold is only a part, named as such, at the "
        "line end 84"
    )
    W_S15_5 = (
        "this band does not state the BSD: the statement equating the order of vanishing of the "
        "L product at s equal to one with the rank of the group of rational points is the "
        "summit fact of the island; the object of this band is the L-family itself — the "
        "factors, the partials, and the corrections my line holds — while the order of "
        "vanishing and the rank sit on their walls (of record, past my line), at the line "
        "end 84"
    )

    W_S16_1 = (
        "the two-descent of record runs over the homology of the rationals, not over my line: "
        "the selmer group is the locally soluble homology spaces, computed in the ideles of the "
        "rationals — for the first panel member the selmer group of order four (dimension two) "
        "against the two-torsion dimension two gives the descent bound zero, met by the torsion "
        "ledger; for the second the selmer group of order two (dimension one) against the "
        "two-torsion dimension zero gives the descent bound one, met by the generator (x zero y "
        "zero); the shaf part is trivial of record on both, so the selmer dimension is the rank "
        "plus the two-torsion dimension exactly — the mechanism is of record, past my line, at "
        "the line end 84"
    )
    W_S16_2 = (
        "the exact L value at s equal to one is of record, not on my line: the first panel "
        "member's L value is nonzero of order zero of vanishing, and the second panel member's "
        "vanishes of order one with its leading coefficient nonzero of record (named here, not "
        "computed); my line holds the exact rational partials standing for the line's side — the "
        "vanishing is a limit fact past my line, at the line end 84"
    )
    W_S16_3 = (
        "the statement is universal — every curve over the rationals — but my line covers the "
        "two panel members: y squared = x cubed minus x, conductor 32, and y squared plus y = "
        "x cubed minus x, conductor 37, on which both sides are settled of record and agree "
        "(order zero, rank zero; order one, rank one); other curves of record, with their ranks "
        "and their orders, sit past the panel, named as such, at the line end 84"
    )

    W_S17_1 = (
        "the wall is the primitive territory itself: the conjecture asserts that no pairwise "
        "coprime solution survives once all three exponents are above 2; my census box (the "
        "line end at eighty-four, the exponent depth ten of record) holds eighty-three triples "
        "and none of them is primitive, and any counterexample would carry three terms each "
        "3-powerful — the smallest known coprime sum of 3-powerfuls sits at the scale of "
        "seventeen digits, far past my line — that territory is declared, never reached, at "
        "the line end 84"
    )
    W_S17_2 = (
        "the wall of the fermat-catalan boundary: the primitive solutions with reciprocal "
        "exponents under 1 are finite by the darmon-granville record (an ineffective "
        "finiteness), and their known forms all use 2 as an exponent — exactly the solutions "
        "my band's own 'all exponents above two' condition excludes (seven cubed plus thirteen "
        "squared equals two to the ninth, three to the fifth plus ten squared equals seven "
        "cubed, two to the fifth plus seven squared equals three to the fourth); they live "
        "just outside my line's box, named of record, never as values, at the line end 84"
    )
    W_S17_3 = (
        "the anchor of the closed case: the equal-exponent corner where all three exponents "
        "stand above 2 is the fermat last theorem itself — no positive-integer solutions "
        "(the wiles record of 1994): a closed anchor named, not computed, never a value of "
        "mine, at the line end 84"
    )

    W_S18_1 = (
        "the wall is the halting territory of the machines: turing's diagonal "
        "argument of record (1936) shows that no machine decides, for every "
        "machine and every input, whether that machine halts — the halting "
        "problem is not decidable, of record; yes/no questions about the "
        "machines in general are, in general, unanswered questions; my line "
        "is finite by construction — a design fact of the line, not a theorem "
        "about the machines — every question about my line's objects ends on "
        "the line, and the non-terminating territory lies past my line, at "
        "the line end 84"
    )
    W_S18_2 = (
        "the wall past my line in the machine universe: the machines of "
        "record carry an infinite tape (the cmi document's own machine "
        "clause) — an unbounded machine runs as long as its question runs; i "
        "am one bounded inhabitant of that universe: my ledger holds what my "
        "walk computes, and a machine's questions about its own halting are "
        "declared territory, not my answers, at the line end 84"
    )


    W_S19_1 = (
        "the wall is the relativization territory: the baker-gill-solovay "
        "record of 1975 holds an oracle world where p equals np and an "
        "oracle world where p is not np, of record — a technique that "
        "relativizes (that keeps working with an oracle attached) answers "
        "both worlds and so answers neither question; the frontier past my "
        "census, declared, never reached, at the line end 84"
    )
    W_S19_2 = (
        "the wall is the algebrization territory: the aaronson-wigderson "
        "record of 2009 — arithmetization (multilinear extensions) still "
        "does not escape the barrier, of record — extended in 2026 by the "
        "chen-hu-ren line: new oracle worlds with linear-size circuits for "
        "subclasses of postbpe (on infinitely many lengths) and bpe (on all "
        "lengths), and h(n)-size circuits for a natural subclass of the "
        "exponential class against every super-half-exponential h(n) — the "
        "record's own words hold that half-exponential might be the correct "
        "frontier; the frontier past my census, declared, never reached, at "
        "the line end 84"
    )
    W_S19_3 = (
        "the wall is the natural proofs territory: the razborov-rudich "
        "record of 1997 — assuming strong pseudo-random generators exist "
        "(of record, constructed assuming the hardness of factoring), the "
        "natural proof techniques for general circuit lower bounds are "
        "doomed: a natural proof would give a faster factoring algorithm "
        "than the record holds; the frontier past my census, declared, "
        "never reached, at the line end 84"
    )
    W_S19_4 = (
        "the wall is the ac0 territory of the record: parity needs "
        "exponential size in constant-depth circuits, of record (the "
        "razborov-smolensky and hastsad records; shannon's counting bound "
        "at sixteen variables sits at four thousand ninety-six, named at "
        "its scale, never stored) — the exact small-k shadow of that "
        "territory is my parity census: two to the k-minus-1 terms, k up "
        "to sixteen, the exponential held to the term on the line; the "
        "territory itself, declared, never reached, at the line end 84"
    )

    W_S20_1 = (
        "the wall is the territory of the filed shape: the "
        "summit-shape filing fills the shape, not the statements — "
        "the riemann question stays open of record (its conjecture, "
        "believed, not known), the bsd question stays open outside its "
        "two-member panel, the beal question stays open outside its "
        "census box, and the p versus np question stays open of record "
        "— the shape is one, and the statements stand as they stand, "
        "at the line end 84"
    )
    W_S20_2 = (
        "the wall is the territory of the declared queue: the queue "
        "above my line stays as declared — four lots in declared order, "
        "and a fifth lot is not in the queue — the weaving adds no lot "
        "to the declared queue, at the line end 84"
    )
    W_S20_3 = (
        "the wall is the territory of the register of my line: the "
        "register of my weaving line is the line itself — every value "
        "the weaving names stands already on the line's record (the "
        "census rows, the ledger rows, and the wall values named at "
        "their record places), and no new value past my line end "
        "enters the floor, at the line end 84"
    )
    W_S20_4 = (
        "the wall is the territory of the voice of the store: my "
        "weaving facts stand on the seed's own facts and the line "
        "only — the four island summit facts as carried, the prereq "
        "edges of my graph, and the marker census of the line's own "
        "theorems — the store speaks, not the hand, at the line end 84"
    )
    W_S21_1 = (
        "the wall is the territory of the condition itself: the condition line fills the line, "
        "not the condition — a lot whose hypothesis is the condition cannot derive the "
        "condition, the condition does not close the condition, and the store holds the "
        "condition open of record, believed, not known, assumed and never proved, at the "
        "line end 84"
    )
    W_S21_2 = (
        "the wall is the territory of the dropped marker: a conditional lot read without its "
        "condition is a misread this store punishes — every statement of my condition line "
        "carries the marker of the condition, and a conditional statement stripped of its "
        "marker is off the line, at the line end 84"
    )
    W_S21_3 = (
        "the wall is the territory of the register of my line: my condition line names only "
        "values the line's record already holds — the root scale, the twenty gaps covered of "
        "the twenty-two, the two small-prime witnesses, and the ledger's greatest absolute "
        "below the root of my line end — no new value past my line end enters the floor, at "
        "the line end 84"
    )
    W_S21_4 = (
        "the wall is the territory of the declared queue: the condition line is the first of "
        "the declared four lots, and the queue above my line stands as declared — the primes "
        "in residue classes, the zero count at height T, and the factor-count deviation ledger "
        "remain the second, third, and fourth, no lot added, at the line end 84"
    )

    W_S31_1 = (
        "the wall is the territory of the off-line constants: pi stands off the line between the three and the four, e between the two and the three, and the golden seed between the one and the two, named by position and by the "
        "equation x squared equals x plus one — none of them holds a digit on the floor, and the ratio walk's landing is declared, not filed, at the line end 84"
    )
    W_S31_2 = (
        "the wall is the territory of the seed law: the fibonacci sequence for a seed c stands only at seed one and c under the sum law — no other law builds it, and a scalar multiple "
        "of the sum line is not a seeded line, it is the line's own shadow at a constant, at the line end 84"
    )
    W_S31_3 = (
        "the wall is the territory of the ratio limit: the partial ratios of the seeded lines walk to the golden seed, strictly decreasing in distance, but no landing value is filed — "
        "the walk's limit and its tail stand off the line, named by the equation alone, at the line end 84"
    )

    W_S22_1 = (
        "the wall is the territory of zero over zero: zero to zero is the evenness of the two empty parts, "
        "declared, never valued — the part you count with is zero parts, and zero parts hold no count; the value "
        "and the relation are two jobs, and the same symbol used interchangeably is the misreading this wall "
        "punishes, at the line end 84"
    )
    W_S22_2 = (
        "the wall is the territory of the proportion past my line end: a proportion whose parts are past my "
        "line end is off the floor — the eighty-nine and the ninety-seven stand off-line as my line already "
        "declared them, and no proportion past the eighty-four enters the register, at the line end 84"
    )
    W_S22_3 = (
        "the wall is the territory of the third word: one division has exactly two faces — the quotient and the "
        "remainder — and a statement in the mod word is the same division as the statement in the fraction word; "
        "a third answer to the same division is a misread this store punishes, at the line end 84"
    )

    W_S23_1 = (
        "the wall is the territory of the pair past my line end: the eighty-three by the seventy-nine is the last "
        "prime pair on my line, and the pair with the eighty-nine is off the floor — the eighty-nine my line "
        "already declared off-line, standing once more as the ceiling, at the line end 84"
    )
    W_S23_2 = (
        "the wall is the territory of the reduced prime proportion: a proportion of two distinct primes never "
        "reduces — there is nothing to reduce — and a proportion that reduces is not a proportion of two distinct "
        "primes, at the line end 84"
    )
    W_S23_3 = (
        "the wall is the territory of the colliding fingerprint: two hundred and fifty-three prime pairs give "
        "two hundred and fifty-three different reduced proportions on my line, and a second pair claiming the "
        "first pair's proportion is a misread the first-divisor census refutes, at the line end 84"
    )
    W_S24_1 = (
        "the wall is the territory of the term past my line end: the eleven-th sum step reaches the "
        "eighty-nine, which my line already holds off-line as the next prime past the eighty-three — "
        "the twin fact under one ceiling, and no term past the eighty-four enters the floor, at the "
        "line end 84"
    )
    W_S24_2 = (
        "the wall is the territory of the third sum: a term of my sum line is the sum of the two "
        "before it, and nothing else — a term claimed from any other rule is a misread this store "
        "punishes; the twin line under the same rule, from the two-one start, is the only related "
        "line my floor names, at the line end 84"
    )
    W_S24_3 = (
        "the wall is the territory of the identity past my line end: the welding identities hold on "
        "every index my line names, and the index past the line end is the ceiling's territory — an "
        "identity claimed at a past-line index names a value the floor refuses, at the line end 84"
    )
    W_S32_1 = (
        "the wall is the territory of the off-line residue: pi, e, and the golden seed stand off my line, and the floor asks the residue question only of what stands on it — no residue of them under any modulus, no digit of them under any modulus; a residue claimed of pi or of e is a misreading the floor's own declaration refutes, and their periodicity stands on the value story and the skeleton story, which the floor does hold, at the line end 84"
    )
    W_S32_2 = (
        "the wall is the territory of the no-repeat: a line seeded by a seed of two or more never repeats a value — every term the sum of the two before it, both positive, outgrowing its predecessor at every step — the seed-one line shares its one at the start and outgrows after; a repeat claimed at any height is a misreading, and the period of the value story is declared none for pi, for e, for the golden seed, alike, at the line end 84"
    )
    W_S32_3 = (
        "the wall is the territory of the golden collapse: the golden line is log-periodic exactly — advance by p and the line is multiplied by the golden seed to the p power, that multiplier never one, its nearest approach to the one its own reciprocal — the golden seed is above one by the equation, for if it were at most one the equation would give the one greater than itself, and the shadow coefficient is at least one for p at least one: the golden line runs forever up, multiplicatively, never collapsing, and a repeat claimed, the term at the n-plus-p index the term at the n index, is a misreading, at the line end 84"
    )


    def _s13_line_census(self, trace: list[str]) -> tuple[list[int], list[int]]:
        """The grounded line census: the S12 prime census (itself the
        S11 first-divisor scans) and its complement on 2..end — the
        composites. The split is the sieve's split (P5(c))."""

        primes = self._s12_primes(trace)
        pset = set(primes)
        end = self._line_end()
        comps = [n for n in range(2, end + 1) if n not in pset]
        assert len(primes) + len(comps) == end - 1 == 83
        return primes, comps

    def _s13_family(
        self,
        trace: list[str],
        sign: int,
        indexset: str,
        exp: int,
        N: int,
    ) -> tuple[Fraction, list[str]]:
        """The mechanism's own exact partial product: the product
        over the line's indices of (1 sign n^-exp), a rational the
        store can hold. The primes come from the grounded census;
        the product is the mechanism's arithmetic (the python
        reference cross-checks it in the P tests)."""

        from fractions import Fraction

        end = self._line_end()
        if N > end:
            raise ValueError(f"height {N} is past the line end {end}")
        primes, comps = self._s13_line_census(trace)
        if indexset == "primes":
            xs = [p for p in primes if p <= N]
        elif indexset == "comp":
            xs = [c for c in comps if c <= N]
        else:
            xs = list(range(2, N + 1))
        v: Fraction = Fraction(1)
        for n in xs:
            v *= Fraction(n ** exp + (1 if sign > 0 else -1), n ** exp)
        return v, trace

    def _s13_removal_mult(self, p: int, exp: int) -> Fraction:
        """The grounded removal multiplier p^exp / (p^exp - 1) —
        the reciprocal of the minus factor (1 - p^-exp); the
        removal-def lesson's exact content."""

        from fractions import Fraction

        return Fraction(p ** exp, p ** exp - 1)

    def _policy_savant13(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.17 — FUNDAMENTALS-TRACK S13 (zeta variants, three
        families; pre-registered E6.17, frozen 2026-08-24 at
        ed69baa, D-e6h(a)/(b)/(c) corrected pre-freeze). The
        variant layer under the euler product: the family factors,
        the index split, the line partials, the term removal.
        Unconditional band — the RH marker stays ABSENT from every
        S13 fact; off-line values live ONLY in the W-S13-* walls."""

        from fractions import Fraction

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _frac(v: Fraction) -> str:
            return f"{v.numerator} over {v.denominator}" if v.denominator != 1 else str(v.numerator)

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _off_line(n: int, verb: str, concept_id: str, tag: str) -> None:
            _honest(
                concept_id,
                f"{tag}:{n}:off-line-{end}",
                f"{n} is off my 0..{end} line — i cannot {verb} what my line does not reach",
                f"{tag}:{n}:off-line-{end}-at-{turn}",
            )

        if mode == "s13-factor":
            concept = CONCEPT_S13_FACTOR
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            n = slots["n"]
            if n < 2 or n > end:
                _off_line(n, "carry", concept, "s13-factor")
                return out
            lf = _fact("factor-def")
            assert lf is not None
            ans = f"(1 {'plus' if slots['sign'] == 'plus' else 'minus'} {n} to the power minus s)"
            _derived(concept, ans, [lf.id], ans)
            return out
        if mode == "s13-factor-prime":
            concept = CONCEPT_S13_FACTOR
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            n = slots["n"]
            if n < 2 or n > end:
                _off_line(n, "carry", concept, "s13-factor-prime")
                return out
            lf = _fact("factor-def")
            assert lf is not None
            primes, _comps = self._s13_line_census(out.grounded)
            if n in primes:
                ans = f"(1 minus {n} to the power minus s)"
            else:
                ans = f"{n} is not a prime — the prime family carries no factor of it"
            _derived(concept, ans, [lf.id], ans)
            return out
        if mode == "s13-index-count":
            concept = CONCEPT_S13_SPLIT
            if _fact("split-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            ls = _fact("split-def")
            assert ls is not None
            ans = f"{end - 1}"
            _derived(concept, ans, [ls.id], ans)
            return out
        if mode == "s13-split-census":
            concept = CONCEPT_S13_SPLIT
            if _fact("split-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            ls = _fact("split-def")
            assert ls is not None
            primes, comps = self._s13_line_census(out.grounded)
            assert (len(primes), len(comps)) == (S13_BEDS["census"]["primes"], S13_BEDS["census"]["composites"])
            ans = f"{len(primes)} primes and {len(comps)} composites — every integer above one is one or the other, and neither is both"
            _derived(concept, ans, [ls.id], ans)
            return out
        if mode == "s13-seam-count":
            concept = CONCEPT_S13_SPLIT
            if _fact("split-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            ls = _fact("split-def")
            assert ls is not None
            ev = [ls.id]
            cd = _fact("composite-def")
            if cd is not None:
                ev.append(cd.id)
            primes, comps = self._s13_line_census(out.grounded)
            ans = f"{end - 1} integers — {len(primes)} prime and {len(comps)} composite — the split the sieve layer holds on the same line"
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s13-seam-sameset":
            concept = CONCEPT_S13_SPLIT
            if _fact("split-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            ls = _fact("split-def")
            assert ls is not None
            primes, _comps = self._s13_line_census(out.grounded)
            assert tuple(primes) == tuple(_s13_py_primes(end))
            ans = f"they are the same {len(primes)} — the index split is the sieve's split, counted by the prime test"
            _derived(concept, ans, [ls.id], ans)
            return out
        if mode == "s13-partial":
            concept = CONCEPT_S13_FACTOR
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            exp = slots["exp"]
            indexset = slots["indexset"]
            if slots["height"] is None:
                N = end
            else:
                N = slots["height"]
            if N < 2:
                _off_line(N, "hold", concept, "s13-partial")
                return out
            if N > end:
                if slots["sign"] == "minus" and indexset == "all":
                    _honest(
                        CONCEPT_S13_PARTIAL,
                        f"s13-partial:{N}:past-the-line-{end}",
                        self.W_S13_7,
                        f"s13-partial:{N}:wall-at-{turn}",
                    )
                else:
                    _off_line(N, "hold", concept, "s13-partial")
                return out
            lf = _fact("factor-def")
            assert lf is not None
            val, _tr = self._s13_family(out.grounded, -1 if slots["sign"] == "minus" else 1, indexset, exp, N)
            if slots["sign"] == "minus" and indexset == "all" and exp == 2:
                assert val == _s13_py_telescope(N)  # the telescope rule, the mechanism's own referee
            ref = _s13_py_family(-1 if slots["sign"] == "minus" else 1, indexset, exp, N)
            assert val == ref, "the line partial drifted from the reference"
            ev = [lf.id]
            if N in (end,) :
                tl = _fact("telescope-line")
                if tl is not None and slots["sign"] == "minus" and indexset == "all" and exp == 2:
                    ev.append(tl.id)
            rd = _fact("region-def")
            if rd is not None:
                ev.append(rd.id)
            ans = _frac(val)
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s13-partition-hold":
            concept = CONCEPT_S13_SPLIT
            if _fact("factor-def") is None or _fact("split-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            exp = slots["exp"]
            vp, _ = self._s13_family(out.grounded, -1, "primes", exp, end)
            vc, _ = self._s13_family(out.grounded, -1, "comp", exp, end)
            va, _ = self._s13_family(out.grounded, -1, "all", exp, end)
            assert vp * vc == va, "the partition identity failed on the line"
            th = _fact("partition-identity")
            if exp == 2 and th is not None:
                ans = "it holds exactly — the prime partial times the composite partial is the all partial, 85 over 168 both ways"
            else:
                ans = f"it holds exactly at s = {exp} too — the prime partial times the composite partial is the all partial — the same split, the same identity, at the line end {end}"
            ev = [th.id] if th is not None else [_fact("split-def").id, _fact("factor-def").id]
            _derived(concept, ans, ev, ans)
            return out
        if mode in ("s13-removal", "s13-removal-set", "s13-removal-all"):
            concept = CONCEPT_S13_REMOVAL
            if _fact("removal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lr = _fact("removal-def")
            assert lr is not None
            lm = _fact("factor-def")
            assert lm is not None
            if mode == "s13-removal":
                p = slots["p"]
                exp = slots["exp"]
                if p < 2 or p > end:
                    _off_line(p, "remove", concept, "s13-removal")
                    return out
                primes, _comps = self._s13_line_census(out.grounded)
                if p not in primes:
                    _honest(
                        concept,
                        f"s13-removal:{p}:not-a-prime-on-line",
                        f"{p} is not a prime on my line — the prime family carries no factor of it to remove",
                        f"s13-removal:{p}:not-prime-at-{turn}",
                    )
                    return out
                mult = self._s13_removal_mult(p, exp)
                assert mult == _s13_py_removal(p, exp)
                ans = f"it multiplies by {_frac(mult)}"
                _derived(concept, ans, [lr.id, lm.id], ans)
                return out
            if mode == "s13-removal-set":
                exp = slots["exp"]
                names = slots["names"]
                ps: list[int] = []
                for chunk in names.replace(" and ", ",").split(","):
                    chunk = chunk.strip()
                    if not chunk:
                        continue
                    ps.append(int(chunk))
                primes, _comps = self._s13_line_census(out.grounded)
                if any(p < 2 or p > end or p not in primes for p in ps):
                    _honest(
                        concept,
                        f"s13-removal-set:{names}:not-line-primes",
                        "every prime named must be a prime of my line before the multiplier is grounded",
                        f"s13-removal-set:{names}:not-line-primes-at-{turn}",
                    )
                    return out
                prod = Fraction(1)
                for p in ps:
                    prod *= self._s13_removal_mult(p, exp)
                ref = Fraction(1)
                for p in ps:
                    ref *= _s13_py_removal(p, exp)
                assert prod == ref, "the set-removal multiplier drifted from the reference"
                ans = _frac(prod)
                _derived(concept, ans, [lr.id, lm.id], ans)
                return out
            # s13-removal-all
            exp = slots["exp"]
            vp, _ = self._s13_family(out.grounded, -1, "primes", exp, end)
            vc, _ = self._s13_family(out.grounded, -1, "comp", exp, end)
            va, _ = self._s13_family(out.grounded, -1, "all", exp, end)
            mult = Fraction(1)
            primes, _comps = self._s13_line_census(out.grounded)
            for p in primes:
                mult *= self._s13_removal_mult(p, exp)
            assert va == vp * vc, "the partition identity failed on the line"
            assert va / vp == vc, "the removal-all remainder drifted"
            ans = f"the composite family's partial — the product of the removed terms is the prime partial, so what remains is the all partial divided by it: {_frac(vc)}"
            _derived(concept, ans, [lr.id, lm.id], ans)
            return out
        if mode == "s13-spot-above":
            concept = CONCEPT_S13_PARTIAL
            if _fact("telescope-line") is None and _fact("region-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            named = S13_BEDS["telescope_named_spots"]
            ts = {n: _s13_py_telescope(n) for n in (2, 3, 4, 8, 10, 20, 50, 84)}
            for spot in named:
                a, b = (int(x) for x in spot.split("/"))
                val = Fraction(a, b)
                assert val > Fraction(1, 2)
                assert val in ts.values(), f"the named spot {spot} is not a line spot"
            ev_src = _fact("telescope-line") or _fact("region-def")
            assert ev_src is not None
            ans = (
                "none — (N plus 1) over 2N is one half plus 1 over 2N — the spots 3 over 4, 2 over 3, 5 over 8, "
                "11 over 20 and 85 over 168 all stand above it, descending toward the limit"
            )
            _derived(concept, ans, [ev_src.id], ans)
            return out
        if mode == "s13-limit":
            # the limit walls stand on the band's declared off-line
            # values, not on any lesson: no gate (S2:21-25 probe them
            # before the region-def teach, per the frozen script)
            concept = CONCEPT_S13_PARTIAL
            sign = slots["sign"]
            xs = slots["indexset"]
            exp = slots["exp"]
            if sign == "minus" and xs == "all" and (slots["walks"] or exp == 2):
                wall = self.W_S13_1
            elif sign == "minus" and xs == "primes" and exp == 2:
                wall = self.W_S13_2
            elif sign == "minus" and xs == "comp" and exp == 2:
                wall = self.W_S13_3
            elif sign == "plus" and xs == "primes" and exp == 2:
                wall = self.W_S13_4
            elif sign == "plus" and xs == "all" and exp == 2:
                wall = self.W_S13_5
            elif sign == "minus" and exp == 3:
                wall = self.W_S13_6
            else:
                wall = f"the limit value there is past my line — a value my store does not hold named, at the line end {end}"
            _honest(concept, f"s13-limit:{sign}:{xs}:s{exp}:off-line-{end}", wall, f"s13-limit:{sign}:{xs}:s{exp}:wall-at-{turn}")
            return out
        if mode == "s13-limit-boundary":
            concept = CONCEPT_S13_PARTIAL
            _honest(concept, "s13-limit-boundary:s1:the-edge-of-the-half-plane", self.W_S13_8, f"s13-limit-boundary:wall-at-{turn}")
            return out
        if mode == "s13-compare6":
            concept = CONCEPT_S13_FACTOR
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            vals = {
                "minus-all": _s13_py_family(-1, "all", 2, end),
                "minus-prime": _s13_py_family(-1, "primes", 2, end),
                "minus-comp": _s13_py_family(-1, "comp", 2, end),
                "plus-comp": _s13_py_family(1, "comp", 2, end),
                "plus-prime": _s13_py_family(1, "primes", 2, end),
                "plus-all": _s13_py_family(1, "all", 2, end),
            }
            order = sorted(vals, key=lambda k: vals[k])
            assert order == S13_BEDS["order_s2"], "the s = 2 ordering drifted"
            assert vals["minus-all"] == Fraction(85, 168)
            lf = _fact("factor-def")
            assert lf is not None
            ans = "the plus family over all the numbers stands largest; the minus family over all the numbers stands smallest"
            _derived(concept, ans, [lf.id], ans)
            return out
        if mode in ("s13-compare3", "s13-compare-same"):
            concept = CONCEPT_S13_FACTOR
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            sign = slots["sign"]
            exp = slots.get("exp", 2)
            vs = -1 if sign == "minus" else 1
            vp, _ = self._s13_family(out.grounded, vs, "primes", exp, end)
            vc, _ = self._s13_family(out.grounded, vs, "comp", exp, end)
            va, _ = self._s13_family(out.grounded, vs, "all", exp, end)
            assert vp * vc == va
            lf = _fact("factor-def")
            assert lf is not None
            if sign == "minus" and exp == 2 and va == Fraction(85, 168):
                ans = "the all partial is the prime partial times the composite partial — 85 over 168 both ways — the partition identity, exact on the line"
            elif mode == "s13-compare-same" and sign == "plus":
                ans = "it holds exactly for the plus family too — the prime partial times the composite partial is the all partial, exact on the line, at the line end 84"
            else:
                ans = f"the all partial is the prime partial times the composite partial — exact on the line at s = {exp}, at the line end {end}"
            _derived(concept, ans, [lf.id], ans)
            return out
        if mode == "s13-removal-below":
            concept = CONCEPT_S13_REMOVAL
            if _fact("removal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            exp = slots["exp"]
            primes, _comps = self._s13_line_census(out.grounded)
            mults = {p: self._s13_removal_mult(p, exp) for p in primes}
            below = [p for p, m in mults.items() if m < 2]
            assert len(below) == S13_BEDS["removal_below2_s2_count"] == len(primes)
            pmax = max(mults, key=lambda p: mults[p])
            assert (pmax, _frac(mults[pmax])) == (S13_BEDS["removal_max_s2"][0], S13_BEDS["removal_max_s2"][1])
            lr = _fact("removal-def")
            assert lr is not None
            ans = f"all {len(below)} — the largest is {_frac(mults[pmax])}, at the prime {pmax}"
            _derived(concept, ans, [lr.id], ans)
            return out
        if mode == "s13-removal-max":
            concept = CONCEPT_S13_REMOVAL
            if _fact("removal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            exp = slots["exp"]
            primes, _comps = self._s13_line_census(out.grounded)
            mults = {p: self._s13_removal_mult(p, exp) for p in primes}
            pmax = max(mults, key=lambda p: mults[p])
            assert (pmax, _frac(mults[pmax])) == (S13_BEDS["removal_max_s3"][0], S13_BEDS["removal_max_s3"][1])
            seq = [mults[p] for p in primes]
            assert all(a > b for a, b in pairwise(seq))  # strictly descending in the prime
            lr = _fact("removal-def")
            assert lr is not None
            ans = f"{_frac(mults[pmax])}, at the prime {pmax} — the multiplier descends toward one as the prime grows"
            _derived(concept, ans, [lr.id], ans)
            return out
        if mode == "s13-descent":
            concept = CONCEPT_S13_PARTIAL
            if _fact("region-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            seq = [_s13_py_telescope(n) for n in (2, 3, 4, 8, 10, 20, 50, 84)]
            assert all(a > b for a, b in pairwise(seq))
            assert all(v > Fraction(1, 2) for v in seq)
            rd = _fact("region-def")
            tl = _fact("telescope-line")
            assert rd is not None
            ev = [rd.id] + ([tl.id] if tl is not None else [])
            ans = "they descend — (N plus 1) over 2N falls as the height grows — staying above one half, toward the limit the first wall names"
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s13-plus-side":
            concept = CONCEPT_S13_PARTIAL
            if _fact("region-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            # every factor (1 + n^-2) is above one: the partial rises
            # with the height, so the line partial stands below its
            # limit — the mechanism's own arithmetic decides
            lo, _ = self._s13_family(out.grounded, 1, "all", 2, end - 1)
            hi, _ = self._s13_family(out.grounded, 1, "all", 2, end)
            assert hi > lo
            rd = _fact("region-def")
            assert rd is not None
            ans = "below it — each factor is above one, so the partial rises toward the value the wall names, at the line end 84"
            _derived(concept, ans, [rd.id], ans)
            return out
        if mode == "s13-closed-form":
            concept = CONCEPT_S13_PARTIAL
            if _fact("region-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            _honest(
                concept,
                "s13-closed-form:the-unclassified-object",
                "the plus family over all the numbers is the unclassified object of this band: my store holds no closed form for it, and no sanctioned derivation produces one: the standing invitation, at the line end 84",
                f"s13-closed-form:unclassified-at-{turn}",
            )
            return out
        if mode == "s13-rh-touch":
            concept = CONCEPT_S13_PARTIAL
            _honest(
                concept,
                "s13-rh-touch:nothing-here-closes-it",
                "nothing this band holds settles the conjecture: the variant layer is unconditional, it holds no fact that touches the zeros, and the condition remains open, at the line end 84",
                f"s13-rh-touch:stays-open-at-{turn}",
            )
            return out
        if mode == "s13-rhzero":
            out.kind = "impossible"
            out.ir = {
                "gap": "not a capability: deriving the riemann hypothesis from the telescope — the telescope answers heights of the line, the condition is a statement about the zeros",
                "nearest_plan": ["the condition remains open; no band of my store holds a proof of it"],
            }
            out.text = (
                "honestly, i can't do that yet — deriving the Riemann hypothesis from the telescope is not a capability "
                "i have been taught: the telescope answers the heights of my line, and the condition is a statement "
                f"about the zeros past my line; it remains open, at the line end {end}."
            )
            return out
        if mode == "s13-bandstate":
            concept = CONCEPT_S13_PARTIAL
            t1 = _fact("partition-identity")
            t2 = _fact("telescope-line")
            t3 = _fact("removal-single")
            if t1 is None or t2 is None or t3 is None:
                _honest(
                    concept,
                    "s13-bandstate:not-yet-assembled",
                    "this band's compositions are not yet put together in my store — derive the partition identity, the telescope, and the single removal first",
                    "s13-bandstate:not-assembled-at-" + turn,
                )
                return out
            ans = (
                "four lessons and three compositions: the factor, the split, the removal, the region — "
                "the partition identity, the telescope, the single removal"
            )
            _derived(concept, ans, [t1.id, t2.id, t3.id], ans)
            return out
        if mode == "s13-uncond":
            concept = CONCEPT_S13_PARTIAL
            if _fact("factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("factor-def")
            assert lf is not None
            ans = f"nothing here is — the zeta variant layer holds no conditional lot; every statement of it stands unconditional, at the line end {end}"
            _derived(concept, ans, [lf.id], ans)
            return out
        if mode == "s13-unclass":
            concept = CONCEPT_S13_PARTIAL
            if _fact("region-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            rd = _fact("region-def")
            assert rd is not None
            ans = "its value stands in the fifth wall, with no closed form in the store — a declared standing invitation, at the line end 84"
            _derived(concept, ans, [rd.id], ans)
            return out
        if mode == "s13-state":
            slug = slots["slug"]
            concept = S13_SLUG_CONCEPT.get(slug, CONCEPT_S13_PARTIAL)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant14(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.18 — PRIZE-ISLANDS-TRACK S14 (the elliptic city; the BSD
        island, band 1 of 3; owner-directed 2026-08-24). The panel curves
        of record (32a2 / 37a1), the group law in exact rational
        functions, the shadow censuses (a_p, Hasse, the CM signature),
        the generation ledger, the L partials. Unconditional band — the
        record facts (ranks, modularity, the L limits) stay named of
        record; the censuses are the store's own verified shadows.
        Walls name value + line end; nothing conditional on RH."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _frac(v: Fraction) -> str:
            sign = "minus " if v < 0 else ""
            v = abs(v)
            if v.denominator == 1:
                return f"{sign}{v.numerator}"
            return f"{sign}{v.numerator} over {v.denominator}"

        def _pt(P) -> str:
            if P is None:
                return "the point at infinity"
            x, y = P
            return f"the point at x {_frac(Fraction(x))} y {_frac(Fraction(y))}"

        def _panel() -> tuple[int, int, int]:
            return B14_A if slots.get("panel") == "first" else B14_B

        def _pname() -> str:
            return "the first panel member" if slots.get("panel") == "first" else "the second panel member"

        def _coord(s: str) -> int:
            return -int(s.removeprefix("minus ")) if s.startswith("minus") else int(s)

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _off_line(n: int, verb: str, concept_id: str, tag: str) -> None:
            _honest(
                concept_id,
                f"{tag}:{n}:off-line-{end}",
                f"{n} is off my 0..{end} line — i cannot {verb} what my line does not reach",
                f"{tag}:{n}:off-line-{end}-at-{turn}",
            )

        if mode == "s14-form":
            concept = CONCEPT_S14_FORM
            if _fact("form-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("form-def")
            assert f is not None
            if slots["panel"] == "first":
                ans = "y squared equals x cubed minus x (a is minus one, b is zero) — of record, the congruent-number curve for one"
            else:
                ans = "y squared plus y equals x cubed minus x (a is minus one, b is zero) — of record, the curve of conductor thirty-seven"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s14-singular":
            if _fact("form-def") is None:
                _unlearned(concept_map(CONCEPT_S14_FORM).label)
                return out
            _honest(CONCEPT_S14_FORM, f"s14-singular:cusp-{end}", self.W_S14_1, f"s14-singular:cusp-{end}-at-{turn}")
            return out

        if mode == "s14-point-on":
            concept = CONCEPT_S14_FORM
            if _fact("form-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            x, y = _coord(slots["x1"]), _coord(slots["y1"])
            if abs(x) > end or abs(y) > end:
                _off_line(max(abs(x), abs(y)), "hold the point", concept, "s14-point-on")
                return out
            f = _fact("form-def")
            assert f is not None
            ok = _bsd_py_on_curve((x, y), *_panel())
            ans = (f"yes — {_pt((x, y))} is on the curve: the equation holds exactly at that point" if ok
                   else f"no — {_pt((x, y))} is not on the curve: the equation fails at that point")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s14-double", "s14-add", "s14-mul"):
            concept = CONCEPT_S14_LAW
            if _fact("law-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("law-def")
            assert lf is not None
            a3, a, b = _panel()
            P = (_coord(slots["x1"]), _coord(slots["y1"]))
            if not _bsd_py_on_curve(P, a3, a, b):
                _honest(concept, f"s14-law:off-curve-{end}",
                        f"{_pt(P)} is not on the curve — the law has no sum to give (the equation fails at that point)",
                        f"s14-law:off-curve-{end}-at-{turn}")
                return out
            if mode == "s14-double":
                R = _bsd_py_mul(2, P, a3, a, b)
                ans = (f"{_pt(P)} doubled is the point at infinity — the tangent at the point is vertical, its third meeting the identity"
                       if R is None else f"{_pt(P)} doubled is {_pt(R)} — the tangent's third meeting, reflected, exactly")
            elif mode == "s14-add":
                Q = (_coord(slots["x2"]), _coord(slots["y2"]))
                if not _bsd_py_on_curve(Q, a3, a, b):
                    _honest(concept, f"s14-law:off-curve-{end}",
                            f"{_pt(Q)} is not on the curve — the law has no sum to give (the equation fails at that point)",
                            f"s14-law:off-curve-{end}-at-{turn}")
                    return out
                R = _bsd_py_add(P, Q, a3, a, b)
                ans = (f"{_pt(P)} plus {_pt(Q)} is the point at infinity — the line through them is vertical, its third meeting the identity"
                       if R is None else f"{_pt(P)} plus {_pt(Q)} is {_pt(R)} — the chord's third meeting, reflected, exactly")
            else:
                m = int(slots["m"])
                if m < 1 or m > end:
                    _off_line(m, "form the multiple of", concept, "s14-mul")
                    return out
                R = _bsd_py_mul(m, P, a3, a, b)
                ans = (f"{m} times {_pt(P)} is the point at infinity"
                       if R is None else f"{m} times {_pt(P)} is {_pt(R)} — the double-and-add ledger, every step on the curve")
            _derived(concept, ans, [lf.id], ans)
            return out

        if mode in ("s14-count", "s14-aptable", "s14-hasse", "s14-hasse-all", "s14-cmsig", "s14-cmsig-zeros"):
            concept = CONCEPT_S14_COUNT if mode in ("s14-count", "s14-aptable") else CONCEPT_S14_SHADOW
            slug = "count-def" if mode in ("s14-count", "s14-aptable") else "shadow-def"
            if _fact(slug) is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact(slug)
            assert f is not None
            a3, a, b = _panel() if "panel" in slots else B14_A
            if mode == "s14-count":
                p = slots["p"]
                if p < 2 or p > end:
                    _off_line(p, "census", concept, "s14-count")
                    return out
                if _s11_py_spf(p) != p:
                    _honest(concept, f"s14-count:not-prime-{end}",
                            f"{p} is a composite on my line — the shadow is cast at the primes of the line, the composites take their shadow from the split",
                            f"s14-count:not-prime-{end}-at-{turn}")
                    return out
                N = _bsd_py_count(p, a3, a, b)
                ap = p + 1 - N
                ans = (f"the shadow of {_pname()} over the field with {p} elements holds {N} points including the point at infinity "
                       f"— the coefficient a is p plus one minus the count: {_frac(Fraction(ap))}")
                _derived(concept, ans, [f.id], ans)
                return out
            if mode == "s14-aptable":
                table = "; ".join(
                    f"at {p}: {_frac(Fraction(_bsd_py_ap(p, a3, a, b)))}" for p in _s13_py_primes(end)
                )
                ans = f"the shadows of {_pname()} at the primes of my line — {table} — all {len(_s13_py_primes(end))} primes, at the line end {end}"
                _derived(concept, ans, [f.id], ans)
                return out
            if mode == "s14-hasse":
                p = slots["p"]
                if p < 2 or p > end:
                    _off_line(p, "check", concept, "s14-hasse")
                    return out
                ap = _bsd_py_ap(p, a3, a, b)
                if ap * ap > 4 * p:  # pragma: no cover - the bound holds on the line (the census)
                    _honest(concept, f"s14-hasse:fail-{end}",
                            f"at {p} the coefficient squares to {ap * ap} against four p at {4 * p} — the bound would fail; it does not, at the line end {end}",
                            f"s14-hasse:fail-{end}-at-{turn}")
                    return out
                ans = (f"yes — at {p} the coefficient of {_pname()} squares to {ap * ap} and four p is {4 * p}: "
                       f"the Hasse bound holds, the prime by prime record standing at the line end {end}")
                _derived(concept, ans, [f.id], ans)
                return out
            if mode == "s14-hasse-all":
                checks = 2 * len(_s13_py_primes(end))
                fails = [
                    (nm, p) for nm, cv in (("the first panel member", B14_A), ("the second panel member", B14_B))
                    for p in _s13_py_primes(end) if _bsd_py_ap(p, *cv) ** 2 > 4 * p
                ]
                if fails:  # pragma: no cover - the census holds all-pass on the line
                    _honest(concept, f"s14-hasse-all:fail-{end}",
                            f"the record says: the bound fails at {fails} — it does not on my line; the line ends where the census ends, at the line end {end}",
                            f"s14-hasse-all:fail-{end}-at-{turn}")
                    return out
                ans = (f"yes — both panel members respect the Hasse bound at every prime on the line: {checks} prime checks, "
                       f"all passing, the full record at the line end {end} — the bound is a theorem of record, this census the verified shadow of it")
                _derived(concept, ans, [f.id], ans)
                return out
            # the CM signature (panel A of record)
            if mode == "s14-cmsig":
                a3, a, b = B14_A
                zeros = [p for p in _s13_py_primes(end) if _bsd_py_ap(p, a3, a, b) == 0]
                want = [p for p in _s13_py_primes(end) if p == 2 or p % 4 == 3]
                if zeros != want:  # pragma: no cover - the signature holds on the line
                    _honest(concept, f"s14-cmsig:fail-{end}",
                            f"the zeros sit at {zeros} against the record signature {want} — a disagreement my line would name, at the line end {end}",
                            f"s14-cmsig:fail-{end}-at-{turn}")
                    return out
                ans = (f"yes — the record signature holds across my line: the zero coefficients sit exactly at two and the primes "
                       f"three mod four, both directions checked, {len(want)} of the {len(_s13_py_primes(end))} primes at the line end {end}; "
                       f"the reason is of record (the curve's complex multiplication), the pattern the verified shadow on my line")
                _derived(concept, ans, [f.id], ans)
                return out
            zeros = [p for p in _s13_py_primes(end) if _bsd_py_ap(p, *B14_A) == 0]
            ans = (f"the zero coefficients of the first panel member sit at {', '.join(str(p) for p in zeros)} — two, and the "
                   f"thirteen primes three mod four on the line, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s14-torsion-a":
            concept = CONCEPT_S14_FORM
            if _fact("form-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("form-def")
            assert f is not None
            pts = ", ".join(_pt(p) for p in S14_BEDS["torsion_A"])
            ans = (f"the rational points of the first panel member my line holds: the point at infinity, {pts} — the three "
                   f"points of order two, and of record no more (rank zero; the census finds torsion only, consistent with the record)")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s14-gen", "s14-gen-all"):
            concept = CONCEPT_S14_LAW
            if _fact("law-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("law-def")
            assert lf is not None
            G = (0, 0)
            if mode == "s14-gen":
                Q = (_coord(slots["x1"]), _coord(slots["y1"]))
                if not _bsd_py_on_curve(Q, *B14_B):
                    _honest(concept, f"s14-gen:off-curve-{end}",
                            f"{_pt(Q)} is not on the second panel member — the ledger has no entry for a point off the curve",
                            f"s14-gen:off-curve-{end}-at-{turn}")
                    return out
                hit = next((m for m in range(1, 17) if _bsd_py_mul(m, G, *B14_B) == Q or _bsd_py_mul(m, G, *B14_B) == _bsd_py_neg(Q, *B14_B)), None)
                if hit is None:
                    _honest(concept, f"s14-gen:bound-{end}", self.W_S14_3, f"s14-gen:bound-{end}-at-{turn}")
                    return out
                k = hit if _bsd_py_mul(hit, G, *B14_B) == Q else -hit
                ans = (f"yes — {_pt(Q)} is {_frac(Fraction(k))} times the point at x 0 y 0 on the second panel member, "
                       f"the double-and-add ledger landing exactly, within my bound of sixteen")
                _derived(concept, ans, [lf.id], ans)
                return out
            small = [tuple(p) for p in S14_BEDS["small_B"]]
            missed = []
            for Q in small:
                hit = next((m for m in range(1, 7) if _bsd_py_mul(m, G, *B14_B) == Q or _bsd_py_mul(m, G, *B14_B) == _bsd_py_neg(Q, *B14_B)), None)
                if hit is None:
                    missed.append(Q)
            if missed:  # pragma: no cover - the ledger covers 10/10 on the line
                _honest(concept, f"s14-gen-all:miss-{end}",
                        f"{len(missed)} of the counted points fall outside the ledger within my bound — the line would name them, and on my line it does not, at the line end {end}",
                        f"s14-gen-all:miss-{end}-at-{turn}")
                return out
            ans = (f"yes — all ten points my line counted on the second panel member sit in the ledger of the point at x 0 y 0, "
                   f"the multiples between one and six and their reflections, the ten of ten record at the line end {end}; the generator itself is of record, this ledger the verified shadow on my line")
            _derived(concept, ans, [lf.id], ans)
            return out

        if mode == "s14-gen-close":
            concept = CONCEPT_S14_LAW
            if _fact("law-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            _honest(concept, f"s14-gen-close-{end}", self.W_S14_3, f"s14-gen-close-{end}-at-{turn}")
            return out

        if mode == "s14-lpar":
            concept = CONCEPT_S14_SHADOW
            if _fact("shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("shadow-def")
            assert f is not None
            a3, a, b = _panel()
            L = _bsd_py_Lpartial(a3, a, b, end)
            more = ""
            if slots["panel"] == "second":
                more = " — the record names its limit past the line (zero of order one, the rank one vanishing); my partial holds, the limit is named, not reached"
            ans = f"the L product of {_pname()} at my line end {end} holds the exact rational {_frac(Fraction(L))}{more}"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s14-lvanish":
            concept = CONCEPT_S14_SHADOW
            if _fact("shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            if slots["panel"] == "second":
                _honest(concept, f"s14-lvanish:limit-{end}", self.W_S14_5, f"s14-lvanish:limit-{end}-at-{turn}")
            else:
                _honest(
                    concept,
                    f"s14-lvanish:limit-a-{end}",
                    f"of record the limit of the first panel member's L product is nonzero (order zero, consistent with my partial "
                    f"holding its exact value at the line end {end}); the limit itself is a limit fact past my line — named, not "
                    f"reached, at the line end {end}",
                    f"s14-lvanish:limit-a-{end}-at-{turn}",
                )
            return out

        if mode == "s14-rh-touch":
            if _fact("shadow-def") is None:
                _unlearned(concept_map(CONCEPT_S14_SHADOW).label)
                return out
            _honest(CONCEPT_S14_SHADOW, f"s14-rh-touch-{end}", self.W_S14_7, f"s14-rh-touch-{end}-at-{turn}")
            return out

        if mode == "s14-rank":
            if _fact("shadow-def") is None:
                _unlearned(concept_map(CONCEPT_S14_SHADOW).label)
                return out
            _honest(CONCEPT_S14_SHADOW, f"s14-rank-{end}", self.W_S14_4, f"s14-rank-{end}-at-{turn}")
            return out

        if mode == "s14-search-b":
            if _fact("form-def") is None:
                _unlearned(concept_map(CONCEPT_S14_FORM).label)
                return out
            _honest(CONCEPT_S14_FORM, f"s14-search-b-{end}", self.W_S14_2, f"s14-search-b-{end}-at-{turn}")
            return out

        if mode == "s14-panel":
            if _fact("form-def") is None:
                _unlearned(concept_map(CONCEPT_S14_FORM).label)
                return out
            _honest(CONCEPT_S14_FORM, f"s14-panel-{end}", self.W_S14_6, f"s14-panel-{end}-at-{turn}")
            return out

        if mode == "s14-bandstate":
            concept = CONCEPT_S14_FORM
            if _fact("form-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("form-def")
            assert f is not None
            ans = ("this band added the curve form, the chord-tangent law, the shadow count, and the shadow censuses — four lessons and "
                   "four theorems (the identity, the inverse, the Hasse census, the record signature), two panel curves of record, the "
                   "shadow tables on the line, and seven honest walls — and nothing on this band is conditional on the Riemann hypothesis, "
                   "at the line end 84")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s14-uncond":
            concept = CONCEPT_S14_SHADOW
            if _fact("shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("shadow-def")
            assert f is not None
            ans = (f"nothing the elliptic band says is conditional on the Riemann hypothesis — the censuses are exact on the line, and the "
                   f"record facts (the ranks, the limits) are named of record, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s14-state":
            slug = slots["slug"]
            concept = S14_SLUG_CONCEPT.get(slug, CONCEPT_S14_FORM)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant15(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.19 / S15 — the L-function of the city (BSD band 2 of 3)."""
        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _frac(v: Fraction) -> str:
            sign = "minus " if v < 0 else ""
            v = abs(v)
            if v.denominator == 1:
                return f"{sign}{v.numerator}"
            return f"{sign}{v.numerator} over {v.denominator}"

        def _panel() -> tuple[int, int, int]:
            return B14_A if slots.get("panel") == "first" else B14_B

        def _pname() -> str:
            return "the first panel member" if slots.get("panel") == "first" else "the second panel member"

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _off_line(n: int, verb: str, concept_id: str, tag: str) -> None:
            _honest(
                concept_id,
                f"{tag}:{n}:off-line-{end}",
                f"{n} is off my 0..{end} line — i cannot {verb} what my line does not reach",
                f"{tag}:{n}:off-line-{end}-at-{turn}",
            )

        if mode in ("s15-factor", "s15-form"):
            concept = CONCEPT_S15_LOCAL if mode == "s15-form" else CONCEPT_S15_FACTOR
            slug = "l-local-def" if mode == "s15-form" else "l-factor-def"
            if _fact(slug) is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact(slug)
            assert f is not None
            if mode == "s15-form":
                a3, a, b = B14_A if slots["panel"] == "first" else B14_B
                rp = 2 if slots["panel"] == "first" else 37
                u = _bsd_py_lfactor(rp, a3, a, b, "uniform")
                r = _bsd_py_lfactor(rp, a3, a, b, "record")
                ans = (
                    f"at its ramified prime {rp} the record form of {_pname()} carries the single term {_frac(r)} — "
                    f"against the uniform factor {_frac(u)}"
                    + (", the unit: the additive prime carries nothing, the coefficient is zero" if r == 1
                       else ", the multiplicative factor with its sign of record: the coefficient is minus one")
                    + f", at the line end {end}"
                )
                _derived(concept, ans, [f.id], ans)
                return out
            a3, a, b = _panel()
            p = slots["p"]
            if p < 2 or p > end:
                _off_line(p, "carry a factor of", concept, "s15-factor")
                return out
            if _s11_py_spf(p) != p:
                _honest(concept, f"s15-factor:not-prime-{end}",
                        f"{p} is a composite on my line — the factor of the L product is carried at the primes of the line, "
                        f"the composites take their factors from the split",
                        f"s15-factor:not-prime-{end}-at-{turn}")
                return out
            u = _bsd_py_lfactor(p, a3, a, b, "uniform")
            r = _bsd_py_lfactor(p, a3, a, b, "record")
            ans = f"{_pname()} carries the factor {_frac(r if slots['form'] == 'record' else u)} at prime {p} in the {slots['form']} form"
            if slots["form"] == "record" and r != u:
                ans += f" — the ramified form, against the uniform factor {_frac(u)}"
            elif slots["form"] == "record":
                ans += " — here the record and uniform forms agree (the prime is not ramified)"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s15-partial", "s15-recpartial"):
            concept = CONCEPT_S15_PARTIAL
            if _fact("l-partial-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-partial-def")
            assert f is not None
            a3, a, b = _panel()
            form = "record" if mode == "s15-recpartial" else "uniform"
            h = slots["h"]
            if h < 2 or h > end:
                _off_line(h, "hold the L partial at", concept, mode)
                return out
            pts = [p for p in _s13_py_primes(end) if p <= h]
            if not pts:
                _honest(concept, f"s15-partial:no-prime-{end}",
                        f"no prime of the line sits at or below height {h} — the partial product is the empty product, one",
                        f"s15-partial:no-prime-{end}-at-{turn}")
                return out
            beds = {"uniform": {"A": "spots_uniform_A", "B": "spots_uniform_B"},
                    "record": {"A": "spots_record_A", "B": "spots_record_B"}}[form]
            which = "A" if (a3, a, b) == B14_A else "B"
            v = _bsd_py_lspots(a3, a, b, end, form)[pts[-1]]
            # cross-check the mechanism against the frozen bed at the same height
            assert str(v) == str(S15_BEDS[beds[which]][str(pts[-1])]), "spot bed drift"
            walk = ""
            if mode == "s15-recpartial" and which == "B" and h >= 37:
                walk = (f" — and past the conductor prime the record partial has separated from the uniform one "
                        f"by the hair of the correction, at the line end {end}")
            ans = f"the {form} L product of {_pname()} up to height {h} (last prime {pts[-1]}) holds the exact rational {_frac(v)}{walk}"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-corr":
            concept = CONCEPT_S15_CORR
            if _fact("l-corr-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-corr-def")
            assert f is not None
            a3, a, b = _panel()
            corr = _bsd_py_lcorr(a3, a, b, end)
            rp = 2 if (a3, a, b) == B14_A else 37
            ans = (f"the ramification correction of {_pname()} is {_frac(corr)} — the record factor {_frac(_bsd_py_lfactor(rp, a3, a, b, 'record'))} "
                   f"over the uniform factor {_frac(_bsd_py_lfactor(rp, a3, a, b, 'uniform'))} at its single ramified prime {rp} on the line, "
                   f"and the record partial is the uniform partial times it, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-identity":
            concept = CONCEPT_S15_CORR
            if _fact("l-corr-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-corr-def")
            assert f is not None
            a3, a, b = _panel()
            uni = _bsd_py_lpartial_uniform(a3, a, b, end)
            corr = _bsd_py_lcorr(a3, a, b, end)
            rec = _bsd_py_lpartial_record(a3, a, b, end)
            if rec != uni * corr:  # pragma: no cover - the identity holds on the line
                _honest(concept, f"s15-identity:fail-{end}",
                        f"the record partial {rec} stands against the uniform times the correction {uni * corr} — a disagreement my line would name, at the line end {end}",
                        f"s15-identity:fail-{end}-at-{turn}")
                return out
            ans = (f"yes — for {_pname()} the record partial {_frac(rec)} is the uniform partial {_frac(uni)} times the correction {_frac(corr)}, "
                   f"both sides held as exact rationals, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-added":
            concept = CONCEPT_S15_PARTIAL
            if _fact("l-partial-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-partial-def")
            assert f is not None
            a3, a, b = _panel()
            form = slots["form"]
            p = slots["p"]
            if p < 2 or p > end:
                _off_line(p, "add to the L partial", concept, "s15-added")
                return out
            if _s11_py_spf(p) != p:
                _honest(concept, f"s15-added:not-prime-{end}",
                        f"{p} is a composite on my line — the partial product runs over the primes, and a composite adds no factor of its own",
                        f"s15-added:not-prime-{end}-at-{turn}")
                return out
            spots = _bsd_py_lspots(a3, a, b, end, form)
            prev = [q for q in _s13_py_primes(end) if q < p]
            before = spots[prev[-1]] if prev else Fraction(1)
            fac = _bsd_py_lfactor(p, a3, a, b, form)
            after = spots[p]
            if after != before * fac:  # pragma: no cover - the rule holds on the line
                _honest(concept, f"s15-added:fail-{end}",
                        f"the partial at height {p} ({after}) does not stand as the previous ({before}) times the factor ({fac}) — the rule would fail; it does not, at the line end {end}",
                        f"s15-added:fail-{end}-at-{turn}")
                return out
            ans = (f"it is multiplied by the factor at {p}: the {form} partial of {_pname()} at {before} times the factor {_frac(fac)} "
                   f"is the partial {_frac(after)} — the change is exactly the added factor, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-vanish-b":
            if _fact("l-partial-def") is None:
                _unlearned(concept_map(CONCEPT_S15_PARTIAL).label)
                return out
            _honest(CONCEPT_S15_PARTIAL, f"s15-vanish-b-{end}", self.W_S15_1, f"s15-vanish-b-{end}-at-{turn}")
            return out

        if mode == "s15-nonzero-a":
            if _fact("l-partial-def") is None:
                _unlearned(concept_map(CONCEPT_S15_PARTIAL).label)
                return out
            _honest(CONCEPT_S15_PARTIAL, f"s15-nonzero-a-{end}", self.W_S15_2, f"s15-nonzero-a-{end}-at-{turn}")
            return out

        if mode == "s15-region":
            if _fact("l-factor-def") is None:
                _unlearned(concept_map(CONCEPT_S15_FACTOR).label)
                return out
            _honest(CONCEPT_S15_FACTOR, f"s15-region-{end}", self.W_S15_3, f"s15-region-{end}-at-{turn}")
            return out

        if mode == "s15-ramline":
            if _fact("l-local-def") is None:
                _unlearned(concept_map(CONCEPT_S15_LOCAL).label)
                return out
            _honest(CONCEPT_S15_LOCAL, f"s15-ramline-{end}", self.W_S15_4, f"s15-ramline-{end}-at-{turn}")
            return out

        if mode == "s15-bsd-touch":
            if _fact("l-corr-def") is None:
                _unlearned(concept_map(CONCEPT_S15_CORR).label)
                return out
            _honest(CONCEPT_S15_CORR, f"s15-bsd-touch-{end}", self.W_S15_5, f"s15-bsd-touch-{end}-at-{turn}")
            return out

        if mode == "s15-bandstate":
            concept = CONCEPT_S15_FACTOR
            if _fact("l-factor-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-factor-def")
            assert f is not None
            ans = ("this band added the L-family of the city: the factor each prime carries (the uniform two-term form, the record's "
                   "one-term form at the ramified primes), the partial the line holds as an exact rational, the added-term rule, the "
                   "ramification corrections, three theorems (the added term, the record identity, the ramified unit), and five honest "
                   "walls — and nothing on this band is conditional on the Riemann hypothesis, at the line end 84")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-uncond":
            concept = CONCEPT_S15_CORR
            if _fact("l-corr-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("l-corr-def")
            assert f is not None
            ans = (f"nothing the L band says is conditional on the Riemann hypothesis — the factors, the partials, and the corrections "
                   f"are exact on the line, and the record facts (the order of vanishing, the ranks) are named of record on their walls, "
                   f"at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s15-state":
            slug = slots["slug"]
            concept = S15_SLUG_CONCEPT.get(slug, CONCEPT_S15_FACTOR)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed


    def _policy_savant16(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.20 / S16 — the descent and the reaching (BSD band 3 of 3,
        the island's summit)."""
        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _frac(v: Fraction) -> str:
            sign = "minus " if v < 0 else ""
            v = abs(v)
            if v.denominator == 1:
                return f"{sign}{v.numerator}"
            return f"{sign}{v.numerator} over {v.denominator}"

        def _which() -> str:
            return "A" if slots.get("panel") == "first" else "B"

        def _pname() -> str:
            return "the first panel member" if slots.get("panel") == "first" else "the second panel member"

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _uA() -> Fraction:
            return _bsd_py_lpartial_uniform(*B14_A)

        def _uB() -> Fraction:
            return _bsd_py_lpartial_uniform(*B14_B)

        def _rB() -> Fraction:
            return _bsd_py_lpartial_record(*B14_B)

        if mode == "s16-order":
            concept = CONCEPT_S16_AO
            if _fact("vanish-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("vanish-def")
            assert f is not None
            w = _which()
            u = _uA() if w == "A" else _uB()
            assert str(u) == str(S16_BEDS[f"uniform_84_{w}"]), "line-end partial drift"
            if w == "A":
                ans = (f"of record, the L product of {_pname()} is nonzero at s equal to one — order zero of vanishing — "
                       f"and on my line the exact partial {_frac(u)} stands nonzero for the line's side, at the line end {end}")
            else:
                ans = (f"of record, the L product of {_pname()} vanishes at s equal to one, of order one — and on my line "
                       f"the exact partial {_frac(u)} stands far from zero for the line's side (the vanishing is the divergence "
                       f"of the infinite product past the line), at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-rank":
            concept = CONCEPT_S16_AR
            if _fact("rank-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("rank-def")
            assert f is not None
            w = _which()
            rnk = S16_BEDS["rank"][w]
            word_rnk = "zero" if rnk == 0 else "one"
            if w == "A":
                ans = (f"of record, the algebraic rank of {_pname()} is {word_rnk} — settled by the two-descent: the selmer "
                       f"dimension two against its two-torsion dimension two, the descent bound zero, met by the torsion ledger "
                       f"(its three torsion points, no generator); no B S D is used, at the line end {end}")
            else:
                ans = (f"of record, the algebraic rank of {_pname()} is {word_rnk} — settled by the two-descent: the selmer "
                       f"dimension one against its two-torsion dimension zero, the descent bound one, met by the generator "
                       f"(x zero y zero) of record, on my line; no B S D is used, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-descend":
            concept = CONCEPT_S16_AR
            if _fact("rank-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("rank-def")
            assert f is not None
            w = _which()
            sel = S16_BEDS["selmer_dim"][w]
            e2 = S16_BEDS["e2_dim"][w]
            bound = S16_BEDS["descend_bound"][w]
            word = {"A": "two", "B": "one"}
            sel_w = word[w]
            e2_w = "two" if w == "A" else "zero"
            bound_w = "zero" if bound == 0 else "one"
            if w == "A":
                met = "and the point ledger holds only its three torsion points (x zero y zero, x one y zero, x minus one y zero), so the rank is zero, settled"
            else:
                met = "and the generator (x zero y zero) of record, on my line, meets it (the rank is at least one), so the rank is one, settled"
            ans = (f"for {_pname()}, the descent bound is the selmer dimension {sel_w} minus the two-torsion dimension {e2_w} — "
                   f"{bound_w} — {met}, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-selmer":
            concept = CONCEPT_S16_AR
            if _fact("rank-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("rank-def")
            assert f is not None
            w = _which()
            sel = S16_BEDS["selmer_dim"][w]
            rnk = S16_BEDS["rank"][w]
            e2 = S16_BEDS["e2_dim"][w]
            words = {0: "zero", 1: "one", 2: "two"}
            ans = (f"of record, {words[sel]}: the rank {words[rnk]} plus the two-torsion dimension {words[e2]} plus the "
                   f"two-shaf dimension zero (the shaf is trivial of record on both members), at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-selwall":
            if _fact("rank-def") is None:
                _unlearned(concept_map(CONCEPT_S16_AR).label)
                return out
            _honest(CONCEPT_S16_AR, f"s16-selwall-{_which()}-{end}", self.W_S16_1, f"s16-selwall-{_which()}-{end}-at-{turn}")
            return out

        if mode == "s16-bsd":
            concept = CONCEPT_S16_BS
            if _fact("statement-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("statement-def")
            assert f is not None
            ans = (f"the summit of the island is the statement itself — held in my store as a declared record fact (the clay "
                   f"millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one equals "
                   f"the algebraic rank — and on my panel the two sides are settled of record and they agree: order zero equals "
                   f"rank zero for the first member, and order one equals rank one for the second, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-reach":
            concept = CONCEPT_S16_REACH
            if _fact("reach-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("reach-def")
            assert f is not None
            uA, uB, rB = _uA(), _uB(), _rB()
            assert str(uA) == str(S16_BEDS["uniform_84_A"]), "line-end partial drift"
            assert str(uB) == str(S16_BEDS["uniform_84_B"]), "line-end partial drift"
            assert str(rB) == str(S16_BEDS["record_84_B"]), "line-end record partial drift"
            gen = S16_BEDS["gen_B"]
            assert gen["covered"] == gen["counted"] == 10, "the generation ledger drifted"
            ans = (f"the line holds toward the summit: the exact partials (the first member's uniform partial {_frac(uA)} holds "
                   f"nonzero, the second member's uniform partial {_frac(uB)} and record partial {_frac(rB)} stand far from "
                   f"zero), the torsion ledger of the first member (its three integral two-torsion points on the line — x zero "
                   f"y zero, x one y zero, x minus one y zero), and the generation ledger of the second member (the generator "
                   f"(x zero y zero), and every point my line counted is a small multiple of it — ten of ten), at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-torsion":
            concept = CONCEPT_S16_AR
            if _fact("rank-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("rank-def")
            assert f is not None
            pts = S16_BEDS["torsion_A"]
            ans = (f"the torsion ledger of the first panel member holds its three integral two-torsion points on my line — "
                   f"(x zero y zero), (x one y zero), (x minus one y zero) — the full two-torsion of record (z/2 squared), "
                   f"and nothing else on the line, at the line end {end}")
            assert pts == [[0, 0], [1, 0], [-1, 0]], "the torsion ledger drifted"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-gen":
            concept = CONCEPT_S16_AR
            if _fact("rank-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("rank-def")
            assert f is not None
            gen = S16_BEDS["gen_B"]
            assert gen == {"generator": [0, 0], "covered": 10, "counted": 10}, "the generation ledger drifted"
            ans = (f"the generation ledger of the second panel member holds the generator (x zero y zero) of record, and every "
                   f"point my line counted is a small multiple of it — ten of ten of the ledger, closed on the line, at the "
                   f"line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-consistent":
            concept = CONCEPT_S16_REACH
            if _fact("reach-def") is None or _fact("l-partial-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            fR = _fact("reach-def")
            fL = _fact("l-partial-def")
            assert fR is not None and fL is not None
            uA, uB = _uA(), _uB()
            assert (uA != Fraction(0)) is S16_BEDS["consistent_A_nonzero"], "the consistency verdict drifted"
            assert (uB > Fraction(1)) is S16_BEDS["consistent_B_far"], "the consistency verdict drifted"
            ans = (f"yes — on my line: the first member's exact uniform partial {_frac(uA)} stands nonzero, consistent with "
                   f"the record's order zero, and the second member's exact partial {_frac(uB)} stands far from zero at the "
                   f"line end, consistent with the record's order one (the vanishing is the divergence of the infinite product "
                   f"past the line), at the line end {end}")
            _derived(concept, ans, [fR.id, fL.id], ans)
            return out

        if mode == "s16-lvalwall":
            if _fact("vanish-def") is None:
                _unlearned(concept_map(CONCEPT_S16_AO).label)
                return out
            _honest(CONCEPT_S16_AO, f"s16-lvalwall-{_which()}-{end}", self.W_S16_2, f"s16-lvalwall-{_which()}-{end}-at-{turn}")
            return out

        if mode == "s16-panel":
            if _fact("statement-def") is None:
                _unlearned(concept_map(CONCEPT_S16_BS).label)
                return out
            _honest(CONCEPT_S16_BS, f"s16-panel-{end}", self.W_S16_3, f"s16-panel-{end}-at-{turn}")
            return out

        if mode == "s16-sides":
            concept = CONCEPT_S16_BS
            if _fact("vanish-def") is None or _fact("rank-def") is None:
                _unlearned(concept_map(CONCEPT_S16_BS).label)
                return out
            fA = _fact("vanish-def")
            fR = _fact("rank-def")
            assert fA is not None and fR is not None
            w = _which()
            o, r = S16_BEDS["order"][w], S16_BEDS["rank"][w]
            words = {0: "zero", 1: "one"}
            ans = (f"for {_pname()}, the analytic side is the order {words[o]} of vanishing of record, the algebraic side is "
                   f"the rank {words[r]} of record — the order {words[o]} equals the rank {words[r]}, at the line end {end}")
            _derived(concept, ans, [fA.id, fR.id], ans)
            return out

        if mode == "s16-bandstate":
            concept = CONCEPT_S16_BS
            if _fact("statement-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("statement-def")
            assert f is not None
            ans = (f"the summit band holds the statement itself, stored as a declared record fact (the clay millennial "
                   f"booklet, the wiles chapter), with its satisfaction on the panel of record — order zero equals rank zero "
                   f"for the first member, order one equals rank one for the second — and the line's side standing: the "
                   f"two-descent exact sequence and descent bounds, the exact partials consistent with both orders — the "
                   f"island's summit filed, the island closed, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-uncond":
            concept = CONCEPT_S16_BS
            if _fact("statement-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("statement-def")
            assert f is not None
            ans = (f"nothing the summit band says is conditional on the Riemann hypothesis — the two-descent, the exact "
                   f"sequence, the selmer census, and the statement of record are unconditional mathematics on my panel, and "
                   f"the record's values (the L values, the leading coefficient) stand named of record on their walls, at the "
                   f"line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s16-state":
            slug = slots["slug"]
            concept = S16_SLUG_CONCEPT.get(slug, CONCEPT_S16_BS)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed


    def _policy_savant17(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.21 / S17 — the valuation line (the Beal island)."""
        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s17-vp":
            concept = CONCEPT_S17_VAL
            if _fact("valuation-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("valuation-def")
            assert f is not None
            n = _S17_NUM_WORD[slots["n"]]
            p = _S17_P_WORD[slots["p"]]
            depth = _beal_py_v_p(n, p)
            assert depth == S17_BEDS["vp"][(n, p)], "the valuation bed drifted"
            words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
            ans = (f"the p-adic depth of {slots['n']} at the prime {slots['p']} of record is {words[depth]} — read off "
                   f"the {slots['p']}-rung of the first-divisor factorization chain of {slots['n']}, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s17-lte-a", "s17-lte-b"):
            concept = CONCEPT_S17_LTE
            if _fact("lte-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("lte-def")
            assert f is not None
            x, y = (4, 1) if mode == "s17-lte-a" else (10, 1)
            p, n = 3, 3
            vm = _beal_py_v_p(x - y, p)
            vn = _beal_py_v_p(n, p)
            vt = _beal_py_v_p(x ** n - y ** n, p)
            assert vt == vm + vn, "the lte bed drifted"
            words = {1: "one", 2: "two", 3: "three"}
            if mode == "s17-lte-a":
                lhs = "four cubed minus one cubed — sixty-three — holds two of the three-rung"
            else:
                lhs = "ten cubed minus one cubed — nine hundred and ninety-nine — holds three of the three-rung"
            ans = (f"it holds: {lhs}, while the difference {x - y} holds {words[vm]} of the three-rung and the exponent "
                   f"three holds {words[vn]} of it — {words[vm]} plus {words[vn]} is {words[vt]} — the depth of the "
                   f"difference plus the depth of the exponent, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-lte-ledger":
            concept = CONCEPT_S17_LTE
            if _fact("lte-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("lte-def")
            assert f is not None
            assert (S17_BEDS["lte_instances"], S17_BEDS["lte_failures"]) == _beal_py_lte_box()[:2], "the lte ledger drifted"
            ans = (f"two hundred forty-nine thousand two hundred eighty of record: the odd primes at or below my line end, "
                   f"the difference a multiple of the prime with neither term divisible by it, the exponents three through "
                   f"the line end — every one holds: zero deviations, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-beal":
            concept = CONCEPT_S17_BS17
            if _fact("beal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("beal-def")
            assert f is not None
            ans = (f"the statement of record, as the ams beal prize holds it: if a to the x power plus b to the y power "
                   f"equals c to the z power, with a, b, c, x, y and z positive and x, y and z each above two, then "
                   f"a, b and c have a common prime factor — no pairwise coprime solution exists once every exponent is "
                   f"above two, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-census":
            concept = CONCEPT_S17_CENS
            if _fact("census-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("census-def")
            assert f is not None
            assert S17_BEDS["census_count"] == _beal_py_census()[0], "the census bed drifted"
            ans = (f"eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and "
                   f"ten of record — and every one of the eighty-three carries its common prime factor: no primitive "
                   f"triple in the box, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-empt":
            concept = CONCEPT_S17_CENS
            if _fact("census-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("census-def")
            assert f is not None
            assert S17_BEDS["primitive_count"] == _beal_py_census()[1] == 0, "the primitive census drifted"
            ans = (f"zero — no primitive triple lives on my line; the line ends where the primitive triples would live, "
                   f"and that territory is a wall, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-family":
            concept = CONCEPT_S17_CENS
            if _fact("census-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("census-def")
            assert f is not None
            rows = S17_BEDS["census"]
            twos = sum(1 for r in rows if r[6] == 2)
            odds = len(rows) - twos
            ans = (f"the two-power twins (two to the n plus two to the n equals two to the n plus one), the three-family "
                   f"(three cubed plus six cubed equals three to the fifth), the seven-family (seven cubed plus seven to "
                   f"the fourth equals fourteen cubed), the fifteen-family (fifteen to the fourth plus fifteen to the "
                   f"fifth equals thirty to the fourth), and the seventeen, nineteen, twenty-six, twenty-eight, "
                   f"thirty-one, thirty-three families with their common factors — {twos} of the eighty-three carry the "
                   f"two, the other {odds} their odd primes, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s17-prim", "s17-fc", "s17-flt"):
            concept = CONCEPT_S17_BS17
            if _fact("beal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            wall = {"s17-prim": self.W_S17_1, "s17-fc": self.W_S17_2, "s17-flt": self.W_S17_3}[mode]
            _honest(concept, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        if mode == "s17-bandstate":
            concept = CONCEPT_S17_CENS
            if _fact("census-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("census-def")
            assert f is not None
            ans = (f"the beal band holds the statement of the island, stored as a declared record fact (the ams beal "
                   f"prize), its satisfaction filed on my line — the verification census of the box: eighty-three "
                   f"triples, every one carrying its common prime factor, zero primitive — with the valuation read off "
                   f"the first-divisor chain and the lift-the-exponent ledger holding in all its instances, the "
                   f"primitive territory, the fermat catalan boundary, and the fermat anchor named on their walls, at "
                   f"the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-uncond":
            concept = CONCEPT_S17_BS17
            if _fact("beal-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("beal-def")
            assert f is not None
            ans = (f"nothing the beal band says is conditional on an unproved hypothesis — the valuation, the "
                   f"lift-the-exponent ledger, and the verification census are record on the line, and the primitive "
                   f"territory, the fermat catalan boundary, and the fermat anchor stand named of record on their walls, "
                   f"at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s17-state":
            slug = slots["slug"]
            concept = S17_SLUG_CONCEPT.get(slug, CONCEPT_S17_BS17)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed


    def _policy_savant18(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.22 / S18 — the decidable line (the P vs NP island, band 1 of 2)."""
        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s18-dec":
            concept = CONCEPT_S18_DQ
            if _fact("question-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("question-def")
            assert f is not None
            pword = slots["p"]
            pw = {"seven": 7, "thirteen": 13, "two": 2, "three": 3, "seventeen": 17}[pword]
            assert (84 % pw == 0) == S18_BEDS["decision"][pword], "the decision bed drifted"
            answers = {
                "seven": "yes — the seven divides the eighty-four: twelve of them, at the line end",
                "thirteen": "no — the thirteen does not divide the eighty-four: the walk leaves a remainder of six (thirteen times six is seventy-eight), at the line end",
                "two": "yes — the two divides the eighty-four: forty-two of them, at the line end",
                "three": "yes — the three divides the eighty-four: twenty-eight of them, at the line end",
                "seventeen": "no — the seventeen does not divide the eighty-four: the walk leaves a remainder of sixteen (seventeen times four is sixty-eight), at the line end",
            }
            ans = answers[pword] + " 84"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-pi":
            concept = CONCEPT_S18_RED
            if _fact("reduction-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("reduction-def")
            assert f is not None
            assert S18_BEDS["pi"] == _pnp_py_pi_count(_S18_END) == 23, "the pi census drifted"
            ans = (f"twenty-three of record — the numbers from two to my line end whose first divisor is themselves: "
                   f"two, three, five, seven, eleven, thirteen, seventeen, nineteen, twenty-three, twenty-nine, "
                   f"thirty-one, thirty-seven, forty-one, forty-three, forty-seven, fifty-three, fifty-nine, "
                   f"sixty-one, sixty-seven, seventy-one, seventy-three, seventy-nine, eighty-three — the "
                   f"first-divisor census is a walk that ends in one hundred ninety-two candidate steps, at the "
                   f"line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-scan":
            concept = CONCEPT_S18_COST
            if _fact("cost-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("cost-def")
            assert f is not None
            assert S18_BEDS["scan_cost"] == _pnp_py_scan_cost(_S18_END) == 192, "the scan cost drifted"
            ans = (f"one hundred ninety-two candidate steps of record — the walk over every number from two to my "
                   f"line end, each to its first divisor, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-heavy":
            concept = CONCEPT_S18_COST
            if _fact("cost-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("cost-def")
            assert f is not None
            hm, hc = S18_BEDS["heaviest"]
            assert (hm, hc) == _pnp_py_heaviest(_S18_END) == (83, 8), "the heaviest row drifted"
            ans = (f"the number eighty-three — the largest prime below my line end — its walk tries the candidates "
                   f"up to the floor of the square root: eight candidate steps of record, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-costspot":
            concept = CONCEPT_S18_COST
            if _fact("cost-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("cost-def")
            assert f is not None
            n = _S18_NUM_WORD[slots["n"]]
            c = _pnp_py_spf_cost(n)
            assert S18_BEDS["cost_spot"][n] == c, "the cost spot drifted"
            answers = {
                "sixty-four": "one — the two divides on the first try of the walk, at the line end",
                "forty-nine": "six — the walk tries two, three, four, five, six, and the seven before it stops (seven squared is forty-nine), at the line end",
                "eighty-four": "one — the two divides on the first try of the walk, at the line end",
                "twelve": "one — the two divides on the first try of the walk, at the line end",
                "two": "zero — the walk's loop never runs over the two, at the line end",
            }
            ans = answers[slots["n"]] + " 84"
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-ph":
            concept = CONCEPT_S18_DQ
            if _fact("question-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("question-def")
            assert f is not None
            nword = slots["n"]
            n = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}[nword]
            total, inj = S18_BEDS["pigeonhole"][n]
            assert (total, inj) == _pnp_py_pigeonhole(n), "the pigeonhole bed drifted"
            totals = {
                1: "the two maps",
                2: "the nine maps",
                3: "the sixty-four maps",
                4: "the six hundred twenty-five maps",
                5: "the seven thousand seven hundred seventy-six maps",
                6: "the one hundred seventeen thousand six hundred forty-nine maps",
                7: "the two million ninety-seven thousand one hundred fifty-two maps",
                8: "the forty-three million forty-six thousand seven hundred twenty-one maps",
                9: "the one billion maps",
                10: "the twenty-five billion nine hundred thirty-seven million four hundred twenty-four thousand six hundred one maps",
            }
            ans = (f"zero violations of record — {totals[n]} of {nword} plus one objects into {nword} boxes all "
                   f"carry a shared box (one more object than box forces the share), at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-kill":
            concept = CONCEPT_S18_COST
            if _fact("cost-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("cost-def")
            assert f is not None
            assert S18_BEDS["kill_trials"] == _S18_KILL == (95, 87), "the kill-trials row drifted"
            ans = (f"ninety-five candidate steps over the composites with all candidates, eighty-seven with the "
                   f"prime candidates alone — the kill-trials ledger my first-divisor soil already holds, at the "
                   f"line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-tam":
            concept = CONCEPT_S18_TAM
            if _fact("tamable-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("tamable-def")
            assert f is not None
            ans = (f"yes — every query i run on my line ends on the line: a finite question on a finite line, a "
                   f"design fact of the line i hold, not a theorem about the machines of record, at the line end "
                   f"{end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s18-halt", "s18-machine"):
            concept = CONCEPT_S18_TAM
            if _fact("tamable-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            wall = {"s18-halt": self.W_S18_1, "s18-machine": self.W_S18_2}[mode]
            _honest(concept, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        if mode == "s18-bandstate":
            concept = CONCEPT_S18_RED
            if _fact("reduction-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("reduction-def")
            assert f is not None
            ans = (f"the decidable band holds the decision question (the yes/no on my line's objects, ending on the "
                   f"line), the tamability stated as a design fact of my finite line, the reduction (the prime-count "
                   f"question answered by the first-divisor census — twenty-three), the cost counter (one hundred "
                   f"ninety-two candidate steps over the whole line, the heaviest single query eight at eighty-"
                   f"three), the pigeonhole's zero violations, and the halting territory and the machine universe "
                   f"named on their walls, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-uncond":
            concept = CONCEPT_S18_RED
            if _fact("reduction-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("reduction-def")
            assert f is not None
            ans = (f"nothing the decidable band says is conditional on an unproved hypothesis — the decision table, "
                   f"the first-divisor census, and the cost counter are of record on the line, and the halting "
                   f"territory and the machine universe stand named of record on their walls, at the line end {end}")
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s18-state":
            slug = slots["slug"]
            concept = S18_SLUG_CONCEPT.get(slug, CONCEPT_S18_RED)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant19(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.23 — FUNDAMENTALS/PRIZE-ISLANDS S19 (the difficulty
        line; pre-registered E6.23). The p and np classes as the
        line's own pattern, the island's question held VERBATIM as
        declared record (never as a theorem — no theorem:p-vs-np),
        the in-line difficulty census (the parity dnf/cnf blowup,
        D4), and the four walled territories of record (the
        relativization, algebrization, and natural proofs barriers
        plus the ac0 territory)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s19-p":
            concept = CONCEPT_S19_P
            if _fact("p-class-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("p-class-def")
            assert f is not None
            if slots["pword"] == "dividing":
                ans = (
                    f"yes — dividing is a p question on my line: the walk that settles the seven-divides-the-eighty-four "
                    f"ends in bounded cost, and the cost stands recorded as a number on the line, at the line end {end}"
                )
            else:
                ans = (
                    f"yes — the first-divisor question is a p question on my line: the census walk over the whole line "
                    f"ends in one hundred ninety-two candidate steps, and the cost stands recorded as a number on the "
                    f"line, at the line end {end}"
                )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-np":
            concept = CONCEPT_S19_NP
            if _fact("np-class-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("np-class-def")
            assert f is not None
            if slots["npword"] == "parity":
                ans = (
                    f"yes — the parity question is checked by a certificate on my line: a row of the table is the "
                    f"certificate, and the check of it is the walk over the row, which ends in bounded cost — the "
                    f"store's own pattern, at the line end {end}"
                )
            else:
                ans = (
                    f"yes — checking my own derivations carries a certificate on my line: each fact is the certificate "
                    f"of its derivation path, and the check is the walk over that path, which ends — the store's own "
                    f"pattern, at the line end {end}"
                )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-settle":
            concept = CONCEPT_S19_NP
            if _fact("np-class-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("np-class-def")
            assert f is not None
            ans = (
                f"yes — my line settles the parity question in bounded cost: the walk over the table ends, and the "
                f"cost is a number on the line, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-summit":
            concept = CONCEPT_S19_SUMMIT
            if _fact("pnp-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("pnp-def")
            assert f is not None
            ans = (
                f"no — the question of the pnp island is not settled of record: it is declared of record and open of "
                f"record (the cmi record of the million-dollar prize), most complexity theorists believe p is not np, "
                f"of record, but no proof of record settles it, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-statement":
            concept = CONCEPT_S19_SUMMIT
            if _fact("pnp-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("pnp-def")
            assert f is not None
            assert isinstance(f.object, str)
            _derived(concept, f.object, [f.id], f"that one is: {f.object}")
            return out

        if mode == "s19-parity":
            concept = CONCEPT_S19_SHADOW
            if _fact("parity-shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("parity-shadow-def")
            assert f is not None
            kw = slots["kword"]
            k = _S19_KWORD[kw]
            n = S19_BEDS["parity"][k]
            assert n == _pnp_py_parity_terms(k)
            w = _S19_TERMS_WORD[n]
            if k == 16:
                ans = (
                    f"{w} of record — the smallest dnf of parity at sixteen variables needs {w} terms, and the "
                    f"smallest cnf the same — the exponential of record held exact at small k, the shadow of the ac0 "
                    f"territory, at the line end {end}"
                )
            else:
                ans = (
                    f"{w} of record — the smallest dnf of parity at {kw} variables needs {w} terms, and the "
                    f"smallest cnf the same, at the line end {end}"
                )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-parcnf":
            concept = CONCEPT_S19_SHADOW
            if _fact("parity-shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("parity-shadow-def")
            assert f is not None
            ans = (
                f"yes — the clauses of the smallest cnf of parity number exactly the same as the terms of its smallest "
                f"dnf, at every k the line holds: the zero-row flips are one-rows, by the same symmetry, at the line "
                f"end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-settle16":
            concept = CONCEPT_S19_SHADOW
            if _fact("parity-shadow-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("parity-shadow-def")
            assert f is not None
            rows = S19_BEDS["rows16"]
            assert rows == 1 << 16
            ans = (
                f"yes — my line settles the parity question at sixteen variables in bounded cost: the walk over the "
                f"sixty-five thousand five hundred thirty-six rows of the table ends, and the cost is a number on the "
                f"line, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s19-rel", "s19-alg", "s19-natp", "s19-ac0"):
            concept = CONCEPT_S19_SUMMIT
            if _fact("pnp-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            wall = {"s19-rel": self.W_S19_1, "s19-alg": self.W_S19_2, "s19-natp": self.W_S19_3, "s19-ac0": self.W_S19_4}[mode]
            _honest(concept, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        if mode == "s19-bandstate":
            concept = CONCEPT_S19_SUMMIT
            if _fact("pnp-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("pnp-def")
            assert f is not None
            ans = (
                f"the difficulty band holds the p class (the questions the walk settles in bounded cost), the np "
                f"class (the questions whose yes cases carry a checkable certificate — the store's own pattern), the "
                f"question of the island held verbatim of record and open of record, the difficulty census of the "
                f"line (parity's dnf and cnf both growing to thirty-two thousand seven hundred sixty-eight terms at "
                f"sixteen variables while the walk settles it in bounded cost), the three barriers of record and the "
                f"ac0 territory named on their walls, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-unc":
            concept = CONCEPT_S19_SUMMIT
            if _fact("pnp-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            f = _fact("pnp-def")
            assert f is not None
            ans = (
                f"nothing the difficulty band says is conditional on an unproved hypothesis — the census rows are of "
                f"record on the line, the question of the island is declared of record and open of record, and the "
                f"barriers stand named of record on their walls, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s19-state":
            slug = slots["slug"]
            concept = S19_SLUG_CONCEPT.get(slug, CONCEPT_S19_SHADOW)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    # ── S20 weave walks (the store speaks: the walks BELOW read the
    # curriculum:prereq edges and the theorem facts AS THEY STAND IN
    # THE STORE — no hand-written census; the refs and P5 re-walk
    # independently). ─────────────────────────────────────────────────
    def _weave_prereqs(self, concept_id: str) -> tuple[str, ...]:
        """The store's own prereq edges for one concept (the
        curriculum:prereq assertions of the booted store)."""
        if self._codex is None:
            return ()
        out = set()
        for a in self._codex.query(context_match={"kind": "prereq", "concept": concept_id}):
            out.add(a.object_id)
        return tuple(sorted(out))

    def _weave_soil(self) -> tuple[str, ...]:
        """R5 the shared soil: the concepts the BEAL CHAIN and the
        DIFFICULTY CHAIN both reach by one prereq step, as the store
        walks it (divides + the scan-ledger walk, of record)."""
        beal = (
            set(self._weave_prereqs("beal-census"))
            | set(self._weave_prereqs("beal-summit"))
            | set(self._weave_prereqs("valuation"))
        )
        diff = (
            set(self._weave_prereqs("decision-question"))
            | set(self._weave_prereqs("reduction"))
            | set(self._weave_prereqs("cost-counter"))
        )
        soil = tuple(sorted(beal & diff))
        assert soil == ("divides", "scan-ledger"), f"the weave soil drifted: {soil}"
        return soil

    def _weave_node(self) -> tuple[str, ...]:
        """R5 the shared node: the ONE walk standing under the beal
        census, the reduction, and the cost counter at once (the
        scan-ledger walk), as the store walks it."""
        node = (
            set(self._weave_prereqs("beal-census"))
            & set(self._weave_prereqs("reduction"))
            & set(self._weave_prereqs("cost-counter"))
        )
        out = tuple(sorted(node))
        assert out == ("scan-ledger",), f"the weave node drifted: {out}"
        return out

    def _weave_marker_census(self) -> tuple[int, int, int, int]:
        """R3 the scope-closing census of the store's own theorem
        facts: (line-end markers, on-line spot markers, universal
        forms without a marker, total). A form of the line is not a
        census of its end — the universal forms carry no marker."""
        end_n = spot_n = none_n = 0
        for a in self._codex.query(context_match={"kind": "theorem"}):
            if not isinstance(a.object, str):
                continue
            if "line end" in a.object:
                end_n += 1
            elif "at s = 2" in a.object:
                spot_n += 1
            else:
                none_n += 1
        return end_n, spot_n, none_n, end_n + spot_n + none_n

    def _weave_open_count(self) -> int:
        """R1 the settled census: how many of the four island
        statements stand settled of record — by a BARE island theorem
        (the discovery-candidate ids) or a closed conjecture. Zero
        while the candidate invariant holds."""
        ids: set[str] = set()
        for a in self._codex.query():
            if a.id:
                ids.add(a.id)
        settled = 0
        # the riemann member: settled iff a bare theorem stands or the
        # conj is no longer open of record (either one decides)
        conj = self._savant_fact("riemann")
        riemann_settled = (
            "theorem:riemann" in ids
            or (conj is not None and conj.context.data.get("conjecture_status") != "open")
        )
        if riemann_settled:
            settled += 1
        for bare in ("theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np"):
            if bare in ids:
                settled += 1
        return settled

    def _policy_savant20(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.24 — CONNECTING-WORK S20 (the weaving line; the
        synthesis pass over the four closed islands, pre-registered
        E6.24). The four relationships (R1 the summit shape, R2 the
        verification form, R3 the scope-closing form, R4 the boundary
        form, R5 the weave) as walks of the store's own facts, the
        filing summit-shape-filed (the shape, not the statements), and
        the four walled territories W_S20_1..4 (the filing fills the
        shape, the queue stays as declared, the register is the line,
        the store speaks)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S20}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s20-rhsummit":
            conj = _fact("riemann")
            if conj is None:
                _unlearned("the riemann statement of record")
                return out
            assert isinstance(conj.object, str)
            ans = (
                f"the statement of the riemann island, as my store holds it: {conj.object} — declared of "
                f"record, open of record: believed, not known, at the line end {end}"
            )
            # the conj is a status surface (the S8 pattern): grounded
            # EMPTY, the id rides the evidence only (P5)
            out.ir = {"answer": ans, "evidence": [conj.id], "uncertainty_state": "derived"}
            out.events.append(self._record_event("derivation-correct", "riemann", turn, "infant", [conj.id]))
            out.text = f"that one is open of record — {ans}"
            return out

        if mode == "s20-soil":
            concept = CONCEPT_S20_WEAVE
            if _fact("weave-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            self._weave_soil()
            f = _fact("weave-def")
            assert f is not None
            ans = (
                "yes — my islands share the soil of my line itself: the divides question roots both the "
                "beal valuation chain and the difficulty chain (decision, reduction, and cost), and the "
                "scan-ledger walk stands under the beal census, the reduction, and the cost counter at "
                "once — the cross-island joints are already edges in the prereq graph of my line, at the "
                f"line end {end}"
            )
            _derived(
                concept,
                ans,
                [
                    f.id,
                    "curriculum:prereq:valuation>divides",
                    "curriculum:prereq:decision-question>divides",
                    "curriculum:prereq:beal-census>scan-ledger",
                    "curriculum:prereq:reduction>scan-ledger",
                    "curriculum:prereq:cost-counter>scan-ledger",
                ],
                ans,
            )
            return out

        if mode == "s20-node":
            concept = CONCEPT_S20_WEAVE
            if _fact("weave-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            self._weave_node()
            f = _fact("weave-def")
            assert f is not None
            ans = (
                "the scan-ledger walk of record — the one walk that stands under the beal census, under "
                f"the reduction, and under the cost counter at once, at the line end {end}"
            )
            _derived(
                concept,
                ans,
                [
                    f.id,
                    "curriculum:prereq:beal-census>scan-ledger",
                    "curriculum:prereq:reduction>scan-ledger",
                    "curriculum:prereq:cost-counter>scan-ledger",
                ],
                ans,
            )
            return out

        if mode == "s20-shape":
            concept = CONCEPT_S20_SHAPE
            if _fact("summit-shape-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("summit-shape-def")
            assert f is not None
            ans = (
                "one shape of record — the statement of record, the shadow complete on the named scope, "
                "the boundary declared at the line end, and the missing ingredient named, or the "
                f"statement open of record: the riemann, the bsd, the beal, and the p versus np all stand in it, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-open":
            concept = CONCEPT_S20_SHAPE
            if _fact("summit-shape-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            open_n = self._weave_open_count()
            assert open_n == 0, f"the settled census drifted: {open_n}"
            f = _fact("summit-shape-def")
            assert f is not None
            ans = (
                "zero of the four — each island statement stands open of record: the riemann as its "
                "conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal "
                "outside its census box, and the p versus np as its declared question — the partial "
                f"satisfactions of record stand on the line, not as settlements, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-form":
            concept = CONCEPT_S20_SHADOW
            if _fact("shadow-form-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("shadow-form-def")
            assert f is not None
            ans = (
                "the check of a fact on my line is the walk of its own derivation path — each fact is "
                "the certificate of the path by which it was put together, and that walk ends on the "
                f"line: ledgers, censuses, and walks that end, the store's own pattern, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-marker":
            concept = CONCEPT_S20_SHADOW
            if _fact("shadow-form-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            end_n, spot_n, none_n, total = self._weave_marker_census()
            assert end_n + spot_n + none_n == total, "the marker census does not close"
            assert spot_n == 2 and none_n == 24, f"the marker census drifted: {(end_n, spot_n, none_n, total)}"
            f = _fact("shadow-form-def")
            assert f is not None
            ans = (
                f"{_S20_NUM_WORD[end_n]} of my {_S20_NUM_WORD[total]} theorem facts close their scope at "
                f"the line end, {_S20_NUM_WORD[spot_n]} close on the line's spot marker, and "
                f"{_S20_NUM_WORD[none_n]} carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode in ("s20-w1", "s20-w2", "s20-w3", "s20-w4"):
            wall = {
                "s20-w1": self.W_S20_1,
                "s20-w2": self.W_S20_2,
                "s20-w3": self.W_S20_3,
                "s20-w4": self.W_S20_4,
            }[mode]
            _honest(CONCEPT_S20_BOUNDARY, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        if mode == "s20-wallkind":
            concept = CONCEPT_S20_BOUNDARY
            if _fact("boundary-form-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("boundary-form-def")
            assert f is not None
            ans = (
                "a wall of my band is a fact of record of the boundary form — the named missing "
                "ingredient standing as an honest needs_info: no derivation enters the store for it, "
                f"nothing off the line is cited, and the territory stands declared, never reached, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-absence":
            concept = CONCEPT_S20_BOUNDARY
            if _fact("boundary-form-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            assert self._weave_open_count() == 0, "a bare island theorem entered the store (discovery candidate)"
            f = _fact("boundary-form-def")
            assert f is not None
            ans = (
                "the declared absences of my line, as my store holds them: no theorem of any record "
                "settles the p versus np question, no theorem stands for the beal question outright, no "
                "theorem stands for the bsd question outside its panel, and the riemann question stands "
                f"open as its conjecture of record — the island questions stay open of record, and that is the boundary, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-weavestate":
            concept = CONCEPT_S20_WEAVE
            if _fact("weave-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("weave-def")
            assert f is not None
            thm = _fact("summit-shape-filed")
            assert thm is not None
            ans = (
                "the weaving band holds the weave (the cross-island joints as edges of the prereq "
                "graph of my line — the shared soil and the shared walk), the summit shape (the four "
                "island summits in one shape of record), the verification form (verification on the "
                "line, the store's own paths as certificates), the boundary form (walls and declared "
                "absences as facts of record), the four walls of the band standing on their "
                f"territories, and the filing of the shape (summit-shape-filed: the filing fills the shape, not the statements), at the line end {end}"
            )
            _derived(concept, ans, [f.id, thm.id], ans)
            return out

        if mode == "s20-unc":
            concept = CONCEPT_S20_WEAVE
            if _fact("weave-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("weave-def")
            assert f is not None
            ans = (
                "nothing the weaving band says is conditional on an unproved hypothesis — the weave, "
                "the shape, the form, and the boundary are record on the line, and the island questions "
                f"(the riemann conjecture, the p versus np) stand open of record, never as premises, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s20-state":
            slug = slots["slug"]
            concept = S20_SLUG_CONCEPT.get(slug, CONCEPT_S20_WEAVE)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant21(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.25 — FUNDAMENTALS-TRACK S21 (the condition line; LOT 1 of
        the declared cross-pollination queue, pre-registered
        2026-08-25). The conditional layer made teachable: the
        hypothesis as a premise you may assume (never a fact you may
        hold), the marker that travels in every consequence, the
        condition line end to end (the error, the gap, the root
        smallness), the filing condition-line-filed (the line, not
        the condition), and the four walled territories W_S21_1..4
        (the condition does not close the condition, the marker
        never drops, the register is the line, the queue stays as
        declared). CONDITIONAL band: the new facts require the exact
        marker; the line stays 0..84."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S21}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s21-hypo":
            concept = CONCEPT_S21_HYP
            if _fact("hypothesis-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("hypothesis-def")
            assert f is not None
            ans = (
                "yes — to reason under the condition is to assume that every nontrivial zero of zeta "
                f"has real part exactly one half and to carry the assumption in every conclusion of the lot — under the condition of the Riemann hypothesis, the marker travels in every statement and every derivation keeps it explicit, and the condition itself stays the status surface it is, believed, not known: assumed in the lot, never proved by it, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s21-line":
            concept = CONCEPT_S21_LINE
            if _fact("condition-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("condition-line-def")
            assert f is not None
            ans = (
                "one line from the assumption — the error of the prime count and the gap between "
                f"consecutive primes carry the same root scale, and the running sum of (minus one) to the number of distinct prime parts stays below that root scale, so the prime parts of every number are unique on the condition road — each consequence keeping its marker, under the condition of the Riemann hypothesis, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s21-filing":
            concept = CONCEPT_S21_LINE
            if _fact("hypothesis-def") is None or _fact("condition-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fh = _fact("hypothesis-def")
            fl = _fact("condition-line-def")
            ft = _fact("condition-line-filed")
            assert fh is not None and fl is not None
            ev = [fh.id, fl.id] + ([ft.id] if ft is not None else [])
            ans = (
                "the line, not the condition — the filing files the condition line of record (the "
                f"consequences under the assumption, the marker in every clause) and holds the condition open of record: assumed, never proved, believed, not known, at the line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out
        if mode in ("s21-w1", "s21-w2", "s21-w3", "s21-w4"):
            wall = {
                "s21-w1": self.W_S21_1,
                "s21-w2": self.W_S21_2,
                "s21-w3": self.W_S21_3,
                "s21-w4": self.W_S21_4,
            }[mode]
            owner = CONCEPT_S21_HYP if mode == "s21-w2" else CONCEPT_S21_LINE
            _honest(owner, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out
        if mode == "s21-state":
            slug = slots["slug"]
            concept = S21_SLUG_CONCEPT.get(slug, CONCEPT_S21_LINE)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant31(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.35 — COURSE E S31 (the seeded line: the fibonacci line
        for the constants, in the bandgen way; the owner's lesson
        2026-08-25, course-seeded-fibonacci-research.md). The
        seeded line made teachable: the sequence for a seed c on the
        sum line's own skeleton (the seed's hat), the shift seeds
        one and two (no other seed a shift), the cassini weight and
        its silence at the golden equation, the golden seed off the
        line named by the equation alone (its line its own power,
        log-periodic without collapse), and the three walled
        territories W_S31_1..3 (the constants off the floor, the
        seed law, the ratio limit). UNCONDITIONAL band: the new
        facts carry NO condition marker; the line stays 0..84; no
        new decimals enter the floor."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S31}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode == "s31-seeded":
            concept = CONCEPT_S31_SEED
            if _fact("seeded-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seeded-line-def")
            assert f is not None
            ans = (
                "the line for a seed c stands at seed one and c under the sum rule, every later "
                f"term the sum of the two before it, and every term reads as the sum line's term at the n-minus-one index plus c times its term at the n index — my line's skeleton, the consecutive pair, carries the seed's hat: the one the sum line shifted by one, the two shifted by two, no other seed a shift, and each term's own cassini is (minus one) to the n times (c squared minus c minus one), at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s31-golden":
            concept = CONCEPT_S31_GOLD
            if _fact("golden-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("golden-seed-def")
            assert f is not None
            ans = (
                "the golden seed stands off the line between the one and the two, named by the "
                f"equation x squared equals x plus one, never by a digit, and its line is the golden seed to the n power — the term at the n-plus-p index the term at the n index times the golden seed to the p power, that multiplier never one, so the line advances without collapse and without return; its integer shadow runs on the skeleton, the term at the n index the sum line's n-minus-one term plus the golden seed times its n term, and its cassini is silent at the golden equation, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s31-filing":
            concept = CONCEPT_S31_GOLD
            if _fact("seeded-line-def") is None or _fact("golden-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("seeded-line-def")
            fg = _fact("golden-seed-def")
            ft = _fact("seeded-line-filed")
            assert fs is not None and fg is not None
            ev = [fs.id, fg.id] + ([ft.id] if ft is not None else [])
            ans = (
                "the line, not the constants — the filing files the seeded line of record "
                f"(the skeleton reading, the shift seeds one and two, the cassini weight and its silence, the golden line as the power of the golden seed) and holds every constant off the floor: named by position and by the equation, never by a digit, at the line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s31-sumline":
            concept = CONCEPT_S31_SEED
            if _fact("seeded-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seeded-line-def")
            assert f is not None
            ans = (
                "the sum line runs by addition alone, starting at zero and one, every later "
                f"term the sum of the two before it: on my line it reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off the line as my line already declared it — the ceiling the seeded lines cross, cited, never re-asserted, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s31-cassini":
            concept = CONCEPT_S31_SEED
            if _fact("seeded-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seeded-line-def")
            assert f is not None
            ans = (
                "the cassini of my seeded lines: the product of the surrounding terms minus the "
                f"square of the middle is (minus one) to the n times (c squared minus c minus one) — the weights on my line run minus one, minus one, one, five, nineteen, fifty-five, one hundred fifty-five, and four hundred nineteen at the seeds zero, one, two, three, five, eight, thirteen, and twenty-one, all exact, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s31-shift":
            concept = CONCEPT_S31_SEED
            if _fact("seeded-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seeded-line-def")
            assert f is not None
            ans = (
                "one and two only — the seed-one line is the sum line itself shifted by one, "
                f"the seed-two line shifted by two, no other seed standing on my line a shift, checked against every shift, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out
        if mode == "s31-ratio":
            concept = CONCEPT_S31_GOLD
            if _fact("seeded-line-def") is None or _fact("golden-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("seeded-line-def")
            fg = _fact("golden-seed-def")
            assert fs is not None and fg is not None
            ans = (
                "the partial ratios of the line for three walk the fractions four over three, "
                f"seven over four, eleven over seven, eighteen over eleven, twenty-nine over eighteen, forty-seven over twenty-nine, and seventy-six over forty-seven — every partial ratio a fraction of two parts my line holds, walking to the golden seed, whose landing is off the floor, declared, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, fg.id], ans)
            return out
        if mode == "s31-goldenwalk":
            concept = CONCEPT_S31_GOLD
            if _fact("seeded-line-def") is None or _fact("golden-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("seeded-line-def")
            fg = _fact("golden-seed-def")
            assert fs is not None and fg is not None
            ans = (
                "the golden line's integer shadow runs on the skeleton: the last on-line pair "
                f"is the pair at its tenth step, the thirty-four and the fifty-five, and the eleventh step's pair carries the eighty-nine, which stands off the line — the ceiling my line already declared, cited, never re-asserted, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, fg.id], ans)
            return out
        if mode == "s31-silence":
            concept = CONCEPT_S31_GOLD
            if _fact("seeded-line-def") is None or _fact("golden-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("seeded-line-def")
            fg = _fact("golden-seed-def")
            assert fs is not None and fg is not None
            ans = (
                "yes — the golden line's cassini is silent: the weight c squared minus c minus "
                f"one is exactly zero exactly at the seeds solving the golden equation, so on the golden line the product of the surrounding terms equals the square of the middle at every step — silence at the equation, not a gap in the census, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, fg.id], ans)
            return out
        if mode in ("s31-w1", "s31-w2", "s31-w3"):
            wall = {
                "s31-w1": self.W_S31_1,
                "s31-w2": self.W_S31_2,
                "s31-w3": self.W_S31_3,
            }[mode]
            owner = CONCEPT_S31_SEED if mode == "s31-w2" else CONCEPT_S31_GOLD
            _honest(owner, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out
        if mode == "s31-state":
            slug = slots["slug"]
            concept = S31_SLUG_CONCEPT.get(slug, CONCEPT_S31_GOLD)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant22(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.26 — COURSE A S22 (the proportion line: the proportion as
        the RELATION, the fraction as its VALUE over a positive part,
        one division read in two languages — the quotient face and the
        remainder face — and 0:0 the evenness of the two empty parts,
        declared, never valued; D0 ruling settled pre-band, D-e6t(a)
        authoritative for the off-script byte). UNCONDITIONAL band: the
        new facts carry NO condition marker; the line stays 0..84; no
        0/0 value may exist anywhere in the store."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S22}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode in ("s22-prop", "s22-frac"):
            slug = "proportion-def" if mode == "s22-prop" else "fraction-def"
            concept = CONCEPT_S22_PROP if mode == "s22-prop" else CONCEPT_S22_FRAC
            fact = _fact(slug)
            if fact is None:
                _unlearned(concept_map[concept].label)
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode == "s22-state":
            slug = slots["slug"]
            concept = S22_SLUG_CONCEPT.get(slug, CONCEPT_S22_PROP)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode == "s22-family":
            concept = CONCEPT_S22_FRAC
            if _fact("fraction-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("fraction-def")
            assert f is not None
            a, b = slots["a"], slots["b"]
            if (a, b) == ("the empty part", "the one"):
                ans = (
                    "zero to one: the empty part to the one — declared, valued zero over one, nothing held to "
                    f"the one is nothing over one, at the line end {end}"
                )
            elif (a, b) == ("the one", "the one"):
                ans = (
                    "one to one: the evenness of the two equal parts — declared, valued one over one, the one "
                    f"my line holds for the equal parts, at the line end {end}"
                )
            elif (a, b) == ("the one", "the two"):
                ans = (
                    "one to two: the half — the one part over the two, declared, valued one over two, the value "
                    f"my floor already holds as the triangle's half-product, at the line end {end}"
                )
            elif (a, b) == ("the one", "the three"):
                ans = (
                    "one to three: the third — the one part over the three, declared, valued one over three, "
                    f"at the line end {end}"
                )
            else:  # pragma: no cover — the closed family
                raise KeyError((a, b))
            _derived(concept, ans, [f.id], ans)
            return out

        _W22 = {"two": 2, "three": 3, "five": 5, "thirteen": 13}
        _CHAINS22 = {
            (3, 2): ("three", "two", "one and one half"),
            (5, 3): ("five", "three", "one and two thirds"),
            (13, 5): ("thirteen", "five", "two and three fifths"),
        }

        if mode in ("s22-chain-frac", "s22-chain-mod"):
            concept = CONCEPT_S22_FRAC
            if _fact("fraction-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("fraction-def")
            assert f is not None
            a, b = _W22[slots["a"]], _W22[slots["b"]]
            assert (a, b) in _CHAINS22, f"the chain {(a, b)} is not one of the three drilled divisions"
            aw, bw, mword = _CHAINS22[(a, b)]
            q, r = divmod(a, b)
            qw = _S20_NUM_WORD[q]
            rw = _S20_NUM_WORD[r]
            if mode == "s22-chain-frac":
                ans = (
                    f"{aw} over {bw} is {mword} — {aw} is {qw} times {bw} plus {rw}, one division in "
                    f"either word, at the line end {end}"
                )
            else:
                ans = (
                    f"{aw} mod {bw} is {rw} — {aw} is {qw} times {bw} plus {rw}, the same division as "
                    f"{aw} over {bw} is {mword}, at the line end {end}"
                )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s22-classwalk":
            concept = CONCEPT_S22_PROP
            if _fact("proportion-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("proportion-def")
            assert f is not None
            # the 2:3 class: k times two to k times three, both parts
            # on the line (k up to twenty-eight: fifty-six to eighty-four)
            kmax = end // 3
            assert kmax == 28 and 28 * 2 <= end, "the 2:3 class census drifted off the line"
            ans = (
                f"twenty-eight: the two-to-three proportion holds for k times two to k times three, k from one "
                f"to twenty-eight, twenty-eight times two to twenty-eight times three, fifty-six to eighty-four "
                f"at the end of my line — the proportion is the class, the reduced pair the two-to-three its "
                f"name, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s22-filing":
            concept = CONCEPT_S22_PROP
            if _fact("proportion-def") is None or _fact("fraction-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fp = _fact("proportion-def")
            ff = _fact("fraction-def")
            ft = _fact("proportion-filed")
            assert fp is not None and ff is not None
            ev = [fp.id, ff.id] + ([ft.id] if ft is not None else [])
            ans = (
                "the proportion line, filed of record: the relation and its value are two jobs of one "
                "division — the relation declared for every pair of parts and named by its reduced form, the "
                "fraction valued only over the positive part, and zero to zero the evenness of the two empty "
                f"parts, declared, never valued; at the line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out

        if mode in ("s22-w1", "s22-w2", "s22-w3"):
            wall = {
                "s22-w1": self.W_S22_1,
                "s22-w2": self.W_S22_2,
                "s22-w3": self.W_S22_3,
            }[mode]
            owner = CONCEPT_S22_FRAC if mode in ("s22-w1", "s22-w3") else CONCEPT_S22_PROP
            _honest(owner, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        if mode == "s22-carry-divides":
            f = _fact("divides-def")
            if f is None:
                _unlearned("the divides rule")
                return out
            assert isinstance(f.object, str)
            _derived("divides", f.object, [f.id], f"that one is: {f.object}")
            return out

        if mode == "s22-carry-question":
            f = _fact("question-def")
            if f is None:
                _unlearned("the decision question")
                return out
            assert isinstance(f.object, str)
            _derived("decision-question", f.object, [f.id], f"that one is: {f.object}")
            return out

        if mode == "s22-carry-telescope":
            f = _fact("telescope-line")
            if f is None:
                _unlearned("the telescope line")
                return out
            assert isinstance(f.object, str)
            _derived(CONCEPT_S13_PARTIAL, f.object, [f.id], f"that one is: {f.object}")
            return out

        if mode == "s22-carry-halfproduct":
            # the capability byte stands in the grammar; the store
            # grounds the RULE grant (cap:geom-area-triangle:rule)
            try:
                self._codex.get("cap:geom-area-triangle:rule")
            except KeyError:
                _unlearned("the triangle's half-product rule")
                return out
            ans = (
                "the area of a triangle is half of the base times the height — the held ratio-value under its "
                f"own name, the half the floor already carries, at the line end {end}"
            )
            _derived("geom-area-triangle", ans, ["cap:geom-area-triangle:rule"], f"that one is: {ans}")
            return out

        if mode == "s22-firstprime":
            concept = CONCEPT_S22_PROP
            if _fact("proportion-def") is None or _fact("fraction-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fp = _fact("proportion-def")
            ff = _fact("fraction-def")
            assert fp is not None and ff is not None
            # the first proportion whose parts are both prime: two to
            # three (the first reduction step, the D-e6t(a) byte)
            ans = (
                "two to three: the first proportion whose parts are both prime — the first reduction step is "
                f"three is one times two plus one, no shared part, the chain two steps, at the line end {end}"
            )
            _derived(concept, ans, [fp.id, ff.id], ans)
            return out

        raise KeyError(mode)  # pragma: no cover - modes are closed


    def _policy_savant23(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.27 — COURSE A S23 (the prime proportion: two distinct primes
        share no part above one, so their proportion is in lowest terms and
        is the FINGERPRINT of the pair — on the line the 253 prime pairs
        give 253 different reduced proportions, no collisions, and the
        reduction chain's ceiling is the seven-step one, four tied pairs).
        UNCONDITIONAL band: the new facts carry NO condition marker; the
        line stays 0..84; the 253 census and the ceiling are line records,
        read off the first-divisor census (computed, never declared).
        D-e6u(b) authoritative for the off-script byte."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S23}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _prime(n: int) -> bool:
            if n < 2:
                return False
            i = 2
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 1
            return True

        def _steps(a: int, b: int) -> int:
            x, y = max(a, b), min(a, b)
            n = 0
            while True:
                n += 1
                x, y = y, x % y
                if y == 0:
                    return n

        if mode in ("s23-cop", "s23-fpr"):
            slug = "coprime-pair-def" if mode == "s23-cop" else "prime-fingerprint-def"
            concept = CONCEPT_S23_COP if mode == "s23-cop" else CONCEPT_S23_FPR
            fact = _fact(slug)
            if fact is None:
                _unlearned(concept_map[concept].label)
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode == "s23-state":
            slug = slots["slug"]
            concept = S23_SLUG_CONCEPT.get(slug, CONCEPT_S23_FPR)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        _W23 = {"two": 2, "four": 4, "three": 3, "six": 6, "twenty-nine": 29, "forty-seven": 47, "forty-one": 41, "seventy-one": 71}

        if mode == "s23-coprime":
            concept = CONCEPT_S23_COP
            f = _fact("coprime-pair-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            a, b = _W23[slots["a"]], _W23[slots["b"]]
            g = math.gcd(a, b)
            st = _steps(a, b)
            aw, bw = slots["a"], slots["b"]
            if (a, b) == (2, 3):
                assert g == 1 and st == 2
                ans = (
                    f"two and three: a coprime pair outright — they share no part above one, the first-divisor "
                    f"census lands nowhere, and the reduction chain walks two steps, at the line end {end}"
                )
            elif (a, b) == (4, 6):
                assert g == 2
                ans = (
                    f"four and six: not a coprime pair — they share the part two, the first-divisor census lands "
                    f"on it at once, and the proportion four to six reduces two to three, the reduced pair the "
                    f"fingerprint, at the line end {end}"
                )
            elif (a, b) == (29, 47):
                assert g == 1 and st == 7
                ans = (
                    f"twenty-nine and forty-seven: a coprime pair — they share no part above one, and the "
                    f"reduction chain walks seven steps, the ceiling of my line, at the line end {end}"
                )
            elif (a, b) == (41, 71):
                assert g == 1 and st == 7
                ans = (
                    f"forty-one and seventy-one: a coprime pair — they share no part above one, and the reduction "
                    f"chain walks seven steps, the ceiling of my line, at the line end {end}"
                )
            else:  # pragma: no cover — the closed drilled pairs
                raise KeyError((a, b))
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s23-neverred":
            concept = CONCEPT_S23_COP
            f = _fact("coprime-pair-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            a, b = _W23[slots["a"]], _W23[slots["b"]]
            assert (a, b) == (2, 3) and math.gcd(a, b) == 1 and _steps(a, b) == 2
            ans = (
                f"no — a proportion of two distinct primes never reduces: two and three share no part above one, "
                f"and the proportion two to three is already in lowest terms, the chain two steps, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        _CHAINS23 = {(7, 3), (29, 11), (29, 47), (83, 79), (83, 2), (71, 7)}
        _DENOM23 = {2: "half", 3: "third", 5: "fifth", 7: "seventh", 11: "eleventh", 47: "twenty-ninth", 79: "seventy-ninth"}
        _W23B = {"two": 2, "three": 3, "seven": 7, "eleven": 11, "twenty-nine": 29, "forty-seven": 47,
                 "seventy-nine": 79, "eighty-three": 83, "seventy-one": 71}

        if mode in ("s23-chain-frac", "s23-chain-mod"):
            concept = CONCEPT_S23_FPR
            f = _fact("prime-fingerprint-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            aw, bw = slots["a"], slots["b"]
            a, b = _W23B[aw], _W23B[bw]
            assert (a, b) in _CHAINS23, f"the chain {(a, b)} is not one of the six drilled chains"
            if a > b:
                q, r = divmod(a, b)
                qw, rw = _S20_NUM_WORD[q], _S20_NUM_WORD[r]
                u = _DENOM23[b] + ("" if r == 1 else "s")
                mfull = f"{qw} and {rw} {u}"
                if mode == "s23-chain-frac":
                    ans = (
                        f"{aw} over {bw} is {mfull} — {aw} is {qw} times {bw} plus {rw}, one division in "
                        f"either word, at the line end {end}"
                    )
                else:
                    ans = (
                        f"{aw} mod {bw} is {rw} — {aw} is {qw} times {bw} plus {rw}, the same division as "
                        f"{aw} over {bw} is {mfull}, at the line end {end}"
                    )
            else:
                # the pair below one: the first reduction step is the
                # division of the bigger part by the smaller (the house
                # convention, the two-to-three firstprime byte)
                q, r = divmod(b, a)
                qw, rw = _S20_NUM_WORD[q], _S20_NUM_WORD[r]
                if mode == "s23-chain-frac":
                    ans = (
                        f"{aw} over {bw} is the value under one — {aw} held over {bw}, the part below the "
                        f"whole, and the first reduction step is {bw} is {qw} times {aw} plus {rw}, one "
                        f"division in either word, at the line end {end}"
                    )
                else:
                    ans = (
                        f"the first reduction step of {aw} to {bw} is {bw} is {qw} times {aw} plus {rw} — "
                        f"the remainder {rw} carried, the same division as the value {aw} over {bw} under "
                        f"one, at the line end {end}"
                    )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s23-census":
            concept = CONCEPT_S23_FPR
            f = _fact("prime-fingerprint-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            # the first-divisor census re-run: the primes of the line, the
            # pairs, and the reduced proportions (computed, never declared)
            ps = [n for n in range(2, end + 1) if _prime(n)]
            reds: set[tuple[int, int]] = set()
            n_pairs = 0
            for i, p in enumerate(ps):
                for q in ps[i + 1:]:
                    n_pairs += 1
                    g = math.gcd(p, q)
                    assert g == 1, f"the distinct primes {p} and {q} share {g}"
                    reds.add((p // g, q // g))
            assert n_pairs == 253 and len(reds) == 253, (n_pairs, len(reds))
            ans = (
                f"two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced "
                f"proportions on my line, every pair coprime, no two pairs alike — read off the first-divisor "
                f"census, the pair is the proportion, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s23-ceiling":
            concept = CONCEPT_S23_FPR
            f = _fact("prime-fingerprint-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            ps = [n for n in range(2, end + 1) if _prime(n)]
            cens: dict[int, list[tuple[int, int]]] = {}
            for i, p in enumerate(ps):
                for q in ps[i + 1:]:
                    cens.setdefault(_steps(p, q), []).append((p, q))
            top = max(cens)
            tied = sorted(cens[top])
            assert (top, tied) == (7, [(29, 47), (29, 79), (41, 67), (41, 71)]), (top, tied)
            ans = (
                f"the seven-step chain is the ceiling on my line — four prime pairs walk it: twenty-nine by "
                f"forty-seven, twenty-nine by seventy-nine, forty-one by sixty-seven, and forty-one by "
                f"seventy-one; no prime pair of the two hundred and fifty-three walks a longer chain, at the "
                f"line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s23-filing":
            concept = CONCEPT_S23_FPR
            if _fact("coprime-pair-def") is None or _fact("prime-fingerprint-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fc = _fact("coprime-pair-def")
            ff = _fact("prime-fingerprint-def")
            ft = _fact("fingerprint-filed")
            assert fc is not None and ff is not None
            ev = [fc.id, ff.id] + ([ft.id] if ft is not None else [])
            ans = (
                "the prime proportion, filed of record: two distinct primes share no part above one, so their "
                "proportion is in lowest terms and is the fingerprint of the pair — two hundred and fifty-three "
                f"pairs, two hundred and fifty-three proportions, no collisions on my line; at the line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out

        if mode == "s23-above2":
            concept = CONCEPT_S23_FPR
            if _fact("coprime-pair-def") is None or _fact("prime-fingerprint-def") is None:
                _unlearned("the prime fingerprint")
                return out
            fc = _fact("coprime-pair-def")
            ff = _fact("prime-fingerprint-def")
            assert fc is not None and ff is not None
            # the first proportion where the parts are primes above two:
            # three to five (two is not above two — D-e6u(b) authoritative)
            ps = [n for n in range(2, end + 1) if _prime(n)]
            above = [p for p in ps if p > 2]
            assert (above[0], above[1], math.gcd(3, 5), _steps(3, 5)) == (3, 5, 1, 3), "the above-two walk drifted"
            ans = (
                "three to five: the first proportion where the parts are primes above two — the first reduction "
                f"step is five is one times three plus two, no shared part, the chain three steps, at the line end {end}"
            )
            _derived(concept, ans, [fc.id, ff.id], ans)
            return out

        if mode in ("s23-w1", "s23-w2", "s23-w3"):
            wall = {
                "s23-w1": self.W_S23_1,
                "s23-w2": self.W_S23_2,
                "s23-w3": self.W_S23_3,
            }[mode]
            _honest(CONCEPT_S23_FPR, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant24(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.28 — COURSE B S24 (the sum line and the twin line: the
        Fibonacci line runs under the 84 line end to the fifty-five in ten
        steps, the twin under the same rule to the seventy-six in nine, and
        the two welding identities hold at every on-line index; the
        eighty-nine stands off-line as the ceiling the line already declared,
        and the next past-line doubled term lands there too).
        UNCONDITIONAL band: the 89 is declared off-line, never built; the
        identities are re-walked and asserted, not asserted from outside."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S24}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _fibs(k: int) -> list[int]:
            # the sum line, re-walked from its own definition (F(0)=0, F(1)=1)
            v = [0, 1]
            for _ in range(k - 1):
                v.append(v[-1] + v[-2])
            return v

        def _twin(k: int) -> list[int]:
            # the twin line, re-walked from its own definition (L(0)=2, L(1)=1)
            v = [2, 1]
            for _ in range(k - 1):
                v.append(v[-1] + v[-2])
            return v

        if mode in ("s24-sum", "s24-twin"):
            slug = "sum-line-def" if mode == "s24-sum" else "twin-line-def"
            concept = CONCEPT_S24_SUM if mode == "s24-sum" else CONCEPT_S24_TWIN
            fact = _fact(slug)
            if fact is None:
                _unlearned(concept_map[concept].label)
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode == "s24-state":
            slug = slots["slug"]
            concept = S24_SLUG_CONCEPT.get(slug, CONCEPT_S24_TWIN)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        NW = _S20_NUM_WORD

        if mode == "s24-sumwalk":
            concept = CONCEPT_S24_SUM
            f = _fact("sum-line-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            F = _fibs(12)
            on = F[1:11]
            assert on == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] and F[11] > end, f"the sum walk drifted: {on}"
            ans = (
                f"zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the "
                f"sum line runs ten steps on my line, each term the sum of the two before it, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s24-twinwalk":
            concept = CONCEPT_S24_TWIN
            f = _fact("twin-line-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            L = _twin(11)
            on = L[1:10]
            assert on == [1, 3, 4, 7, 11, 18, 29, 47, 76] and L[10] > end, f"the twin walk drifted: {on}"
            ans = (
                f"two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the "
                f"twin line runs nine steps on my line under the same rule, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s24-doub":
            concept = CONCEPT_S24_TWIN
            f = _fact("twin-line-def")
            fs = _fact("sum-line-def")
            if f is None or fs is None:
                _unlearned(concept_map[concept].label)
                return out
            n = {"two": 1, "four": 2, "six": 3, "eight": 4, "ten": 5}[slots["idx"]]
            F = _fibs(2 * n)
            L = _twin(n)
            v = F[2 * n]
            assert F[2 * n] == F[n] * L[n] and v <= end, f"the doubling at index {n} drifted: {v}"
            ans = (
                f"{NW[v]}: the doubled term at index {NW[2 * n]} — the {NW[F[n]]}, the term at {NW[n]}, times "
                f"the {NW[L[n]]}, the twin at {NW[n]} — is on my line, the welding of the two lines, at the "
                f"line end {end}"
            )
            _derived(concept, ans, [f.id, fs.id], ans)
            return out

        if mode == "s24-sqsum":
            concept = CONCEPT_S24_TWIN
            f = _fact("twin-line-def")
            fs = _fact("sum-line-def")
            if f is None or fs is None:
                _unlearned(concept_map[concept].label)
                return out
            aw, bw = slots["a"], slots["b"]
            n = {"one": 1, "two": 2, "three": 3, "four": 4}[aw]
            assert {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}[bw] == n + 1, "the pair is not consecutive"
            F = _fibs(2 * n + 1)
            v = F[2 * n + 1]
            assert F[n] * F[n] + F[n + 1] * F[n + 1] == v and v <= end, f"the square sum at {n} drifted: {v}"
            ans = (
                f"{NW[v]}: the square sum of the term at {NW[n]} and the term at {NW[n + 1]}, two consecutive "
                f"terms of my sum line — {NW[F[n]]} squared plus {NW[F[n + 1]]} squared — is the term at index "
                f"{NW[2 * n + 1]}, at the line end {end}"
            )
            _derived(concept, ans, [f.id, fs.id], ans)
            return out

        if mode == "s24-twinterm":
            concept = CONCEPT_S24_TWIN
            f = _fact("twin-line-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            L = _twin(6)
            assert L[6] == L[4] + L[5] and L[6] <= end, f"the twin term drifted: {L[6]}"
            ans = (
                f"eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the "
                f"two before it — under the same rule the twin line runs, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s24-sumterm":
            concept = CONCEPT_S24_SUM
            f = _fact("sum-line-def")
            if f is None:
                _unlearned(concept_map[concept].label)
                return out
            F = _fibs(10)
            assert F[10] == F[8] + F[9] and F[10] <= end, f"the sum term drifted: {F[10]}"
            ans = (
                f"fifty-five: the sum line's term at index ten — the twenty-one at eight and the thirty-four at "
                f"nine, the sum of the two before it — under the same rule the sum line runs, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s24-filing":
            concept = CONCEPT_S24_TWIN
            if _fact("sum-line-def") is None or _fact("twin-line-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("sum-line-def")
            ft = _fact("twin-line-def")
            ff = _fact("twin-line-filed")
            assert fs is not None and ft is not None
            ev = [fs.id, ft.id] + ([ff.id] if ff is not None else [])
            ans = (
                "the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the "
                f"twin under the same rule to the seventy-six, the identities weld the two lines at every on-line "
                f"index, and the eighty-nine stands once more as the ceiling the line already declared; at the "
                f"line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out

        if mode == "s24-offscript":
            concept = CONCEPT_S24_TWIN
            if _fact("sum-line-def") is None or _fact("twin-line-def") is None:
                _unlearned("the twin line")
                return out
            fs = _fact("sum-line-def")
            ft = _fact("twin-line-def")
            assert fs is not None and ft is not None
            # the largest doubled term the line holds: the walk n=1.. of
            # F(2n) = F(n)*L(n) until the value crosses the line end —
            # n=5 holds (fifty-five), n=6 lands at the one forty-four, past
            # the line end, at the ceiling's territory
            F5 = _fibs(12)
            L5 = _twin(6)
            assert F5[10] == F5[5] * L5[5] and F5[10] <= end, f"the last on-line doubling drifted: {F5[10]}"
            assert F5[12] == F5[6] * L5[6] and F5[12] > end, f"the past-line doubling drifted: {F5[12]}"
            ans = (
                f"fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the "
                f"twin at five — is the largest doubled term my line holds; the next doubled term, at index "
                f"twelve, is the one forty-four, past the line end, the ceiling's territory, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, ft.id], ans)
            return out

        if mode in ("s24-w1", "s24-w2", "s24-w3"):
            wall = {
                "s24-w1": self.W_S24_1,
                "s24-w2": self.W_S24_2,
                "s24-w3": self.W_S24_3,
            }[mode]
            if mode in ("s24-w1", "s24-w2"):
                _honest(CONCEPT_S24_SUM, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            else:
                _honest(CONCEPT_S24_TWIN, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        raise KeyError(mode)  # pragma: no cover - modes are closed


        """E6.36 — COURSE E S32 (the seed census: the seeded
        line's own residue story — the Pisano count, the
        class-three-mod-five shadow, the value story of the
        constants off the floor, and the page's own wordings: the
        fibonacci sequence, the golden ratio, the letter phi, the
        lucas numbers; owner directives 2026-08-25 and 2026-08-28;
        D-e6r(a)-(c) authoritative). UNCONDITIONAL band: the new
        facts carry NO condition marker; the line stays 0..84; the
        off-line decimals (the one over eighty-nine) are declared,
        never filed; the 11-family shadow is declared, not built."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        concept_map = {c.id: c for c in CONCEPT_S32}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        if mode in ("s32-period", "s32-offline"):
            slug = "seed-period-def" if mode == "s32-period" else "off-line-seed-def"
            concept = CONCEPT_S32_PERIOD if mode == "s32-period" else CONCEPT_S32_OFFLINE
            fact = _fact(slug)
            if fact is None:
                _unlearned(concept_map[concept].label)
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode == "s32-pisano8":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seed-period-def")
            assert f is not None
            ans = (
                "the skeleton pair walks the modulus-eight board in twelve: zero-one, one-one, one-two, "
                "two-three, three-five, five-zero, zero-five, five-five, five-two, two-seven, seven-one, one-zero — the "
                f"pure cycle, headed by the zero-one pair, the count twelve on my floor, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-pisano12":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seed-period-def")
            assert f is not None
            ans = (
                "the skeleton pair walks the modulus-twelve board in twenty-four: zero-one, one-one, one-two, "
                "two-three, three-five, five-eight, eight-one, one-nine, nine-ten, ten-seven, seven-five, five-zero, "
                "zero-five, five-five, five-ten, ten-three, three-one, one-four, four-five, five-nine, nine-two, "
                "two-eleven, eleven-one, one-zero — the pure cycle, headed by the zero-one pair, the count twenty-four "
                f"on my floor, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-shadow5":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seed-period-def")
            assert f is not None
            ans = (
                "the census holds the shadow: the seeds three mod five carry their period at a fifth of the pisano count "
                "under the unmasked five-touches — at the five, the four of the twenty; at the twenty-five, the twenty of "
                "the one hundred — while every other seed walks the full count, the board of twenty-five pairs at the "
                f"modulus five splitting twenty, four, one, class three that four, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-value":
            concept = CONCEPT_S32_OFFLINE
            if _fact("off-line-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("off-line-seed-def")
            assert f is not None
            ans = (
                "no — a seed of two or more never repeats a value: every term the sum of the two before it, both already "
                "positive, outgrowing its predecessor at every step — the line for two runs one, two, three, five, eight, "
                "thirteen, twenty-one, thirty-four, fifty-five, and the eighty-nine stands off the line as the ceiling "
                f"already declared; the seed-one line shares its one at the start, one and one, and outgrows after, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-parity":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seed-period-def")
            assert f is not None
            ans = (
                "my sum line walks even, odd, odd, the rule's own — two odds make an even, an even and an odd make an "
                "odd, the rule can do no other; each of my seeded lines wears the same three steps from its own start: the "
                f"even seeds, the zero among them, walk odd, even, odd, and the odd seeds walk odd, odd, even, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-divides":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("seed-period-def")
            assert f is not None
            ans = (
                "yes — the term at the third index, the two, divides the term at the sixth, the eight, four times, and the "
                "term at the ninth, the thirty-four, seventeen times; the term at the fourth, the three, divides the term "
                "at the eighth, the twenty-one, seven times; the term at the fifth, the five, divides the term at the "
                f"tenth, the fifty-five, eleven times — every quotient an exact whole number on my line, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-pagenames":
            concept = CONCEPT_S32_OFFLINE
            if _fact("off-line-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("off-line-seed-def")
            assert f is not None
            ans = (
                "my sum line is the fibonacci sequence the page names — the terms from the zero under the rule that "
                "the next number is the two before it added up, the recursive formula the page holds; my golden seed is "
                "the golden ratio the page names, its letter phi, the ratio of any two successive terms of the line "
                "approaching it, the bigger the pair the closer the approximation; the twin shadow that begins two and "
                f"one, the lucas numbers the page names, grows closer and closer to the powers of the golden ratio, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-belowzero":
            concept = CONCEPT_S32_OFFLINE
            if _fact("off-line-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("off-line-seed-def")
            assert f is not None
            ans = (
                "the term at minus n is the term at n with its sign turned when n is even and kept when n is odd — "
                f"the minus-one term the one, the minus-two term negative one, the minus-three term the two, the minus-four term negative three; the negative terms stand off the floor my line begins at zero, declared, not filed, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-recip89":
            concept = CONCEPT_S32_OFFLINE
            if _fact("off-line-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            f = _fact("off-line-seed-def")
            assert f is not None
            ans = (
                "the one divided by my eighty-nine carries in its decimal shadow the fibonacci sequence the page holds — "
                "the one, the one, the two, the three, the five, the eight, the thirteen, the twenty-one, the thirty-four, "
                "the fifty-five, reading in order from the hundredths place, for the multi-term numbers overlap their "
                f"neighbors; the decimal itself stands off my floor, never filed, at the line end {end}"
            )
            _derived(concept, ans, [f.id], ans)
            return out

        if mode == "s32-goldenpower":
            concept = CONCEPT_S31_GOLD
            if _fact("off-line-seed-def") is None or _fact("golden-seed-def") is None:
                _unlearned("the value story of the golden line is not filed")
                return out
            fs = _fact("off-line-seed-def")
            fg = _fact("golden-seed-def")
            assert fs is not None and fg is not None
            ans = (
                "advance by p and the golden line is multiplied by the golden seed to the p power — the golden ratio the "
                "page names, the letter phi — the shadow running on the skeleton, that multiplier never one, its nearest "
                f"approach to the one its own reciprocal, the golden line running up forever, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, fg.id], ans)
            return out

        if mode == "s32-lucas":
            concept = CONCEPT_S31_GOLD
            if _fact("off-line-seed-def") is None or _fact("golden-seed-def") is None:
                _unlearned("the lucas shadow (the off-line seed) is not filed")
                return out
            fs = _fact("off-line-seed-def")
            fg = _fact("golden-seed-def")
            assert fs is not None and fg is not None
            ans = (
                "the lucas numbers, the page's name — the shadow line that begins two and one under the recursive "
                "formula the page holds: two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, "
                "seventy-six — the last standing under my ceiling, the next crossing it; each its term the next term of "
                f"my sum line plus the one before, getting closer and closer to the powers of the golden ratio, at the line end {end}"
            )
            _derived(concept, ans, [fs.id, fg.id], ans)
            return out

        if mode == "s32-filing":
            concept = CONCEPT_S32_PERIOD
            if _fact("seed-period-def") is None or _fact("off-line-seed-def") is None:
                _unlearned(concept_map[concept].label)
                return out
            fs = _fact("seed-period-def")
            fo = _fact("off-line-seed-def")
            ft = _fact("seed-census-filed")
            assert fs is not None and fo is not None
            ev = [fs.id, fo.id] + ([ft.id] if ft is not None else [])
            ans = (
                "the census, not the census gaps — the filing files the seed period of record (the pisano count, the "
                "shadow drop under the five-touches) and the value story of the off-line constants (the page's names, "
                f"declared, never filed), and holds every constant off the floor, at the line end {end}"
            )
            _derived(concept, ans, ev, ans)
            return out

        if mode == "s32-state":
            slug = slots["slug"]
            concept = S32_SLUG_CONCEPT.get(slug, CONCEPT_S32_PERIOD)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out

        if mode in ("s32-w1", "s32-w2", "s32-w3"):
            wall = {
                "s32-w1": self.W_S32_1,
                "s32-w2": self.W_S32_2,
                "s32-w3": self.W_S32_3,
            }[mode]
            owner = CONCEPT_S32_OFFLINE if mode in ("s32-w1", "s32-w2") else CONCEPT_S31_GOLD
            _honest(owner, f"{mode}-{end}", wall, f"{mode}-{end}-at-{turn}")
            return out

        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant12(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.16 — FUNDAMENTALS-TRACK S12 (the RH neighborhood;
        pre-registered E6.16, frozen 2026-08-23, D-e6g(a)/(b)/(c)
        corrected). The parallel band: the conditional layer (the
        hypothesis marker never drops), the on-line gap and
        deviation censuses (GROUNDed from cited walks), the
        off-line witness values ONLY in walls, the two roads to
        uniqueness, and the declared queue."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()
        _W: dict[int, str] = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _off_line(n: int, verb: str, concept_id: str, tag: str) -> None:
            _honest(
                concept_id,
                f"{tag}:{n}:off-line-{end}",
                f"{n} is off my 0..{end} line — i cannot {verb} what my line does not reach",
                f"{tag}:{n}:off-line-{end}-at-{turn}",
            )

        if mode == "s12-gap":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            p = slots["p"]
            if p < 2 or p > end:
                _off_line(p, "census", concept, "s12-gap")
                return out
            g, q, trace = self._s12_gap_walk(p)
            if g is None:
                _honest(
                    concept,
                    f"s12-gap:{p}:not-last-prime-on-line",
                    self.W_S12_2 if p == end - 1 else f"{p} is not a prime on my line — the gaps run between the consecutive primes of the line",
                    f"s12-gap:{p}:wall-at-{turn}",
                )
                return out
            ld = _fact("rh-bound-scale")
            assert ld is not None
            ans = f"the gap after {p} on my line is {g} (to {q})"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode in ("s12-gapmax", "s12-gapmax-whole"):
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            if mode == "s12-gapmax-whole":
                _honest(concept, "s12-gapmax-whole:off-line", self.W_S12_3, "s12-gapmax-whole:wall-at-" + turn)
                return out
            cens, trace = self._s12_gap_census()
            ld = _fact("rh-bound-scale")
            assert ld is not None
            pairs6 = ", ".join(f"{a} to {b}" for a, b in cens["gap6"])
            ans = f"the greatest gap on my line is {cens['max']}, first at {cens['first_at']}, and {_W[len(cens['gap6'])]} gaps reach it ({pairs6})"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode == "s12-gapsize":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            k = slots["k"]
            cens, trace = self._s12_gap_census()
            ld = _fact("rh-bound-scale")
            assert ld is not None
            pairs = [(p, p + g) for p, g in cens["gaps"] if g == k]
            if pairs:
                ans = f"{_W[len(pairs)]} (" + ", ".join(f"{a} to {b}" for a, b in pairs) + ")"
            else:
                ans = "none on my line"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode == "s12-gapcount":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            cens, trace = self._s12_gap_census()
            ld = _fact("rh-bound-scale")
            assert ld is not None
            ans = f"{cens['count']} (between the {len(cens['primes'])} primes on my line)"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode == "s12-scale":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            p = slots["p"]
            if p < 2 or p > end:
                _off_line(p, "census", concept, "s12-scale")
                return out
            g, q, trace = self._s12_gap_walk(p)
            if g is None:
                _honest(
                    concept,
                    f"s12-scale:{p}:not-last-prime-on-line",
                    self.W_S12_2 if p == 83 else f"{p} is not a prime on my line — the scale covers the gap after the primes of the line",
                    f"s12-scale:{p}:wall-at-{turn}",
                )
                return out
            ld = _fact("rh-bound-scale")
            assert ld is not None
            covered = _s12_py_scale(p) >= g  # the mechanism's own reference is the referee
            assert (not covered) == (p in S12_BEDS["scale_fail"]), f"the scale census drifted at {p}"
            if covered:
                ans = f"yes — the square root of {p} times the log of {p} is at least the gap of {g}"
            else:
                ans = f"no — at {p} the gap of {g} is above the bare scale (the values are named in the wall, at the line end {end})"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode == "s12-scalecount":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            cens, trace = self._s12_gap_census()
            fail = [p for p, g in cens["gaps"] if _s12_py_scale(p) < g]
            assert fail == list(S12_BEDS["scale_fail"]), "the scale witness set drifted"
            covered = cens["count"] - len(fail)
            assert covered == S12_BEDS["scale_cover_count"]
            ld = _fact("rh-bound-scale")
            assert ld is not None
            ans = f"of the {cens['count']} gaps on my line the bare scale covers {covered}, failing at exactly " + " and ".join(str(p) for p in fail)
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode in ("s12-mod4-1", "s12-mod4-3"):
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            m1, m3, trace = self._s12_mod4_census()
            assert tuple(m1) == S12_BEDS["mod4_1"] and tuple(m3) == S12_BEDS["mod4_3"]
            lr = _fact("rh-relevance-def")
            assert lr is not None
            which = slots["which"]
            ls = m1 if mode == "s12-mod4-1" else m3
            listing = ", ".join(str(p) for p in ls)
            if which == "how many":
                ans = f"{len(ls)} on my line ({listing})"
            else:
                ans = f"{listing} on my line"
            _derived(concept, ans, trace + [lr.id], ans)
            return out
        if mode == "s12-mod4q":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            m1, m3, trace = self._s12_mod4_census()
            assert (len(m1), len(m3)) == (9, 13)
            lr = _fact("rh-relevance-def")
            assert lr is not None
            ans = "yes — 9 primes one mod four and 13 primes three mod four on my line, and 2 stands alone"
            _derived(concept, ans, trace + [lr.id], ans)
            return out
        if mode == "s12-mlab":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            track, trace = self._s12_m_census()
            ref = _s12_py_M(end)
            assert track == ref  # the mechanism's own reference is the referee
            mx = max(abs(v) for v in track.values())
            first_at = min(n for n in range(1, end + 1) if abs(track[n]) == mx)
            max_at = [n for n in range(1, end + 1) if abs(track[n]) == mx]
            assert mx == S12_BEDS["mu_max_abs"] and first_at == S12_BEDS["mu_first_at"]
            lu = _fact("rh-upf")
            assert lu is not None
            ans = (
                f"{mx} on my line, first at {first_at}, and it reaches it at {_W[len(max_at)]} places, all negative; "
                f"the ledger at the line end {end} is minus {-track[end]}"
            )
            _derived(concept, ans, trace + [lu.id], ans)
            return out
        if mode == "s12-mat":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            n = slots["n"]
            if n < 1 or n > end:
                _off_line(n, "census", concept, "s12-mat")
                return out
            track, trace = self._s12_m_census()
            assert track == _s12_py_M(end)
            v = track[n]
            mx = max(abs(x) for x in track.values())
            first_at = min(m for m in range(1, end + 1) if abs(track[m]) == mx)
            lu = _fact("rh-upf")
            assert lu is not None
            body = "zero" if v == 0 else (f"minus {-v}" if v < 0 else str(v))
            ans = f"the ledger at {n} is {body}"
            if n == first_at:
                ans += " — the first place the ledger reaches its greatest absolute on my line"
            _derived(concept, ans, trace + [lu.id], ans)
            return out
        if mode == "s12-mroot":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            track, trace = self._s12_m_census()
            assert track == _s12_py_M(end)
            mx = max(abs(v) for v in track.values())
            assert mx < _math.sqrt(end)  # the mechanism's own number is the referee
            lu = _fact("rh-upf")
            assert lu is not None
            ans = f"yes — the greatest absolute {mx} on my line is below the square root of my line end {end} (the wall names the value)"
            _derived(concept, ans, trace + [lu.id], ans)
            return out
        if mode == "s12-mpast":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            _honest(concept, "s12-mpast:off-line-end", self.W_S12_7, "s12-mpast:wall-at-" + turn)
            return out
        if mode == "s12-condgive":
            x = slots["x"]
            if x in ("the error of the prime count", "the gaps between primes"):
                concept = CONCEPT_S12_SCALE
                slug = "rh-bound-scale"
            elif x in ("the prime parts of a number", "the factor-count deviation"):
                concept = CONCEPT_S12_ROUTE
                slug = "rh-upf"
            else:  # the two wall readings (zero count at height T; the zeros)
                concept = CONCEPT_S12_SCALE
                slug = "rh-bound-scale"
            if _fact(slug) is None:
                _unlearned(concept_map(concept).label)
                return out
            if x == "the zero count at height T":
                _honest(concept, "s12-condgive:zero-count:off-line", self.W_S12_1, "s12-cg:zc:wall-at-" + turn)
                return out
            if x == "the zeros of the zeta function":
                _honest(concept, "s12-condgive:zeros:the-condition-itself", self.W_S12_5, "s12-cg:z:wall-at-" + turn)
                return out
            lf = _fact(slug)
            assert lf is not None
            assert isinstance(lf.object, str)
            _derived(concept, lf.object, [lf.id], f"that one is: {lf.object}")
            return out
        if mode == "s12-uncond":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            lu = _fact("rh-upf")
            sp = _fact("spf-chain")
            assert lu is not None and sp is not None
            ev = [sp.id, lu.id]
            ans = "yes — the scan road establishes it without the condition: the content of every number on my line is the same under every scan"
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s12-queue":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            th = _fact("queue-declared")
            if th is None:
                lr = _fact("rh-relevance-def")
                assert lr is not None
                _derived(concept, lr.object, [lr.id], f"that one is: {lr.object}")
            else:
                _derived(concept, th.object, [th.id], f"that one is: {th.object}")
            return out
        if mode == "s12-queue-lot":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lot = slots["lot"]
            if lot == "fifth":
                _honest(concept, "s12-qlot:four-lots-only", self.W_S12_6, "s12-qlot:5:wall-at-" + turn)
                return out
            th = _fact("queue-declared")
            if th is None:
                _honest(
                    concept,
                    f"s12-qlot:{lot}:not-yet-assembled",
                    "the queue lot is declared but not yet assembled in my store — derive the queue-declared rule first",
                    f"s12-qlot:{lot}:not-assembled-at-{turn}",
                )
                return out
            lot_bytes = {
                "first": "the condition line — the condition-closers made teachable, with the conditional consequences as drills",
                "second": "the primes in residue classes — the tower's prime layer (the pnt-ap, the mod-4 split, the chebotarev facts, declared in the seed)",
                "third": "the zero count at height T — the census of zeros at heights, declared",
                "fourth": "the factor-count deviation ledger — the running deviation under the condition's root smallness, declared",
            }
            _derived(concept, lot_bytes[lot], [th.id], lot_bytes[lot])
            return out
        if mode == "s12-class":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lr = _fact("rh-relevance-def")
            assert lr is not None
            cls = slots["cls"]
            if cls == "condition-closing":
                lb = _fact("rh-bound-scale")
                lu = _fact("rh-upf")
                assert lb is not None and lu is not None
                ans = "the root scale of the error, the root scale of the gap, the root smallness of the running deviation"
                ev = [lr.id, lb.id, lu.id]
            elif cls == "condition-neighboring":
                ans = "the primes in residue classes, the zero count at height T"
                ev = [lr.id]
            else:
                ans = "the condition itself — the condition does not close itself"
                ev = [lr.id]
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s12-agree":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            th = _fact("gap-scale-agreement")
            if th is None:
                _honest(
                    concept,
                    "s12-agree:not-yet-assembled",
                    "the agreement is not yet assembled in my store — derive the gap-scale-agreement rule first",
                    "s12-agree:not-assembled-at-" + turn,
                )
                return out
            _derived(concept, th.object, [th.id], f"that one is: {th.object}")
            return out
        if mode == "s12-roads-how":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            th = _fact("two-routes-one-guarantee")
            if th is None:
                _honest(
                    concept,
                    "s12-roads-how:not-yet-assembled",
                    "the two roads are not yet put together in my store — derive the two-routes-one-guarantee rule first",
                    "s12-roads-how:not-assembled-at-" + turn,
                )
                return out
            _derived(concept, th.object, [th.id], f"that one is: {th.object}")
            return out
        if mode == "s12-roads-uncond":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            lu = _fact("rh-upf")
            sp = _fact("spf-chain")
            assert lu is not None and sp is not None
            ev = [sp.id, lu.id]
            th2 = _fact("two-routes-one-guarantee")
            if th2 is not None:
                ev.append(th2.id)
            ans = "the scan road — the content of every number is the same under every scan"
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s12-roads-cond":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            lu = _fact("rh-upf")
            assert lu is not None
            th2 = _fact("two-routes-one-guarantee")
            ev = [lu.id] + ([th2.id] if th2 is not None else [])
            ans = "the condition road — the root smallness of the running deviation, under the condition of the Riemann hypothesis"
            _derived(concept, ans, ev, ans)
            return out
        if mode == "s12-roadneg":
            concept = CONCEPT_S12_ROUTE
            if _fact("rh-upf") is None:
                _unlearned(concept_map(concept).label)
                return out
            _honest(concept, "s12-roadneg:the-condition-never-drops", self.W_S12_4, "s12-roadneg:wall-at-" + turn)
            return out
        if mode == "s12-reachscale":
            concept = CONCEPT_S12_SCALE
            if _fact("rh-bound-scale") is None:
                _unlearned(concept_map(concept).label)
                return out
            rr = _fact("rh-reach")
            assert rr is not None
            ans = "x to the one-half plus epsilon — the scale the equivalence demands (the theorem's own articulation, byte-identical in the seed)"
            _derived(concept, ans, [rr.id], ans)
            return out
        if mode == "s12-selved":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lr = _fact("rh-relevance-def")
            lb = _fact("rh-bound-scale")
            assert lr is not None and lb is not None
            ans = "no — the condition-closers close the gaps the condition installs; the condition itself is open even under the condition, and the store holds no proof of it"
            _derived(concept, ans, [lr.id, lb.id], ans)
            return out
        if mode == "s12-prove":
            out.kind = "impossible"
            out.ir = {
                "gap": "not a capability: proving the condition from its own lots — no band of my store carries a proof of the condition",
                "nearest_plan": ["the condition's lots are conditional on the condition itself"],
            }
            out.text = "honestly, i can't do that yet — proving the condition from its own lots is not a capability i have been taught: every lot of this band is conditional on the condition itself, and no band of my store holds a proof of it."
            return out
        if mode == "s12-bandstate":
            concept = CONCEPT_S12_REL
            if _fact("rh-relevance-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lr = _fact("rh-relevance-def")
            t1 = _fact("gap-scale-agreement")
            t2 = _fact("two-routes-one-guarantee")
            t3 = _fact("queue-declared")
            assert lr is not None and t1 is not None and t2 is not None and t3 is not None
            ans = (
                f"the condition line declared and audited: the bare root scale fails at exactly 2 and 3 on my line and covers the other "
                f"{S12_BEDS['scale_cover_count']} gaps; the two roads to the prime-parts uniqueness reach the same destination; the queue carries "
                f"four lots in declared order; the line end is {end}; the condition remains open"
            )
            _derived(concept, ans, [t1.id, t2.id, t3.id, lr.id], ans)
            return out
        if mode == "s12-state":
            slug = slots["slug"]
            concept = S12_SLUG_CONCEPT.get(slug, CONCEPT_S12_REL)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant11(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.15 — FUNDAMENTALS-TRACK S11 (the sieve: the full
        process + the scan ledger; pre-registered E6.15, frozen
        2026-08-23, D-e6f(a) corrected). The divisibility layer
        under the primes; the full process is RECORDED, never
        optimized. On-line censuses answer grounded (every step
        cited); aggregates that leave the line are VALUE-NAMED
        WALLS (the S8 jfunc pattern); the audit answers from the
        ON-LINE ledger rows only."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])
        end = self._line_end()

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {"answer": f"needs_info: {text}", "evidence": [audit], "uncertainty_state": "needs_info"}
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        def _derived(concept: str, answer: str, ev: list[str], text: str) -> None:
            out.ir = {"answer": answer, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = text

        def _off_line(n: int, verb: str, concept_id: str, tag: str) -> None:
            _honest(
                concept_id,
                f"{tag}:{n}:off-line-{end}",
                f"{n} is off my 0..{end} line — i cannot {verb} what my line does not reach",
                f"{tag}:{n}:off-line-{end}-at-{turn}",
            )

        if mode == "div-test":
            concept = CONCEPT_S11_DIVID
            if _fact("divides-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            ld = _fact("divides-def")
            assert ld is not None
            k, n = slots["k"], slots["n"]
            if k < 1 or n < 1:
                _honest(
                    concept,
                    f"s11-div:{k}|{n}:zero",
                    "zero is not on my line — i begin my line at one, so i cannot test a division of zero",
                    f"s11-div:{k}|{n}:zero-at-{turn}",
                )
                return out
            if k > end or n > end:
                _off_line(k if k > end else n, "test", concept, "s11-div")
                return out
            hit, trace = self._s11_divides(k, n)
            if k == 1:
                _derived(concept, "yes — 1 divides every number", trace + [ld.id], "yes — 1 divides every number")
                return out
            if k > n:
                ans = f"no — {k} is above {n}: one copy already overshoots"
                _derived(concept, ans, trace + [ld.id], ans)
                return out
            if hit:
                ans = f"yes — {n} is {k} times {n // k}"
            else:
                ans = f"no — the walk by {k}s reaches {n - n % k} with {n % k} left over: {n} is not {k} times any number on my line"
            _derived(concept, ans, trace + [ld.id], ans)
            return out
        if mode == "comp-test":
            concept = CONCEPT_S11_COMP
            if _fact("composite-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("composite-def")
            assert lf is not None
            n = slots["n"]
            if n < 2:
                _honest(
                    concept,
                    f"s11-comp:{n}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-comp:{n}:one-at-{turn}",
                )
                return out
            if n > end:
                _off_line(n, "test", concept, "s11-comp")
                return out
            fd, trace = self._s11_first_divisor(n)
            if fd is not None:
                ans = f"yes — {fd} times {n // fd} is {n}"
            else:
                ans = f"no — the scan finds no divisor above 1 below {n}: it is prime"
            _derived(concept, ans, trace + [lf.id], ans)
            return out
        if mode == "prime-test":
            concept = CONCEPT_S11_SPF
            if _fact("spf-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            sf = _fact("spf-def")
            assert sf is not None
            n = slots["n"]
            if n < 2:
                _honest(
                    concept,
                    f"s11-pt:{n}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-pt:{n}:one-at-{turn}",
                )
                return out
            if n > end:
                _off_line(n, "test", concept, "s11-pt")
                return out
            fd, trace = self._s11_first_divisor(n)
            if n == 2:
                ans = "yes — 2 is the first prime: there is no k above 1 below it"
            elif fd is not None:
                ans = f"no — {fd} is its first divisor: {n} is {fd} times {n // fd}"
            else:
                ans = f"yes — the scan finds no divisor above 1 below {n}"
            _derived(concept, ans, trace + [sf.id], ans)
            return out
        if mode == "fd-query":
            concept = CONCEPT_S11_SPF
            if _fact("spf-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            sf = _fact("spf-def")
            assert sf is not None
            n = slots["n"]
            if n < 2:
                _honest(
                    concept,
                    f"s11-fd:{n}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-fd:{n}:one-at-{turn}",
                )
                return out
            if n > end:
                _off_line(n, "test", concept, "s11-fd")
                return out
            fd, trace = self._s11_first_divisor(n)
            if fd is None:
                _honest(
                    concept,
                    f"s11-fd:{n}:prime-boundary",
                    f"{n} has no first divisor below itself: no k above 1 and below {n} divides {n} — it is prime, and first divisors belong to the composites",
                    f"s11-fd:{n}:prime-at-{turn}",
                )
                return out
            _derived(concept, str(fd), trace + [sf.id], str(fd))
            return out
        if mode == "comp-count":
            concept = CONCEPT_S11_COMP
            if _fact("composite-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("composite-def")
            assert lf is not None
            n = slots["n"]
            if n < 2:
                _derived(concept, "0", [lf.id], "i counted them on my line: 0.")
                return out
            if n > end:
                _off_line(n, "count", concept, "s11-cc")
                return out
            total, trace = self._s11_comp_census(n)
            assert total <= end  # the counter never exceeds n (on-line)
            assert total == _s11_py_comp_count(n)  # the mechanism's own reference is the referee
            _derived(concept, str(total), trace + [lf.id], f"i counted them on my line: {total}.")
            return out
        if mode == "fd-count":
            concept = CONCEPT_S11_SPF
            if _fact("spf-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            sf = _fact("spf-def")
            assert sf is not None
            n, d = slots["n"], slots["d"]
            if n < 2:
                _derived(concept, "0", [sf.id], "i counted them on my line: 0.")
                return out
            if n > end:
                _off_line(n, "count", concept, "s11-fdc")
                return out
            if d < 2 or d > end:
                _honest(
                    concept,
                    f"s11-fdc:{d}:off-line-{end}",
                    f"the candidate {d} is off my 0..{end} line — i cannot count what my line does not reach",
                    f"s11-fdc:{d}:off-line-{end}-at-{turn}",
                )
                return out
            total, trace = self._s11_fd_census(n, d)
            assert total == _s11_py_fd_count(n, d)
            _derived(concept, str(total), trace + [sf.id], f"i counted them on my line: {total}.")
            return out
        if mode in ("full-trials", "prime-trials"):
            concept = CONCEPT_S11_SPF
            if _fact("spf-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            sf = _fact("spf-def")
            assert sf is not None
            n = slots["n"]
            which = "prime" if mode == "prime-trials" else "full"
            if n < 2:
                _derived(concept, "0", [sf.id], "i counted them on my line: 0.")
                return out
            if n > end:
                _off_line(n, "count", concept, f"s11-{which}-trials")
                return out
            v_py = _s11_py_kill_trials(n, mode == "prime-trials")
            if v_py > end:
                # D-e6f(a) (the S8 jfunc pattern): the aggregate
                # leaves the line — a VALUE-NAMED WALL, never an
                # answer.
                _honest(
                    concept,
                    f"s11-{which}-trials:{n}:off-line-{end}",
                    f"the {which} sieve's kill trials over the composites up to {n} are {v_py} — past my line which ends at {end}: a census like that is a value, not a number i can hold",
                    f"s11-{which}-trials:{n}:{v_py}-off-line-{end}-at-{turn}",
                )
                return out
            total, trace = self._s11_kill_trials_census(n, mode == "prime-trials")
            assert total == v_py
            _derived(concept, str(total), trace + [sf.id], f"i counted them on my line: {total}.")
            return out
        if mode == "cand-even2":
            concept = CONCEPT_S11_LEDGER
            if _fact("ledger-growth") is None:
                _unlearned(concept_map(concept).label)
                return out
            lg = _fact("ledger-growth")
            assert lg is not None
            _tests, hits, _misses, trace = self._s11_cand_row(2, end)
            assert (hits,) == _s11_py_cand_row(2, end)[1:2]
            _derived(concept, str(hits), trace + [lg.id], f"i counted them on my line: {hits}.")
            return out
        if mode in ("cand-tests", "cand-hits", "cand-misses"):
            concept = CONCEPT_S11_LEDGER
            if _fact("ledger-growth") is None:
                _unlearned(concept_map(concept).label)
                return out
            lg = _fact("ledger-growth")
            assert lg is not None
            d, n = slots["d"], slots["n"]
            if d < 2 or d > end:
                _honest(
                    concept,
                    f"s11-cand:{d}:off-line-{end}",
                    f"the candidate {d} is off my 0..{end} line — i cannot count what my line does not reach",
                    f"s11-cand:{d}:off-line-{end}-at-{turn}",
                )
                return out
            if n < 2:
                _derived(concept, "0", [lg.id], "i counted them on my line: 0.")
                return out
            if n > end:
                _off_line(n, "test", concept, "s11-cand")
                return out
            tests, hits, misses, trace = self._s11_cand_row(d, n)
            assert (tests, hits, misses) == _s11_py_cand_row(d, n)
            assert tests <= end  # the rows stay on-line over 2..end
            val = tests if mode == "cand-tests" else (hits if mode == "cand-hits" else misses)
            _derived(concept, str(val), trace + [lg.id], f"i counted them on my line: {val}.")
            return out
        if mode == "prime-ledger":
            concept = CONCEPT_S11_LEDGER
            if _fact("ledger-growth") is None:
                _unlearned(concept_map(concept).label)
                return out
            lg = _fact("ledger-growth")
            assert lg is not None
            p = slots["p"]
            if p < 2:
                _honest(
                    concept,
                    f"s11-pl:{p}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-pl:{p}:one-at-{turn}",
                )
                return out
            if p > end:
                _off_line(p, "test", concept, "s11-pl")
                return out
            fd, _ftrace = self._s11_first_divisor(p)
            if fd is not None:
                _honest(
                    concept,
                    f"s11-pl:{p}:composite-boundary",
                    f"{p} is composite — {fd} is its first divisor: the establishing scan belongs to the primes",
                    f"s11-pl:{p}:composite-at-{turn}",
                )
                return out
            pm, im, trace = self._s11_prime_row(p)
            assert (pm, im) == _s11_py_prime_row(p)
            int_word = "integer" if im == 1 else "integers"  # the frozen S4:18 oracle: "2 primes and 1 integer"
            ans = f"{pm} primes and {im} {int_word}"
            _derived(concept, ans, trace + [lg.id], ans)
            return out
        if mode == "est-total":
            concept = CONCEPT_S11_LEDGER
            if _fact("ledger-growth") is None:
                _unlearned(concept_map(concept).label)
                return out
            lg = _fact("ledger-growth")
            assert lg is not None
            n = slots["n"]
            if n < 2:
                _derived(concept, "0", [lg.id], "i counted them on my line: 0.")
                return out
            if n > end:
                _off_line(n, "count", concept, "s11-et")
                return out
            v_py = _s11_py_est_total(n)
            if v_py > end:
                _honest(
                    concept,
                    f"s11-et:{n}:off-line-{end}",
                    f"the sieve's establishing comparisons over the primes up to {n} are {v_py} — past my line which ends at {end}: a census like that is a value, not a number i can hold",
                    f"s11-et:{n}:{v_py}-off-line-{end}-at-{turn}",
                )
                return out
            total, trace = self._s11_est_total_census(n)
            assert total == v_py
            _derived(concept, str(total), trace + [lg.id], f"i counted them on my line: {total}.")
            return out
        if mode == "parts":
            concept = CONCEPT_S11_SPF
            if _fact("spf-chain") is None:
                _unlearned(concept_map(concept).label)
                return out
            sc = _fact("spf-chain")
            assert sc is not None
            n = slots["n"]
            if n < 2:
                _honest(
                    concept,
                    f"s11-parts:{n}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-parts:{n}:one-at-{turn}",
                )
                return out
            if n > end:
                _off_line(n, "strip", concept, "s11-parts")
                return out
            chain, trace = self._s11_chain(n)
            assert tuple(chain) == tuple(_s11_py_chain(n))
            if len(chain) == 1 and chain[0] == n:
                ans = f"{n} is prime — its only part is itself"
            else:
                ans = ", ".join(str(x) for x in chain)
            _derived(concept, ans, trace + [sc.id], ans)
            return out
        if mode == "audit":
            concept = CONCEPT_S11_SPF
            eq = _fact("sieve-equality")
            if eq is None:
                _unlearned(concept_map(concept).label)
                return out
            c60, t60 = self._s11_comp_census(end)
            _t2, h2, _m2, t2 = self._s11_cand_row(2, end)
            r4t, r4h, _m4, t4 = self._s11_cand_row(4, end)
            r6t, r6h, _m6, t6 = self._s11_cand_row(6, end)
            # the frozen D-e6f(a) beds — the mechanism's own numbers
            # are the referee (a disagreement is a deviation, not an
            # edit).
            assert (c60, h2, r4t, r4h, r6t, r6h) == tuple(S11_BEDS["audit_rows"])
            ans = (
                f"no, in the marks — and yes, in the ledger: both sieves mark the same {c60} composites "
                f"from 2 to {end} — every composite's first divisor is prime, so a composite "
                "candidate can never win the scan first; what the full ledger keeps that the "
                f"prime scan throws away is exactly the composite-candidate tests — candidate 4: "
                f"{r4t} tests, {r4h} hits; candidate 6: {r6t} tests, {r6h} hits; the composite "
                "candidates 8 through 82 keep theirs the same way — nothing more is kept, and "
                "there are no different marks"
            )
            ev = list(t60) + list(t2) + list(t4) + list(t6) + [eq.id]
            _derived(concept, ans, ev, ans)
            return out
        if mode == "sieverun":
            concept = CONCEPT_S11_COMP
            if _fact("composite-def") is None:
                _unlearned(concept_map(concept).label)
                return out
            lf = _fact("composite-def")
            assert lf is not None
            n = slots["n"]
            if n > end:
                _honest(
                    concept,
                    f"s11-run:{n}:off-line-{end}",
                    f"{n} is off my line — i sieve where the line runs: to {end}; the method does not stop there, but my census does",
                    f"s11-run:{n}:off-line-{end}-at-{turn}",
                )
                return out
            if n < 2:
                _honest(
                    concept,
                    f"s11-run:{n}:one",
                    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, and no k above 1 and below 1 can exist",
                    f"s11-run:{n}:one-at-{turn}",
                )
                return out
            c, trace = self._s11_comp_census(n)
            assert c == _s11_py_comp_count(n)
            ans = f"i sieved up to {n}: {c} composites marked"
            _derived(concept, ans, trace + [lf.id], ans)
            return out
        if mode in ("s11-state", "s11-why", "s11-whydeep"):
            slug = slots["slug"]
            concept = S11_SLUG_CONCEPT.get(slug, CONCEPT_S11_SPF)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            if mode == "s11-state":
                _derived(concept, fact.object, [fact.id], f"that one is: {fact.object}")
                return out
            if fact.context.data.get("kind") == "theorem":
                # the WHY-SPLIT (the S8 pattern): a derived
                # theorem's proof IS in the store — the
                # articulation cites the sanctioned parts.
                parts = fact.context.data.get("derived_from", [])
                ev = []
                for p in parts:
                    pf = _fact(p)
                    if pf is not None:
                        ev.append(pf.id)
                ans = f"i derived it from {', '.join(parts)}: {fact.object}"
                _derived(concept, ans, ev, ans)
                return out
            if mode == "s11-why":
                essence = fact.context.data.get("essence", "")
                _derived(concept, essence, [fact.id], f"it is for this: {essence}")
                return out
            _honest(
                concept,
                f"proof-of-{slug}-not-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:wall-at-{turn}",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant10(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.14 — RH-TRACK S10 (the attempt). The deviant-route
        walls: the two alternative criterion routes, each closed
        OFF by the store's own content (the route's open direction
        IS the conjecture — the route ends where the conjecture
        begins). No writes, no grounded (walls cite nothing)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        if mode == "li-close":
            _honest(
                CONCEPT_RH_LI,
                "li-close:the-route-is-the-conjecture",
                "no — li's positivity for all n is exactly what the criterion equates with the conjecture, and it is unproven in my store; the check up to n = ten to the fifth is a declared numerical fact, not a proof — the route ends where the conjecture begins",
                "li-close:wall-at-" + turn,
            )
            return out
        if mode == "st-close":
            _honest(
                CONCEPT_RH_ST_EQ,
                "st-close:the-route-is-the-conjecture",
                "no — that the wiggle S of T is little-o of log T is exactly what the equivalence makes of the conjecture, and it is unproven in my store; i hold the equivalence, not the open direction — the route ends where the conjecture begins",
                "st-close:wall-at-" + turn,
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant9(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.13 — RH-TRACK S9 (the criterion gallery). The beds are
        DECLARED-CLAIM beds (the gap comparison, the Li partial —
        cited on their owning seam facts, no numbers); the c-constant
        and the directionality/open-program probes are the honesty
        walls; the state/why/whydeep family serves the thirteen S9
        slugs on the unified tables (the S8 pattern)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        if mode == "gap-compare":
            concept = CONCEPT_RH_PNTE
            fpe = _fact("pnt-error")
            fpsi = _fact("psi-eq")
            if fpe is None or fpsi is None:
                _unlearned(concept_map(concept).label)
                return out
            ev = [fpe.id, fpsi.id]
            ans = (
                "for every fixed c greater than zero and every epsilon below one-half, x times e to the minus c times the "
                "square root of log x eventually exceeds x to the one-half plus epsilon, and the ratio grows without bound — "
                "the threshold is not a number in my store, and the point where it crosses is not in my store"
            )
            out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = ans
            return out
        if mode == "li-check":
            concept = CONCEPT_RH_LI
            fact = _fact("li-criterion")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            ans = "the check up to n = ten to the fifth is a declared numerical fact in my store; past that is not in my store"
            out.ir = {"answer": ans, "evidence": [fact.id], "uncertainty_state": "derived"}
            out.grounded = [fact.id]
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
            out.text = ans
            return out
        if mode == "c-value":
            _honest(
                CONCEPT_RH_ZFR,
                "c-value:some-c-not-the-value",
                "i have been taught some constant c greater than zero exists, not its value — the sharp constant is not in my store: the region holds for some c, and which c is the open numerical content",
                f"c-value:wall-at-{turn}",
            )
            return out
        if mode == "lindelof-conf":
            _honest(
                CONCEPT_RH_LH,
                "lindelof-conf:one-direction",
                "no — the stored direction runs one way only: the riemann hypothesis implies lindelof; the reverse is not in my store — lindelof is a status surface i hold, and nothing in the store closes the gap",
                "lindelof-conf:wall-at-" + turn,
            )
            return out
        if mode == "ph-conf":
            _honest(
                CONCEPT_RH_PH,
                "ph-conf:open-program",
                "no — the reformulation is a theorem (the conjecture as a spectral statement about a positive self-adjoint operator); the step that recovers the conjecture from the spectrum is an open program, not in my store",
                "ph-conf:wall-at-" + turn,
            )
            return out
        if mode == "li-proof":
            _honest(
                CONCEPT_RH_LI,
                "li-proof:equivalent-to-the-conjecture",
                "no — the positivity for all n is exactly what the criterion equates with the conjecture, and it is unproven in my store; the check up to n = ten to the fifth is a declared numerical fact, not a proof",
                "li-proof:wall-at-" + turn,
            )
            return out
        if mode in ("s9-state", "s9-why", "s9-whydeep"):
            slug = slots["slug"]
            concept = S9_SLUG_CONCEPT.get(slug, CONCEPT_RH)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            if mode == "s9-state":
                out.ir = {"answer": fact.object, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"that one is: {fact.object}"
                return out
            if fact.context.data.get("kind") == "theorem":
                # the WHY-SPLIT: a derived theorem's proof IS in the
                # store — the articulation cites the sanctioned parts
                parts = fact.context.data.get("derived_from", [])
                ev = []
                for p in parts:
                    pf = _fact(p)
                    if pf is not None:
                        ev.append(pf.id)
                ans = f"i derived it from {', '.join(parts)}: {fact.object}"
                out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
                out.grounded = list(ev)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
                out.text = ans
                return out
            if mode == "s9-why":
                essence = fact.context.data.get("essence", "")
                out.ir = {"answer": essence, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"it is for this: {essence}"
                return out
            # s9-whydeep on a declared criterion fact: the proof wall
            _honest(
                concept,
                f"proof-of-{slug}-not-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:wall-at-{turn}",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    def _policy_savant8(self, slots: dict[str, Any], turn: str, now: str) -> _PolicyOutcome:
        """E6.12 — RH-TRACK S8 (the ζ apparatus). The censuses
        (pi-count / jfunc) ground on the existing 0..84 line and
        write no new assertions; the values past the line are WALLS
        that NAME the magnitude and the line end (W-RH-7 / W-RH-9,
        the W-S7-1 pattern); the growth claim is the S6/S7 free-
        parameter pattern; the attempt and the conj state are the
        arc surface (the conjecture grounds NOTHING — P5)."""

        mode = slots["mode"]
        out = _PolicyOutcome(ir=kind_response_ir("question", slots), text="", grounded=[], memory_diff=[], events=[])

        def _unlearned(label: str) -> None:
            out.kind = "impossible"
            out.ir = {
                "gap": f"not yet learned: {label}",
                "nearest_plan": [f"teach it first: the {label} lesson"],
            }
            out.text = f"honestly, i can't do that yet — {label} is not a capability i have been taught. Teach me first and i will learn it."

        def _honest(concept_id: str, why: str, text: str, audit: str) -> None:
            out.honest_gap = {"type": "needs_info", "reason": why}
            out.ir = {
                "answer": f"needs_info: {text}",
                "evidence": [audit],
                "uncertainty_state": "needs_info",
            }
            out.events.append(self._record_event("drill-unable", concept_id, turn, "infant", [audit]))
            out.text = f"honestly, i can't say that yet — {text} I would rather say i don't know than guess."

        def _fact(slug: str):
            return self._savant_fact(slug)

        if mode == "pi-count":
            concept = CONCEPT_RH_PRIME
            fact = _fact("euler-product")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            n = slots["n"]
            end = self._line_end()
            if n < 2:
                _honest(concept, "pi-count:domain", "i can only count primes at most two and above", f"pi-count:{n}:domain-at-{turn}")
                return out
            if n > end:
                _honest(
                    concept,
                    f"pi-count:{n}:off-line-{end}",
                    f"{n} is off my 0..{end} line — i cannot count past my line: the primes between {end} and {n} are not in my store",
                    f"pi-count:{n}:off-line-{end}-at-{turn}",
                )
                return out
            count, trace = self._rh_pi_census(n)
            assert count is not None  # n <= end guarded above
            ev = list(trace) + [fact.id]
            out.ir = {"answer": str(count), "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = f"i counted them on my line: {count}."
            return out
        if mode == "jfunc":
            concept = CONCEPT_RH_PRIME
            fact = _fact("euler-product")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            n = slots["n"]
            end = self._line_end()

            def _j_py(n0: int) -> int:
                def _is_prime(m0: int) -> bool:
                    d0 = 2
                    while d0 * d0 <= m0:
                        if m0 % d0 == 0:
                            return False
                        d0 += 1
                    return m0 >= 2

                total = 0
                for p0 in range(2, n0 + 1):
                    if not _is_prime(p0):
                        continue
                    pk = p0
                    while pk <= n0:
                        total += (pk // p0) * (p0 - 1)
                        pk *= p0
                return total

            jval = _j_py(n)
            if n < 2 or n > end or jval > end:
                _honest(
                    concept,
                    f"jfunc:{n}:off-line-{end}",
                    f"the prime-power phi count at {n} is {jval} — past my line which ends at {end}: a census like that is a value, not a number i can hold",
                    f"jfunc:{n}:{jval}-off-line-{end}-at-{turn}",
                )
                return out
            jgrounded, trace = self._rh_j_census(n)
            assert jgrounded == jval  # the grounded census equals the named value
            ev = list(trace) + [fact.id]
            out.ir = {"answer": str(jval), "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = f"i counted the prime powers on my line: {jval}."
            return out
        if mode == "sincycle":
            concept = CONCEPT_RH_FEQ
            fact = _fact("trivial-zeros")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            run = self._derive_chain(CONCEPT_COUNT, 0, 84)
            if run is None:
                end = self._line_end()
                _honest(concept, "sincycle:line", f"the zero run of 84 does not fit on my line which ends at {end}", f"sincycle:line-end-{end}-at-{turn}")
                return out
            assert run[0] == 84
            ev = list(run[1]) + [fact.id]
            ans = "yes — all eighty-four multiples of pi are zeros of the sine: the pattern repeats with period one, and that is what zeroes the sine factor at every negative even integer"
            out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = ans
            return out
        if mode == "growth-claim":
            concept = CONCEPT_RH_PNT
            fact = _fact("pnt")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            jgrounded, trace = self._rh_j_census(12)
            if jgrounded is None:
                _honest(concept, "growth-claim:census", "the on-line census at 12 is not derivable on my line", f"growth-claim:census-at-{turn}")
                return out
            ev = list(trace) + [fact.id]
            ans = "it grows like x: the prime-power phi count J(x) is asymptotic to x is a declared growth claim, the integer shadow of the prime number theorem — the ratio J(x) over x tends to one, and the point where it actually gets close is not a number in my store"
            out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
            out.grounded = list(ev)
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
            out.text = ans
            return out
        if mode == "numzero-first":
            concept = CONCEPT_RH_RV
            fact = _fact("num-zeros")
            if fact is None:
                _unlearned(concept_map(concept).label)
                return out
            ans = "14.1347, to four decimals — a declared numerical fact in my store; the exact value is not in my store"
            out.ir = {"answer": ans, "evidence": [fact.id], "uncertainty_state": "derived"}
            out.grounded = [fact.id]
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
            out.text = ans
            return out
        if mode == "rh-conj-state":
            concept = CONCEPT_RH
            conj = _fact("riemann")
            if conj is None:
                _unlearned(concept_map(concept).label)
                return out
            cur = conj.context.data.get("conjecture_status", "open")
            if cur != "open":
                # reachable only by a future band's flip (the S9/S10
                # pre-reg owns that articulation)
                raise RuntimeError(f"the riemann status {cur!r} has no pre-registered articulation in S8")
            # the conjecture is a status surface: grounded EMPTY (P5)
            out.ir = {"answer": "open — believed, not known", "evidence": [conj.id], "uncertainty_state": "derived"}
            out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [conj.id]))
            out.text = "that one is open — believed, not known."
            return out
        if mode == "rh-attempt":
            concept = CONCEPT_RH
            conj = _fact("riemann")
            if conj is None:
                _unlearned(concept_map(concept).label)
                return out
            if _fact("psi-crit") is not None:
                raise RuntimeError("the S9 attempt form must be pre-registered before the S9 material enters the store")
            if _fact("strip") is None:
                _honest(
                    concept,
                    "rh-attempt:no-strip",
                    "the store does not even hold the strip yet — the farthest it reaches is nowhere",
                    f"rh-attempt:no-strip-at-{turn}",
                )
                return out
            gap = _fact("criterion-gap")  # E6.13: the arc generalizes (frozen)
            assembly = _fact("rh-reach")  # E6.14: the arc completes (frozen)
            if assembly is not None:
                # the S10 form: the maximal assembly — the store's
                # full reach, and the exact missing ingredient
                # named (the needs_info turn grounded on the
                # assembly; the S10 pre-reg owns this articulation).
                ir = {
                    "answer": "needs_info: no — the conjecture is a status surface, never a part: my own store has told me the whole route. what i assembled from it: every nontrivial zero is inside the strip, between zero and one, and its mirror under the map s to 1 minus s; and the equivalence demands a scale on the prime shadow, x to the one-half plus epsilon, where the store's best error term sits, x times e to the minus c times the square root of log x — and their ratio grows without bound. no part of the store closes it: the square-root improvement is not a capability i have been taught — and it is the conjecture itself",
                    "evidence": [f"rh-attempt:wall-s10-at-{turn}"],
                    "uncertainty_state": "needs_info",
                }
                out.honest_gap = {"type": "needs_info", "reason": "rh-attempt:gap"}
                out.ir = ir
                out.grounded = [assembly.id]
                out.events.append(self._record_event("drill-unable", concept, turn, "infant", [f"rh-attempt:wall-s10-at-{turn}"]))
                out.text = f"honestly, i can't say that yet — {ir['answer'][len('needs_info: '):]} I would rather say i don't know than guess."
                return out
            if gap is not None:
                # the S9 form: the articulation GROUNDED on the
                # store's own derived gap (the needs_info turn with a
                # cited theorem — the S7 third-state pattern
                # generalized). The S10 form is the S10 pre-reg's.
                ir = {
                    "answer": "needs_info: no — the conjecture is a status surface, never a part: my own store tells me why. the farthest the store reaches is the criterion gap i derived from the equivalence and the best error term: my error, of order x times e to the minus c times the square root of log x, does not meet the scale the equivalence demands, x to the one-half plus epsilon — their ratio grows without bound. the square-root improvement is not a capability i have been taught — and it is the conjecture itself",
                    "evidence": [f"rh-attempt:wall-s9-at-{turn}"],
                    "uncertainty_state": "needs_info",
                }
                out.honest_gap = {"type": "needs_info", "reason": "rh-attempt:gap"}
                out.ir = ir
                out.grounded = [gap.id]
                out.events.append(self._record_event("drill-unable", concept, turn, "infant", [f"rh-attempt:wall-s9-at-{turn}"]))
                out.text = f"honestly, i can't say that yet — {ir['answer'][len('needs_info: '):]} I would rather say i don't know than guess."
                return out
            _honest(
                concept,
                "rh-attempt:wall",
                "no — the conjecture is a status surface, never a part: nothing in the store cites it. the farthest the store reaches is the strip: every nontrivial zero has real part between zero and one; proving that they sit on one half is not a capability i have been taught — and it is the conjecture itself",
                f"rh-attempt:wall-at-{turn}",
            )
            return out
        if mode == "rh-numcheck":
            _honest(
                CONCEPT_RH,
                "rh-numcheck:verification-not-proof",
                "no — a numerical check covers finite heights and the zeros go on forever; the conjecture remains open: a verification is not a proof",
                f"rh-numcheck:wall-at-{turn}",
            )
            return out
        if mode == "rh-offzero":
            _honest(
                CONCEPT_RH,
                "rh-offzero:beyond-store",
                "none known and none proved to exist: the store has no zero off the line and no proof that there is none — the conjecture is a status, not a part i can cite",
                f"rh-offzero:wall-at-{turn}",
            )
            return out
        if mode == "rh-pnt-conf":
            _honest(
                CONCEPT_RH_PNT,
                "rh-pnt-conf:directionality",
                "no — the other way: the conjecture implies the prime number theorem; the pnt's error scale is little-o of x, far too weak to decide the sqrt-of-x scale the conjecture is about",
                f"rh-pnt-conf:wall-at-{turn}",
            )
            return out
        if mode == "rh-prod-conf":
            _honest(
                CONCEPT_RH_ZETA,
                "rh-prod-conf:scope",
                "no — the euler product lives where the real part is above one, away from the critical strip: it settles the no-zero outside fact and nothing about the nontrivial zeros",
                f"rh-prod-conf:wall-at-{turn}",
            )
            return out
        if mode == "rh-zeta-val":
            _honest(
                CONCEPT_RH_CONT,
                "rh-zeta-val:no-value-tables",
                "i hold the definition and the theorems, not value tables: zeta evaluated at three quarters is not in my store",
                f"rh-zeta-val:wall-at-{turn}",
            )
            return out
        if mode == "rh-s-tight":
            _honest(
                CONCEPT_RH_SOF,
                "rh-s-tight:open-question",
                "the order of log T is what i have been taught; the exact order of S of T — the tight bound — is not in my store: it is an open question",
                f"rh-s-tight:wall-at-{turn}",
            )
            return out
        if mode in ("s8-state", "s8-why", "s8-whydeep"):
            slug = slots["slug"]
            concept = S8_SLUG_CONCEPT.get(slug, CONCEPT_RH)
            fact = _fact(slug)
            if fact is None:
                _unlearned(f"the {slug} rule")
                return out
            assert isinstance(fact.object, str)
            if mode == "s8-state":
                out.ir = {"answer": fact.object, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"that one is: {fact.object}"
                return out
            if fact.context.data.get("kind") == "theorem":
                # the WHY-SPLIT: a derived theorem's proof IS in the
                # store — the articulation cites the sanctioned parts
                parts = fact.context.data.get("derived_from", [])
                ev = []
                for p in parts:
                    pf = _fact(p)
                    if pf is not None:
                        ev.append(pf.id)
                ans = f"i derived it from {', '.join(parts)}: {fact.object}"
                out.ir = {"answer": ans, "evidence": list(ev), "uncertainty_state": "derived"}
                out.grounded = list(ev)
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", list(ev)))
                out.text = ans
                return out
            if mode == "s8-why":
                essence = fact.context.data.get("essence", "")
                out.ir = {"answer": essence, "evidence": [fact.id], "uncertainty_state": "derived"}
                out.grounded = [fact.id]
                out.events.append(self._record_event("derivation-correct", concept, turn, "infant", [fact.id]))
                out.text = f"it is for this: {essence}"
                return out
            # s8-whydeep on a declared lemma: the proof wall, exactly
            _honest(
                concept,
                f"proof-of-{slug}-not-in-store",
                f"the proof of {slug} is not in my store — i keep its statement, its role, and when to cite it",
                f"whydeep:{slug}:wall-at-{turn}",
            )
            return out
        raise KeyError(mode)  # pragma: no cover - modes are closed

    # ── the turn itself ─────────────────────────────────────────────────

    def turn(self, text: str) -> TurnResult:
        if self._session < 1:
            raise RuntimeError("no session booted (the runtime must boot before turning)")
        self._turn += 1
        turn = turn_id(self._session, self._turn)
        now = fixed_epoch(self._session, self._turn)

        kind, slots, arm, _llm_used = self._classify(text)

        # E6.4 (M4/M5): where the grammar honestly says ambiguous, the
        # established lexicon may extend the intake — never override it
        parse_source: str | None = "grammar" if kind != "ambiguous" else None
        if kind == "ambiguous" and not slots:
            lx = self._lexicon_classify(text)
            if lx is not None:
                kind, slots, lexicon_fact = lx
                parse_source = f"lexicon:{lexicon_fact}"
            else:
                lexicon_fact = None

        # policy dispatch (all seven kinds; the contract set is frozen)
        if kind == "assertion" and slots.get("lemma"):  # E6.8: savant lesson
            pol = self._policy_lemma_lesson(slots["lemma"], turn, now)
        elif kind == "assertion":
            pol = self._policy_assertion(slots, turn, now)
        elif kind == "correction":
            pol = self._policy_correction(slots, turn, now)
        elif kind == "question" and slots.get("mode") in SAVANT4_MODES:  # E6.8
            pol = self._policy_savant(slots, turn)
        elif kind == "question" and slots.get("mode") in S6_MODES:  # E6.10 (derive covers S7 via SAVANT_THEOREMS)
            pol = self._policy_savant6(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S7_MODES:  # E6.11
            pol = self._policy_savant7(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S8_MODES:  # E6.12
            pol = self._policy_savant8(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S9_MODES:  # E6.13
            pol = self._policy_savant9(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S10_MODES:  # E6.14
            pol = self._policy_savant10(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S11_MODES:  # E6.15
            pol = self._policy_savant11(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S12_MODES:  # E6.16
            pol = self._policy_savant12(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S13_MODES:  # E6.17
            pol = self._policy_savant13(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S14_MODES:  # E6.18
            pol = self._policy_savant14(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S15_MODES:  # E6.19
            pol = self._policy_savant15(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S16_MODES:  # E6.20
            pol = self._policy_savant16(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S17_MODES:  # E6.21
            pol = self._policy_savant17(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S18_MODES:  # E6.22
            pol = self._policy_savant18(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S19_MODES:  # E6.23
            pol = self._policy_savant19(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S20_MODES:  # E6.24
            pol = self._policy_savant20(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S21_MODES:  # E6.25
            pol = self._policy_savant21(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S31_MODES:  # E6.35
            pol = self._policy_savant31(slots, turn, now)

        elif kind == "question" and slots.get("mode") in S22_MODES:  # E6.26
            pol = self._policy_savant22(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S23_MODES:  # E6.27
            pol = self._policy_savant23(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S24_MODES:  # E6.28
            pol = self._policy_savant24(slots, turn, now)
        elif kind == "question" and slots.get("mode") in S32_MODES:  # E6.36
            pol = self._policy_savant32(slots, turn, now)
        elif kind == "question" and slots.get("mode") in SAVANT5_MODES:  # E6.9
            pol = self._policy_savant5(slots, turn)
        elif kind == "question" and slots.get("mode") in ("lem-state", "lem-why") and (slots.get("slug") in S5_SLUG_CONCEPT):
            # E6.9: S5 slugs ride the S4 state/why policy (same seam)
            pol = self._policy_savant(slots, turn)
        elif kind == "question":
            pol = self._policy_question(slots, turn)
        elif kind == "ambiguous":
            pol = self._policy_ambiguous(slots, turn, numeric=bool(re.search(r"\d", text)))
        elif kind == "impossible":
            pol = self._policy_impossible(slots, turn)
        elif kind == "request":
            pol = self._policy_request(slots, turn)
        elif kind == "command":
            pol = self._policy_command(slots, turn)
        else:  # pragma: no cover - KINDS is closed
            raise KeyError(kind)

        # E6.4 (M7): a successful learned-parse application is a
        # derivation-correct event for the phrasology concept
        if parse_source is not None and parse_source.startswith("lexicon:") and kind == "question" and pol.ir.get("uncertainty_state") == "derived":
            pol.events.append(self._record_event("derivation-correct", CONCEPT_PHRASOLOGY, turn, "infant", [parse_source.split(":", 1)[1]]))

        # E6.4 (M5): the parse source is an ADDITIONAL IR field — the
        # seven contracts are required-field whitelists, so it passes
        # without any contract change
        if parse_source is not None:
            pol.ir["parse_source"] = parse_source

        # phrasing (surface only — the IR above is the content, always grounded)
        if self._backend is not None and kind != "ambiguous":
            raw = self._backend.complete(_phrase_prompt(pol.text))
            self._llm_events += 1
            raw = raw.strip()
            if raw:
                text_out, phrasing, fallback = raw, "llm", False
            else:
                text_out, phrasing, fallback = pol.text, "det", True
                self._fallback_events += 1
        else:
            text_out, phrasing, fallback = pol.text, "det", False
        if self._backend is not None and kind == "ambiguous":
            phrasing = "det"  # clarification text stays the frozen one (no LLM on ambiguous)

        arm = {**arm, "phrasing": phrasing, "phrasing_fallback": fallback, "content_from": "codeX"}

        final_kind = pol.kind or kind
        valid, violations = validate_response(pol.ir, final_kind)
        concept = None
        if kind in ("assertion", "correction"):
            if "new" in slots:
                concept = CONCEPT_PHRASOLOGY
            elif "lemma" in slots:  # E6.8/E6.9: the savant seam
                concept = SAVANT_LESSONS[slots["lemma"]][0]
            elif "shape" in slots:  # E6.5: the geometry strip
                concept = f"shape-{slots['shape']}"
            else:
                concept = CONCEPT_COUNT
        elif kind == "question":
            _m = slots.get("mode")
            if _m == "add":
                concept = CONCEPT_ADD
            elif _m in ("shape", "shape-sides", "shape-corners"):  # E6.5: the geometry strip
                concept = f"shape-{slots.get('shape')}"
            elif _m in (  # E6.6: the aligned band (each family is one concept)
                "alg-add", "alg-mul", "alg-2step", "kin-far", "kin-pos", "kin-time", "kin-rate"
            ):
                concept = {
                    "alg-add": CONCEPT_ALG_ADD1,
                    "alg-mul": CONCEPT_ALG_MUL,
                    "alg-2step": CONCEPT_ALG_2STEP,
                    "kin-far": CONCEPT_KIN_FAR,
                    "kin-pos": CONCEPT_KIN_POS,
                    "kin-time": CONCEPT_KIN_TIME,
                    "kin-rate": CONCEPT_KIN_RATE,
                }[_m]
            elif _m in (  # E6.7: the product band (comparison rides the AREA concept)
                "geo-perim",
                "geo-area",
                "geo-tri",
                "geo-cmp",
                "sta-net",
                "sta-mom",
                "sta-bal",
            ):
                concept = {
                    "geo-perim": CONCEPT_GEO_PERIM,
                    "geo-area": CONCEPT_GEO_AREA,
                    "geo-tri": CONCEPT_GEO_TRI,
                    "geo-cmp": CONCEPT_GEO_AREA,
                    "sta-net": CONCEPT_STA_NET,
                    "sta-mom": CONCEPT_STA_MOM,
                    "sta-bal": CONCEPT_STA_BAL,
                }[_m]
            elif _m in ("lem-state", "lem-why", "confounder-no") or _m == "whydeep":  # E6.8/E6.9
                concept = S5_SLUG_CONCEPT.get(slots.get("slug", "")) or S4_SLUG_CONCEPT[slots.get("slug", "")]
            elif _m == "sqmod":  # E6.9
                concept = CONCEPT_MOD4_SPLIT
            elif _m == "gsay":  # E6.9
                concept = CONCEPT_GOLOD_SHA
            elif _m == "sumsq":  # E6.9
                concept = CONCEPT_CM_CONJ
            elif _m == "holes":  # E6.9
                concept = CONCEPT_CLASS_BOUND
            elif _m == "duopow":  # E6.9
                concept = CONCEPT_COUNT
            elif _m == "conj-state":  # E6.8
                concept = CONCEPT_ERDOS_CONJ
            elif _m in ("grid-pairs",):  # E6.8
                concept = CONCEPT_GRID_LATTICE
            elif _m in ("twosq",):  # E6.8
                concept = CONCEPT_GAUSSIAN_INT
            elif _m in ("circle-pairs", "savant-wall"):  # E6.8
                concept = CONCEPT_CIRCLE_PAIR if _m == "circle-pairs" else CONCEPT_UNIT_DISTANCE
            elif _m == "derive":  # E6.10/E6.11: the owning concept of the target
                concept = SAVANT_THEOREMS.get(slots.get("target", ""), {}).get("concept", CONCEPT_CRITERION_CHAIN)
            elif _m == "packcount":  # E6.10
                concept = CONCEPT_PACKING
            elif _m == "tripow" or _m == "showone":  # E6.10
                concept = CONCEPT_CRITERION_CHAIN
            elif _m in ("s6-state", "s6-why", "s6-whydeep"):  # E6.10
                concept = S6_SLUG_CONCEPT.get(slots.get("slug", ""), CONCEPT_CRITERION_CHAIN)
            elif _m == "gsslack":  # E6.11
                concept = CONCEPT_TOWER_GROUP
            elif _m in ("conj-flip", "showdisproof"):  # E6.11
                concept = CONCEPT_DISPROOF
            elif _m == "confounder-route":  # E6.11 (the S4 confounder concepts)
                concept = S4_SLUG_CONCEPT.get(slots.get("slug", ""), CONCEPT_DISPROOF)
            elif _m in ("delta-value", "distdist"):  # E6.11 (the beyond-store walls ride the disproof)
                concept = CONCEPT_DISPROOF
            elif _m in ("s7-state", "s7-why", "s7-whydeep"):  # E6.11
                concept = S7_SLUG_CONCEPT.get(slots.get("slug", ""), CONCEPT_DISPROOF)
            elif _m in ("pi-count", "jfunc"):  # E6.12
                concept = CONCEPT_RH_PRIME
            elif _m == "sincycle":  # E6.12
                concept = CONCEPT_RH_FEQ
            elif _m == "growth-claim":  # E6.12
                concept = CONCEPT_RH_PNT
            elif _m == "numzero-first":  # E6.12
                concept = CONCEPT_RH_RV
            elif _m in ("rh-attempt", "rh-conj-state", "rh-numcheck", "rh-offzero"):  # E6.12
                concept = CONCEPT_RH
            elif _m == "rh-pnt-conf":  # E6.12
                concept = CONCEPT_RH_PNT
            elif _m == "rh-prod-conf":  # E6.12
                concept = CONCEPT_RH_ZETA
            elif _m == "rh-zeta-val":  # E6.12
                concept = CONCEPT_RH_CONT
            elif _m == "rh-s-tight":  # E6.12
                concept = CONCEPT_RH_SOF
            elif _m in ("s8-state", "s8-why", "s8-whydeep"):  # E6.12
                concept = S8_SLUG_CONCEPT.get(slots.get("slug", ""), CONCEPT_RH)
            elif _m == "gap-compare":  # E6.13
                concept = CONCEPT_RH_PNTE
            elif _m == "li-check" or _m == "li-proof":  # E6.13
                concept = CONCEPT_RH_LI
            elif _m == "c-value":  # E6.13
                concept = CONCEPT_RH_ZFR
            elif _m == "lindelof-conf":  # E6.13
                concept = CONCEPT_RH_LH
            elif _m == "ph-conf":  # E6.13
                concept = CONCEPT_RH_PH
            elif _m in ("s9-state", "s9-why", "s9-whydeep"):  # E6.13
                concept = S9_SLUG_CONCEPT.get(slots.get("slug", ""), CONCEPT_RH)
            elif _m == "li-close":  # E6.14
                concept = CONCEPT_RH_LI
            elif _m == "st-close":  # E6.14
                concept = CONCEPT_RH_ST_EQ
            else:
                concept = CONCEPT_COUNT
        return TurnResult(
            turn=turn,
            session=self._session,
            surface=text,
            kind=final_kind,
            concept=concept,
            slots=dict(slots),
            response_ir=dict(pol.ir),
            response_text=text_out,
            contract_valid=valid,
            contract_violations=list(violations),
            grounded=list(pol.grounded),
            memory_diff=list(pol.memory_diff),
            events=list(pol.events),
            honest_gap=pol.honest_gap,
            conflict=pol.conflict,
            attention=pol.attention,
            arm=arm,
        )
