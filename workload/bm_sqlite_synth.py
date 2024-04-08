"""
SQLite benchmark.

The goal of the benchmark is to test CFFI performance and going back and forth
between SQLite and Python a lot. Therefore the queries themselves are really
simple.
"""

import sqlite3
import math
import time
import random
import string


# class AvgLength(object):

#     def __init__(self):
#         self.sum = 0
#         self.count = 0

#     def step(self, x):
#         if x is not None:
#             self.count += 1
#             self.sum += len(x)

#     def finalize(self):
#         return self.sum / float(self.count)


# def bench_sqlite(loops):

#     conn = sqlite3.connect(":memory:")
#     conn.execute('create table cos (x, y, z);')
#     for i in range(loops):
#         cos_i = math.cos(i)
#         conn.execute('insert into cos values (?, ?, ?)',
#                      [i, cos_i, str(i)])

#     conn.create_function("cos", 1, math.cos)
#     for x, cosx1, cosx2 in conn.execute("select x, cos(x), y from cos"):
#         assert math.cos(x) == cosx1 == cosx2

#     conn.create_aggregate("avglength", 1, AvgLength)
#     cursor = conn.execute("select avglength(z) from cos;")
#     cursor.fetchone()[0]

#     conn.execute("delete from cos;")
#     conn.close()

def generate_large_string(size=1024):
    """Generate a random string of specified size."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


class AvgLength(object):
    def __init__(self):
        self.sum = 0
        self.count = 0
        self.data = []  # Store data to make memory usage higher

    def step(self, x):
        if x is not None:
            self.count += 1
            self.sum += len(x)
            self.data.append(x)  # Add the string to the list

    def finalize(self):
        # Concatenate all strings and find unique characters for more complexity
        long_str = ''.join(self.data)
        unique_chars = set(long_str)
        return self.sum / float(self.count) + len(unique_chars)


def bench_sqlite(loops):
    conn = sqlite3.connect(":memory:")
    conn.execute(
        'CREATE TABLE cos (id INTEGER PRIMARY KEY, x REAL, y REAL, z TEXT);')
    conn.execute(
        'CREATE TABLE sin (id INTEGER PRIMARY KEY, x REAL, y REAL, z TEXT);')

    for i in range(loops):
        cos_i, sin_i = math.cos(i), math.sin(i)
        large_str_cos = generate_large_string(10240)
        large_str_sin = generate_large_string(10240)
        conn.execute('INSERT INTO cos (x, y, z) VALUES (?, ?, ?);',
                     (i, cos_i, large_str_cos))
        conn.execute('INSERT INTO sin (x, y, z) VALUES (?, ?, ?);',
                     (i, sin_i, large_str_sin))
        conn.execute('INSERT INTO sin (x, y, z) VALUES (?, ?, ?);',
                     (i, sin_i, large_str_sin))

    # Perform a JOIN operation between 'cos' and 'sin' tables on 'id'
    join_query = '''
    SELECT cos.id, cos.x, sin.y, cos.z 
    FROM cos 
    JOIN sin ON cos.id = sin.id 
    WHERE cos.x > ? AND sin.y < ? 
    ORDER BY cos.id DESC 
    LIMIT 10;
    '''
    # for row in conn.execute(join_query, (0.5, -0.5)):
    #     print(row)

    # Use the aggregate function to calculate the average length of 'z' in both tables
    conn.create_aggregate("avglength", 1, AvgLength)
    avg_length_cos = conn.execute(
        "SELECT avglength(z) FROM cos;").fetchone()[0]
    avg_length_sin = conn.execute(
        "SELECT avglength(z) FROM sin;").fetchone()[0]
    # print(
    #     f"Average length in 'cos': {avg_length_cos}, 'sin': {avg_length_sin}")

    # Cleanup
    conn.execute("DELETE FROM cos;")
    conn.execute("DELETE FROM sin;")
    conn.close()


if __name__ == "__main__":
    # runner = pyperf.Runner()
    # runner.metadata['description'] = "Benchmark Python aggregate for SQLite"
    # runner.bench_time_func('sqlite_synth', bench_sqlite)
    loops = 10000
    start_time = time.time()
    bench_sqlite(loops)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
