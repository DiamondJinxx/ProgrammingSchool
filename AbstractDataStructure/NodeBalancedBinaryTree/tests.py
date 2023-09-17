import pytest
import random
from BalancedBST import BalancedBST, BSTNode


@pytest.fixture()
def tree():
    return BalancedBST()


def test_empty_array(tree):
    tree.GenerateTree([])
    assert tree.Root is None
    assert tree.IsBalanced(tree.Root) == True


def test_random_array(tree):
    for i in range(random.randint(5, 15)):
        source_array = [i for i in range(random.randint(10, 100))]
        tree.GenerateTree(source_array)
        assert tree.IsBalanced
