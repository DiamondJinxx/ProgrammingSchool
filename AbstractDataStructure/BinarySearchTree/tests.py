import unittest
from SearchTree import BST, BSTNode, BSTFind


class BinarySearchTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = BSTNode(24, 'Dima', None)
        self.tree = BST(self.root)
        self.tree.Root.LeftChild = BSTNode(21, 'Dasha', self.tree.Root)
        self.tree.Root.RightChild = BSTNode(50, 'Maksim', self.tree.Root)


    def test_create(self):
        self.assertTrue(self.tree.Root is self.root)
    

    def test_find_node_by_key(self):
        self.tree.Root.LeftChild.RightChild = BSTNode(22, 'Olechka', self.tree.Root.RightChild)
        find_node = self.tree.FindNodeByKey(22)
        self.assertTrue(find_node.NodeHasKey)
        self.assertTrue(find_node.Node is self.tree.Root.LeftChild.RightChild)


    def test_find_node_by_key_to_left(self):
        find_node = self.tree.FindNodeByKey(17)
        self.assertFalse(find_node.NodeHasKey)
        self.assertTrue(find_node.Node is self.tree.Root.LeftChild)
        self.assertTrue(find_node.ToLeft)


    def test_find_node_by_key_to_right(self):
        find_node = self.tree.FindNodeByKey(22)
        self.assertFalse(find_node.NodeHasKey)
        self.assertTrue(find_node.Node is self.tree.Root.LeftChild)
        self.assertFalse(find_node.ToLeft)


    def test_add_key_value_to_left(self):
        self.tree.AddKeyValue(17, 'Ru')
        find_node = self.tree.FindNodeByKey(17)
        self.assertTrue(find_node.Node.Parent is self.tree.Root.LeftChild)
        self.assertTrue(find_node.NodeHasKey)
        self.assertTrue(find_node.Node is self.tree.Root.LeftChild.LeftChild)

    def test_add_key_value_to_right(self):
        self.tree.AddKeyValue(45, 'Elena')
        find_node = self.tree.FindNodeByKey(45)
        self.assertTrue(find_node.Node.Parent is self.tree.Root.RightChild)
        self.assertTrue(find_node.NodeHasKey)
        self.assertTrue(find_node.Node is self.tree.Root.RightChild.LeftChild)
        
    def test_add_existing_key_value(self):
        self.tree.AddKeyValue(45, 'Elena')
        self.assertFalse(self.tree.AddKeyValue(45, 'Elena'))
        
    def test_find_min_max_from_root(self):
        self.tree.AddKeyValue(22,'Olechka')
        self.tree.AddKeyValue(45, 'Elena')
        self.tree.AddKeyValue(23, 'Zhora')
        min_node = self.tree.FinMinMax(FromNode=None, FindMax=False)
        self.assertTrue(min_node is self.tree.Root.LeftChild)
        max_node = self.tree.FinMinMax(FromNode=None, FindMax=True)
        self.assertTrue(max_node is self.tree.Root.RightChild)

    def test_find_min_max_from_subtree(self):
        self.tree.AddKeyValue(22,'Olechka')
        self.tree.AddKeyValue(45, 'Elena')
        self.tree.AddKeyValue(23, 'Zhora')
        self.tree.AddKeyValue(17, 'Misha')
        self.tree.AddKeyValue(75, 'Victor')
        min_node = self.tree.FinMinMax(self.tree.Root.LeftChild, FindMax=False)
        self.assertTrue(min_node is self.tree.Root.LeftChild.LeftChild)
        max_node = self.tree.FinMinMax(self.tree.Root.RightChild, FindMax=True)
        self.assertTrue(max_node is self.tree.Root.RightChild.RightChild)


if __name__ == '__main__':
    unittest.main()

