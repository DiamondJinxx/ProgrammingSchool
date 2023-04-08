from stack import Stack


stack = Stack()

stack.push(1)
stack.push('2')
stack.push(1.123)
stack.push('some new stack element')
print(f'len is: {stack.size()}')

while not stack.is_empty():
    print(stack.pop())

print(stack.pop())
print(stack.peek())
print(f'len is: {stack.size()}')
