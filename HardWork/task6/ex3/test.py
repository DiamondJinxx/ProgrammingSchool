from .merge_intervals import merge

def test_easy_merging() -> None:
    data = [[1,3], [2,5]]
    result = merge(data)
    assert result == [[1,5]]

def test_when_intervals_dont_have_intesaction() -> None:
    data = [[1,3], [4,5]]
    result = merge(data)
    assert result == [[1,3], [4,5]]

