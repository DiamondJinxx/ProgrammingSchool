class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        # в качестве value поступают строки!
        return len(value) % self.size

    def seek_slot(self, value):
        # находит индекс пустого слота для значения, или None
        return None

    def put(self, value):
        # записываем значение по хэш-функции
        
        # возвращается индекс слота или None,
        # если из-за коллизий элемент не удаётся
        # разместить 
        slot = self.seek_slot(value)
        if slot is not None:
            self.slots[slot] = value
        return slot

    def find(self, value):
        # находит индекс слота со значением, или None
        slot = self.hash_fun(value)
        if self.slots[slot] == value:
            return slot

        return None