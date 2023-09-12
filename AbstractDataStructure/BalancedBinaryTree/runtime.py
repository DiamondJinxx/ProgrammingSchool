from GenerateBinaryTree import *

source_array = [i for i in range(9, 0, -1)]
result_array = GenerateBBSTArray(source_array)
assert len(result_array) == 15
print(result_array)
# assert result_array == [
# 5, 3, 8, 2, 4, 7, 9, 1, None, None, None, 6, None, None, None
# ]
