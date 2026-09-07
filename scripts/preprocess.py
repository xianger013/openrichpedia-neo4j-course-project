#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from openrichpedia_kg.graph import build_graph, validate_graph
from openrichpedia_kg.io import write_processed


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse OpenRichpedia source files into Neo4j-ready CSV files.")
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()

    graph = build_graph(args.raw_dir)
    report = validate_graph(graph)
    if report.errors:
        raise SystemExit("数据验证失败:\n- " + "\n- ".join(report.errors))
    write_processed(graph, args.output_dir)
    print(json.dumps({
        "nodes": report.node_count,
        "relationships": report.relationship_count,
        "kinds": report.kind_counts,
        "relationship_types": report.relationship_type_counts,
        "output": str(args.output_dir),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
