import pytest

from graph import Graph

COLORS = ["red", "blue", "green", "yellow", "orange", "purple"]


class ColoringTestBase:
    def _callFUT(self, graph, colors):
        raise NotImplementedError

    @pytest.mark.parametrize(
        "edges, chromatic_number",
        [
            (
                [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")],
                2,
            ),
            (
                [
                    ("a", "b"),
                    ("b", "c"),
                    ("c", "d"),
                    ("d", "a"),
                    ("a", "c"),
                ],
                3,
            ),
            (
                [
                    ("a", "b"),
                    ("b", "c"),
                    ("c", "d"),
                    ("d", "a"),
                    ("a", "c"),
                    ("b", "d"),
                ],
                4,
            ),
            (
                [
                    ("a", "b"),
                    ("b", "c"),
                    ("c", "d"),
                    ("d", "e"),
                    ("e", "a"),
                    ("b", "d"),
                    ("a", "c"),
                    ("b", "d"),
                    ("c", "e"),
                    ("d", "a"),
                    ("e", "b"),
                ],
                5,
            ),
            (
                [
                    ("a", "b"),
                    ("b", "c"),
                    ("c", "d"),
                    ("d", "e"),
                    ("e", "f"),
                    ("f", "a"),
                    ("a", "c"),
                    ("b", "d"),
                    ("a", "c"),
                    ("b", "d"),
                    ("c", "e"),
                    ("d", "f"),
                    ("e", "a"),
                    ("f", "b"),
                ],
                3,
            ),
        ],
    )
    def test_good_pattern(self, edges, chromatic_number):
        vertices = list(dict.fromkeys(v for e in edges for v in e))

        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert set(result.keys()) == set(vertices)
        assert len(set(result.values())) == chromatic_number

        for vertex, color in result.items():
            assert color in COLORS

            for neighbor in graph.neighbors(vertex):
                assert result[neighbor] != color

    @pytest.mark.parametrize(
        "vertices, edges, chromatic_number",
        [
            (
                ["1", "2", "3", "4", "5", "6", "7", "8"],
                [
                    ("1", "4"),
                    ("1", "6"),
                    ("1", "8"),
                    ("2", "3"),
                    ("2", "5"),
                    ("2", "7"),
                    ("3", "6"),
                    ("3", "8"),
                    ("4", "5"),
                    ("4", "7"),
                    ("5", "8"),
                    ("6", "7"),
                ],
                2,
            ),
        ],
    )
    def test_bad_pattern(self, vertices, edges, chromatic_number):
        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert set(result.keys()) == set(vertices)
        assert chromatic_number <= len(set(result.values())) <= len(vertices) / 2

        for vertex, color in result.items():
            assert color in COLORS

            for neighbor in graph.neighbors(vertex):
                assert result[neighbor] != color


class TestGreedy(ColoringTestBase):
    def _callFUT(self, graph, colors):
        from graph.coloring import greedy

        return greedy(graph, colors)


class TestWelshPowell(ColoringTestBase):
    def _callFUT(self, graph, colors):
        from graph.coloring import welsh_powell

        return welsh_powell(graph, colors)


class TestDSatur(ColoringTestBase):
    def _callFUT(self, graph, colors):
        from graph.coloring import dsatur

        return dsatur(graph, colors)
