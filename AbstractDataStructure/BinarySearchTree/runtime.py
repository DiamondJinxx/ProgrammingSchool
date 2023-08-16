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
# print_tree(root)
find_node = tree.FindNodeByKey(50)
print(find_node.Node)
print(find_node.NodeHasKey)
print(find_node.ToLeft)
