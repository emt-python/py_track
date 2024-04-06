#!/bin/bash

# gcc -O3 -c main.c -o main.o
# g++ -O3 -c sort.cpp -o sort.o
# g++ -O3 main.o sort.o -o myprogram
rm -rf *.o main
OPT="-O3"
g++ $OPT -std=c++17 -c sort.cpp -o sort.o -ltbb 
gcc $OPT -c test_align_page.c -o test_align_page.o
gcc $OPT -c main.c -o main.o
g++ $OPT -std=c++17 test_align_page.o sort.o -o test_align_page -ltbb
# g++ $OPT -std=c++17 main.o sort.o -o main -ltbb
