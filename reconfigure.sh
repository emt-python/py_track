#!/bin/bash

BUILD=cpython_org

echo "Please hit enter to continue..."
read
echo "reconfiguring..."

# sudo apt-get install libffi-dev

/home/lyuze/workspace/$BUILD/python -m pip uninstall -y setuptools Cython cython
/home/lyuze/workspace/$BUILD/python -m pip install setuptools

cd ~/workspace/cython
rm -rf build
/home/lyuze/workspace/$BUILD/python -m pip install .
# if it's no gil version, you have to use make instead of pip
# make

cd ~/workspace/py_track
rm -rf build
/home/lyuze/workspace/cpython/python ./setup_gc_count_list.py build_ext --inplace
