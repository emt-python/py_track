#!/bin/bash

total_lines=$(wc -l <obj_dump_sorted.txt)                                 # Get the total number of lines
lines_to_extract=$((total_lines / 100))                                   # Calculate 1/10th of total lines
head -n $lines_to_extract obj_dump_sorted.txt >obj_dump_sorted_little.txt # Redirect the first 1/10th to a new file
