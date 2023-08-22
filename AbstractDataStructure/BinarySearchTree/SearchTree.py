from collections import deque
from typing import List, Tuple

class BSTNode:
	
    def __init__(self, key, val, parent):
        self.NodeKey = key # ключ узла
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.LeftChild = None # левый потомок
        self.RightChild = None # правый потомок

    def has_one_child(self):
        return self.LeftChild or self.RightChild

    def is_leaf(self):
        return self.LeftChild is None and self.RightChild is None

    def is_left_child(self):
        return self.Parent and self.Parent.LeftChild is self

    def is_right_child(self):
        return self.Parent and self.Parent.RightChild is self

    def set_new_child(self, new, old):
        if self.RightChild is old:
            self.RightChild = new
        if self.LeftChild is old:
            self.LeftChild = new

    def __str__(self):
        return str((self.NodeKey, self.NodeValue, str(self.Parent)))


class BSTFind: # промежуточный результат поиска

    def __init__(self):
        self.Node = None # None если 
        # в дереве вообще нету узлов

        self.NodeHasKey = False # True если узел найден
        self.ToLeft = False # True, если родительскому узлу надо 
        # добавить новый узел левым потомком

class BST:

    def __init__(self, node):
        self.Root = node # корень дерева, или None
        self.count = 1 if self.Root else 0

    def FindNodeByKey(self, key):
        # ищем в дереве узел и сопутствующую информацию по ключу
        result = BSTFind()
        tmp_node = self.Root
        if tmp_node is None:
            return result
        while tmp_node.NodeKey != key:
            if key < tmp_node.NodeKey and tmp_node.LeftChild is not None:
                tmp_node = tmp_node.LeftChild
            if key < tmp_node.NodeKey and tmp_node.LeftChild is None:
                result.ToLeft = True
                break
            if key > tmp_node.NodeKey and tmp_node.RightChild is not None:
                tmp_node = tmp_node.RightChild
            if key > tmp_node.NodeKey and tmp_node.RightChild is None:
                result.ToLeft = False
                break
        result.Node = tmp_node
        result.NodeHasKey = tmp_node.NodeKey == key
        return result

    def AddKeyValue(self, key, val):
        # добавляем ключ-значение в дерево
        # return False # если ключ уже есть
        find_node = self.FindNodeByKey(key)
        if find_node.NodeHasKey:
            return False
        self.count += 1
        if not self.Root:
            self.Root = BSTNode(key, val, None)
            return True
        parent_node = find_node.Node
        new_node = BSTNode(key, val, parent_node) 
        if find_node.ToLeft:
            parent_node.LeftChild = new_node
        else:
            parent_node.RightChild = new_node
        return True
  
    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        if not self.Root or not FromNode:
            return None
        node = FromNode
        condition_child = node.RightChild if FindMax else node.LeftChild
        while condition_child:
            node = condition_child
            condition_child = node.RightChild if FindMax else node.LeftChild
        return node


    def DeleteNodeByKey(self, key):
        # удаляем узел по ключу
        # return False # если узел не найден
        find_node = self.FindNodeByKey(key)
        if not find_node.NodeHasKey:
            return False
        node = find_node.Node
        self.count -= 1
        # if node is root and no one nodes in tree
        if node is self.Root and node.is_leaf():
            self.Root = None
            return True
        
        # node just a leaf
        if node.is_leaf() and node.is_right_child():
            node.Parent.RightChild = None
            node.Parent = None
            return True
        if node.is_leaf() and node.is_left_child():
            node.Parent.LeftChild = None
            node.Parent = None
            return True

        if node.LeftChild and not node.RightChild:
            heir = node.LeftChild 
        else:
            heir = self.FinMinMax(node.RightChild, False)

        # complexity node
        if heir.is_left_child():
            heir.Parent.LeftChild = None
            heir.RightChild = node.RightChild
        # unstead infinity recursion
        if heir.is_left_child() and node.LeftChild and node.RightChild:
            heir.LeftChild = node.LeftChild
        if heir.is_right_child():
            heir.LeftChild = node.LeftChild
        heir.Parent = node.Parent
        if heir.Parent is None:
            self.Root = heir 
        else: 
            heir.Parent.set_new_child(heir, node)  
        return True

    def Count(self):
        return self.count # количество узлов в дереве
    
    def WideAllNodes(self) -> Tuple[BSTNode]:
        result = []
        #NOTE: does this solutions work faster then sample below?
        # if not self.Root:
        #    return ()
        q = deque([self.Root]) if self.Root else deque()
        while q:
            node = q.popleft()
            result.append(node)
            if node.LeftChild:
                q.append(node.LeftChild)
            if node.RightChild:
                q.append(node.RightChild)

        return tuple(result)

    def DeepAllNodes(self, order: int) -> Tuple[BSTNode]:
        """
        order:
            0 - in-order
            1 - post-order
            2 - pre-order
        """
        def dfs(root: BSTNode, order: int) -> List[BSTNode]:
            if not root or order not in range(3):
                return []
            nodes = []
            if order == 2:
                nodes.append(root)
            nodes.extend(dfs(root.LeftChild, order))
            if order == 0:
                nodes.append(root)
            nodes.extend(dfs(root.RightChild, order))
            if order == 1:
                nodes.append(root)
            return nodes
        return tuple(dfs(self.Root, order))

