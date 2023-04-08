class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def pop(self):
        value = None if self.is_empty() else self.stack.pop(0)
        return value

    def push(self, value):
        self.stack.insert(0, value)

    def peek(self):
        value = None if self.is_empty() else self.stack[0]
        return value

    def is_empty(self) -> bool:
        return self.size() == 0


def is_balanced(line: str) -> bool:
    open_brackets = '({['
    close_brackets = ']})'
    brackets = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    stack = Stack()
    for char in line:
        if char not in open_brackets and char not in close_brackets:
            continue
        if char in open_brackets:
            stack.push(char)
            continue
        if char in close_brackets and stack.peek() == brackets[char]:
            stack.pop()
            continue
        return False
    return stack.is_empty()
