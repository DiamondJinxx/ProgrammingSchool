from typing import List
from my_queue import Queue

l = [1,2,3,4,5]

def rotate(array: List[int], times: int):
    return array[times:] + array[:times]

queue = Queue()
for i in l:
    queue.enqueue(i)
print(queue.data)
queue.rotate(12)
print(queue.data)
queue.rotate(-4)
print(queue.data)
