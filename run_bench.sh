#!/bin/bash

echo >out.txt

workloads=("networkx_bc" "networkx_tc" "networkx_bfs" "networkx_gmc" "networkx_ac" "networkx_lc")

for wl in "${workloads[@]}"; do
    echo "running ${wl}" >>out.txt

    ./do_damo.sh org ${wl} >>out.txt 2>&1
    # ~/workspace/cpython/python workload/${wl}.py > out.txt 2>&1
done
