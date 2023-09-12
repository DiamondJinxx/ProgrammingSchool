from GenerateBinaryTree import GenerateBBSTArray
import pytest


@pytest.fixture()
def array_setup(request):
    array = [i for i in range(1, 6)]
    return array


def test_array(array_setup):
    result_array = GenerateBBSTArray(array_setup)
    assert len(result_array) == 7
    assert result_array == [3, 2, 5, 1, None, 4, None]


def test_empty_array():
    result_array = GenerateBBSTArray([])
    assert len(result_array) == 0


def test_array_with_single_element():
    result_array = GenerateBBSTArray([1])
    assert len(result_array) == 1
    assert result_array == [1]


def test_bigger_array():
    source_array = [i for i in range(9, 0, -1)]
    result_array = GenerateBBSTArray(source_array)
    assert len(result_array) == 15
    assert result_array == [
        5, 3, 8, 2, 4, 7, 9, 1, None, None, None, 6, None, None, None
    ]
