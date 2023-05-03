from dictionary import NativeDictionary

def debug(d: NativeDictionary) -> None:
    print(f'size is: {d.size}')
    print(f'slots is: {d.slots}')
    print(f'values is: {d.values}')


d = NativeDictionary(20)
debug(d)
