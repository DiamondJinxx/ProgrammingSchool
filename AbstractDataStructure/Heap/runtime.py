from Heap import Heap

heap = Heap()
heap.MakeHeap([6, 5, 4, 3, 2, 1, 0], 2)
print(heap.HeapArray)
print(heap.GetMax())
print(heap.HeapArray)
while heap.GetMax() != -1:
    pass

print(heap.HeapArray)
