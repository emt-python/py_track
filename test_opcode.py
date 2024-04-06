import dis


def example():
    a = 1
    b = 2
    c = a + b
    print(c)


example()
dis.dis(example)

#   4           0 RESUME                   0

#   5           2 LOAD_CONST               1 (45678)
#               4 STORE_FAST               0 (x)

#   6           6 LOAD_FAST                0 (x)
#               8 LOAD_CONST               2 (1)
#              10 BINARY_OP                0 (+)
#              14 STORE_FAST               0 (x)
#              16 RETURN_CONST             0 (None)
