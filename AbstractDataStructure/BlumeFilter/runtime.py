from bloom import BloomFilter

def bin_print(num: int):
    print('{0:b}'.format(num))

bf = BloomFilter(32)
test = '0123456789'
test_keys = [test[i:] + test[: i] for i in range(10)]
i = 0
for key in test_keys:
    i += 1
    if i % 2 == 0:
        continue
    bf.add(key)
    print(i)

for key in test_keys:
    print(key, bf.is_value(key))