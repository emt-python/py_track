import gc

a_minor = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 11
a_minor2 = [a_minor, '123', '8vj', 'jihfqdwopiuf',
            '346787', 24634643, 43656]  # 6
a = [867987, 56789, 'opihwgr', a_minor2, 56778, 45723,
     'trh34', 1267643, 72478, 67564]  # 5

D = {"key1": "value1", "key2": "value2"}
C = [3, 4, 5]  # C contains integers and a dictionary
B = [1, "text", C]  # B contains an integer, a string, and a reference to C
A = [0, B, 6, [7, 8, "more text"]]

referents = gc.get_referents(A)
# print(referents)
