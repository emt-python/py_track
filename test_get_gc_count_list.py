import sys
import random
import time
import gc_count_module
import gc
# gc.disable()

func = "obj_dump"
sys.setswitchinterval(0.0001)

get_refcnt = False
if get_refcnt == True:
    def standard_deviation(data):
        mean = sum(data) / len(data)
        variance = sum([(x - mean) ** 2 for x in data]) / len(data)
        return variance ** 0.5
    a_refcnt_list = []
    b_refcnt_list = []
    a_refcnt_list_changes = []
    b_refcnt_list_changes = []


def stream_to_file(tuple_list):
    import csv
    csv_file = 'all_ids.csv'
    print("streaming...")
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write each tuple as a row in the CSV file
        for row in tuple_list:
            writer.writerow(row)
    print("complete")
# flat_elem_A = []
# flat_elem_B = []
# flat_elem_result = []
# row_id_A = []
# row_id_B = []
# row_id_result = []
# existing_ids = set()


def matrix_multiply():
    random.seed(1)
    matrix_size = 600
    # matrix_A = [[random.randint(1000, 2000) for _ in range(
    #     matrix_size)] for _ in range(matrix_size)]
    # matrix_B = [[random.randint(2001, 3000) for _ in range(
    #     matrix_size)] for _ in range(matrix_size)]

    matrix_A = random.sample(range(3000, 400000), matrix_size * matrix_size)
    matrix_A = [matrix_A[i:i+matrix_size]
                for i in range(0, len(matrix_A), matrix_size)]
    matrix_B = random.sample(range(400000, 800000), matrix_size * matrix_size)
    matrix_B = [matrix_B[i:i+matrix_size]
                for i in range(0, len(matrix_B), matrix_size)]

    result = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
    if get_refcnt == True:
        a_prev = 0
        b_prev = 0

    # gc_count_module.print_get_sizeof()
    gc_count_module.start_count_gc_list(
        250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 1, 10, 3500000)
    start = time.time()
    # with open("all_ids.csv", "w") as fd:
    for i in range(matrix_size):
        # current_time = time.time()
        # formatted_time = "{:.3f}".format(current_time)
        # if id(matrix_A[i]) not in existing_ids:
        # fd.write("A\trow\t{}\t{}\n".format(id(matrix_A[i]), formatted_time))
        # existing_ids.add(id(matrix_A[i]))
        for j in range(matrix_size):
            # current_time = time.time()
            # formatted_time = "{:.3f}".format(current_time)
            # fd.write("B\tcol\t{}\t{}\n".format(id(matrix_B[j]), formatted_time))
            for k in range(matrix_size):
                # result[i][j] += A[i][j] * B[j][k] # upper
                # result[i][j] += A[j][k] * B[k][i] # whole
                result[i][j] += matrix_A[i][k] * matrix_B[k][j]
                # if id(matrix_A[i][k]) not in existing_ids:
                # fd.write("A\telem\t{}\t{}\n".format(id(matrix_A[i][k]), formatted_time))
                # existing_ids.add(id(matrix_A[i][k]))
                # if id(matrix_B[k][j]) not in existing_ids:
                # fd.write("B\telem\t{}\t{}\n".format(id(matrix_B[k][j]), formatted_time))
                # existing_ids.add(id(matrix_B[k][j]))
                # if id(result[i][j]) not in existing_ids:
                # fd.write("res\telem\t{}\t{}\n".format(id(result[i][j]), formatted_time))
                # existing_ids.add(id(result[i][j]))

                # flat_elem_result.append(("res", "elem", id(result[i][j])))
                # row_id_result.append(("res", "row", id(result[i])))
                # c_cur = sys.getrefcount(result[i][j])
                # c_refcnt_list.append(c_cur)
                # c_refcnt_list_changes.append(c_cur - c_prev)
                # c_prev = c_cur
                if get_refcnt == True:
                    if k == 30 and i == 29:
                        a_cur = sys.getrefcount(matrix_A[i][k])
                        a_refcnt_list.append(a_cur)
                        a_refcnt_list_changes.append(a_cur - a_prev)
                        a_prev = a_cur
                    if k == 190 and j == 190:
                        b_cur = sys.getrefcount(matrix_B[k][j])
                        b_refcnt_list.append(b_cur)
                        b_refcnt_list_changes.append(b_cur - b_prev)
                        b_prev = b_cur
    # print("id_A: {}, id_B: {}, id_result: {}".format(
    #     id(matrix_A), id(matrix_B), id(result)))

    latency = time.time() - start
    print("latency: {:.3f} for {}*{}".format(latency,
          matrix_size, matrix_size), file=sys.stderr)
    gc_count_module.close_count_gc_list()

    # all_elem_id = []
    # elem_resultA = [[id(element) for element in row] for row in matrix_A]
    # flat_elem_A = [id_value for row in elem_resultA for id_value in row]
    # print("A: min: {}, max: {}".format(min(flat_elem_A), max(flat_elem_A)))
    # flat_elem_A = [("A", "elem", elem) for elem in flat_elem_A]
    # row_id_A = [id(element_) for element_ in matrix_A]
    # row_id_A = [("A", "row", elem) for elem in row_id_A]
    # all_elem_id.extend(flat_elem_A)
    # all_elem_id.extend(row_id_A)

    # elem_resultB = [[id(element) for element in row] for row in matrix_B]
    # flat_elem_B = [id_value for row in elem_resultB for id_value in row]
    # print("B: min: {}, max: {}".format(min(flat_elem_B), max(flat_elem_B)))
    # flat_elem_B = [("B", "elem", elem) for elem in flat_elem_B]
    # row_id_B = [id(element_) for element_ in matrix_B]
    # row_id_B = [("B", "row", elem) for elem in row_id_B]
    # all_elem_id.extend(flat_elem_B)
    # all_elem_id.extend(row_id_B)

    # elem_result = [[id(element) for element in row] for row in result]
    # flat_elem_result = [id_value for row in elem_result for id_value in row]
    # print("result: min: {}, max: {}".format(
    #     min(flat_elem_result), max(flat_elem_result)))
    # flat_elem_result = [("res", "elem", elem) for elem in flat_elem_result]
    # row_id_result = [id(element_) for element_ in result]
    # row_id_result = [("res", "row", elem) for elem in row_id_result]
    # all_elem_id.extend(flat_elem_result)
    # all_elem_id.extend(row_id_result)

    # stream_to_file(all_elem_id)

    if get_refcnt == True:
        a_refcnt_list_changes.pop(0)
        b_refcnt_list_changes.pop(0)

        print("a stddev:", standard_deviation(a_refcnt_list))
        print("b stddev:", standard_deviation(b_refcnt_list))

        print("a max:", max(a_refcnt_list), "min:", min(a_refcnt_list))
        print("b max:", max(b_refcnt_list), "min:", min(b_refcnt_list))

        print("a changes stddev:", standard_deviation(a_refcnt_list_changes))
        print("b changes stddev:", standard_deviation(b_refcnt_list_changes))

        print("a changes max:", max(a_refcnt_list_changes),
              "min:", min(a_refcnt_list_changes))
        print("b changes max:", max(b_refcnt_list_changes),
              "min:", min(b_refcnt_list_changes))

        print(a_refcnt_list)
        print(b_refcnt_list)
        print()
        print(a_refcnt_list_changes)
        print(b_refcnt_list_changes)


# gc_count_module.start_count_gc_list(
#     200_000, "/home/lyuze/workspace/py_track/{}.txt".format(func), 0, 21, 250000)
gc.collect()
matrix_multiply()
# import dis
# bytecode = dis.Bytecode(matrix_multiply)
# for instruction in bytecode:
#     print("\t", instruction.opname, instruction.argval)
# gc_count_module.close_count_gc_list()
# time.sleep(41)
# time.sleep(1)
