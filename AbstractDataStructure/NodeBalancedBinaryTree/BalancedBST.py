class BSTNode:

    def __init__(self, key, parent):
        self.NodeKey = key  # ключ узла
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок
        self.Level = 0  # уровень узла


class BalancedBST:

    def __init__(self):
        self.Root = None  # корень дерева

    def GenerateTree(self, a):
        if not a:
            return
        a.sort()
        self.Root = self.feel(None, a)

    def feel(self, parent: BSTNode, array):
        if not array:
            return None
        middle = len(array) // 2
        node = BSTNode(array[middle], parent)
        node.Level = parent.Level + 1 if parent else 0
        node.LeftChild = self.feel(node, array[:middle])
        node.RightChild = self.feel(node, array[middle + 1:])
        return node

    def IsBalanced(self, root_node):
        return self.dfs_balance(root_node)[0]

    def dfs_balance(self, node):
        if not node:
            return True, 0
        left, right = self.dfs_balance(node.LeftChild), self.dfs_balance(
            node.RightChild)
        is_balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1
        return is_balanced, 1 + max(left[1], right[1])

    @property
    def height(self):
        return self.dfs_balance(self.Root)[1]
