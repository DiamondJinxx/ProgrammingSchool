from SearchTree import BST, BSTNode, BSTFind

def print_tree(root: BSTNode):
    if not root:
        return
    print(f'{root.NodeKey}: {root.NodeValue}')
    if root.LeftChild:
        print_tree(root.LeftChild)
    if root.RightChild:
        print_tree(root.RightChild)

root = BSTNode(24, 'Dima', None)
tree = BST(root)
tree.AddKeyValue(50, 'Maksim')
tree.AddKeyValue(21, 'Dasha')
tree.AddKeyValue(22,'Olechka')
tree.AddKeyValue(45, 'Elena')
tree.AddKeyValue(23, 'Zhora')
min_node = tree.FinMinMax(None, False)
print(min_node.NodeKey)
max_node = tree.FinMinMax(None, True)
print(max_node.NodeKey)
max_node_subtree = tree.FinMinMax(tree.Root.LeftChild, True)
print(max_node_subtree.NodeKey)
