from SimpleTree import SimpleTree, SimpleTreeNode



root = SimpleTreeNode(1, None)
tree = SimpleTree(root)
left_child = SimpleTreeNode(2, root)
right_child = SimpleTreeNode(3, root)
tree.AddChild(root, left_child)
tree.AddChild(root, right_child)
tree.AddChild(left_child, SimpleTreeNode(4, left_child))
tree.AddChild(left_child, SimpleTreeNode(5, left_child))
tree.AddChild(left_child, SimpleTreeNode(6, left_child))

def dfs(root):
    if not root:
        return 0
    # print(root.NodeValue)
    count = 1
    for child in root.Children:
        count += dfs(child)
    return count

print(dfs(root))