from .merge_intervals import merge

def test_easy_merging() -> None:
    result = merge()
    assert result
