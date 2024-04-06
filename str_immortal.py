import sys

a = "3443vdsff"
print(sys.getrefcount(a))
# b = "3443vdsff"
b = a
c = a
print(sys.getrefcount(a))
print(sys.getrefcount(c))
