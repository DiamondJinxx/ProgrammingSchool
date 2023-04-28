class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        return len(value) % self.size

    def seek_slot(self, value):
        slot_index = self.hash_fun(value)
        if self.slots[slot_index] is None:
            return slot_index
        # while don't come back in index from hash_func - run
        i = 0
        while i < self.size:
            slot_index = (slot_index + self.step) % self.size
            if self.slots[slot_index] is None:
                return slot_index
            i += 1
        return None

    def put(self, value):
        slot = self.seek_slot(value)
        if slot is not None:
            self.slots[slot] = value
        return slot

    def find(self, value):
        slot = self.hash_fun(value)
        if self.slots[slot] == value:
            return slot
        try:
            return self.slots.index(value)
        except ValueError:
            return None