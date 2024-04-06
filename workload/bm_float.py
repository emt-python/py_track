"""
Artificial, floating point-heavy benchmark originally used by Factor.
"""

import math
import time

POINTS = 50000


class Point(object):
    def __init__(self, i):
        self.x = x = math.sin(i)
        self.y = math.cos(i) * 3
        self.z = (x * x) / 2
        # Significantly increase the size of the data structures
        self.w = [math.sin(j / 100.0) for j in range(10000)]  # Larger list
        self.info = {
            'index': i,
            'data': [math.cos(j) for j in range(10000)],
            'additional': [x * y for x, y in zip(range(10000), range(10000, 20000))]
        }

    def __repr__(self):
        return f"<Point: x={self.x}, y={self.y}, z={self.z}, info_index={self.info['index']}>"

    def normalize(self):
        norm = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= norm
        self.y /= norm
        self.z /= norm
        # Process large lists to increase memory traffic
        self.w = [val / norm for val in self.w]
        self.info['data'] = [val / norm for val in self.info['data']]
        self.info['additional'] = [
            val / norm for val in self.info['additional']]

    def maximize(self, other):
        super().maximize(other)
        # Additional large list comparison and merging
        self.info['additional'] = [max(val, other_val) for val, other_val in zip(
            self.info['additional'], other.info['additional'])]
        return self


def maximize(points):
    next_point = points[0]
    for p in points[1:]:
        next_point = next_point.maximize(p)
    return next_point


def benchmark(n):
    points = [Point(i) for i in range(n)]
    for p in points:
        p.normalize()
    # return maximize(points)


if __name__ == "__main__":
    start = time.time()
    benchmark(POINTS)
    print("compute time: {:.2f}".format(time.time() - start))
