#!/bin/bash

# Usage: ./perf_stat_periodic.sh <pid> <output_file>

pid=$1 # The PID of the target process
workload_name=$2
# output_file=traces/"$workload_name"_perf_stat.log
output_file=perf_stat.log
echo >$output_file
# Check if PID and output file are provided
# if [[ -z "$pid" || -z "$output_file" ]]; then
#     echo "Usage: $0 <pid> <output_file>"
#     exit 1
# fi

# # Check if the process with the given PID exists
# if ! ps -p "$pid" >/dev/null 2>&1; then
#     echo "Process with PID $pid does not exist."
#     exit 1
# fi
# echo "profiling $workload_name" >>"$output_file"
# Infinite loop to collect perf stat data every second
while kill -0 $pid 2>/dev/null; do
    # echo "Collecting perf stat at $(date)" >>"$output_file"

    # perf stat -p $pid -e dTLB-loads,dTLB-load-misses,LLC-loads,LLC-load-misses,LLC-stores -- sleep 1 2>>"$output_file"
    temp_file=$(mktemp)
    perf stat -p $pid -e cycles,instructions,LLC-loads,LLC-load-misses,LLC-stores -- sleep 1 2>"$temp_file" && mv "$temp_file" "$output_file"
    # perf stat -p $pid -e cycles,instructions,LLC-loads,LLC-load-misses,LLC-stores -- sleep 1 2>>"$output_file"
    # sudo perf stat -e cycles,instructions,LLC-loads,LLC-load-misses,LLC-stores -a sleep 1 2>>"$output_file"

    # sleep 0.5
done

echo "Process $pid has exited."
