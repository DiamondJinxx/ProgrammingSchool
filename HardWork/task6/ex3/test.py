from .merge_intervals import merge

def test_easy_merging() -> None:
    data = [[1,3], [2,5]]
    result = merge(data)
    assert result == [[1,5]]

def test_when_intervals_dont_have_intesaction() -> None:
    data = [[1,3], [4,5]]
    result = merge(data)
    assert result == [[1,3], [4,5]]

def test_when_first_interval_inside_second() -> None:
    data = [[3,4], [1,5]]
    result = merge(data)
    assert result == [[1,5]]

def test_many_intervals() -> None:
    data = [[1,3], [2,5], [6, 8]]
    result = merge(data)
    assert result == [[1,5], [6,8]]

def test_complex_intervals() -> None:
    data = [[1,3],[2,6],[8,10],[15,18]]
    result = merge(data)
    assert result == [[1,6], [8,10], [15,18]]
