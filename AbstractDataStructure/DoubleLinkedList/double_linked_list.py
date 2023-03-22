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
        self.lengh = None

    def len(self):
        return self.lengh

    def insert(self, afterNode, newNode):
        pass # здесь будет ваш код

    def add_in_head(self, newNode):
        pass # здесь будет ваш код