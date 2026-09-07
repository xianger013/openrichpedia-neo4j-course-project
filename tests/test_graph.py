from pathlib import Path

from openrichpedia_kg.graph import build_graph, validate_graph

FIXTURES = Path('tests/fixtures')


def test_build_graph_creates_typed_nodes_and_expected_relationships():
    graph = build_graph(FIXTURES)
    nodes = {node.id: node for node in graph.nodes}
    rels = {(r.source_id, r.target_id, r.type) for r in graph.relationships}

    assert nodes['wd:Q956'].kind == 'City'  # City beats generic Place
    assert nodes['rps:0290'].kind == 'Sight'
    assert nodes['rpp:01'].kind == 'Person'
    assert nodes['img-city:Q956_0'].kind == 'Image'
    assert ('wd:Q956', 'rps:0290', 'HAS_SIGHT') in rels
    assert ('wd:Q956', 'img-city:Q956_0', 'HAS_IMAGE') in rels
    assert ('rpp:01', 'rp:032000', 'HAS_IMAGE') in rels
    assert (
        'http://rich.wangmengsd.com/resource/022510',
        'http://rich.wangmengsd.com/resource/000280',
        'CONTAINS',
    ) in rels


def test_validate_graph_reports_no_dangling_endpoints_for_fixture():
    graph = build_graph(FIXTURES)
    report = validate_graph(graph)
    assert report.errors == ()
    assert report.node_count == len(graph.nodes)
    assert report.relationship_count == len(graph.relationships)


def test_validate_graph_detects_duplicate_nodes_and_dangling_edges():
    from openrichpedia_kg.graph import GraphData
    from openrichpedia_kg.model import Node, Relationship

    graph = GraphData(
        nodes=(
            Node('x', 'X', 'Place', 'fixture'),
            Node('x', 'X duplicate', 'Place', 'fixture'),
        ),
        relationships=(Relationship('x', 'missing', 'HAS_IMAGE', 'fixture'),),
    )
    report = validate_graph(graph)
    assert '存在重复节点 ID。' in report.errors
    assert '关系终点不存在: missing' in report.errors


def test_build_graph_deduplicates_identical_relationships(tmp_path):
    import shutil

    for source in FIXTURES.iterdir():
        shutil.copy(source, tmp_path / source.name)
    pic_people = tmp_path / 'pic_people.js'
    original = pic_people.read_text(encoding='utf-8')
    pic_people.write_text(
        original.replace('];', '{"head":"rp:032000","tail":"rpp:01"},\n];'),
        encoding='utf-8',
    )
    graph = build_graph(tmp_path)
    matches = [
        r for r in graph.relationships
        if (r.source_id, r.target_id, r.type) == ('rpp:01', 'rp:032000', 'HAS_IMAGE')
    ]
    assert len(matches) == 1
