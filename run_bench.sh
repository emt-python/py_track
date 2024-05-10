#!/bin/bash

echo >out.txt

workloads=("bm_sqlalchemy" "bm_xml_etree_parse" "networkx_bc" "networkx_gmc" "networkx_kc" "networkx_bfs"
    "networkx_lc" "networkx_ac" "networkx_sp", "networkx_mmm")
# workloads=("dummy" "dummy")

for wl in "${workloads[@]}"; do
    ./test_numa_traffic.sh base python ${wl} >>out.txt 2>&1
    echo -e "\n" >>out.txt
    ./test_numa_traffic.sh cxl python ${wl} >>out.txt 2>&1
    echo -e "\n" >>out.txt
    ./test_numa_traffic.sh base pypper ${wl} >>out.txt 2>&1
    echo -e "\n" >>out.txt
    ./test_numa_traffic.sh cxl pypper ${wl} >>out.txt 2>&1
    echo -e "\n" >>out.txt
    # ./do_damo.sh org ${wl} >>out.txt 2>&1
    # ~/workspace/cpython/python workload/${wl}.py > out.txt 2>&1
done
