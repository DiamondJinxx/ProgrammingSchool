from dictionary import NativeDictionary

def debug(d: NativeDictionary) -> None:
    print(f'size is: {d.size}')
    print(f'slots is: {d.slots}')
    print(f'values is: {d.values}')


d = NativeDictionary(20)
d.put('Dima', 23)
debug(d)
d.put('Dima', 24)
debug(d)
print(d.is_key('Dima123'))