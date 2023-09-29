class Vertex:

    def __init__(self, val):
        self.Value = val

    def __str__(self) -> str:
        return f'{self.Value}'

    def __eq__(self, other):
        if not other:
            return False
        return self.Value == other.Value

  
class SimpleGraph:
	
    def __init__(self, size):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex = [None] * size
        self.count = 0
        
    def AddVertex(self, v):
        # ваш код добавления новой вершины 
        # с значением value 
        # в свободное место массива vertex
        if self.__is_full():
            return
        self.vertex[self.count] = Vertex(v)
        self.count += 1


    def __is_full(self) -> bool:
        return self.count == self.max_vertex
	
    # здесь и далее, параметры v -- индекс вершины
    # в списке  vertex
    def RemoveVertex(self, v):
        # ваш код удаления вершины со всеми её рёбрами
        if self.count == 0 or self.vertex[v] is None:
            return
        self.vertex[v] = None
        for i in range(self.max_vertex):
            self.m_adjacency[v][i] = 0
            self.m_adjacency[i][v] = 0
        self.count -= 1
	
    def IsEdge(self, v1, v2):
        # True если есть ребро между вершинами v1 и v2
        v1_idx = self.__vertex_idx(v1)
        v2_idx = self.__vertex_idx(v2)
        if v1_idx == -1 or v2_idx == -1:
            return False
        return self.m_adjacency[v1_idx][v2_idx] == 1 and self.m_adjacency[v2_idx][v1_idx] == 1

	
    def AddEdge(self, v1, v2):
        # добавление ребра между вершинами v1 и v2
        v1_idx = self.__vertex_idx(v1)
        v2_idx = self.__vertex_idx(v2)
        if v1_idx == -1 or v2_idx == -1:
            return
        self.m_adjacency[v1_idx][v2_idx] = 1
        self.m_adjacency[v2_idx][v1_idx] = 1
	
    def RemoveEdge(self, v1, v2):
        # удаление ребра между вершинами v1 и v2
        v1_idx = self.__vertex_idx(v1)
        v2_idx = self.__vertex_idx(v2)
        if v1_idx == -1 or v2_idx == -1:
            return
        self.m_adjacency[v1_idx][v2_idx] = 0
        self.m_adjacency[v2_idx][v1_idx] = 0

    
    def __contains__(self, v) -> bool:
        if not issubclass(type(v), Vertex):
            v = Vertex(v)
        return v in self.vertex

    def __vertex_idx(self, ver):
        ver = Vertex(ver)
        idx = -1
        for i, v in enumerate(self.vertex):
            if v == ver:
                idx = i
                break
        return idx