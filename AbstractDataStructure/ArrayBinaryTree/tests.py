import unittest
from ArrayBinaryTree import aBST


class ArrayBinaryTreeTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bst = aBST(2)
        self.bst.Tree[0] = 24
        self.bst.Tree[1] = 21
        self.bst.Tree[2] = 50
        self.bst.Tree[3] = 17
        self.bst.Tree[4] = 23
    
    def test_create_tree(self):
        bst = aBST(0)
        self.assertTrue(bool(bst))
        self.assertEqual(len(bst.Tree), 1)
        # tree size is : 2^(depth + 1) - 1
        bst = aBST(2)
        self.assertTrue(bool(bst))
        self.assertEqual(len(bst.Tree), 7)
        self.assertTrue(all(map(lambda node: node is None, bst.Tree)))

    def test_find_key_index(self):
        self.bst.Tree[5] = 45
        self.bst.Tree[6] = 75
        node_idx = self.bst.FindKeyIndex(17)
        self.assertEqual(node_idx, 3)
        node_idx = self.bst.FindKeyIndex(45)
        self.assertEqual(node_idx, 5)

    def test_find_key_index_return_empty_node_index(self):
        node_idx = self.bst.FindKeyIndex(75)
        self.assertEqual(node_idx, -6)
        node_idx = self.bst.FindKeyIndex(45)
        self.assertEqual(node_idx, -5)

    def test_find_key_index_not_find(self):
        self.bst.Tree[5] = 45
        self.bst.Tree[6] = 75
        node_idx = self.bst.FindKeyIndex(48)
        self.assertIsNone(node_idx)

    def test_find_key_index_empty_tree(self):
        bst = aBST(2)
        new_index = bst.FindKeyIndex(12)
        self.assertEqual(new_index, 0)

    def test_add_key(self):
        expected_index = 5
        index = self.bst.AddKey(45)
        self.assertEqual(index, expected_index)
        self.assertEqual(self.bst.Tree[index], self.bst.Tree[expected_index])

    def test_add_key_to_full_tree(self):
        self.bst.Tree[5] = 45
        self.bst.Tree[6] = 75
        index = self.bst.AddKey(12)
        self.assertEqual(index, -1)
        self.assertIsNone(self.bst.FindKeyIndex(12))

    def test_add_key_if_key_exist(self):
        new_node_index = self.bst.AddKey(17) 
        self.assertEqual(new_node_index, 3)

    def test_add_key_to_root_of_empty_tree(self):
        bst = aBST(0)
        new_node = 12
        new_node_index = bst.AddKey(new_node)        
        self.assertEqual(new_node_index, 0)
        self.assertEqual(bst.Tree[new_node_index], new_node) 

    def test_add_key_add_existing_root(self):
        bst = aBST(0)
        bst.Tree[0] = 12
        new_node_index = bst.AddKey(12)
        self.assertEqual(new_node_index, 0)


if __name__ == '__main__':
    unittest.main()
