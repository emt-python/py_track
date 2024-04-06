#!/bin/bash
g++ -c -o sparse_wrapper.o sparse_wrapper.cpp
gcc -c -o test_sparse_set.o test_sparse_set.c
g++ -o myprogram test_sparse_set.o sparse_wrapper.o
