import pytest
from Heap import Heap


@pytest.fixture()
def source_array():

    def array_factory(begin=1, end=5):
        return [i for i in range(begin, end + 1)]

    return array_factory


def test_heap_ctor():
    heap = Heap()
    assert heap.HeapArray == []


def test_make_empty_heap():
    heap = Heap()
    heap.MakeHeap([], 3)
    assert len(heap.HeapArray) == 15
    for node in heap:
        assert node is None


def test_make_heap(source_array):
    heap = Heap()
    heap.MakeHeap(source_array(), 2)
    assert len(heap.HeapArray) == 7
    assert heap.HeapArray == [5, 4, 3, 2, 1, None, None]
    heap.MakeHeap(source_array(end=9), 3)
    assert len(heap.HeapArray) == 15
    assert heap.HeapArray == [
        9, 8, 7, 6, 5, 4, 3, 2, 1, None, None, None, None, None, None
    ]


def test_add_element(source_array):
    heap = Heap()
    heap.MakeHeap(source_array(begin=2), 2)
    assert heap.Add(0)
    assert heap.HeapArray == [5, 4, 3, 2, 0, None, None]
    assert heap.Add(6)
    assert heap.HeapArray == [6, 4, 5, 2, 0, 3, None]
    assert heap.Add(7)
    assert heap.HeapArray == [7, 4, 6, 2, 0, 3, 5]


def test_add_element_if_full_heap(source_array):
    heap = Heap()
    heap.MakeHeap(source_array(end=7), 2)
    assert not heap.Add(12)


def test_get_max(source_array):
    heap = Heap()
    heap.MakeHeap(source_array(), 2)
    assert heap.GetMax() == 5
    # assert heap.HeapArray == []
