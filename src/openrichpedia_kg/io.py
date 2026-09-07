from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .graph import GraphData, validate_graph


def write_processed(graph: GraphData, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "nodes.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "name", "kind", "source_file"])
        writer.writeheader()
        for node in graph.nodes:
            writer.writerow(asdict(node))

    with (output_dir / "relationships.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["source_id", "target_id", "type", "source_file"]
        )
        writer.writeheader()
        for rel in graph.relationships:
            writer.writerow(asdict(rel))

    report = validate_graph(graph)
    stats = {
        "node_count": report.node_count,
        "relationship_count": report.relationship_count,
        "kind_counts": report.kind_counts,
        "relationship_type_counts": report.relationship_type_counts,
        "errors": list(report.errors),
        "warnings": list(report.warnings),
    }
    (output_dir / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
