class TestGraph:
    def _getTargetClass(self):
        from graph import Graph

        return Graph

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_init(self):
        g = self._makeOne()
        assert g.vertices() == []
        assert g.edges() == set()

    def test_add_vertex(self):
        g = self._makeOne()
        g.add_vertex("a")
        g.add_vertex("b")
        g.add_vertex("c")
        assert g.vertices() == ["a", "b", "c"]

    def test_add_edge(self):
        g = self._makeOne()
        g.add_vertex("a")
        g.add_vertex("b")
        g.add_edge("a", "b")
        assert g.edges() == {("a", "b")}

    def test_neighbors(self):
        g = self._makeOne()
        g.add_vertex("a")
        g.add_vertex("b")
        g.add_edge("a", "b")
        assert g.neighbors("a") == {"b"}
        assert g.neighbors("b") == {"a"}
