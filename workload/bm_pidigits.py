# coding: utf-8
"""
Calculating some of the digits of π.

This benchmark stresses big integer arithmetic.

Adapted from code on:
http://benchmarksgame.alioth.debian.org/
"""

import time
import itertools


DEFAULT_DIGITS = 20000
icount = itertools.count
islice = itertools.islice


def gen_x():
    return map(lambda k: (k, 4 * k + 2, 0, 2 * k + 1), icount(1))


def compose(a, b):
    aq, ar, as_, at = a
    bq, br, bs, bt = b
    return (aq * bq,
            aq * br + ar * bt,
            as_ * bq + at * bs,
            as_ * br + at * bt)


def extract(z, j):
    q, r, s, t = z
    return (q * j + r) // (s * j + t)


def gen_pi_digits():
    z = (1, 0, 0, 1)
    x = gen_x()
    while 1:
        y = extract(z, 3)
        while y != extract(z, 4):
            z = compose(z, next(x))
            y = extract(z, 3)
        z = compose((10, -10 * y, 0, 1), z)
        yield y


def calc_ndigits(n):
    return list(islice(gen_pi_digits(), n))


def add_cmdline_args(cmd, args):
    cmd.extend(("--digits", str(args.digits)))


if __name__ == "__main__":

    start_time = time.time()
    calc_ndigits(DEFAULT_DIGITS)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
