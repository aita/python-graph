from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generic

from .type_helper import Vertex


@dataclass
class Graph(Generic[Vertex]):
    """Undirected graph"""

    adj: dict[Vertex, set[Vertex]] = field(
        default_factory=lambda: defaultdict[Vertex, set[Vertex]](set)
    )

    def vertices(self) -> list[Vertex]:
        return list(self.adj.keys())

    def edges(self) -> set[tuple[Vertex, Vertex]]:
        return {
            (start, end)
            for start, ends in self.adj.items()
            for end in ends
            if start < end
        }

    def neighbors(self, vertex: Vertex) -> set[Vertex]:
        return self.adj[vertex].copy()

    def add_vertex(self, vertex: Vertex) -> None:
        if vertex not in self.adj:
            self.adj[vertex] = set()

    def add_edge(self, start: Vertex, end: Vertex) -> None:
        assert start != end
        self.adj[start].add(end)
        self.adj[end].add(start)
