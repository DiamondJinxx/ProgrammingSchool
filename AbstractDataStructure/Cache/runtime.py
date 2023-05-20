from cache import NativeCache
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def debug(nc: NativeCache):
    print(f'slots : {nc.slots}')
    print(f'values : {nc.values}')
    print(f'hits : {nc.hits}')

nc = NativeCache(17)
debug(nc)
print(randomword(5))
for i in range(nc.size):
    nc.put(str(i),randomword(4))
debug(nc)
for i in range(nc.size):
    for j in range(random.randint(0, 10)):
        nc.get(str(i))
debug(nc)

nc.put('new', 'new')

print('--------------------------------')
debug(nc)
