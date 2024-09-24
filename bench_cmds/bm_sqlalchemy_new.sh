#!/bin/bash
DRAM_RATIO=$1
BIN=$HOME/workspace/py_track/workload
# if [[ -z "$1" ]]; then
SCRIPT="${BIN}/bm_sqlalchemy_new.py"
# else
#     BENCH_RUN="${BIN}/XSBench_instru -t 24 -g 130000 -p 10000000"
# fi

# 4725 MB
# 1182
# 2363
# 3545

# or 8993 MB
# 2248
# 4496
# 6744
# 80000
BENCH_DRAM=""

if [[ "x${DRAM_RATIO}" == "x25" ]]; then
    BENCH_DRAM="2248"
elif [[ "x${DRAM_RATIO}" == "x50" ]]; then
    BENCH_DRAM="4496"
elif [[ "x${DRAM_RATIO}" == "x75" ]]; then
    BENCH_DRAM="6744"
elif [[ "x${DRAM_RATIO}" == "x100" ]]; then
    BENCH_DRAM="80000"
fi

export SCRIPT
export BENCH_DRAM
