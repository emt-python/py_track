# coding: UTF-8
""" Telco Benchmark for measuring the performance of decimal calculations

- http://speleotrove.com/decimal/telco.html
- http://speleotrove.com/decimal/telcoSpec.html

A call type indicator, c, is set from the bottom (least significant) bit of the duration (hence c is 0 or 1).
A rate, r, is determined from the call type. Those calls with c=0 have a low r: 0.0013; the remainder (‘distance calls’) have a ‘premium’ r: 0.00894. (The rates are, very roughly, in Euros or dollarates per second.)
A price, p, for the call is then calculated (p=r*n). This is rounded to exactly 2 fractional digits using round-half-even (Banker’s round to nearest).
A basic tax, b, is calculated: b=p*0.0675 (6.75%). This is truncated to exactly 2 fractional digits (round-down), and the total basic tax variable is then incremented (sumB=sumB+b).
For distance calls: a distance tax, d, is calculated: d=p*0.0341 (3.41%). This is truncated to exactly 2 fractional digits (round-down), and then the total distance tax variable is incremented (sumD=sumD+d).
The total price, t, is calculated (t=p+b, and, if a distance call, t=t+d).
The total prices variable is incremented (sumT=sumT+t).
The total price, t, is converted to a string, s.

"""

# import gc_count_module
import time
from decimal import ROUND_HALF_EVEN, ROUND_DOWN, Decimal, getcontext, Context
import io
import os
from struct import unpack


def rel_path(*path):
    return os.path.join(os.path.dirname(__file__), *path)


cur_dir = os.path.dirname(os.path.realpath(__file__))


def bench_telco(loops, filename):
    getcontext().rounding = ROUND_DOWN
    rates = list(map(Decimal, ('0.0013', '0.00894')))
    twodig = Decimal('0.01')
    Banker = Context(rounding=ROUND_HALF_EVEN)
    basictax = Decimal("0.0675")
    disttax = Decimal("0.0341")

    with open(filename, "rb") as infil:
        data = infil.read()

    infil = io.BytesIO(data)
    outfil = io.StringIO()
    for _ in range(loops):
        infil.seek(0)

        sumT = Decimal("0")   # sum of total prices
        sumB = Decimal("0")   # sum of basic tax
        sumD = Decimal("0")   # sum of 'distance' tax

        for i in range(50000):
            datum = infil.read(8)
            if datum == '':
                break
            n, =  unpack('>Q', datum)

            calltype = n & 1
            r = rates[calltype]

            p = Banker.quantize(r * n, twodig)

            b = p * basictax
            b = b.quantize(twodig)
            sumB += b

            t = p + b

            if calltype:
                d = p * disttax
                d = d.quantize(twodig)
                sumD += d
                t += d

            sumT += t
            print(t, file=outfil)

        outfil.seek(0)
        outfil.truncate()


def bench_telco_v2(loops, filename):
    getcontext().rounding = ROUND_DOWN
    rates = list(map(Decimal, ('0.0013', '0.00894'))) * \
        100  # Increase rates list size
    twodig = Decimal('0.01')
    Banker = Context(rounding=ROUND_HALF_EVEN)
    basictax = Decimal("0.0675")
    disttax = Decimal("0.0341")

    with open(filename, "rb") as infil:
        data = infil.read()

    # Duplicate the input data to increase memory usage
    data = data * 100  # Increase the size of data read from the file

    infil = io.BytesIO(data)
    outfil = io.StringIO()
    intermediate_results = []  # Store intermediate results to increase memory usage

    for _ in range(loops):  # Increase the number of loops
        infil.seek(0)

        sumT = Decimal("0")  # sum of total prices
        sumB = Decimal("0")  # sum of basic tax
        sumD = Decimal("0")  # sum of 'distance' tax

        # Increase the range to process more data
        for i in range(50000):  # Process more data points
            datum = infil.read(8)
            if datum == b'':  # Correctly handle the binary read
                break
            n, = unpack('>Q', datum)

            calltype = n & 1
            # Adjust for increased rates list size
            r = rates[calltype % len(rates)]

            p = Banker.quantize(r * n, twodig)

            b = p * basictax
            b = b.quantize(twodig)
            sumB += b

            t = p + b

            if calltype:
                d = p * disttax
                d = d.quantize(twodig)
                sumD += d
                t += d

            sumT += t
            intermediate_results.append(t)  # Store each total in memory

        # Use more memory by keeping intermediate results instead of truncating
        # Reset outfil for the next loop iteration to simulate processing without losing data
        # outfil = io.StringIO()


if __name__ == "__main__":

    filename = rel_path(cur_dir, "telco-bench-dupped-large.bin")
    loops = 20
    start = time.time()
    # gc_count_module.start_count_gc_list(
    #     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 10, 1_000_000)
    bench_telco_v2(loops, filename)
    # gc_count_module.close_count_gc_list()
    elapsed_time = time.time() - start
    print(f"Compute time: {elapsed_time:.2f} seconds")
