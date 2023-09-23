from Heap import Heap

heap = Heap()
source_array = [i for i in range(1, 10)]
heap.MakeHeap(source_array, 3)
print(heap.HeapArray)
