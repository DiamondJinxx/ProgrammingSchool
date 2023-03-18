class Node:

    def __init__(self, v):
        self.value = v
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.lengh = 0

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item
        self.lengh = self.lengh + 1

    def print_all_nodes(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next

    def find(self, val):
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val):
        finding_items = []
        node = self.head
        while node is not None:
            if node.value == val:
                finding_items.append(node)
            node = node.next
        return finding_items

    def delete(self, val, all=False):
        if self.is_empty():
            return
        if not all:
            if self.head.value == val:
                self.head = self.head.next
                self.lengh = self.lengh - 1
                return
            node = self.head.next
            prev_node = self.head
            while node is not None:
                if node.value == val:
                    prev_node.next = node.next
                    self.lengh = self.lengh - 1
                    break
                prev_node = node
                node = node.next

        self.actual_tail() 


    def actual_tail(self):
        new_tail = self._get_real_tail()
        self.tail = new_tail
    
    def _get_real_tail(self) -> Node:
        node = self.head
        while node is not None:
            if node.next is None:
                return node
            node = node.next
                
    def clean(self):
        self.head = None
        self.tail = None
        self.lengh = 0

    def len(self):
        return self.lengh

    def insert(self, afterNode, newNode):
        if afterNode is None:
            if self.is_empty():
                newNode.next = None
                self.add_in_tail(newNode)
                return
            newNode.next = self.head
            self.head = newNode
            self.lengh = self.lengh + 1
            return
        if afterNode == self.tail:
            self.add_in_tail(newNode)
            return
        node = self.head
        while node is not None:
            if node is afterNode:
                newNode.next = node.next
                node.next = newNode
                self.lengh = self.lengh + 1
                return
            node = node.next

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def is_empty(self):
        return self.len() == 0
