import unittest
from double_linked_list import Node, LinkedList2


class TestLinkedList2(unittest.TestCase):
    def setUp(self):
        self.ll = LinkedList2()

    def test_constructor(self):
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertEqual(self.ll.len(), 0)

    def test_add_in_tail_empty_list(self):
        node = Node(2)
        self.ll.add_in_tail(node)
        self.assertTrue(self.ll.head is node)
        self.assertTrue(self.ll.tail is node)
        self.assertIsNone(self.ll.head.next)
        self.assertIsNone(self.ll.head.prev)
        self.assertIsNone(self.ll.tail.prev)
        self.assertIsNone(self.ll.tail.prev)