heat_set = {
    (1, 3),
    (2, 4),
    (2, 6),
    (9, 10),
    (13, 19),
    (20, 21),
    (21, 29),
    (30, 31),
    (100, 190),
    (100, 120),
    (130, 200),
    (201, 202)
}
while True:
    merged = set()
    for tuple1 in heat_set:
        remaining_counter = len(heat_set) - 1
        for tuple2 in heat_set:
            if tuple1 != tuple2:
                if tuple1[1] >= tuple2[0] and tuple1[0] <= tuple2[1]:
                    merged.add(
                        (min(tuple1[0], tuple2[0]), max(tuple1[1], tuple2[1])))
                else:
                    remaining_counter -= 1
        if remaining_counter == 0:
            merged.add(tuple1)
    if merged == heat_set:
        break
    else:
        heat_set = merged.copy()

print(heat_set)
