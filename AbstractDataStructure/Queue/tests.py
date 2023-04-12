import unittest
from my_queue import Queue

class QueueTests(unittest.TestCase):
    def test_enqueue(self):
        queue = Queue()
        self.assertEqual(queue.size(), 0)
        
        expected_item = 123
        queue.enqueue(expected_item)
        self.assertEqual(queue.stack_one.stack[0], expected_item)

    def test_dequeue(self):
        queue = Queue()
        expected_size = 10
        for i in range(expected_size):
            queue.enqueue(i)
        self.assertEqual(queue.size(), expected_size)

        for i in range(expected_size):
            self.assertEqual(queue.dequeue(), i)
        self.assertEqual(queue.size(), 0)
    
    def test_size(self):
        queue = Queue()
        expected_size = 10
        for i in range(expected_size):
            queue.enqueue(i)
        self.assertEqual(queue.size(), expected_size)

    def test_rotate_lower_then_size(self):
        size = 5
        expected_list = [3,4,5,1,2]
        queue = Queue()
        for i in range(1, size + 1,):
            queue.enqueue(i)
        queue.rotate(2)
        for item in expected_list:
            self.assertEqual(item, queue.dequeue())

    def test_rotate_greater_then_size(self):
        size = 5
        expected_list = [3,4,5,1,2]
        queue = Queue()
        for i in range(1, size + 1,):
            queue.enqueue(i)
        queue.rotate(12)
        for item in expected_list:
            self.assertEqual(item, queue.dequeue())

    def test_rotate_negative_times(self):
        size = 5
        expected_list = [4, 5, 1, 2, 3]
        queue = Queue()
        for i in range(1, size + 1,):
            queue.enqueue(i)
        queue.rotate(-12)
        for item in expected_list:
            self.assertEqual(item, queue.dequeue())