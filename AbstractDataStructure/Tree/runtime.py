from SimpleTree import SimpleTree, SimpleTreeNode
from pprint import pprint



root = SimpleTreeNode(1, None)
tree = SimpleTree(root)
left_child = SimpleTreeNode(2, root)
right_child = SimpleTreeNode(3, root)
tree.AddChild(root, left_child)
tree.AddChild(root, right_child)
left_second_child = SimpleTreeNode(4, left_child)
right_second_child = SimpleTreeNode(4, left_child)
tree.AddChild(left_child, left_second_child)
tree.AddChild(left_child, right_second_child)
right_right_child = SimpleTreeNode(6, right_child)
tree.AddChild(right_child, right_right_child)

# pprint(tree.nodes_lvl())
print(tree.EvenTrees())
