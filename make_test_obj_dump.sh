#!/bin/bash

total_lines=$(wc -l <obj_dump_sorted.txt)
lines_to_extract=$((total_lines / 1000))
head -n $lines_to_extract obj_dump_sorted.txt >obj_dump_sorted_little.txt
