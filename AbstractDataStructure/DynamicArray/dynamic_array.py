import ctypes
decrease = 1.5
increase =2

class DynArray:
    _min_capacity = 16

    def __init__(self):
        self.count = 0
        self.capacity = DynArray._min_capacity
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count
    
    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()
    
    def __getitem__(self, i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        return self.array[i]
    
    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity
    
    def append(self, itm):
        if self.count == self.capacity:
            self.resize(increase * self.capacity)
        self.array[self.count] = itm
        self.count += 1