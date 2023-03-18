import unittest
from linked_list import LinkedList, Node

class TestLinkedList(unittest.TestCase):
    def setUp(self) -> None:
        self.s_list = LinkedList()

    def test_constructor(self):
        self.assertIsNone(self.s_list.head)
        self.assertIsNone(self.s_list.tail)

    def test_insert_single_item(self):
        test_node = Node(15)
        self.s_list.add_in_tail(test_node)
        self.assertEqual(self.s_list.head, test_node)
        self.assertEqual(self.s_list.tail, test_node)

    def test_insert_sample_item(self):
        first_node = Node(1)
        second_node = Node(2)
        self.s_list.add_in_tail(first_node)
        self.s_list.add_in_tail(second_node)
        
        self.assertEqual(self.s_list.head, first_node)
        self.assertEqual(self.s_list.tail, second_node)

    def test_find_by_value(self):
        for i in range(15):
            self.s_list.add_in_tail(Node(i))
        item_to_find = 7
        item = self.s_list.find(item_to_find)
        self.assertIsNotNone(item)
        self.assertEqual(item.value, item_to_find)
    
    def test_not_find_by_value(self):
        for i in range(15):
            self.s_list.add_in_tail(Node(i))
        item_to_find = 20
        item = self.s_list.find(item_to_find)
        self.assertIsNone(item)


if __name__ == 'main':
    unittest.main()