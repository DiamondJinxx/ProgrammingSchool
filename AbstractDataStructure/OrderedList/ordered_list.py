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
        pass
        # автоматическая вставка value 
        # в нужную позицию

    def find(self, val):
        return None # здесь будет ваш код

    def delete(self, val):
        pass # здесь будет ваш код

    def clean(self, asc):
        self.__ascending = asc
        self.head = None 
        self.tail = None 

    def len(self):
        return 0 # здесь будет ваш код

    def get_all(self):
        r = []
        node = self.head
        while node != None:
            r.append(node)
            node = node.next
        return r

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