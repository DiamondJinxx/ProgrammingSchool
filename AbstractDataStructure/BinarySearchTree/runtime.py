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
tree.AddKeyValue(45, 'Elena')
# tree.AddKeyValue(23, 'Zhora')
tree.AddKeyValue(17, 'Misha')
tree.AddKeyValue(75, 'Victor')
print(tuple(map(lambda node: node.NodeKey, tree.WideAllNodes())))
