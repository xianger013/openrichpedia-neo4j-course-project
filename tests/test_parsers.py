from openrichpedia_kg.parsers import (
    parse_city_hierarchy,
    parse_named_js_objects,
    parse_pair_relations,
)


def test_parse_city_hierarchy_handles_trailing_commas():
    text = open("tests/fixtures/city.js", encoding="utf-8").read()
    nodes, rels = parse_city_hierarchy(text, "city.js")
    by_id = {n.id: n for n in nodes}
    assert by_id["wd:Q956"].kind == "City"
    assert by_id["rps:0290"].name == "Forbidden City"
    assert {(r.source_id, r.target_id, r.type) for r in rels} == {
        ("wd:Q956", "rps:0290", "HAS_SIGHT"),
        ("wd:Q956", "rps:0286", "HAS_SIGHT"),
    }


def test_parse_named_js_objects_normalizes_qids():
    text = open("tests/fixtures/city_sight.js", encoding="utf-8").read()
    nodes = parse_named_js_objects(text, "city_sight.js", kind="Place", normalize_qids=True)
    assert [(n.id, n.name) for n in nodes] == [("wd:Q956", "Beijing"), ("wd:Q90", "Paris")]


def test_parse_named_js_objects_supports_single_quotes():
    text = open("tests/fixtures/people.js", encoding="utf-8").read()
    nodes = parse_named_js_objects(text, "people.js", kind="Person")
    assert nodes[0].id == "rpp:01"
    assert nodes[1].name == "Ada Lovelace"


def test_parse_pair_relations_accepts_short_and_long_keys():
    short = open("tests/fixtures/pic_city.js", encoding="utf-8").read()
    long = open("tests/fixtures/pic_people.js", encoding="utf-8").read()
    assert parse_pair_relations(short)[:1] == [("Q956_0", "Q956")]
    assert parse_pair_relations(long) == [("rp:032000", "rpp:01")]
