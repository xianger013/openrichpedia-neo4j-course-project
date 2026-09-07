from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    name: str
    kind: str
    source_file: str


@dataclass(frozen=True, slots=True)
class Relationship:
    source_id: str
    target_id: str
    type: str
    source_file: str
