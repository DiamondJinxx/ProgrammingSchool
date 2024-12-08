# Описание задачи https://leetcode.com/problems/missing-number/description/
#
def missing_number(nums: list[int]) -> int:
    nums_sum = sum(nums)
    return len(nums) * (len(nums) + 1) // 2 - nums_sum
