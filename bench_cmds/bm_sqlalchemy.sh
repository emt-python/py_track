#!/bin/bash
DRAM_RATIO=$1
BIN=$HOME/workspace/py_track/workload
# if [[ -z "$1" ]]; then
SCRIPT="${BIN}/bm_sqlalchemy.py"
# else
#     BENCH_RUN="${BIN}/XSBench_instru -t 24 -g 130000 -p 10000000"
# fi

# 3626 MB
BENCH_DRAM=""

if [[ "x${DRAM_RATIO}" == "x25" ]]; then
    BENCH_DRAM="907"
elif [[ "x${DRAM_RATIO}" == "x50" ]]; then
    BENCH_DRAM="1814"
elif [[ "x${DRAM_RATIO}" == "x75" ]]; then
    BENCH_DRAM="2721"
elif [[ "x${DRAM_RATIO}" == "x100" ]]; then
    BENCH_DRAM="8000"
fi

export SCRIPT
export BENCH_DRAM
