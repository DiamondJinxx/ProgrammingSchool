class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.prev = None

class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lengh = 0

    def print_all_nodes(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.next = None
            item.tail = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item
        self.lengh += 1

    def find(self, val):
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next

    def find_all(self, val):
        nodes = []
        node = self.head
        while node is not None:
            if node.value == val:
                nodes.append(node)
            node = node.next
        return nodes

    def delete(self, val, all=False):
        pass # здесь будет ваш код

    def clean(self):
        self.head = None
        self.tail = None
        self.lengh = 0

    def len(self):
        return self.lengh

    def insert(self, afterNode, newNode):
        if afterNode is None and self.is_empty():
            self.add_in_head(newNode)
            return
        if afterNode is None and not self.is_empty():
            self.add_in_tail(newNode)
            return
        node = self.head
        while node is not None:
            if node is afterNode:
                newNode.next = node.next
                newNode.prev = node
                node.next.prev = newNode
                node.next = newNode
                return
            node = node.next

    def add_in_head(self, newNode):
        if self.head is None:
            self.add_in_tail(newNode)
            return
        self.head.prev = newNode
        newNode.next = self.head
        self.head = newNode
        self.lengh += 1

    def is_empty(self):
        return self.len() == 0