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

    def is_empty(self) -> bool:
        return len(self.adj) == 0

    def copy(self) -> "Graph[Vertex]":
        graph = Graph[Vertex]()
        for vertex in self.vertices():
            graph.add_vertex(vertex)
        for edge in self.edges():
            graph.add_edge(*edge)
        return graph

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

    def remove_vertex(self, vertex: Vertex) -> None:
        for neighbor in self.adj[vertex]:
            self.adj[neighbor].remove(vertex)
        del self.adj[vertex]
