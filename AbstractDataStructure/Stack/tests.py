import unittest
from stack import Stack


class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_pop(self):
        stack = Stack()
        old_size = stack.size()
        
