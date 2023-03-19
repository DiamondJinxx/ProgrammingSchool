import unittest
from linked_list import LinkedList, Node


# получилли много больших тестов, частично пересекающихся,
# как написать тесты так, чтобы их было меньше, а покрытие было больше? 
# знать краевые случаи состояний своей программы?
class TestLinkedList(unittest.TestCase):
    def setUp(self) -> None:
        self.s_list = LinkedList()

    def test_constructor(self):
        self.assertIsNone(self.s_list.head)
        self.assertIsNone(self.s_list.tail)
        self.assertEqual(self.s_list.lengh, 0)

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

    def test_find_all_by_value(self):
        node_one = Node(1)
        node_two = Node(1)
        # проверять будем id объектов
        nodes_to_check = [node_one, node_two]
        self.s_list.add_in_tail(Node(2))
        self.s_list.add_in_tail(node_one)
        self.s_list.add_in_tail(Node(3))
        self.s_list.add_in_tail(Node(4))
        self.s_list.add_in_tail(Node(5))
        self.s_list.add_in_tail(node_two)
        self.s_list.add_in_tail(Node(6))
        fa = self.s_list.find_all(1)
        self.assertEqual(len(nodes_to_check), len(fa))
        for first, second in zip(fa, nodes_to_check):
            self.assertTrue(first is second)

    def test_not_find_all_by_value(self):
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(2))
        self.s_list.add_in_tail(Node(3))
        self.s_list.add_in_tail(Node(4))
        self.s_list.add_in_tail(Node(5))
        self.s_list.add_in_tail(Node(6))
        fa = self.s_list.find_all(9)
        self.assertEqual(len(fa), 0)


    def test_delete_one_element_with_value(self):
        values = [2,2,4,4,4,2,2,4]
        item_to_remove = 4
        for val in values:
            self.s_list.add_in_tail(Node(val))
        self.s_list.delete(item_to_remove)
        values.remove(4)
        self.assertEqual(len(values), self.s_list.len())

    def test_delete_all_element_with_value(self):
        values = [2,2,4,4,4,2,2,4]
        item_to_remove = 4
        for val in values:
            self.s_list.add_in_tail(Node(val))
        self.s_list.delete(item_to_remove, all=True)
        values = [ item for item in values if item != item_to_remove]
        self.assertEqual(len(values), self.s_list.len())
        self.assertEqual(self.s_list.tail.value, 2)

    def test_delete_item_in_head(self):
        new_head = Node(2)
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(new_head)
        self.s_list.add_in_tail(Node(3))
        self.s_list.delete(1)
        self.assertTrue(self.s_list.head is new_head)
        self.assertEqual(self.s_list.len(), 2)

    def test_delete_item_in_tail(self):
        new_tail = Node(2)
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(new_tail)
        self.s_list.add_in_tail(Node(3))
        self.s_list.delete(3)
        self.assertTrue(self.s_list.tail is new_tail)
        self.assertEqual(self.s_list.len(), 2)

    def test_delete_all_items(self):
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(1))
        self.s_list.delete(1, True)
        self.assertEqual(self.s_list.len(), 0)
        self.assertIsNone(self.s_list.head)
        self.assertIsNone(self.s_list.tail)

    def test_lengh(self):
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(2))
        self.s_list.add_in_tail(Node(3))
        self.assertEqual(self.s_list.len(), 3)
        self.s_list.delete(1)
        self.s_list.delete(2)
        self.assertEqual(self.s_list.len(), 1)
    
    def test_clean(self):
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(2))
        self.assertEqual(self.s_list.head.value, 1)
        self.assertEqual(self.s_list.tail.value, 2)
        self.s_list.clean()
        self.assertIsNone(self.s_list.head)
        self.assertIsNone(self.s_list.tail)
        self.assertEqual(self.s_list.len(), 0)

    def test_insert_afternode_is_none(self):
        newNode = Node('new')
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(Node(2))
        self.s_list.add_in_tail(Node(3))
        self.s_list.insert(None, newNode)
        self.assertEqual(self.s_list.head, newNode)

    def test_insert_in_empty_list(self):
        newNode = Node('new')
        self.s_list.insert(None, newNode)
        self.assertEqual(self.s_list.head, newNode)
        self.assertEqual(self.s_list.tail, newNode)
        self.assertEqual(self.s_list.len(), 1)
    
    def test_insert(self):
        new_node = Node('new')
        after_node = Node('afterNode')
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(after_node)
        self.s_list.add_in_tail(Node(3))
        old_list_len = self.s_list.len()
        self.s_list.insert(after_node, new_node)
        node = self.s_list.head
        actual_tail: Node
        while node is not None:
            if node is after_node:
                self.assertTrue(node.next is new_node)
            if node.next is None:
                actual_tail = node
            node = node.next
        self.assertEqual(old_list_len + 1, self.s_list.len())
        self.assertTrue(actual_tail is self.s_list.tail)
        

    def test_insert_after_tail(self):
        new_node = Node('new')
        after_node = Node('afterNode')
        self.s_list.add_in_tail(Node(1))
        self.s_list.add_in_tail(after_node)
        self.s_list.add_in_tail(Node(3))
        self.s_list.insert(self.s_list.tail, new_node)
        self.assertTrue(self.s_list.tail is new_node)



if __name__ == 'main':
    unittest.main()