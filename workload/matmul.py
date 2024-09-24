import sys
import random
import time
import gc
import dis
import string
import gc_count_module
import os

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

if sys.argv[1] == "no_gc":
    print("running no gc")
    import gc
    gc.disable()
elif sys.argv[1] == "with_gc":
    print("running with gc")
else:
    print("Using GC or not? Forget to specify?")

enable_tracing = False
if len(sys.argv) != 2:
    print("enable tracing")
    enable_tracing = True


def generate_random_string(max_length):
    # Generate length between 1 and max_length
    length = random.randint(1, max_length)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_matrix(size, max_str_length):
    return [[generate_random_string(max_str_length) for _ in range(size)] for _ in range(size)]


def matrix_multiply():
    random.seed(1)
    matrix_size = 600
    # 800: 5000000, 9400000
    # max_str_length = 5
    # matrix_A = generate_matrix(matrix_size, max_str_length)
    # matrix_B = generate_matrix(matrix_size, max_str_length)
    matrix_A = random.sample(range(30000, 400000), matrix_size * matrix_size)
    matrix_A = [matrix_A[i:i+matrix_size]
                for i in range(0, len(matrix_A), matrix_size)]
    matrix_B = random.sample(range(400000, 800000),
                             matrix_size * matrix_size)
    matrix_B = [matrix_B[i:i+matrix_size]
                for i in range(0, len(matrix_B), matrix_size)]

    result = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    if is_pypper and enable_tracing:
        gc_count_module.start_count_gc_list(
            250_000, "obj_dump.txt", 1, 1024, 1_000_000, 5)
    start = time.time()
    for i in range(matrix_size):
        for j in range(matrix_size):
            for k in range(matrix_size):
                result[i][j] += matrix_A[i][k] * matrix_B[k][j]
    if is_pypper and enable_tracing:
        gc_count_module.close_count_gc_list()
    latency = time.time() - start
    print("latency: {:.3f} for {}*{}".format(latency,
          matrix_size, matrix_size), file=sys.stderr)


opcode_counts = {opname: 0 for opname in dis.opname}


def trace(frame, event, arg):
    if event == 'call':
        # Get bytecode for the current frame
        code_obj = frame.f_code
        bytecode = code_obj.co_code

        # Iterate through bytecode instructions
        for offset in range(0, len(bytecode), 2):  # Assuming Python 3.6+
            opcode = bytecode[offset]
            opcode_counts[dis.opname[opcode]] += 1
    return trace


gc.collect()
matrix_multiply()
time.sleep(1)
# sys.settrace(None)

# for opcode, count in opcode_counts.items():
#     if count > 0:
#         print(f"{opcode}: {count}")
