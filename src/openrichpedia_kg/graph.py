from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .model import Node, Relationship
from .parsers import normalize_qid, parse_city_hierarchy, parse_named_js_objects, parse_pair_relations

NODE_PRIORITY = {"Image": 0, "Place": 1, "Person": 2, "Sight": 3, "City": 4}
ALLOWED_RELATIONSHIP_TYPES = frozenset({"HAS_SIGHT", "HAS_IMAGE", "CONTAINS"})
REQUIRED_FILES = (
    "city.js",
    "city_sight.js",
    "pic_city.js",
    "people.js",
    "pic_people.js",
    "contain.js",
)


@dataclass(frozen=True, slots=True)
class GraphData:
    nodes: tuple[Node, ...]
    relationships: tuple[Relationship, ...]


@dataclass(frozen=True, slots=True)
class ValidationReport:
    node_count: int
    relationship_count: int
    kind_counts: dict[str, int]
    relationship_type_counts: dict[str, int]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def _read(raw_dir: Path, filename: str) -> str:
    path = raw_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"缺少原始数据文件 {path}。请先运行 scripts/fetch_openrichpedia.py 下载固定版本数据。"
        )
    return path.read_text(encoding="utf-8")


def _uri_name(uri: str) -> str:
    path = urlparse(uri).path.rstrip("/")
    return path.rsplit("/", 1)[-1] if path else uri


def _merge_node(store: dict[str, Node], node: Node) -> None:
    current = store.get(node.id)
    if current is None or NODE_PRIORITY[node.kind] > NODE_PRIORITY[current.kind]:
        store[node.id] = node
        return
    # Keep a useful human-readable name when priority is equal and the current
    # node only contains its identifier as a fallback label.
    if NODE_PRIORITY[node.kind] == NODE_PRIORITY[current.kind] and current.name == current.id and node.name != node.id:
        store[node.id] = node


def build_graph(raw_dir: str | Path) -> GraphData:
    raw_dir = Path(raw_dir)
    nodes: dict[str, Node] = {}
    relationships: set[Relationship] = set()

    city_nodes, city_rels = parse_city_hierarchy(_read(raw_dir, "city.js"), "city.js")
    for node in city_nodes:
        _merge_node(nodes, node)
    relationships.update(city_rels)

    for node in parse_named_js_objects(
        _read(raw_dir, "city_sight.js"), "city_sight.js", kind="Place", normalize_qids=True
    ):
        _merge_node(nodes, node)

    for image_id, entity_id in parse_pair_relations(_read(raw_dir, "pic_city.js")):
        source_id = normalize_qid(entity_id)
        target_id = f"img-city:{image_id}"
        if source_id not in nodes:
            _merge_node(nodes, Node(source_id, source_id, "Place", "pic_city.js"))
        _merge_node(nodes, Node(target_id, image_id, "Image", "pic_city.js"))
        relationships.add(Relationship(source_id, target_id, "HAS_IMAGE", "pic_city.js"))

    for node in parse_named_js_objects(_read(raw_dir, "people.js"), "people.js", kind="Person"):
        _merge_node(nodes, node)

    for image_id, person_id in parse_pair_relations(_read(raw_dir, "pic_people.js")):
        if person_id not in nodes:
            _merge_node(nodes, Node(person_id, person_id, "Person", "pic_people.js"))
        _merge_node(nodes, Node(image_id, image_id, "Image", "pic_people.js"))
        relationships.add(Relationship(person_id, image_id, "HAS_IMAGE", "pic_people.js"))

    for head, tail in parse_pair_relations(_read(raw_dir, "contain.js")):
        _merge_node(nodes, Node(head, _uri_name(head), "Image", "contain.js"))
        _merge_node(nodes, Node(tail, _uri_name(tail), "Image", "contain.js"))
        relationships.add(Relationship(head, tail, "CONTAINS", "contain.js"))

    sorted_nodes = tuple(sorted(nodes.values(), key=lambda n: (n.kind, n.id)))
    sorted_rels = tuple(sorted(relationships, key=lambda r: (r.type, r.source_id, r.target_id)))
    return GraphData(sorted_nodes, sorted_rels)


def validate_graph(graph: GraphData) -> ValidationReport:
    ids = {node.id for node in graph.nodes}
    errors: list[str] = []
    warnings: list[str] = []

    if len(ids) != len(graph.nodes):
        errors.append("存在重复节点 ID。")

    for rel in graph.relationships:
        if rel.type not in ALLOWED_RELATIONSHIP_TYPES:
            errors.append(f"发现不支持的关系类型: {rel.type}")
        if rel.source_id not in ids:
            errors.append(f"关系起点不存在: {rel.source_id}")
        if rel.target_id not in ids:
            errors.append(f"关系终点不存在: {rel.target_id}")

    kind_counts: dict[str, int] = {}
    for node in graph.nodes:
        kind_counts[node.kind] = kind_counts.get(node.kind, 0) + 1
    rel_counts: dict[str, int] = {}
    for rel in graph.relationships:
        rel_counts[rel.type] = rel_counts.get(rel.type, 0) + 1

    if not graph.nodes:
        warnings.append("图中没有节点。")
    if not graph.relationships:
        warnings.append("图中没有关系。")

    return ValidationReport(
        node_count=len(graph.nodes),
        relationship_count=len(graph.relationships),
        kind_counts=dict(sorted(kind_counts.items())),
        relationship_type_counts=dict(sorted(rel_counts.items())),
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(warnings),
    )
