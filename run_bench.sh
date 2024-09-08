#!/bin/bash
# echo 2 | sudo tee /proc/sys/vm/panic_on_oom
cmd_prefix="numactl --cpunodebind 0 --preferred 0 -- "
python_bin=/home/lyuze/workspace/cpython/python
workloads=("networkx_ac" "networkx_astar" "networkx_bc" "networkx_bellman" "networkx_bfs_rand" "networkx_bfs" "networkx_bidirectional"
    "networkx_gmc" "networkx_kc" "networkx_lc" "networkx_mmm" "networkx_sp" "networkx_tc")
mem_splits=("25" "50" "75" "100")
gen_with_traces() {
    for wl in "${workloads[@]}"; do
        for split in "${mem_splits[@]}"; do
            source bench_cmds/${wl}.sh $split
            echo "----------running $wl w/ $split-------------"
            pkill -9 memeater
            echo 3 | sudo tee /proc/sys/vm/drop_caches

            trap '$cmd_prefix $python_bin $SCRIPT with_gc 1 & check_pid=$!; wait $check_pid' SIGUSR1
            stdbuf -oL ./memeater $BENCH_DRAM $$ &
            MEMAETER_PID=$!
            wait $MEMAETER_PID
            echo "killing memeaterr"
            kill -9 $MEMAETER_PID
            # ./test_numa_traffic.sh base pypper ${wl} with_gc 1
            sleep 10

            # echo 3 | sudo tee /proc/sys/vm/drop_caches
            # echo "----------running $wl w/ gc cxl -------------"
            # ./test_numa_traffic.sh cxl normal ${wl} with_gc
            # sleep 3

            # echo "----------running damo $wl w/o gc -------------"
            # ./do_damo.sh base ${wl} no_gc
            # echo "----------running damo $wl w/ gc -------------"
            # ./do_damo.sh base ${wl} with_gc
        done
    done
}

dry_run() {
    for wl in "${workloads[@]}"; do
        echo "----------running $wl w/ gc-------------"
        ~/workspace/cpython/python ./workload/${wl}.py with_gc 1
    done
}
echo >out.txt
gen_with_traces >>out.txt 2>&1

# dry_run >>out.txt 2>&1
