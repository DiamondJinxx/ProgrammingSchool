class BloomFilter:

    def __init__(self, f_len):
        self.filter_len = f_len
        self.filter = 0


    def hash1(self, str1):
        return 1 << self.__hash(str1, 17)

    def hash2(self, str1):
        return 1 << self.__hash(str1, 223)

    def add(self, str1):
        mask1 = self.hash1(str1)
        mask2 = self.hash2(str1)
        self.filter = self.filter | mask1 | mask2

    def is_value(self, str1):
        mask1 = self.hash1(str1)
        mask2 = self.hash2(str1)
        return bool(self.filter & mask1) and bool(self.filter & mask2)

    def __hash(self, key: str, magic: int):
        result = 0
        for c in key:
            code = ord(c)
            result = (result * magic + code) % self.filter_len
        return result