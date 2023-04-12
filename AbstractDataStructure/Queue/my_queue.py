# no wanna try to use import
class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def pop(self):
        value = None if self.is_empty() else self.stack.pop()
        return value

    def push(self, value):
        self.stack.append(value)

    def peek(self):
        value = None if self.is_empty() else self.stack[-1]
        return value

    def is_empty(self) -> bool:
        return self.size() == 0

class Queue:
    def __init__(self):
        self.stack_one = Stack()
        self.stack_two = Stack()

    def enqueue(self, item):
        self.stack_one.push(item)

    def dequeue(self):
        if self.stack_two.is_empty():
            while not self.stack_one.is_empty():
                self.stack_two.push(self.stack_one.pop())

        return None if self.is_empty() else self.stack_two.pop()

    def size(self):
        return self.stack_one.size() + self.stack_two.size()
    
    def is_empty(self) -> bool:
        return self.size() == 0
    
    def rotate(self, times: int):
        if self.is_empty():
            return
        times = times % self.size()
        common_data = self.stack_two.stack[::-1] + self.stack_one.stack
        common_data = common_data[times:] + common_data[:times]
        if self.stack_two.is_empty():
            self.stack_one.stack = common_data
            return
        if self.stack_one.is_empty():
            self.stack_two.stack = common_data
            return
        self.stack_one.stack = common_data[self.stack_two.size():]
        self.stack_two.stack = common_data[:self.stack_two.size()][::-1]

    @property
    def data(self):
        return self.stack_two.stack[::-1] + self.stack_one.stack
        
    
# task 6.2: enqueue - o(1), dequeue - O(n) I think
