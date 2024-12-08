
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda interval: interval[0])
    result = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= result[-1][1]:
            result[-1][1] = max(intervals[i][1], result[-1][1])
            continue
        result.append(intervals[i])
    return result
