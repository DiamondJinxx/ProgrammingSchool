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
    origins_with_expected_results = {
        "VIII": 8,
        "XVIII": 18,
        "XV": 15,
        "XII": 12,
    }
    for origin, expected_result in origins_with_expected_results.items():
        result = romanToInt(origin)
        assert result == expected_result

def test_sub() -> None:
    origins_with_expected_results = {
        "XIV": 14,
        "IX": 9,
        "XXIX": 29,
        "LIV": 54,
    }
    for origin, expected_result in origins_with_expected_results.items():
        result = romanToInt(origin)
        assert result == expected_result
