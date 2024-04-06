import time
from sympy import expand, symbols, integrate, tan, summation
from sympy.core.cache import clear_cache


def bench_expand():
    for _ in range(10):
        x, y, z = symbols('x y z')
        # Increase the power to make the expression more complex.
        expand((1 + x + y + z) ** 50)


def bench_integrate():
    for _ in range(10):
        x, y = symbols('x y')
        # Increase the complexity of the function to be integrated.
        f = (1 / tan(x)) ** 20
    return integrate(f, x)


def bench_sum():
    for _ in range(10):
        x, i = symbols('x i')
        # Increase the bounds of summation to make the operation more intensive.
        summation(x ** i / i, (i, 1, 1000))


def bench_str():
    for _ in range(10):
        x, y, z = symbols('x y z')
        # Increase the power to make the string representation longer.
        str(expand((x + 2 * y + 3 * z) ** 60))


def bench_sympy(loops, func):
    for _ in range(loops):
        # Don't benchmark clear_cache(), exclude it of the benchmark.
        clear_cache()
        func()


BENCHMARKS = ("expand", "integrate", "sum", "str")


def add_cmdline_args(cmd, args):
    if args.benchmark:
        cmd.append(args.benchmark)


if __name__ == "__main__":

    import gc
    gc.disable()

    benchmarks = BENCHMARKS

    start_time = time.time()
    loops = 1
    for bench in benchmarks:
        name = 'sympy_%s' % bench
        func = globals()['bench_' + bench]
        bench_sympy(loops, func)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
