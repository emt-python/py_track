import time
import json
import sys

import argparse


EMPTY = ({}, 2000)
SIMPLE_DATA = {'key1': 0, 'key2': True, 'key3': 'value', 'key4': 'foo',
               'key5': 'string'}
SIMPLE = (SIMPLE_DATA, 1000)
NESTED_DATA = {'key1': 0, 'key2': SIMPLE[0], 'key3': 'value', 'key4': SIMPLE[0],
               'key5': SIMPLE[0], 'key': '\u0105\u0107\u017c'}
NESTED = (NESTED_DATA, 100000)
HUGE = ([NESTED[0]] * 10000, 1000)

CASES = ['EMPTY', 'SIMPLE', 'NESTED', 'HUGE']


def bench_json_dumps(data):
    for obj, count_it in data:
        for _ in count_it:
            json.dumps(obj)


def add_cmdline_args(cmd, args):
    if args.cases:
        cmd.extend(("--cases", args.cases))


def main():
    # cases = CASES
    parser = argparse.ArgumentParser(
        description="Run different Python benchmarks.")
    parser.add_argument(
        'benchmark', help='The benchmark to run (iter, mapreduce, fibonacci, queue)')
    args = parser.parse_args()

    if args.benchmark == 'empty':
        case = 'EMPTY'
    elif args.benchmark == 'simple':
        case = 'SIMPLE'
    elif args.benchmark == 'nested':
        case = 'NESTED'
    elif args.benchmark == 'huge':
        case = 'HUGE'
    else:
        raise ValueError("Unknown benchmark requested.")

    data = []
    # for case in cases:
    start_time = time.time()
    obj, count = globals()[case]
    print(count)
    data.append((obj, range(count)))

    bench_json_dumps(data)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()
