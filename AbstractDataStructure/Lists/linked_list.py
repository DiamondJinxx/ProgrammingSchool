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
        while node != None:
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
        return [] 

    def delete(self, val, all=False):
        node = self.head
        prev_node = node
        while node is not None:
            if node.value == val:
                prev_node.next = node.next
                self.lengh = self.lengh - 1
                if not all:
                    return
            prev_node = node
            node = node.next
                
    def clean(self):
        self.head = None
        self.tail = None 

    def len(self):
        return self.lengh 

    def insert(self, afterNode, newNode):
        pass
    

