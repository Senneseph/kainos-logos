"""The M3 curriculum map (T7 #157) — bands are DATA (P11).

The owner's 2026-08-22 directives (board #157, comment 450) ARE the
band map:

1. Geometry learns CONCURRENTLY with math from the K–5 band (not a
   later band) — band 1 = numerics ∥ geometry, on the same
   teachable-strip seam (one line, two domains).
2. Later bands ALIGN physics with math on overlapping topics
   (algebra ∥ kinematics; geometry-advanced ∥ vectors/statics;
   calculus ∥ mechanics; statistics ∥ probabilistic physics), and
   each band ends on a JOINT evaluation — one probe set spanning the
   aligned domains, not two silos.

A band is `implemented` only when its strip is built, taught,
probed, and verified by an official experiment (band 1 = e6.5,
2026-08-22). `declared` bands carry the map's names and alignments
— no mechanism, no probes, no claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kainos.tutor.mastery import BANDS

__all__ = ["BAND_MAP", "BandSpec", "band_by_name", "validate_band_map"]


@dataclass(frozen=True)
class BandSpec:
    """One rung of the curriculum sweep, as store-data would name it."""

    name: str  # band-1 .. band-5
    band: str  # mastery band vocabulary (pre-k | k-5 | 6-8 | 9-12 | college-1)
    domains: tuple[str, ...]  # the math domains this band teaches
    aligned_physics: tuple[str, ...]  # directive #2: the physics side (may be empty)
    concepts: tuple[str, ...]  # the concept ids the band owns
    status: str  # "implemented" | "declared"
    evidence: tuple[str, ...] = field(default_factory=tuple)  # official experiment(s)

    def __post_init__(self) -> None:
        if self.band not in BANDS:
            raise ValueError(f"band {self.name!r}: unknown mastery band {self.band!r}")
        if self.status not in ("implemented", "declared"):
            raise ValueError(f"band {self.name!r}: status must be implemented|declared, got {self.status!r}")
        if self.status == "implemented" and not self.evidence:
            raise ValueError(f"band {self.name!r}: an implemented band must cite its official evidence")


#: The declared M3 band map (the owner's directives, verbatim in scope).
BAND_MAP: tuple[BandSpec, ...] = (
    BandSpec(
        name="band-1",
        band="k-5",
        domains=("arithmetic", "geometry"),
        aligned_physics=(),  # directive #1: the K–5 band IS geometry ∥ math
        concepts=(
            "count-successor",
            "add-within-10",
            "add-two-digit",
            "sub-within-30",
            "mult-within-100",
            "compare-numbers",
            "shape-triangle",
            "shape-square",
            "shape-rectangle",
            "shape-circle",
        ),
        status="implemented",
        evidence=("e6.5",),  # official: results/phase-6/e6.5.json (2026-08-22)
    ),
    BandSpec(
        name="band-2",
        band="6-8",
        domains=("algebra",),
        aligned_physics=("kinematics",),  # algebra ∥ kinematics (directive #2)
        concepts=(
            "alg-inverse-1step",
            "alg-inverse-mul",
            "alg-two-step",
            "kin-distance",
            "kin-position",
            "kin-solve-time",
            "kin-rate",
        ),
        status="implemented",
        evidence=("e6.6",),  # official: results/phase-6/e6.6.json (2026-08-22)
    ),
    BandSpec(
        name="band-3",
        band="9-12",
        domains=("geometry-advanced",),
        aligned_physics=("vectors", "statics"),  # geometry ∥ vectors/statics
        concepts=(
            "geom-perimeter",
            "geom-area",
            "geom-area-triangle",
            "stat-net-1d",
            "stat-moment",
            "stat-balance",
        ),
        status="implemented",
        evidence=("e6.7",),  # official: results/phase-6/e6.7.json (2026-08-22)
    ),
    BandSpec(
        name="band-4",
        band="9-12",
        domains=("calculus",),
        aligned_physics=("mechanics",),  # calculus ∥ mechanics
        concepts=(),
        status="declared",
    ),
    BandSpec(
        name="band-5",
        band="college-1",
        domains=("statistics",),
        aligned_physics=("probabilistic physics",),  # statistics ∥ probabilistic physics
        concepts=(),
        status="declared",
    ),
    # SAVANT-TRACK (owner 2026-08-22, pre-registered in
    # experiments.md §SAVANT-TRACK): the learning-bound stress test.
    # CODEX must learn, from source-level material only (the paper
    # never reaches the student — the denylist), everything the
    # unit-distance-disproof paper rests on, and reproduce its
    # conclusions. A separate curriculum axis (domain "savant").
    # band-4 (calculus ∥ mechanics) is PARKED until the savant test
    # concludes (owner directive), then folds back into this map.
    BandSpec(
        name="savant-1",
        band="college-1",
        domains=("unit-distance",),
        aligned_physics=(),
        concepts=(
            "unit-distance",
            "grid-lattice",
            "gaussian-int",
            "circle-pair-2",
            "kst-bound",
            "sst-bound",
            "erdos-conj",
            "norm-flat",
            "norm-convex",
            "norm-generic",
        ),
        status="implemented",
        evidence=("e6.8",),  # official: results/phase-6/e6.8.json (2026-08-22)
    ),
    BandSpec(
        name="savant-2",
        band="college-1",
        domains=("number-fields",),
        aligned_physics=(),
        concepts=(
            "number-field",
            "prime-split",
            "mod4-split",
            "disc-rd",
            "adjoin-i",
            "cyclotomic-cubic",
            "char-cutout",
            "class-bound",
            "chebotarev",
            "pnt-ap",
            "frattini",
            "golod-shaf",
            "shafarevich",
            "cm-conj",
            "minkowski-embed",
            "hajir-maire",
        ),
        status="implemented",
        evidence=("e6.9",),  # official: results/phase-6/e6.9.json (2026-08-22)
    ),
    BandSpec(
        name="savant-3",
        band="college-1",
        domains=("geometric-criterion",),
        aligned_physics=(),
        concepts=(
            "window-setup",
            "averaging",
            "projection",
            "packing",
            "slack-margins",
            "criterion-chain",
        ),
        status="implemented",
        evidence=("e6.10",),  # official: results/phase-6/e6.10.json
    ),
    BandSpec(
        name="savant-4",
        band="college-1",
        domains=("tower",),
        aligned_physics=(),
        concepts=(
            "tower-base",
            "tower-group",
            "tower-primes",
            "tower-class",
            "disproof",
        ),
        status="implemented",
        evidence=("e6.11",),  # official: results/phase-6/e6.11.json (S7: tower => disproof, the savant test proper)
    ),
    # RH-TRACK (owner 2026-08-23, pre-registered in experiments.md
    # §E6.12): the Riemann Hypothesis as the next target — "a similar
    # training technique as before and then attempt the Hypothesis
    # itself". The difference from the savant test: we do NOT know
    # whether a proof exists, nor exactly what material a proof would
    # require — so the track throws as much of the important
    # literature's content at the store as the pre-regs authorize.
    # Three bands: S8 the ζ apparatus (foundations), S9 the criterion
    # gallery (candidate routes to the hypothesis), S10 the attempt
    # (the RH test proper). A separate curriculum axis (domain "rh").
    BandSpec(
        name="rh-1",
        band="college-1",
        domains=("rh",),
        aligned_physics=(),
        concepts=(
            "zeta-series",
            "zeta-cont",
            "func-eq",
            "critical-strip",
            "prime-count",
            "pnt",
            "rv-count",
            "s-of-t",
            "riemann",
        ),
        status="implemented",
        evidence=("e6.12",),  # official: results/phase-6/e6.12.json (S8: the ζ apparatus; the conjecture enters as open)
    ),
    BandSpec(
        name="rh-2",
        band="college-1",
        domains=("rh",),
        aligned_physics=(),
        concepts=(
            "psi-eq",
            "pi-eq",
            "st-eq",
            "li-criterion",
            "polya-hilbert",
            "lindelof",
            "zero-free",
            "pnt-error",
            "hardy-line",
            "zero-density",
        ),
        status="implemented",
        evidence=("e6.13",),  # official: results/phase-6/e6.13.json (S9: the criterion gallery; the store's own derived gap grounds the attempt)
    ),
    BandSpec(
        name="rh-3",
        band="college-1",
        domains=("rh",),
        aligned_physics=(),
        concepts=(),
        status="implemented",
        evidence=("e6.14",),  # official: results/phase-6/e6.14.json (S10: the attempt — the maximal assembly rh-reach, the S10-form wall, the discovery-candidate invariant)
    ),
)


def band_by_name(name: str) -> BandSpec:
    for b in BAND_MAP:
        if b.name == name:
            return b
    raise KeyError(f"unknown band: {name!r}")


def validate_band_map(registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """The map's integrity, as a VALUE (pure): band-vocabulary sanity,
    no duplicate concepts across bands, and — when a concept registry
    is passed — that every declared concept id of an IMPLEMENTED band
    exists in it with the band's mastery band. `declared` bands with
    no concepts are structurally fine (nothing invented)."""

    problems: list[str] = []
    seen: dict[str, str] = {}
    for b in BAND_MAP:
        for c in b.concepts:
            if c in seen:
                problems.append(f"concept {c!r} in two bands: {seen[c]} and {b.name}")
            seen[c] = b.name
        if registry is not None and b.status == "implemented":
            rank = {name: i for i, name in enumerate(BANDS)}
            for c in b.concepts:
                cc = registry.get(c)
                if cc is None:
                    problems.append(f"{b.name}: concept {c!r} not in the concept registry")
                # a band owns its rung and may INHERIT lower-rung concepts
                # (the K–5 strip stands on the pre-k counting base)
                elif rank.get(cc.band, 99) > rank[b.band]:
                    problems.append(f"{b.name}: concept {c!r} is in mastery band {cc.band!r}, above {b.band!r}")
    return {"bands": len(BAND_MAP), "implemented": sum(1 for b in BAND_MAP if b.status == "implemented"), "problems": problems}
