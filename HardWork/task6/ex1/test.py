from .roman_to_int import romanToInt

def test_one_to_int() -> None:
    origin = "I"
    result = romanToInt(origin)
    assert result
