class NativeDictionary:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size  # for keys
        self.values = [None] * self.size

    def hash_fun(self, key):
        return len(key) % self.size

    def is_key(self, key):
        return key in self.slots

    def put(self, key, value):
        index = self.hash_fun(key)
        self.slots[index] = key
        self.values[index] = value

    def get(self, key):
       index = self.hash_fun(key)
       return self.values[index] if self.is_key(key) else None