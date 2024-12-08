
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda interval: interval[0])
    interval1 = intervals[0]
    interval2 = intervals[1]
    result = [interval1]
    if interval2[0] <= interval1[1]:
        result[-1][1] = max(interval2[1], result[-1][1])
    else:
        result.append(interval2)
    return result
