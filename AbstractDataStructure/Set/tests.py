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
        expected_size = 2
        expected_values = [5, 6]
        for i in range(10):
            self.ps.put(i)
        set2 = PowerSet()
        set2_values = expected_values + [10, 12]
        for value in set2_values:
            set2.put(value)
        inter = self.ps.intersection(set2)
        self.assertEqual(inter.size(), expected_size)
        for value in expected_values:
            self.assertTrue(inter.get(value))

    def test_empty_intersection(self):
        for i in range(10):
            self.ps.put(i)
        set2 = PowerSet()
        set2_values = [10, 12]
        for value in set2_values:
            set2.put(value)
        inter = self.ps.intersection(set2)
        self.assertEqual(inter.size(), 0 )

    def test_union(self):
        expected_size = 12
        expected_values = [i for i in range(10)] + [i for i in range(10, 12)]
        for i in range(10):
            self.ps.put(i)
        set2 = PowerSet()
        for i in range(5, 12):
            set2.put(i)

        union = self.ps.union(set2)
        self.assertEqual(union.size(), expected_size)
        for val in expected_values:
            self.assertTrue(union.get(val))

    def test_union_empty_second_param(self):
        expected_size = 10
        expected_values = [i for i in range(10)] 
        for i in range(10):
            self.ps.put(i)
        set2 = PowerSet()

        union = self.ps.union(set2)
        self.assertEqual(union.size(), expected_size)
        for val in expected_values:
            self.assertTrue(union.get(val))

    def test_difference(self):
        expected_size = 5
        for i in range(10):
            self.ps.put(i)
        set2 = PowerSet()
        for i in range(5):
            set2.put(i)
        diff = self.ps.difference(set2)
        self.assertEqual(diff.size(), expected_size)
        for i in range(5, 10):
            self.assertTrue(diff.get(i)) 
        

    def test_difference_empty_result(self):
        set2 = PowerSet()
        for i in range(10):
            self.ps.put(i)
            set2.put(i)
        
        diff = self.ps.difference(set2)
        self.assertEqual(diff.size(), 0)

    def test_issubset(self):
        set2 = PowerSet()
        set3 = PowerSet()
        set4 = PowerSet()
        for i in range(10):
            self.ps.put(i)
            set2.put(i)
        for i in range(20):
            set3.put(i) 
        for i in range(5):
            set4.put(i)
        set4.put(14)
        set4.put(15)
        self.assertTrue(self.ps.issubset(set2))
        self.assertFalse(self.ps.issubset(set3))
        self.assertFalse(self.ps.issubset(set4))

