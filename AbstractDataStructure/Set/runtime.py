from powerset import PowerSet

ps = PowerSet()
ps.put(1)
ps.put(2)
ps.put(3)
ps.put(4)
ps.put(5)
for item in ps:
    print(item)

print(6 in ps)