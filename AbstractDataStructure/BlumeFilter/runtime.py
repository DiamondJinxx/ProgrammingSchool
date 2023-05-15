from bloom import BloomFilter

def bin_print(num: int):
    print('{0:b}'.format(num))

bf = BloomFilter(32)
arr = int()
# print(type(arr))
# # set to one
# # print(arr | 1 << 7)
# # set to zero
# # print(arr & ~(1 << 7))
# v = arr | 1 << 5
# bin_print(10)
# print(v)
# #read 
# print(v & 1 << 5)
# v = arr & ~(1 << 5)
# print(v)
test = '0123456789'
for i in range(10):
    print(test[i:] + test[: i])

# print(bf.hash1(test))
# print(bf.hash2(test))