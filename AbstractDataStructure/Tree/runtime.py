from SimpleTree import SimpleTree, SimpleTreeNode



root = SimpleTreeNode(1, None)
tree = SimpleTree(root)
left_child = SimpleTreeNode(2, root)
right_child = SimpleTreeNode(3, root)
tree.AddChild(root, left_child)
tree.AddChild(root, right_child)
print(tree.Root.Children)
