from .merge_intervals import merge

def test_easy_merging() -> None:
    result = merge([[1,3], [2, 5]])
    assert result
