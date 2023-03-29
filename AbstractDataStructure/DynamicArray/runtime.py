from dynamic_array import DynArray

def log(array):
    print(f'count: {array.count}')
    print(f'capacity: {array.capacity}')
    # print(f'array: {array.array}')

def print_all_elements(da):
    for i in range(0, len(da)):
        print(da[i])

da = DynArray()
# log(da)


for i in range(1024):
    da.append(i)

da.insert(21, 'insert_element')
log(da)

da.delete(da.count)
log(da)
da.delete(da.count)
log(da)
for i in range(0, 1015):
    da.delete(0)
log(da)
da.delete(1)
log(da)
da.delete(1)
log(da)
da.delete(1)
log(da)
da.insert(0, 1)
log(da)
