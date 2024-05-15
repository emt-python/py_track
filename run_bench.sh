#!/bin/bash

# echo >out.txt

workloads=("bm_xml_etree_parse")
# workloads=("bm_sqlalchemy_new" "nested_sets" "large_results" "bulk_insert" "seperate_db")
# workloads=("bm_sqlalchemy" "bm_xml_etree_parse" "networkx_bc" "networkx_gmc" "networkx_kc" "networkx_bfs"
#     "networkx_sp", "networkx_mmm")
# workloads=("dummy" "dummy")

for wl in "${workloads[@]}"; do
    # ./setup_sqlalchemy.sh python
    ./test_numa_traffic.sh org tpp ${wl} > tpp.txt 2>&1
    sleep 5
    ./test_numa_traffic.sh org pypper ${wl} 1 > pypper.txt 2>&1
    sleep 5
    ./test_numa_traffic.sh org normal ${wl} > normal.txt 2>&1
    sleep 5
    ./test_numa_traffic.sh org autonuma ${wl} > autonuma.txt 2>&1
    # ./do_damo.sh org ${wl} >>out.txt 2>&1
    # ~/workspace/cpython/python workload/${wl}.py > out.txt 2>&1
done
