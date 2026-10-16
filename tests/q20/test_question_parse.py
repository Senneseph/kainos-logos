"""Question parser: templates -> Query IR (CONSTRAINT/HYPOTHESIS), unknown -> UnresolvedRef (step 14.1)."""

from kainos.q20.question_parse import ParsedQuestion, parse_question


def test_is_it_property():
    p = parse_question("Is it alive?")
    assert p.query.kind == "CONSTRAINT"
    assert p.query.property == "alive"
    assert p.unresolved == ()


def test_does_it_have_property():
    p = parse_question("Does it have wheels?")
    assert p.query.kind == "CONSTRAINT"
    assert p.query.property == "has_wheels"
    p = parse_question("Does it have an engine?")
    assert p.query.property == "has_engine"


def test_how_many_part():
    p = parse_question("How many wheels?")
    assert p.query.kind == "CONSTRAINT"
    assert p.query.property == "wheel_count"
    p = parse_question("How many wheels does it have?")
    assert p.query.property == "wheel_count"


def test_is_it_a_category():
    p = parse_question("Is it a vehicle?")
    assert p.query.kind == "HYPOTHESIS"
    assert p.query.category == "vehicles"
    assert p.query.question_id == "q_cat_vehicles"


def test_can_it_carry():
    p = parse_question("Can it carry a person?")
    assert p.query.kind == "CONSTRAINT"
    assert p.query.property == "can_carry_person"


def test_canonical_surfaces_match_question_ids():
    p = parse_question("Was it made by humans?")
    assert p.query.kind == "CONSTRAINT"
    assert p.query.property == "manufactured"
    assert p.query.question_id == "q_made"
    p = parse_question("Is it green?")
    assert p.query.property == "is_green"


def test_case_and_punctuation_insensitive():
    p = parse_question("is it alive?")
    assert p.query.property == "alive"
    p = parse_question("IS IT ALIVE")
    assert p.query.property == "alive"


def test_unknown_word_is_unresolved_ref():
    p = parse_question("Is it tasty?")
    assert p.query is None
    assert p.unresolved == ("tasty",)
    p = parse_question("Does it have tentacles?")
    assert p.query is None
    assert p.unresolved == ("tentacles",)
    p = parse_question("How many legs?")
    assert p.query is None
    assert p.unresolved == ("legs",)
    p = parse_question("Is it a spaceship?")
    assert p.query is None
    assert p.unresolved == ("spaceship",)
    p = parse_question("Does it have a radio?")
    assert p.query is None
    assert p.unresolved == ("radio",)


def test_return_type_is_parsed_question():
    p = parse_question("Is it alive?")
    assert isinstance(p, ParsedQuestion)
    assert p.surface == "Is it alive?"
