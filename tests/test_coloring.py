import pytest

from graph import Graph

COLORS = ["red", "blue", "green", "yellow", "orange", "purple"]


class TestGreedy:
    def _callFUT(self, graph, colors):
        from graph.coloring import greedy

        return greedy(graph, colors)

    def test_empty(self):
        graph = Graph()
        result = self._callFUT(graph, COLORS)
        assert result == {}

    def test_2_orphan_vertices(self):
        graph = Graph()
        graph.add_vertex("a")
        graph.add_vertex("b")
        result = self._callFUT(graph, COLORS)
        assert result == {"a": "red", "b": "red"}

    @pytest.mark.parametrize(
        "edges, expected",
        [
            (
                [("a", "b"), ("b", "c")],
                {"a": "red", "b": "blue", "c": "red"},
            ),
            (
                [("a", "b"), ("b", "c"), ("c", "a")],
                {"a": "red", "b": "blue", "c": "green"},
            ),
        ],
    )
    def test_3_vertices(self, edges, expected):
        vertices = list(dict.fromkeys(v for e in edges for v in e))

        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert result == expected

    @pytest.mark.parametrize(
        "edges, expected",
        [
            (
                [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")],
                {"a": "red", "b": "blue", "c": "red", "d": "blue"},
            ),
            (
                [
                    ("a", "b"),
                    ("b", "c"),
                    ("c", "d"),
                    ("d", "a"),
                    ("a", "c"),
                ],
                {"a": "red", "b": "blue", "c": "green", "d": "blue"},
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
                {"a": "red", "b": "blue", "c": "green", "d": "yellow"},
            ),
        ],
    )
    def test_4_vertices(self, edges, expected):
        vertices = list(dict.fromkeys(v for e in edges for v in e))

        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert result == expected


class TestWelshPowell:
    def _callFUT(self, graph, colors):
        from graph.coloring import welsh_powell

        return welsh_powell(graph, colors)

    @pytest.mark.parametrize(
        "edges, expected_num_colors",
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
    def test(self, edges, expected_num_colors):
        vertices = list(dict.fromkeys(v for e in edges for v in e))

        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert len(set(result.values())) == expected_num_colors

        for vertex, color in result.items():
            assert color in COLORS

            for neighbor in graph.neighbors(vertex):
                assert result[neighbor] != color


class TestDSATUR:
    def _callFUT(self, graph, colors):
        from graph.coloring import dsatur

        return dsatur(graph, colors)

    @pytest.mark.parametrize(
        "edges, expected_num_colors",
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
    def test(self, edges, expected_num_colors):
        vertices = list(dict.fromkeys(v for e in edges for v in e))

        graph = Graph()
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            graph.add_edge(*e)

        result = self._callFUT(graph, COLORS)
        assert len(set(result.values())) == expected_num_colors

        for vertex, color in result.items():
            assert color in COLORS

            for neighbor in graph.neighbors(vertex):
                assert result[neighbor] != color
