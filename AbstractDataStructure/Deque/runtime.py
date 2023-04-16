from deque import Deque

def is_palindrome(line: str) -> bool:
    deq = Deque()
    for char in line:
        deq.addTail(char)
    while deq.size() > 0:
        head = deq.removeFront()
        tail = deq.removeTail()
        if tail is None:
            return True
        if head != tail:
            return False
    return True

        