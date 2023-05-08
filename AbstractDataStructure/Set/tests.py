import unittest
from powerset import PowerSet

class TestPowerSet(unittest.TestCase):
    def setUp(self):
        self.ps = PowerSet()

    def test_put(self):
        element = 1
        self.ps.put(element)
        self.assertEqual(self.ps.size(), 1)
        self.assertTrue(self.ps.data[0] is element)
    
    def test_put_same_elements(self):
        element = 12
        self.ps.put(element)
        self.assertEqual(self.ps.size(), 1)
        self.ps.put(element)
        self.assertEqual(self.ps.size(), 1)

    def test_get(self):
        pass

    def test_remove(self):
        start_size = 10
        remove_item = 5
        for i in range(start_size):
            self.ps.put(i)
        self.assertEqual(self.ps.size(), start_size)
        self.ps.remove(remove_item)
        self.assertEqual(self.ps.size(), start_size - 1)
        self.assertTrue(not self.ps.get(remove_item))

    def test_intersection(self):
        pass

    def test_union(self):
        pass

    def test_difference(self):
        pass

    def test_issubset(self):
        pass
