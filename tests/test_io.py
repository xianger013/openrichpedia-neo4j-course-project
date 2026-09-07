import csv
import json
from pathlib import Path

from openrichpedia_kg.graph import build_graph
from openrichpedia_kg.io import write_processed


def test_write_processed_creates_csv_and_stats(tmp_path):
    graph = build_graph(Path('tests/fixtures'))
    write_processed(graph, tmp_path)

    nodes = list(csv.DictReader((tmp_path / 'nodes.csv').open(encoding='utf-8-sig')))
    rels = list(csv.DictReader((tmp_path / 'relationships.csv').open(encoding='utf-8-sig')))
    stats = json.loads((tmp_path / 'stats.json').read_text(encoding='utf-8'))

    assert nodes[0].keys() == {'id', 'name', 'kind', 'source_file'}
    assert rels[0].keys() == {'source_id', 'target_id', 'type', 'source_file'}
    assert stats['node_count'] == len(nodes)
    assert stats['relationship_count'] == len(rels)
    assert stats['errors'] == []
