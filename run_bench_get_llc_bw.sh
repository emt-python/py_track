#!/bin/bash
workloads=("networkx_astar" "networkx_bc" "networkx_bellman" "networkx_bfs_rand" "networkx_bfs"
    "networkx_bidirectional" "networkx_kc" "networkx_lc" "networkx_sp" "networkx_tc" "bm_sqlalchemy" "bm_sqlalchemy_new")
# workloads=("matmul")
for wl in "${workloads[@]}"; do
    ./test_numa_traffic.sh base normal $wl with_gc >out.txt 2>&1
    # plot charts
    python3 dump_LLC_load_miss.py $wl
    python3 ./plot_bw_new.py $wl
done
