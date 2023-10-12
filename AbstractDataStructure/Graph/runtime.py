from Graph import SimpleGraph, Vertex
from pprint import pprint

def print_graph(graph: SimpleGraph):
    print('-' * 30)
    print(' ' * 3, end='')
    for v in graph.vertex:
        print(v, end=' ')
    print()
    print(' ' * 2, end='')
    for _ in graph.vertex:
        print('__', end='')
    print()
    for idx, ver in enumerate(graph.vertex):
        print(f'{ver}| ', end='')
        for i in range(graph.max_vertex):
            print(graph.m_adjacency[idx][i], end=' ')
        print()

    print('-' * 30)

g = SimpleGraph(6)
g.vertex[0] = Vertex('A')
g.m_adjacency[0][2] = 1
g.m_adjacency[2][0] = 1
g.m_adjacency[0][3] = 1
g.m_adjacency[3][0] = 1
g.vertex[1] = Vertex('B')
g.m_adjacency[1][4] = 1
g.m_adjacency[4][1] = 1
g.vertex[2] = Vertex('C')
g.m_adjacency[2][4] = 1
g.m_adjacency[4][2] = 1
g.vertex[3] = Vertex('D')
g.vertex[4] = Vertex('E')
g.count = 5
# print_graph(g)
g.AddVertex('F')
# print('-'* 20)
print_graph(g)
# g.RemoveVertex(0)
# print('-'* 20)
# print_graph(g)
r = g.DepthFirstSearch(3, 0)
r = list(map(lambda v: v.Value, r))
pprint(r)
