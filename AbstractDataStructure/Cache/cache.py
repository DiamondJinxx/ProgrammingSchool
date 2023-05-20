class NativeCache:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size
        self.hits = [0] * self.size
        self.step = 3 # for practice take size as 17 or 19

    def hash_fun(self, key):
        return len(key) % self.size

    def is_key(self, key):
        return key in self.slots

    def seek_slot(self, key):
        slot_index = self.hash_fun(key)
        if self.slots[slot_index] is None:
            return slot_index
        # while don't come back in index from hash_func - run
        i = 0
        while i < self.size:
            slot_index = (slot_index + self.step) % self.size
            if self.slots[slot_index] is None:
                return slot_index
            i += 1
        min_hit_index = self.seek_min()
        self._reset(min_hit_index)
        return min_hit_index
    
    def seek_min(self) -> int:
        return self.hits.index(min(self.hits))

    def put(self, key, value):
        index = self.seek_slot(key)
        if index is not None:
            self.slots[index] = key
            self.values[index] = value
        return index

    def get(self, key: str):
        if self.is_key(key):
            index = self.slots.index(key)
            self.hits[index] += 1
            return self.values[index]
        return None


    def _reset(self, index):
        self.values[index] = None
        self.slots[index] = None
        self.hits[index] = 0

    