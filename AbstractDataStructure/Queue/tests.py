import unittest
from my_queue import Queue

class QueueTests(unittest.TestCase):
    def test_enqueue(self):
        queue = Queue()
        self.assertEqual(queue.size(), 0)
        
        expected_item = 123
        queue.enqueue(expected_item)
        self.assertEqual(queue.data[0], expected_item)

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
