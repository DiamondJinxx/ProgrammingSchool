from BalancedBST import BalancedBST, BSTNode


def print_tree(node: BSTNode, level=0):
    if node is None:
        return
    print_tree(node.RightChild, level + 1)
    print(' ' * 4 * level + '+- ' + str(node.NodeKey))
    print_tree(node.LeftChild, level + 1)


tree = BalancedBST()
array = [i for i in range(1, 6)]
source_array = [i for i in range(9, 0, -1)]
# tree.GenerateTree(array)
# tree.GenerateTree(source_array)
# print_tree(tree.Root)
# print(tree.IsBalanced(tree.Root))

tree.GenerateTree([])
print_tree(tree.Root)
print(tree.IsBalanced(tree.Root))
