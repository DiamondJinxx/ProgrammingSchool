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
        new_child_one = SimpleTreeNode(4,  right_child)
        new_child = SimpleTreeNode(5,  right_child)
        tree.AddChild(right_child, new_child_one)
        tree.AddChild(right_child, new_child)
        old_count = tree.Count()
        tree.DeleteNode(right_child)
        self.assertEqual(tree.Count(), old_count - 3)
        self.assertIsNone(right_child.Parent)
    
    def test_delete_from_empty_children(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        tree.AddChild(root, SimpleTreeNode(2, root))
        self.assertEqual(len(tree.Root.Children), 1)
        tree.DeleteNode(SimpleTreeNode(12, root))
        self.assertEqual(len(tree.Root.Children), 1)


    def test_count(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        left_child = SimpleTreeNode(2, root)
        right_child = SimpleTreeNode(3, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        self.assertEqual(tree.Count(), 3)
    
    def test_count_if_root_is_none(self):
        tree = SimpleTree(None)
        self.assertEqual(tree.Count(), 0)

    def test_leaf_count(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        left_child = SimpleTreeNode(2, root)
        right_child = SimpleTreeNode(3, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        tree.AddChild(right_child, SimpleTreeNode(4, right_child))
        tree.AddChild(right_child, SimpleTreeNode(5, right_child))
        self.assertEqual(tree.LeafCount(), 3)

    def test_leaf_count_if_root_is_none(self):
        tree = SimpleTree(None)
        self.assertEqual(tree.LeafCount(), 0)

    def test_get_all_nodes(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        self.assertEqual(tree.GetAllNodes(), [root])
        left_child = SimpleTreeNode(2, root)
        right_child = SimpleTreeNode(3, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        self.assertEqual(tree.GetAllNodes(), [root, left_child, right_child])
        left_second_child = SimpleTreeNode(4, left_child)
        right_second_child = SimpleTreeNode(4, left_child)
        tree.AddChild(left_child, left_second_child)
        tree.AddChild(left_child, right_second_child)
        expected = [root, left_child, left_second_child, right_second_child, right_child]
        nodes = tree.GetAllNodes()
        for expected_child, child in zip(expected, nodes):
            self.assertTrue(expected_child is child)
    
    def test_get_all_nodes_from_empty_tree(self):
        tree = SimpleTree(None)
        self.assertFalse(tree.GetAllNodes())

    def test_find_nodes_by_value(self):
        root = SimpleTreeNode(5, None)
        tree = SimpleTree(root)
        left_child = SimpleTreeNode(1, root)
        right_child = SimpleTreeNode(5, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        self.assertEqual(len(tree.FindNodesByValue(5)), 2)
        expected = [root, right_child]
        nodes_wiht_value = tree.FindNodesByValue(5)
        for expected_node, node in zip(expected, nodes_wiht_value):
            self.assertTrue(expected_node is node)

    def test_move_node(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        tree = SimpleTree(root)
        left_child = SimpleTreeNode(2, root)
        right_child = SimpleTreeNode(3, root)
        tree.AddChild(root, left_child)
        tree.AddChild(root, right_child)
        tree.AddChild(left_child, SimpleTreeNode(4, left_child))
        tree.AddChild(left_child, SimpleTreeNode(5, left_child))
        tree.MoveNode(left_child, right_child)
        self.assertEqual(len(root.Children), 1)
        self.assertTrue(left_child.Parent is right_child)
        self.assertTrue(left_child in right_child.Children)
        self.assertEqual(len(right_child.Children), 1)
