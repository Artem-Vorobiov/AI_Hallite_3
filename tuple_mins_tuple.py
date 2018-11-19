
a = (2,2)
b = (1,0)
c = tuple(x-y for x, y in zip(a, b))

print(type(a))
print(type(b))
print(c)