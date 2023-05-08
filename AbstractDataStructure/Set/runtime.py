from powerset import PowerSet

def debug(ps: PowerSet) -> None:
    print(f'size: {ps.size()}')
    print(f'data: {ps.data}')

ps = PowerSet()
# ps.put(1)
# ps.put(2)
# ps.put(3)
# ps.put(4)
# ps.put(5)

# set2 = PowerSet()
# set2.put(2)
# set2.put(3)
# set2.put(8)
# set2.put(9)

# inter = ps.intersection(set2)
# debug(inter)

# set3 = PowerSet()
# set3.put(10)
# set3.put(11)
# set3.put(12)
# empty_inter = ps.intersection(set3)
# debug(empty_inter)


# union = ps.union(set2)
# debug(union)
for i in range(10):
    ps.put(i)
set2 = PowerSet()
for i in range(5, 12):
    set2.put(i)

union = ps.union(set2)
debug(union)
# for val in expected_values:
    # assertTrue(union.get(val))
expected_values = [i for i in range(10)] + [i for i in range(10, 13)]
print(expected_values)