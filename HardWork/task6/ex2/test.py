from .missing_number import missing_number


def test_simple_missung_number() -> None:
    data = [1,0,3]
    result = missing_number(data)
    assert result

