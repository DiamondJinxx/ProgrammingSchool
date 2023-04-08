class StackTail:
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
