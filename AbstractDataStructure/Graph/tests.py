import pytest
from Graph import SimpleGraph, Vertex

_GRAPH_SIZE = 6

@pytest.fixture()
def empty_graph():
    return SimpleGraph(_GRAPH_SIZE)


@pytest.fixture()
def graph():
    graph = SimpleGraph(_GRAPH_SIZE)
    graph.vertex[0] = Vertex('A')
    graph.m_adjacency[0][2] = 1
    graph.m_adjacency[2][0] = 1
    graph.m_adjacency[0][3] = 1
    graph.m_adjacency[3][0] = 1
    graph.vertex[1] = Vertex('B')
    graph.m_adjacency[1][4] = 1
    graph.m_adjacency[4][1] = 1
    graph.vertex[2] = Vertex('C')
    graph.m_adjacency[2][4] = 1
    graph.m_adjacency[4][2] = 1
    graph.vertex[3] = Vertex('D')
    graph.vertex[4] = Vertex('E')
    graph.count = 5
    return graph

@pytest.fixture()
def numeric_graph():
    graph = SimpleGraph(_GRAPH_SIZE)
    graph.vertex[0] = Vertex('1')
    graph.m_adjacency[0][2] = 1
    graph.m_adjacency[2][0] = 1
    graph.m_adjacency[0][3] = 1
    graph.m_adjacency[3][0] = 1
    graph.vertex[1] = Vertex('2')
    graph.m_adjacency[1][4] = 1
    graph.m_adjacency[4][1] = 1
    graph.vertex[2] = Vertex('3')
    graph.m_adjacency[2][4] = 1
    graph.m_adjacency[4][2] = 1
    graph.vertex[3] = Vertex('4')
    graph.vertex[4] = Vertex('5')
    graph.count = 5
    return graph

def test_is_edge(graph, numeric_graph):
    assert not graph.IsEdge(0, 1)
    assert graph.IsEdge(0, 3)
    assert not numeric_graph.IsEdge(0, 1)
    assert numeric_graph.IsEdge(0, 3)

def test_add_vertex(graph):
    assert 'F' not in graph
    graph.AddVertex('F')
    assert 'F' in graph
    for idx, ver in enumerate(graph.vertex):
        assert not graph.IsEdge(5, idx)

def test_add_vertex_to_full_graph(graph):
    graph.AddVertex('F')
    assert 'G' not in graph
    graph.AddVertex('G')
    assert 'G' not in graph

def test_add_edge(graph):
    assert not graph.IsEdge(0, 1)
    graph.AddEdge(0, 1)
    assert graph.IsEdge(0, 1)

# def test_add_edge_with_not_existing_vertex(graph):
    # assert not graph.IsEdge('A', 'H')
    # graph.AddEdge('A', 'H')
    # assert not graph.IsEdge('A', 'H')

def test_remove_edge(graph):
    assert graph.IsEdge(0, 3)
    graph.RemoveEdge(0, 3)
    assert not graph.IsEdge(0, 3)

def test_remove_vertex(graph):
    assert 'A' in graph
    assert graph.IsEdge(0, 2)
    assert graph.IsEdge(0, 3)
    graph.RemoveVertex(0)
    assert 'A' not in graph
    assert not graph.IsEdge(0, 2)
    assert not graph.IsEdge(0, 3)


