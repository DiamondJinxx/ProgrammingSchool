def GenerateBBSTArray(a):
    if not a:
        return []
    bst_list = [None for i in range(tree_size(a))]
    a.sort()
    add(bst_list, a)
    return bst_list


def add(bst_list, array, index=0):
    if not array:
        return
    middle = len(array) // 2
    bst_list[index] = array[middle]

    add(bst_list, array[:middle], 2 * index + 1)
    add(bst_list, array[middle + 1:], 2 * index + 2)


def tree_size(a):
    d = 0
    size = 2**(d + 1) - 1
    while len(a) > size:
        d += 1
        size = 2**(d + 1) - 1
    return size
