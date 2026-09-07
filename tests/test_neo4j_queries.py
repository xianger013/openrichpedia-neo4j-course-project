import pytest

from openrichpedia_kg.neo4j_import import node_query, relationship_query


def test_node_query_whitelists_labels():
    query = node_query('City')
    assert 'SET n:City' in query
    with pytest.raises(ValueError):
        node_query('City`) MATCH (x) DETACH DELETE x //')


def test_relationship_query_whitelists_relationship_type():
    query = relationship_query('HAS_IMAGE')
    assert 'MERGE (source)-[:HAS_IMAGE]->(target)' in query
    with pytest.raises(ValueError):
        relationship_query('DELETE_ALL')
