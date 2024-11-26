from .missing_number import missing_number


def test_simple_missung_number() -> None:
    data = [1,0,3]
    result = missing_number(data)
    assert result

def test_missing_number_return_number() -> None:
    data = [1,0,3]
    result = missing_number(data)
    assert result == 2

def test_complex_seq() -> None:
    data = [1,2,3,0,5,6]
    result = missing_number(data)
    assert result == 4

def test_second_complex_seq() -> None:
    data = [1,2,3,4,0,6]
    result = missing_number(data)
    assert result == 5
