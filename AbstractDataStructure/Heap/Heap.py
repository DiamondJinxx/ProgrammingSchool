class Heap:

    def __init__(self):
        self.HeapArray = []  # хранит неотрицательные числа-ключи
        self.count = 0

    def MakeHeap(self, a, depth):
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth
        self.HeapArray = [None for i in range(2**(depth + 1) - 1)]
        for node in a:
            self.Add(node)

    def GetMax(self):
        # вернуть значение корня и перестроить кучу
        if self._is_empty():
            return -1
        self.count -= 1
        maximum = self.HeapArray[0]
        root = -1
        for idx in range(len(self.HeapArray) - 1, -1, -1):
            if self.HeapArray[idx] is not None:
                root = idx
                break
        if root == 0:
            self.HeapArray[root] = None
            return maximum
        self.HeapArray[0] = self.HeapArray[root]
        self.HeapArray[root] = None
        root = 0
        max_child = self.__max_child(root)
        while max_child != -1 and self.HeapArray[root] < self.HeapArray[
                max_child]:
            self.HeapArray[root], self.HeapArray[max_child] = self.HeapArray[
                max_child], self.HeapArray[root]
            root = max_child
            max_child = self.__max_child(root)
        return maximum

    def __max_child(self, parent):
        """Get max child. If both child is None - return -1."""
        left = parent * 2 + 1
        right = parent * 2 + 2
        if self.HeapArray[left] is None and self.HeapArray[right] is None:
            return -1
        if self.HeapArray[left] is None and self.HeapArray[right] is not None:
            return right
        if self.HeapArray[left] is not None and self.HeapArray[right] is None:
            return left
        if self.HeapArray[left] > self.HeapArray[right]:
            return left
        return right

    def Add(self, key):
        # добавляем новый элемент key в кучу и перестраиваем её
        if not self.HeapArray or None not in self.HeapArray:
            return False
        new_node = self.HeapArray.index(None)
        self.HeapArray[new_node] = key
        diff = 1 if self.__is_left_child(new_node) else 2
        parent = (new_node - diff) // 2

        # move key up if need
        while parent >= 0 and self.HeapArray[parent] < self.HeapArray[new_node]:
            self.HeapArray[parent], self.HeapArray[new_node] = self.HeapArray[
                new_node], self.HeapArray[parent]
            new_node = parent
            diff = 1 if self.__is_left_child(new_node) else 2
            parent = (new_node - diff) // 2

        self.count += 1
        return True

    def __iter__(self):
        return iter(self.HeapArray)

    def __is_left_child(self, child):
        """Check child is left child"""
        return child % 2 == 1

    def _is_empty(self):
        return self.count == 0
