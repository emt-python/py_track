import time
import argparse
from math import sin, cos, tan


def do_work_fn(x, i, complex_data):
    # Ensure x is an integer for bitwise operations
    x = int(x)
    result = (x >> 8) | (i & x) & (i | x)
    # Perform floating-point operations separately
    complex_operation = sin(result) * cos(i) * tan(i) * sin(i)
    complex_operation = sin(complex_operation) * \
        cos(result) * tan(i) * sin(result)
    # Convert the result of floating-point operations to an integer if needed for further bitwise operations
    complex_data.append(complex_operation)
    # If further bitwise operations are required, ensure to convert back to int
    # Example conversion, adjust as necessary
    return int(complex_operation * 1000)


def inline_loop(x, its, complex_data):
    x = int(x)  # Ensure x is an integer for bitwise operations
    for i in range(its):
        # Bitwise operations require integer operands
        x = x | (x >> 8) | (i & x)
        if i % 10000 == 0:  # Manipulate complex_data at intervals
            # Directly append i to complex_data without conversion, assuming i is always an integer
            complex_data.append(i)
    return x


def fn_call_loop(x, its, complex_data):
    x = int(x)  # Ensure x starts as an integer for bitwise operations
    for i in range(its):
        # do_work_fn ensures to return an int
        x = x | do_work_fn(x, i, complex_data)
    return x


def main():
    parser = argparse.ArgumentParser(
        description='Test time breakdown with increased memory and cache usage.')
    parser.add_argument('--inline', dest='inline', type=int,
                        default=250000000, help="inline iterations")
    parser.add_argument('--fn_call', dest='fn_call', type=int,
                        default=25000000, help="function call iterations")  # 250000000
    args = parser.parse_args()

    complex_data = []  # Data structure to increase memory usage
    x = 0

    # start_fn_call = time.perf_counter()
    for i in range(1):
        x = fn_call_loop(x, args.fn_call, complex_data)
    # elapsed_fn_call = time.perf_counter() - start_fn_call
    # print(f"elapsed fn call = {elapsed_fn_call:.2f}s")

    # start_inline_loop = time.perf_counter()
    # for a in range(1):
    #     x = inline_loop(x, args.inline, complex_data)
    # elapsed_inline_loop = time.perf_counter() - start_inline_loop
    # print(f"elapsed inline loop = {elapsed_inline_loop:.2f}s")

    # print(f"ratio fn_call/total = {100 * elapsed_fn_call / (elapsed_fn_call + elapsed_inline_loop):.2f}%")
    # print(f"ratio inline/total = {100 * elapsed_inline_loop / (elapsed_fn_call + elapsed_inline_loop):.2f}%")


if __name__ == '__main__':
    main()
