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

    def test_add_in_tail(self):
        node_head = Node(1)
        self.ll.add_in_tail(node_head)
        for i in range(2, 10):
            self.ll.add_in_tail(Node(i))
        node_tail = Node(15)
        self.ll.add_in_tail(node_tail)
        self.assertEqual(self.ll.lengh, 10)
        self.assertTrue(self.ll.head is node_head)
        self.assertTrue(self.ll.tail is node_tail)


    def test_find_one_element(self):
        node_to_find = Node(32)
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(5))
        self.ll.add_in_tail(node_to_find)
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(3))
        node = self.ll.find(32)
        self.assertTrue(node is node_to_find)

    def test_find_nothing(self):
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(5))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(3))
        node = self.ll.find(1231)
        self.assertIsNone(node)
    
    def test_find_all(self):
        val_to_find = 32
        # TODO: randon generated value and random order
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(5))
        self.ll.add_in_tail(Node(val_to_find))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(3))
        self.ll.add_in_tail(Node(val_to_find))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(val_to_find))
        self.ll.add_in_tail(Node(5))
        finding_nodes = self.ll.find_all(32)
        self.assertEqual(len(finding_nodes), 3)
        for node in finding_nodes:
            self.assertEqual(node.value, val_to_find)

    def test_add_in_head(self):
        new_head = Node(321)
        old_head = Node(1)
        self.ll.add_in_tail(old_head)
        self.ll.add_in_tail(Node(2))
        self.ll.add_in_tail(Node(3))
        self.assertTrue(self.ll.head is old_head)

        self.ll.add_in_head(new_head)
        self.assertTrue(self.ll.head is new_head)
        self.assertTrue(self.ll.head.next is old_head)
        self.assertTrue(self.ll.head.prev is None)
        self.assertTrue(old_head.prev is new_head)
        self.assertEqual(self.ll.len(), 4)


    def test_add_in_head_empty_list(self):
        new_head = Node(321)
        self.ll.add_in_head(new_head)
        self.assertTrue(self.ll.head is new_head)
        self.assertTrue(self.ll.head.next is None)
        self.assertTrue(self.ll.head.prev is None)
        self.assertTrue(self.ll.tail is new_head)
        self.assertEqual(self.ll.len(), 1)


    def test_delete(self):
        pass

    def test_delete_in_head(self):
        pass

    def test_delete_in_tail(self):
        pass

    def test_detelete_all(self):
        pass

    def test_clean(self):
        for i in range(10):
            self.ll.add_in_tail(Node(i))
        self.assertEqual(self.ll.len(), 10)

        self.ll.clean()
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertEqual(self.ll.len(), 0)

    def test_insert(self):
        pass

    def test_insert_empty_list(self):
        pass

    def test_insert_afternode_is_none_full_list(self):
        pass

