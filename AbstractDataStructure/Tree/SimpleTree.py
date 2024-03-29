class SimpleTreeNode:
	
    def __init__(self, val, parent):
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.Children = [] # список дочерних узлов
	
class SimpleTree:

    def __init__(self, root):
        self.Root = root # корень, может быть None
	
    def AddChild(self, ParentNode, NewChild):
        # ваш код добавления нового дочернего узла существующему ParentNode
        if ParentNode is None:
            return
        NewChild.Parent = ParentNode
        ParentNode.Children.append(NewChild)
  
    def DeleteNode(self, NodeToDelete):
        # remove Node from list and let GC make his work
        if NodeToDelete.Parent is not None and NodeToDelete in NodeToDelete.Parent.Children:
            NodeToDelete.Parent.Children.remove(NodeToDelete)
        NodeToDelete.Parent = None

    def GetAllNodes(self):
        # ваш код выдачи всех узлов дерева в определённом порядке
        def dfs(root):
            if not root:
                return []
            result = [root]
            for child in root.Children:
                result.extend(dfs(child))
            return result
        return dfs(self.Root)

    def FindNodesByValue(self, val):
        # ваш код поиска узлов по значению
        def dfs(root):
            if not root:
                return []
            result = []
            if root.NodeValue == val: result.append(root)
            for child in root.Children:
                result.extend(dfs(child))
            return result
        return dfs(self.Root)
   
    def MoveNode(self, OriginalNode, NewParent):
        # ваш код перемещения узла вместе с его поддеревом -- 
        # в качестве дочернего для узла NewParent
        old_parent = OriginalNode.Parent
        old_parent.Children.remove(OriginalNode)
        OriginalNode.Parent = NewParent
        NewParent.Children.append(OriginalNode)
   
    def Count(self):
        # количество всех узлов в дереве
        def dfs(root) -> int:
            if not root:
                return 0
            count = 1
            for child in root.Children:
                count += dfs(child)
            return count
        return dfs(self.Root)

    def LeafCount(self):
        # количество листьев в дереве
        def dfs(root) -> int:
            if not root:
                return 0
            if not root.Children:
                return 1
            count = 0
            for child in root.Children:
                count += dfs(child)
            return count
        return dfs(self.Root)

    def nodes_lvl(self):
        # we can use hash table in SimpleTree for store lvl: [nodes]
        def dfs(root, prev_lvl):
            if not root:
                return []
            current_lvl = prev_lvl + 1
            result = [(root, current_lvl)]
            for child in root.Children:
                result.extend(dfs(child, current_lvl))
            return result
        return dfs(self.Root, 0)

    def EvenTrees(self):
        if not self.Root:
            return []
        res = []
        stack = []
        node = self.Root
        for i in range(len(node.Children)):
            vizit = []
            vizit.append(node)
            stack.insert(0, node.Children[i])
            while stack:
                stack.extend(stack[0].Children)
                vizit.insert(0, stack[0])
                stack.pop(0)
            if len(vizit) % 2 == 1:
                res.append(node)
                res.append(node.Children[i])

        return res
