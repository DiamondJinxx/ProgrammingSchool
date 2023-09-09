class aBST:

    def __init__(self, depth):
        tree_size = 2**(depth + 1) - 1
        self.depth = depth
        self.Tree = [None] * tree_size # массив ключей

    def FindKeyIndex(self, key):
        # ищем в массиве индекс ключа
        return self.dfs(0, key)
	
    def AddKey(self, key):
        # добавляем ключ в массив
        index_for_new_node = self.FindKeyIndex(key)
        if index_for_new_node is None:
            return -1
        # special case with root, becose -0 equal to 0 :)
        is_node_exist = (index_for_new_node == 0 and not self.is_empty()) or index_for_new_node > 0
        if is_node_exist:
            return index_for_new_node
        self.Tree[-index_for_new_node] = key
        return -index_for_new_node

    def dfs(self, root_idx, key):
        if root_idx >= len(self):
            return None
        if self.Tree[root_idx] == key:
            return root_idx
        if self.Tree[root_idx] is None:
            return -root_idx
        left_child = root_idx * 2 + 1
        right_child = root_idx * 2 + 2
        if key < self.Tree[root_idx]:
            return self.dfs(left_child, key)
        if key > self.Tree[root_idx]:
            return self.dfs(right_child, key)

    def __len__(self):
        return len(self.Tree)

    def is_empty(self):
        return all(map(lambda node: node is None, self.Tree))
