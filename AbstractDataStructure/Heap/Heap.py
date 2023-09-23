class Heap:

    def __init__(self):
        self.HeapArray = []  # хранит неотрицательные числа-ключи

    def MakeHeap(self, a, depth):
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth
        self.HeapArray = [None for i in range(2**(depth + 1) - 1)]
        a.sort()
        a.reverse()
        for index, node in enumerate(a):
            self.HeapArray[index] = node

    def GetMax(self):
        # вернуть значение корня и перестроить кучу
        return self.HeapArray[0]
        return -1  # если куча пуста

    def Add(self, key):
        # добавляем новый элемент key в кучу и перестраиваем её
        if not self.HeapArray or None not in self.HeapArray:
            return False
        new_node = self.HeapArray.index(None)
        self.HeapArray[new_node] = key
        diff = 1 if self._is_left_child(new_node) else 2
        parent = (new_node - diff) // 2

        # move key up if need
        while parent >= 0 and self.HeapArray[parent] < self.HeapArray[new_node]:
            self.HeapArray[parent], self.HeapArray[new_node] = self.HeapArray[
                new_node], self.HeapArray[parent]
            new_node = parent
            diff = 1 if self._is_left_child(new_node) else 2
            parent = (new_node - diff) // 2

        return True

    def __iter__(self):
        return iter(self.HeapArray)

    def _is_left_child(self, index):
        return index % 2 == 1
