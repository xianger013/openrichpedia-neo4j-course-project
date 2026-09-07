#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from getpass import getpass
from pathlib import Path

from neo4j import GraphDatabase

from openrichpedia_kg.neo4j_import import import_processed


def main() -> None:
    parser = argparse.ArgumentParser(description="Import processed OpenRichpedia CSV files into Neo4j.")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "neo4j://localhost:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--database", default=os.getenv("NEO4J_DATABASE", "neo4j"))
    args = parser.parse_args()
    password = os.getenv("NEO4J_PASSWORD") or getpass("Neo4j password: ")

    with GraphDatabase.driver(args.uri, auth=(args.user, password)) as driver:
        driver.verify_connectivity()
        result = import_processed(driver, args.processed_dir, database=args.database)
    print(f"导入完成：{result['nodes']} 个节点，{result['relationships']} 条关系。")


if __name__ == "__main__":
    main()
