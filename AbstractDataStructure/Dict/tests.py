import unittest
from dictionary import NativeDictionary

class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.nd = NativeDictionary(10)

    def test_put(self):
        key = 'Meepo'
        self.nd.put(key, 4)
        self.assertEqual(self.nd.get(key), 4)
        self.nd.put(key, 5)
        self.assertEqual(self.nd.get(key), 5)

    def test_get(self):
        key = 'Meepo'
        not_key = 'Lina'
        self.nd.put(key, 4)
        self.assertEqual(self.nd.get(key), 4)
        self.assertIsNone(self.nd.get(not_key))

    def test_is_key(self):
        key = 'Meepo'
        self.nd.put(key, 5)
        
        self.assertTrue(self.nd.is_key(key))
        self.assertFalse(self.nd.is_key('not in keys'))
