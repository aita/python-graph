import heapq
from dataclasses import dataclass
from typing import Generic, TypeVar

from .graph import Graph
from .type_helper import Vertex as V

C = TypeVar("C")


def greedy(graph: Graph[V], colors: list[C]) -> dict[V, C]:
    """
    Greedy algorithm for graph coloring.
    """
    coloring: dict[V, C] = {}

    for vertex in graph.vertices():
        if vertex in coloring:
            continue

        for color in colors:
            if all(
                coloring.get(neighbor) != color for neighbor in graph.neighbors(vertex)
            ):
                coloring[vertex] = color
                break
        else:
            raise ValueError("No coloring found")

    return coloring


def welsh_powell(graph: Graph[V], colors: list[C]) -> dict[V, C]:
    """
    Welsh-Powell algorithm for graph coloring.
    """
    coloring: dict[V, C] = {}

    color_index = 0
    vertices = sorted(graph.vertices(), key=lambda v: len(graph.neighbors(v)))
    for i, v1 in enumerate(vertices):
        if v1 in coloring:
            continue

        if color_index >= len(colors):
            raise ValueError("No coloring found")
        color = colors[color_index]
        color_index += 1
        coloring[v1] = color

        for v2 in vertices[i:]:
            if v2 in coloring:
                continue

            if all(coloring.get(neighbor) != color for neighbor in graph.neighbors(v2)):
                coloring[v2] = color
                break

    return coloring


@dataclass(order=True)
class DSATURVertex(Generic[V]):
    saturation_degree: int
    degree: int
    vertex: V


def dsatur(graph: Graph[V], colors: list[C]) -> dict[V, C]:
    """
    DSATUR algorithm for graph coloring.
    """
    coloring: dict[V, C] = {}
    vertices = {
        v: DSATURVertex(0, -len(graph.neighbors(v)), v) for v in graph.vertices()
    }

    queue = list(vertices.values())
    heapq.heapify(queue)
    while queue:
        v = heapq.heappop(queue)

        for color in colors:
            if all(
                coloring.get(neighbor) != color
                for neighbor in graph.neighbors(v.vertex)
            ):
                coloring[v.vertex] = color
                break
        else:
            raise ValueError("No coloring found")

        for neighbor in graph.neighbors(v.vertex):
            vertices[neighbor].saturation_degree -= 1
        heapq.heapify(queue)

    return coloring


def rlf(graph: Graph[V], colors: list[C]) -> dict[V, C]:
    """
    RLF algorithm for graph coloring.
    """
    coloring: dict[V, C] = {}

    k = 0
    G = graph.copy()
    while not G.is_empty():
        U = G.vertices()
        v0 = max(U, key=lambda v: len(G.neighbors(v)))
        S = {v0}
        while True:
            A = [x for x in U if all(y not in S for y in G.neighbors(x))]
            if not A:
                break
            v = min(A, key=lambda x: len(G.neighbors(x) - S))
            S.add(v)
            U.remove(v)
        for v in S:
            G.remove_vertex(v)
        if k >= len(colors):
            raise ValueError("No coloring found")
        for v in S:
            coloring[v] = colors[k]
        k += 1

    return coloring
