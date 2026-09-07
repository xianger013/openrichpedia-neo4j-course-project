from __future__ import annotations

import json
import re
from .model import Node, Relationship

_TRAILING_COMMA = re.compile(r",\s*([}\]])")
_OBJECT_RE = re.compile(r"\{([^{}]*)\}", re.S)
_FIELD_RE = re.compile(
    r'(?:["\']?)(?P<key>[A-Za-z_][A-Za-z0-9_]*)(?:["\']?)\s*:\s*(?:"(?P<double>(?:\\.|[^"])*)"|\'(?P<single>(?:\\.|[^\'])*)\')',
    re.S,
)


def normalize_qid(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"Q\d+", value):
        return f"wd:{value}"
    return value


def _decode_js_string(raw: str, quote: str) -> str:
    if quote == '"':
        return json.loads(f'"{raw}"')
    # JSON cannot directly decode single-quoted JavaScript strings.  Handle the
    # escapes present in this dataset without round-tripping Unicode through bytes.
    return (
        raw.replace(r"\'", "'")
        .replace(r'\"', '"')
        .replace(r"\n", "\n")
        .replace(r"\t", "\t")
        .replace(r"\\", "\\")
    )


def _fields(block: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for match in _FIELD_RE.finditer(block):
        if match.group("double") is not None:
            result[match.group("key")] = _decode_js_string(match.group("double"), "\"")
        else:
            result[match.group("key")] = _decode_js_string(match.group("single"), "'")
    return result


def parse_city_hierarchy(text: str, source_file: str) -> tuple[list[Node], list[Relationship]]:
    cleaned = _TRAILING_COMMA.sub(r"\1", text.strip())
    payload = json.loads(cleaned)
    nodes: list[Node] = []
    rels: list[Relationship] = []
    for city in payload:
        city_id = normalize_qid(str(city["value"]))
        nodes.append(Node(city_id, str(city["label"]), "City", source_file))
        for sight in city.get("children", []):
            sight_id = str(sight["value"])
            nodes.append(Node(sight_id, str(sight["label"]), "Sight", source_file))
            rels.append(Relationship(city_id, sight_id, "HAS_SIGHT", source_file))
    return nodes, rels


def parse_named_js_objects(
    text: str,
    source_file: str,
    *,
    kind: str,
    normalize_qids: bool = False,
) -> list[Node]:
    nodes: list[Node] = []
    for block in _OBJECT_RE.findall(text):
        fields = _fields(block)
        if "value" not in fields or "label" not in fields:
            continue
        node_id = normalize_qid(fields["value"]) if normalize_qids else fields["value"]
        nodes.append(Node(node_id, fields["label"], kind, source_file))
    return nodes


def parse_pair_relations(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for block in _OBJECT_RE.findall(text):
        fields = _fields(block)
        head = fields.get("h", fields.get("head"))
        tail = fields.get("t", fields.get("tail"))
        if head is not None and tail is not None:
            pairs.append((head, tail))
    return pairs
