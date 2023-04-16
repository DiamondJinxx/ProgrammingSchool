import unittest
from deque import Deque

class TestDeque(unittest.TestCase):
    def test_add_front(self):
        deq = Deque()
        new_item = 'new'
        deq.addFront(new_item)
        self.assertEqual(deq.size(), 1)
        self.assertTrue(deq.front() is new_item)
        second_new = 'second_new'
        deq.addFront(second_new)
        self.assertEqual(deq.size(), 2)
        self.assertTrue(deq.front() is second_new)
        self.assertTrue(deq.tail() is new_item)


    def test_remove_front(self):
        deq = Deque()
        f1 = 'f1'
        f2 = 'f2'
        deq.addFront(f1)
        deq.addFront(f2)
        self.assertTrue(deq.front() is f2)
        self.assertTrue(deq.tail() is f1)
        self.assertEqual(deq.size(), 2)
        deq.removeFront()
        self.assertEqual(deq.size(), 1)
        self.assertTrue(deq.front() is f1)
        deq.removeFront()
        res = deq.removeFront()
        self.assertIsNone(res)


    def test_add_tail(self):
        deq = Deque()
        t1 = 't1'
        t2 = 't2'
        f1 = 'f1'
        deq.addTail(t1)
        self.assertTrue(deq.tail() is t1)
        self.assertTrue(deq.front() is t1)
        self.assertEqual(deq.size(), 1)
        deq.addTail(t2)
        self.assertTrue(deq.tail() is t2)
        self.assertTrue(deq.front() is t1)
        self.assertEqual(deq.size(), 2)

    def test_remove_tail(self):
        deq = Deque()
        t1 = 't1'
        t2 = 't2'
        f1 = 'f1'
        deq.addFront(t2)
        deq.addFront(f1)
        deq.addTail(t1)
        self.assertEqual(deq.size(), 3)
        self.assertTrue(deq.front() is f1)
        self.assertTrue(deq.tail() is t1)
        deq.removeTail()
        self.assertTrue(deq.tail() is t2)
        self.assertEqual(deq.size(), 2)

    def test_remove_all_front(self):
        deq = Deque()
        for i in range(50):
            deq.addFront(i)
        for i in range(49, -1, -1):
            val = deq.removeFront()
            self.assertEqual(val, i)
        self.assertIsNone(deq.front())
        self.assertIsNone(deq.tail())
        self.assertEqual(deq.size(), 0)
        
    def test_remove_all_tail(self):
        deq = Deque()
        for i in range(50):
            deq.addFront(i)
        for i in range(49, -1, -1):
            val = deq.removeTail()
            self.assertEqual(val, 49 - i)
        self.assertIsNone(deq.front())
        self.assertIsNone(deq.tail())
        self.assertEqual(deq.size(), 0)