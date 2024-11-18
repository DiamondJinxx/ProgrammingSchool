from .roman_to_int import romanToInt

def test_one_to_int() -> None:
    origin = "I"
    result = romanToInt(origin)
    assert result == 1

def test_basic_sum_to_int() -> None:
    origin = "II"
    result = romanToInt(origin)
    assert result == 2

def test_basic_sub_to_int() -> None:
    origin = "IV"
    result = romanToInt(origin)
    assert result == 4

def test_sum() -> None:
    origin = "VIII"
    result = romanToInt(origin)
    assert result == 8

