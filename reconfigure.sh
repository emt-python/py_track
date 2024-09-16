#!/bin/bash

BUILD=cpython

echo "Please hit enter to continue..."
read
echo "reconfiguring..."

# if changed the Pyobject header, remember to rebuild cython
$HOME/workspace/$BUILD/python -m pip uninstall -y setuptools Cython cython
$HOME/workspace/$BUILD/python -m pip install setuptools

cd ~/workspace/cython
rm -rf build
$HOME/workspace/$BUILD/python -m pip install .
# if it's no gil version, you have to use make instead of pip
# make

cd ~/workspace/py_track
rm -rf build
$HOME/workspace/cpython/python ./setup_gc_count_list.py build_ext --inplace
$HOME/workspace/cpython/python ./setup_gc_count_list.py install --install-lib ~/.local/lib/python3.12/site-packages

# build memeater and eats
gcc -o memeater memeater.c -lnuma -O3
gcc -o eat eat.c -lnuma -O3