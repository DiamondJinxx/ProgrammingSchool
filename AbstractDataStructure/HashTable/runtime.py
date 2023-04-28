from hash_table import HashTable
import pprint


def debug(ht: HashTable) -> None:
    print(f'slots: {ht.slots}')

string = 'some_looooooong_string'
ht = HashTable(19, 3)
# print(ht.hash_fun(string))
# ht.put(string)
# debug(ht)
# ht.put(string)
# debug(ht)
slot_index = ht.hash_fun(string)
for i in range(ht.size):
    ht.put(str(i))
# ht.put(string)
# ht.put(string)
# debug(ht)
# print(ht.seek_slot(string))
debug(ht)
print(ht.find('2'))
print(ht.find('32'))