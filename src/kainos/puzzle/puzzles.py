"""E4.1 puzzle instances — pure data (the core never hardcodes a puzzle).

``EINSTEIN``: the owner's appendix text, encoded clue-for-clue in the four
canonical forms, clue ids = line order in the appendix. The one semantic
choice: clue 4 "the green house is on the left of the white house" is
encoded ``Left`` (immediately left — the STRICTER reading). The dev run
tests both readings; whichever solves is adopted and recorded (D-e1,
phase-4 results).

``TRANSFER_4x4``: arm E — a DIFFERENT puzzle with DIFFERENT dimension names
and no house/colour at all; the SAME core code must pick it up from the
spec data, solve it uniquely, and prove it (pattern transfer is the
experiment: zero code changes).
"""

from __future__ import annotations

from kainos.puzzle.core import At, Dimension, Left, Next, Pair, PuzzleSpec

__all__ = ["EINSTEIN", "EINSTEIN_FISH_TERM", "EINSTEIN_HIDDEN_ARM", "TRANSFER_4x4"]

#: The question of the puzzle: "who owns the fish?"
EINSTEIN_FISH_TERM = "fish"

#: Arm B hides exactly this term (typed-but-unknown): the answer's own term.
EINSTEIN_HIDDEN_ARM = frozenset({"fish"})

_COLOR = Dimension("color", ("red", "green", "white", "yellow", "blue"))
_NATION = Dimension("nationality", ("brit", "swede", "dane", "norwegian", "german"))
_DRINK = Dimension("drink", ("tea", "coffee", "milk", "beer", "water"))
_CIGAR = Dimension("cigar", ("pall_mall", "dunhill", "blends", "blue_master", "prince"))
_PET = Dimension("pet", ("dogs", "birds", "cats", "horses", "fish"))

#: Clue texts, verbatim from the appendix (ids = 1-based line order).
EINSTEIN_CLUE_TEXTS: tuple[str, ...] = (
    "The Brit lives in the red house",
    "The Swede keeps dogs as pets",
    "The Dane drinks tea",
    "The green house is on the left of the white house",
    "The green house's owner drinks coffee",
    "The person who smokes Pall Mall rears birds",
    "The owner of the yellow house smokes Dunhill",
    "The man living in the center house drinks milk",
    "The Norwegian lives in the first house",
    "The man who smokes blends lives next to the one who keeps cats",
    "The man who keeps horses lives next to the man who smokes Dunhill",
    "The owner who smokes BlueMaster drinks beer",
    "The German smokes Prince",
    "The Norwegian lives next to the blue house",
    "The man who smokes blend has a neighbor who drinks water",
)

EINSTEIN_CLUES = (
    Pair("color", "red", "nationality", "brit"),  # 1
    Pair("nationality", "swede", "pet", "dogs"),  # 2
    Pair("nationality", "dane", "drink", "tea"),  # 3
    Left("color", "green", "color", "white"),  # 4 (adjacent reading; D-e1)
    Pair("color", "green", "drink", "coffee"),  # 5
    Pair("cigar", "pall_mall", "pet", "birds"),  # 6
    Pair("color", "yellow", "cigar", "dunhill"),  # 7
    At("drink", "milk", 3),  # 8 (center of 5)
    At("nationality", "norwegian", 1),  # 9
    Next("cigar", "blends", "pet", "cats"),  # 10
    Next("pet", "horses", "cigar", "dunhill"),  # 11
    Pair("cigar", "blue_master", "drink", "beer"),  # 12
    Pair("nationality", "german", "cigar", "prince"),  # 13
    Next("nationality", "norwegian", "color", "blue"),  # 14
    Next("cigar", "blends", "drink", "water"),  # 15
)

EINSTEIN = PuzzleSpec(5, (_COLOR, _NATION, _DRINK, _CIGAR, _PET), EINSTEIN_CLUES)

#: Arm D: the contradictory clue appended to the full set (clue id 16):
#: "The Norwegian lives in the fifth house" vs clue 9 (first house).
EINSTEIN_CONTRADICTION_CLUE = At("nationality", "norwegian", 5)
EINSTEIN_CONTRADICTION_TEXT = "The Norwegian lives in the fifth house"

# ── arm E: the transfer puzzle (4 positions, 4 NEW dimensions) ─────────────

_WALL = Dimension("wall", ("gold", "red", "green", "blue"))
_PERSON = Dimension("person", ("ada", "ben", "cy", "dee"))
_MEAL = Dimension("meal", ("tofu", "lamb", "salmon", "rice"))
_MUSIC = Dimension("music", ("jazz", "drums", "piano", "cello"))

TRANSFER_CLUES = (
    At("person", "ada", 1),  # 1 Ada lives in the first room
    Pair("wall", "red", "person", "ben"),  # 2 Ben's room has a red wall
    Pair("wall", "gold", "music", "jazz"),  # 3 the gold-walled resident plays jazz
    Pair("meal", "salmon", "person", "cy"),  # 4 Cy eats salmon
    Next("person", "ada", "music", "drums"),  # 5 Ada's neighbor plays drums
    Left("wall", "blue", "wall", "gold"),  # 6 the blue wall is left of the gold wall
    Pair("wall", "green", "meal", "rice"),  # 7 the green-walled room's meal is rice
    Pair("music", "piano", "meal", "tofu"),  # 8 the piano player's meal is tofu
    Next("person", "cy", "music", "jazz"),  # 9 Cy's neighbor plays jazz
)

TRANSFER_4x4 = PuzzleSpec(4, (_WALL, _PERSON, _MEAL, _MUSIC), TRANSFER_CLUES)
TRANSFER_CLUE_TEXTS: tuple[str, ...] = (
    "Ada lives in the first room",
    "Ben's room has a red wall",
    "The resident of the gold-walled room plays jazz",
    "Cy eats salmon",
    "Ada's neighbor plays drums",
    "The blue-walled room is on the left of the gold-walled room",
    "The meal in the green-walled room is rice",
    "The piano player's meal is tofu",
    "Cy's neighbor plays jazz",
)

