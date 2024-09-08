#!/bin/bash
DRAM_RATIO=$1
BIN=/home/lyuze/workspace/py_track/workload
# if [[ -z "$1" ]]; then
SCRIPT="${BIN}/networkx_bfs_rand.py"
# else
#     BENCH_RUN="${BIN}/XSBench_instru -t 24 -g 130000 -p 10000000"
# fi

# 5319 MB
BENCH_DRAM=""

if [[ "x${DRAM_RATIO}" == "x25" ]]; then
    BENCH_DRAM="1330"
elif [[ "x${DRAM_RATIO}" == "x50" ]]; then
    BENCH_DRAM="2660"
elif [[ "x${DRAM_RATIO}" == "x75" ]]; then
    BENCH_DRAM="3990"
elif [[ "x${DRAM_RATIO}" == "x100" ]]; then
    BENCH_DRAM="80000"
fi

export SCRIPT
export BENCH_DRAM
