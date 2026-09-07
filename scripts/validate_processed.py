#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ALLOWED_KINDS = {"City", "Sight", "Place", "Person", "Image"}
ALLOWED_RELS = {"HAS_SIGHT", "HAS_IMAGE", "CONTAINS"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated Neo4j CSV files.")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    nodes_path = args.processed_dir / "nodes.csv"
    rels_path = args.processed_dir / "relationships.csv"

    with nodes_path.open(encoding="utf-8-sig", newline="") as handle:
        nodes = list(csv.DictReader(handle))
    with rels_path.open(encoding="utf-8-sig", newline="") as handle:
        rels = list(csv.DictReader(handle))

    ids = [row["id"] for row in nodes]
    errors: list[str] = []
    if len(ids) != len(set(ids)):
        errors.append("nodes.csv 存在重复 id")
    id_set = set(ids)
    for row in nodes:
        if row["kind"] not in ALLOWED_KINDS:
            errors.append(f"未知节点类型: {row['kind']}")
    for row in rels:
        if row["type"] not in ALLOWED_RELS:
            errors.append(f"未知关系类型: {row['type']}")
        if row["source_id"] not in id_set or row["target_id"] not in id_set:
            errors.append(f"悬空关系: {row['source_id']} -> {row['target_id']}")

    if errors:
        raise SystemExit("验证失败:\n- " + "\n- ".join(dict.fromkeys(errors)))
    print(f"验证通过：{len(nodes)} 个节点，{len(rels)} 条关系。")


if __name__ == "__main__":
    main()
