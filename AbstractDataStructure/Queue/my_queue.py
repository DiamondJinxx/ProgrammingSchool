class Queue:
    def __init__(self):
        # инициализация хранилища данных
        self.data = []

    def enqueue(self, item):
        # вставка в хвост
        self.data.append(item)

    def dequeue(self):
        return None if self.is_empty() else self.data.pop(0)

    def size(self):
        return len(self.data) # размер очереди
    
    def is_empty(self) -> bool:
        return self.size() == 0