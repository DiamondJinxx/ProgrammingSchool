from stack import Stack as StackHead
from stack_tail import StackTail
import time



# по замерам интересное конечно 
# stack_head = StackHead()

# start_time = time.time()
# for i in range(100_000):
#     stack_head.push(i)
# print(f'Добавление элементов в stack_head: {time.time() - start_time}')

# stack_tail = StackTail()

# start_time = time.time()
# for i in range(100_000):
#     stack_tail.push(i)
# print(f'Добавление элементов в stack_tail: {time.time() - start_time}')

# for i in range(100_000):
#     stack_head.pop()
# print(f'Удаление элементов из stack_head: {time.time() - start_time}')

# stack_tail = StackTail()

# start_time = time.time()
# for i in range(100_000):
#     stack_tail.pop()
# print(f'Удаление элементов из stack_tail: {time.time() - start_time}')

def is_balanced(line: str) -> bool:
    open_brackets = '({['
    close_brackets = ']})'
    brackets = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    stack = StackHead()
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

line_balanced = ''
print(is_balanced(line_balanced))
