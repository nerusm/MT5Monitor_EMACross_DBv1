import sys

print(sys.argv)
l = sys.argv[1]
print(l)
print(type(l))
# l=list(l)
# print(type(l))
# print(l)

LIST = l.split(sep=",")
print(type(LIST))
print(int(LIST[1]))
for e in LIST:
    print(type(int(e)))
