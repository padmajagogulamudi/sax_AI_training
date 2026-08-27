set1={"a","b","c"}
set1.discard("d")
set1.remove("a")
# print(set1)
set1.add("x")
# print(set1)
# set1.update("y")
# set1.update("m")
# set1.update("z")
# set1.update([2,4,7])
print(set1)
# print(set1)
# print(set1)
# print(set1)
set2=set(("g1","h1","i1"))
set3=set1.union(set2)
print(set3)
print(set1)

# set1.add(set2)
# print(set1) cannot use 'set' as a set element (unhashable type: 'set')
set11 = {"apple", "banana", "cherry"}
set22 = {"google", "microsoft", "apple"}
# set11.difference_update(set22)

print(set11.difference(set22))

set4=set11.symmetric_difference(set22)
print(set4)
print(set11.intersection(set22))
set1.clear()
print(set1)
