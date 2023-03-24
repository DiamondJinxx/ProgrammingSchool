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
        node_to_delete = Node(4)
        node = Node(2)
        node_before = Node(3)
        node_after = Node(5)
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(node)
        self.ll.insert(node, node_before)
        self.ll.insert(node_before, node_to_delete)
        self.ll.insert(node_to_delete, node_after)
        self.ll.add_in_tail(Node(7))
        self.ll.add_in_tail(Node(8))

        old_len = self.ll.len()
        self.ll.delete(node_to_delete.value)

        self.assertEqual(self.ll.len(), old_len - 1)
        self.assertTrue(node_before.next is node_after)
        self.assertTrue(node_after.prev is node_before)

    def test_delete_in_head(self):
        old_head = Node('old_head')
        new_head = Node('new_head')
        tail = Node('tail')
        self.ll.add_in_tail(old_head)
        self.ll.add_in_tail(new_head)
        self.ll.add_in_tail(tail)
        old_len = self.ll.len()

        self.ll.delete(old_head.value)
        self.assertEqual(self.ll.len(), old_len - 1)
        self.assertTrue(self.ll.head is new_head)
        self.assertIsNone(self.ll.head.prev)

    def test_delete_in_tail(self):
        head = Node('head')
        new_tail = Node('new_tail')
        old_tail = Node('old_tail')
        self.ll.add_in_tail(head)
        self.ll.add_in_tail(new_tail)
        self.ll.add_in_tail(old_tail)
        old_len = self.ll.len()

        self.ll.delete(old_tail.value)

        self.assertEqual(self.ll.len(), old_len - 1)
        self.assertTrue(self.ll.tail is new_tail)
        self.assertIsNone(self.ll.tail.next)


    def test_detelete_all_list(self):
        for i in range(10):
            self.ll.add_in_tail(Node(1))
        old_new = self.ll.len()
        
        self.ll.delete(1, True)

        self.assertEqual(self.ll.len(), 0)
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    def test_detelete_all_elements(self):
        for i in range(10):
            self.ll.add_in_tail(Node(1))
        not_delete = Node('not_delete')
        self.ll.add_in_tail(not_delete)
        for i in range(10):
            self.ll.add_in_tail(Node(1))

        self.ll.delete(1, True)
        self.assertEqual(self.ll.len(), 1)
        self.assertTrue(self.ll.head is not_delete)
        self.assertTrue(self.ll.tail is not_delete)

    def test_delete_list_is_one_element(self):
        self.ll.add_in_tail(Node(2))
        self.ll.delete(2)

        self.assertEqual(self.ll.len(), 0)
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    def test_clean(self):
        for i in range(10):
            self.ll.add_in_tail(Node(i))
        self.assertEqual(self.ll.len(), 10)

        self.ll.clean()
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertEqual(self.ll.len(), 0)

    def test_insert(self):
        after_node = Node('after')
        old_node = Node('old after')
        new_node = Node('new node')
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(1))
        self.ll.add_in_tail(Node(5))
        self.ll.add_in_tail(after_node)
        self.ll.add_in_tail(old_node)
        self.ll.add_in_tail(Node(3))
        self.ll.add_in_tail(Node(8))
        self.ll.add_in_tail(Node(1))
        old_len = self.ll.len()

        self.ll.insert(after_node, new_node)

        self.assertEqual(self.ll.len(), old_len+1)
        self.assertTrue(after_node.next is new_node)
        self.assertTrue(old_node.prev is new_node)
        self.assertTrue(new_node.next is old_node)
        self.assertTrue(new_node.prev is after_node)


    def test_insert_empty_list(self):
        new_node = Node('new node')
        self.ll.insert(None, new_node)

        self.assertEqual(self.ll.len(), 1)
        self.assertTrue(new_node.next is None)
        self.assertTrue(new_node.prev is None)
        self.assertTrue(self.ll.head is new_node)
        self.assertTrue(self.ll.tail is new_node)

    def test_insert_afternode_is_none_full_list(self):
        old_node = Node('old')
        self.ll.add_in_tail(old_node)
        new_node = Node('new node')
        self.ll.insert(None, new_node)

        self.assertTrue(self.ll.head is old_node)
        self.assertTrue(self.ll.tail is new_node)
        self.assertTrue(self.ll.head.next is new_node)
        self.assertTrue(self.ll.tail.prev is old_node)
