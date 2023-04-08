import unittest
from stack import Stack


class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_push(self):
        stack = Stack()
        self.assertEqual(stack.size(), 0)
        new = 'new'
        stack.push(new)
        # I think we should not use pop or peek methods, because we didn't test its before
        self.assertEqual(new, stack.stack[0])
        # but I use size() method, yes, logick is my second name
        self.assertEqual(stack.size(), 1)

    def test_pop(self):
        stack = Stack()
        value = 'new'
        stack.push(value)
        self.assertEqual(value, stack.pop())
        self.assertTrue(stack.is_empty())
        self.assertIsNone(stack.pop())

        for i in range(10):
            stack.push(i)

        for i in range(9, -1, -1):
            self.assertEqual(i, stack.pop())
        self.assertTrue(stack.is_empty())

    def test_peek(self):
        stack = Stack()
        new = 'new'
        stack.push(new)
        self.assertEqual(new, stack.peek())
        self.assertEqual(1, stack.size())
        stack.pop()
        self.assertIsNone(stack.peek())

    def test_size(self):
        stack = Stack()
        self.assertEqual(stack.size(), 0)
        expected_size = 10
        for i in range(0, expected_size):
            stack.push(i)
        self.assertEqual(stack.size(), expected_size)
