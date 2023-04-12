class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        return None if self.is_empty() else self.data.pop(0)

    def size(self):
        return len(self.data)
    
    def is_empty(self) -> bool:
        return self.size() == 0
    
    def rotate(self, times: int):
        if self.is_empty():
            return
        times = times % self.size()
        self.data = self.data[times:] + self.data[:times]
    
# task 6.2: enqueue - o(1), dequeue - O(n) I think
