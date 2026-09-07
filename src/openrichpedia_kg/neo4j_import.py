from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Iterable

NODE_LABELS = frozenset({"City", "Sight", "Place", "Person", "Image"})
RELATIONSHIP_TYPES = frozenset({"HAS_SIGHT", "HAS_IMAGE", "CONTAINS"})


def node_query(kind: str) -> str:
    if kind not in NODE_LABELS:
        raise ValueError(f"Unsupported node label: {kind}")
    return f"""
UNWIND $rows AS row
MERGE (n:Entity {{id: row.id}})
SET n.name = row.name,
    n.kind = row.kind,
    n.source_file = row.source_file
SET n:{kind}
""".strip()


def relationship_query(rel_type: str) -> str:
    if rel_type not in RELATIONSHIP_TYPES:
        raise ValueError(f"Unsupported relationship type: {rel_type}")
    return f"""
UNWIND $rows AS row
MATCH (source:Entity {{id: row.source_id}})
MATCH (target:Entity {{id: row.target_id}})
MERGE (source)-[:{rel_type}]->(target)
""".strip()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _chunks(rows: list[dict[str, str]], size: int) -> Iterable[list[dict[str, str]]]:
    for start in range(0, len(rows), size):
        yield rows[start : start + size]


def import_processed(
    driver,
    processed_dir: str | Path,
    *,
    database: str = "neo4j",
    batch_size: int = 1000,
) -> dict[str, int]:
    processed_dir = Path(processed_dir)
    nodes = _read_csv(processed_dir / "nodes.csv")
    relationships = _read_csv(processed_dir / "relationships.csv")

    grouped_nodes: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in nodes:
        if row["kind"] not in NODE_LABELS:
            raise ValueError(f"Unsupported node label in CSV: {row['kind']}")
        grouped_nodes[row["kind"]].append(row)

    grouped_relationships: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in relationships:
        if row["type"] not in RELATIONSHIP_TYPES:
            raise ValueError(f"Unsupported relationship type in CSV: {row['type']}")
        grouped_relationships[row["type"]].append(row)

    with driver.session(database=database) as session:
        session.run(
            "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS "
            "FOR (n:Entity) REQUIRE n.id IS UNIQUE"
        ).consume()
        for kind, rows in grouped_nodes.items():
            for batch in _chunks(rows, batch_size):
                session.run(node_query(kind), rows=batch).consume()
        for rel_type, rows in grouped_relationships.items():
            for batch in _chunks(rows, batch_size):
                session.run(relationship_query(rel_type), rows=batch).consume()

    return {"nodes": len(nodes), "relationships": len(relationships)}
