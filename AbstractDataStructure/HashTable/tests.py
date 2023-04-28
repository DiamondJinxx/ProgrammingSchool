import unittest
from hash_table import HashTable


class HashTableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ht = HashTable(19, 3)

    def test_hash_fun(self):
        value = 'some_string'
        expected_hash = len(value) % 19
        self.assertEqual(expected_hash, self.ht.hash_fun(value))
    
    def test_seek_slot(self):
        string = 'some_string'
        expected_slot = self.ht.hash_fun(string)
        self.assertEqual(expected_slot, self.ht.seek_slot(string))

        # collision
        for i in range(self.ht.size):
            self.ht.put(string)
        self.assertIsNone(self.ht.seek_slot(string))
    
    def test_put(self):
        string = 'some_string'
        expected_slot = self.ht.hash_fun(string)
        slot = self.ht.put(string)
        self.assertEqual(expected_slot, slot)

        # collision
        for i in range(self.ht.size):
            self.ht.put(string)
        self.assertIsNone(self.ht.put(string))

    
    def test_find(self):
        value = 'some_string'
        index = self.ht.hash_fun(value)
        self.ht.put(value)
        self.assertEqual(index, self.ht.find(value))

        not_in_table = 'not_in_table'
        self.assertIsNone(self.ht.find(not_in_table))

    