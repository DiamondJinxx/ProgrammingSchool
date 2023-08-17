from SearchTree import BST, BSTNode, BSTFind


def print_tree(node: BSTNode, level=0):
    if node is None:
        return
    print_tree(node.RightChild, level + 1)
    print(' ' * 4 * level + '+- ' + str((node.NodeKey, node.NodeValue)))
    print_tree(node.LeftChild, level + 1)


root = BSTNode(24, 'Dima', None)
tree = BST(root)
tree.AddKeyValue(50, 'Maksim')
tree.AddKeyValue(21, 'Dasha')
# tree.AddKeyValue(22,'Olechka')
# tree.AddKeyValue(45, 'Elena')
# tree.AddKeyValue(23, 'Zhora')
# tree.AddKeyValue(17, 'Misha')
# tree.AddKeyValue(75, 'Victor')
print(tree.Count())
print_tree(tree.Root)
# tree.DeleteNodeByKey(45)
# tree.DeleteNodeByKey(22)
# tree.DeleteNodeByKey(23)
tree.DeleteNodeByKey(50)
tree.DeleteNodeByKey(24)
tree.DeleteNodeByKey(21)
# tree.DeleteNodeByKey(75)
# tree.DeleteNodeByKey(17)
print(tree.DeleteNodeByKey(17))
print('-' * 20)
print_tree(tree.Root)
print(tree.Count())
