from ordered_list import OrderedList, OrderedStringList


def debug(lst: OrderedList):
    head = lst.head if lst.head is None else lst.head.value
    tail = lst.tail if lst.tail is None else lst.tail.value
    print(f"head is: {head}")
    print(f"tail is: {tail}")
    print(f"size is: {lst.len()}")
    print(f'all elemts: {lst.get_all()}')
    print(f'all values: {lst.get_all_value()}')



# lst = OrderedList(True)
# debug(lst)
# lst.add(12)
# debug(lst)
# lst.add(11)
# debug(lst)
# lst.add(15)
# debug(lst)
# lst.add(11)
# debug(lst)
# lst.add(12)
# debug(lst)
# lst.add(20)
# debug(lst)

# lst.add(16)
# debug(lst)
# lst.add(13)
# debug(lst)

# print(lst.find(16).value)


# убывающий
lst = OrderedList(False)
debug(lst)
lst.add(12)
debug(lst)
lst.add(11)
debug(lst)
lst.add(15)
debug(lst)
lst.add(11)
debug(lst)
lst.add(12)
debug(lst)
lst.add(20)
debug(lst)
lst.add(16)
debug(lst)
lst.add(13)
debug(lst)
lst.delete(15)
debug(lst)
lst.delete(12)
debug(lst)
lst.delete(20)
debug(lst)
lst.delete(11)
debug(lst)
lst.delete(11)
debug(lst)
lst.delete(16)
debug(lst)
lst.delete(13)
debug(lst)
lst.delete(12)
debug(lst)

# lst = OrderedStringList(True)
# lst.add('some')
# debug(lst)
# lst.add('any')
# debug(lst)
# lst.add('full damage')
# debug(lst)

