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
        self.__inc_len()

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
        if self.is_empty():
            return

        while self.head is not None and self.head.value == val:
            if self.head.next is not None:
                self.head.next.prev = None
            else:
                self.tail = None
            self.head = self.head.next
            self.__dec_len()
            if not all:
                return
        node = self.head
        while node is not None:
            if node.value != val:
                node = node.next
                continue
            self.__dec_len()
            if node.next is None:
                node.prev.next = None
                self.tail = node.prev
                return

            node.next.prev = node.prev
            node.prev.next = node.next
            if node.prev.next is None:
                self.tail = node.prev
            if not all:
                return
            node = node.next
        self.tail = None if self.head is None else self.tail

    def add_front(self, item):
        self.add_in_head(item)
    
    def remove_front(self):
        if self.is_empty():
            return None
        if self.head.next is not None:
            self.head.next.prev = None
        result = self.head
        self.head = self.head.next
        self.__dec_len()
        if self.is_empty():
            self.clean()
        return result

    def add_tail(self, item):
        self.add_in_tail(item)

    def remove_tail(self):
        if self.is_empty():
            return None
        if self.tail.prev is not None:
            self.tail.prev.next = None
        result = self.tail
        self.tail = self.tail.prev
        self.__dec_len()
        if self.is_empty():
            self.clean()
        return result

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
            if node is not afterNode:
                node = node.next
                continue
            newNode.next = node.next
            newNode.prev = node
            if node.next is not None:
                node.next.prev = newNode
            else:
                self.tail = newNode
            node.next = newNode
            self.__inc_len()
            return

    def add_in_head(self, newNode):
        if self.head is None:
            self.add_in_tail(newNode)
            return
        self.head.prev = newNode
        newNode.next = self.head
        self.head = newNode
        self.__inc_len()

    def is_empty(self):
        return self.len() == 0

    def __inc_len(self):
        self.lengh += 1

    def __dec_len(self):
        self.lengh -= 1
