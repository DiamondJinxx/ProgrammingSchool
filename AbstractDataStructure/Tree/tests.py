import unittest
from SimpleTree import SimpleTree, SimpleTreeNode

class SimpleTreeTest(unittest.TestCase):
    
    def test_add_child_to_parent(self):
        parent = SimpleTreeNode(1, None)
        self.assertFalse(bool(parent.Children))
        tree = SimpleTree(parent)
        child = SimpleTreeNode(2, None)
        tree.AddChild(parent, child)
        self.assertEqual(len(parent.Children), 1)
        self.assertTrue(parent.Children[0] is child)
        self.assertTrue(child.Parent is parent)

    def test_delete_node(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        left_child = SimpleTreeNode(2, root)
        right_child = SimpleTreeNode(3, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        tree.DeleteNode(left_child)
        self.assertEqual(len(tree.Root.Children), 1)
        self.assertIsNone(left_child.Parent)
    
    def test_delete_from_empty_children(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        tree.DeleteNode(SimpleTreeNode(12, root))