class PowerSet:

    def __init__(self):
        self.data = []

    def size(self):
        return len(self.data)

    def put(self, value):
        if not self.get(value):
            self.data.append(value)

    def get(self, value):
        return value in self.data

    def remove(self, value):
        result = False
        if self.get(value):
            self.data.remove(value)
            result = True 
        return result

    def intersection(self, set2):
        result = PowerSet()
        biger_set = self if self.size() > set2.size() else set2
        lower_set = self if self.size() < set2.size() else set2
        for item in biger_set:
            if lower_set.get(item):
                result.put(item)
        return result 

    def union(self, set2):
        result = PowerSet()
        for item in self.data:
            result.put(item)
        for item in set2.data:
            result.put(item)
        return result

    def difference(self, set2):
        result = PowerSet()
        for item in self.data:
            if not set2.get(item):
                result.put(item) 
        return result

    def issubset(self, set2):
        for item in set2:
            if not self.get(item):
                return False
        return True

    def __iter__(self):
        return iter(self.data)
