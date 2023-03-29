import unittest
from dynamic_array import DynArray


class TestDynamicArray(unittest.TestCase):

    def test_insert_capacity_not_grow(self):
        da = DynArray()
        for i in range(10):
            da.append(i)

        old_capacity = da.capacity
        da.insert(0, 'new_item')
        self.assertEqual(da[0], 'new_item')
        self.assertEqual(old_capacity, da.capacity)
        self.assertEqual(da.count, 11)

    def test_insert_capacity_grow(self):
        da = DynArray()
        new_capacity = da.capacity * 2
        for i in range(16):
            da.append(i)
        new_item = 'new_item'
        da.insert(0, new_item)
        self.assertEqual(da[0], new_item)
        self.assertEqual(new_capacity, da.capacity)

    def test_insert_out_of_range(self):
        da = DynArray()
        for i in range(16):
            da.append(i)
        with self.assertRaises(IndexError):
            da.insert(20, 'new_item')

    def test_delete_capacity_not_change_minimum(self):
        da = DynArray()
        old_capacity = da.capacity
        for i in range(15):
            da.append(i)
        da.delete(0)
        da.delete(0)
        self.assertEqual(da[0], 2)
        self.assertEqual(old_capacity, da.capacity)
        self.assertEqual(da.count, 13)
    
    def test_delete_capacity_changed(self):
        da = DynArray()
        for i in range(31):
            da.append(i)
        for i in range(0, 20):
            da.delete(0)
        self.assertEqual(21, da.capacity)
        for i in range(0, 5):
            da.delete(0)
        self.assertEqual(16, da.capacity)

    def test_delete_out_of_range(self):
        da = DynArray()
        for i in range(16):
            da.append(i)
        with self.assertRaises(IndexError):
            da.delete(20)
