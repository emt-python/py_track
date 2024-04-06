# import sys
# sys.path.append('/home/lyuze/workspace/cython')


from Cython.Build import cythonize
from setuptools import setup

setup(
    # ext_modules = cythonize("fibonacci.pyx")
    ext_modules=cythonize("matmul.pyx")
)
