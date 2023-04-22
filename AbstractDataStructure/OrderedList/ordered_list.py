class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc
        self.size = 0

    def compare(self, v1, v2):
        cmp = 0
        if v1 < v2:
            cmp = -1
        if v1 > v2:
            cmp = +1
        return cmp
        # -1 if v1 < v2
        # 0 if v1 == v2
        # +1 if v1 > v2

    def add(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.__inc_size()
            return
        
        if self.__ascending and self.compare(value, self.head.value) == -1 or not self.__ascending and self.compare(value, self.head.value) == 1:
            self.__insert_before(self.head, new_node)
            return
        if self.__ascending and self.compare(value, self.tail.value) == 1 or not self.__ascending and self.compare(value, self.tail.value) == -1:
            self.__insert_after(self.tail, new_node)
            return

        node = self.head
        while node is not None:
            if self.compare(node.value, value) == 0: # can remove if use 
                self.__insert_after(node, new_node)
                return
            
            if self.__ascending and self.compare(value, node.value) == 1 and self.compare(value, node.next.value) < 0:
                self.__insert_after(node, new_node)
                return
            if not self.__ascending and self.compare(value, node.value) == -1 and self.compare(value, node.next.value) == 1:
                self.__insert_after(node, new_node)
                return
            node = node.next

    def __insert_before(self, before_node, new_node):
        new_node.prev = before_node.prev
        new_node.next = before_node
        if before_node.prev is not None:
            before_node.prev.next = new_node
        else:
            self.head = new_node
        before_node.prev = new_node   
        self.__inc_size()     

    def __insert_after(self, after_node, new_node):
        new_node.prev = after_node
        new_node.next = after_node.next
        if after_node.next is not None:
            after_node.next.prev = new_node
        else:
            self.tail = new_node
        after_node.next = new_node
        self.__inc_size()

    def find(self, val):
        finded = None
        node = self.head
        while node is not None:
            if node.value == val:
                finded = node
                break
            if self.__ascending and node.value > val or not self.__ascending and node.value < val:
                break
            node = node.next
        return finded
    
    def delete(self, val):
        if self.head is None:
            return
        if self.head.value == val and self.head.next is not None:
            self.head.next.prev = None
            self.head = self.head.next
            self.__dec_size()
            return 
        if self.head.value == val:
            self.head = None
            self.__dec_size()
        node = self.head
        while node is not None:
            if node.value != val:
                node = node.next
                continue
            self.__dec_size()
            if node.next is None:
                node.prev.next = None
                self.tail = node.prev
                return

            node.next.prev = node.prev
            node.prev.next = node.next
            if node.prev.next is None:
                self.tail = node.prev
            return
        self.tail = None if self.head is None else self.tail

    def clean(self, asc):
        self.__ascending = asc
        self.head = None 
        self.tail = None 

    def len(self):
        return self.size

    def get_all(self):
        r = []
        node = self.head
        while node != None:
            r.append(node)
            node = node.next
        return r
    
    def get_all_value(self):
        r = []
        node = self.head
        while node != None:
            r.append(node.value)
            node = node.next
        return r
    
    def __inc_size(self):
        self.size += 1

    def __dec_size(self):
        self.size -= 1

class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        cpm = 0
        v1 = v1.strip()
        v2 = v2.strip()
        if v1 < v2:
            cmp = -1
        if v1 > v2:
            cmp = +1
        return cmp