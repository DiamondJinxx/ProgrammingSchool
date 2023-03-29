import ctypes


decrease = 1.5
increase = 2


class DynArray:
    __min_capacity = 16
    
    def __init__(self):
        self.count = 0
        self.capacity = DynArray.__min_capacity
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self,i):
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
            self.resize(increase*self.capacity)
        self.array[self.count] = itm
        self.count += 1

    def insert(self, i, itm):
        if i < 0 or i > self.count:
            raise IndexError('Index is out of bounds')
        if i == self.count:
            self.append(itm)
            return
        if self.count + 1 >= self.capacity:
            self.resize(increase*self.capacity)
        for j in range(self.count, i, -1):
            self.array[j] = self.array[j - 1]
        self.array[i] = itm
        self.count += 1
        

    def delete(self, i):
        if i < 0 or i > self.count:
            raise IndexError('Index is out of bounds')
        if self.is_empty():
            return
        diff = 0
        for j in range(0, self.count - 1):
            if j == i:
                diff += 1
            self.array[j] = self.array[j + diff]
        self.count -= 1
        if self.count < int(self.capacity / 2):
            new_capacity = int(self.capacity / decrease)
            if new_capacity < DynArray.__min_capacity:
                new_capacity = DynArray.__min_capacity
            self.resize(new_capacity)
    
    def is_empty(self):
        return self.count == 0
