import random

d = { "Venezuela" : 1, "Spain" : 2, "USA" : 3, "Italy" : 4}
a = random.choice(list(d.keys()))

# print(a)
# print(type(a))

www = { tuple((0,1)) : 1, tuple((0,2)) : 2, tuple((0,3)) : 3, tuple((0,4)) : 4}
print('\n\t', www)

zzz = random.choice(list(www.keys()))
print('\n\t', zzz)

print(www[zzz])
del www[zzz]
print('\n\t', www)