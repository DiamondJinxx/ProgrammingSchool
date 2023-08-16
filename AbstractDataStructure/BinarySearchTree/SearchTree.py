class BSTNode:
	
    def __init__(self, key, val, parent):
        self.NodeKey = key # ключ узла
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.LeftChild = None # левый потомок
        self.RightChild = None # правый потомок


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
        if not self.Root:
            self.Root = BSTNode(key, val, None)
            return
        parent_node = find_node.Node
        new_node = BSTNode(key, val, parent_node) 
        if find_node.ToLeft:
            parent_node.LeftChild = new_node
        else:
            parent_node.RightChild = new_node
  
    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        return None
	
    def DeleteNodeByKey(self, key):
        # удаляем узел по ключу
        return False # если узел не найден

    def Count(self):
        return 0 # количество узлов в дереве
