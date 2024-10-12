#!/bin/bash
# echo 2 | sudo tee /proc/sys/vm/panic_on_oom
solution=$1
LOG_FILE=out.txt
EMT_METADATA="no_extra"
cmd_prefix="numactl --cpunodebind 0 --preferred 0 -- "

source setup_env.sh $solution $$

workloads=("networkx_astar")
# workloads=("networkx_astar" "networkx_bellman" "networkx_bfs_rand"
#     "networkx_bidirectional" "networkx_kc" "networkx_sp" "bm_sqlalchemy_user_insert")
# workloads=("bm_sqlalchemy" "bm_sqlalchemy_new" "bm_sqlalchemy_user_insert" "networkx_astar" "networkx_bellman" "networkx_bfs_rand" "networkx_bfs"
#     "networkx_bidirectional" "networkx_kc" "networkx_lc" "networkx_sp" "networkx_tc")
# "bm_sqlalchemy_user_update" "bm_sqlalchemy_user_update_v2" "bm_sqlalchemy_user_delete"
# mem_splits=("25" "50" "75" "100")
mem_splits=("25")
gen_with_traces() {
    for wl in "${workloads[@]}"; do
        for split in "${mem_splits[@]}"; do
            for runs in {1..1}; do
                if [ "$solution" = "pypper" ] && [ "$split" != "100" ]; then
                    EMT_METADATA="reserve_extra"
                fi
                source bench_cmds/${wl}.sh $split
                echo "----------running $wl w/ $split-------------"
                pkill -9 memeater
                echo 3 | sudo tee /proc/sys/vm/drop_caches

                if [ "$solution" = "memtis" ]; then
                    BENCH_DRAM=$((BENCH_DRAM + 4096))
                    sudo memtis_scripts/set_mem_size.sh htmm 0 ${BENCH_DRAM}
                    # trap '$cmd_prefix $launch_memtis_bin $python_bin $SCRIPT with_gc & check_pid=$!; wait $check_pid' SIGUSR1
                    trap "$cmd_prefix $CUR_DIR/memtis_scripts/launch_bench $python_bin $SCRIPT with_gc & check_pid=\$!; wait \$check_pid" SIGUSR1
                    stdbuf -oL $cmd_prefix $CUR_DIR/eat $$ &
                    EAT_PID=$!
                    wait $EAT_PID
                    echo "killing eats"
                    kill -9 $EAT_PID
                else
                    trap '$cmd_prefix $python_bin $SCRIPT with_gc 1 & check_pid=$!; ./spawn_perf_stat.sh $check_pid $wl & sudo ./spawn_pcm.sh $check_pid $wl & wait $check_pid' SIGUSR1
                    stdbuf -oL $cmd_prefix ./memeater $BENCH_DRAM $KERN_RESERVE $EMT_METADATA $$ &
                    MEMAETER_PID=$!
                    wait $MEMAETER_PID
                    echo "killing memeaterr"
                    kill -9 $MEMAETER_PID
                fi
                # ./test_numa_traffic.sh base pypper ${wl} with_gc 1

                if [ "$solution" = "memtis" ]; then
                    sudo memtis_scripts/set_htmm_memcg.sh htmm $$ disable
                fi
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
    done
}

dry_run() {
    for wl in "${workloads[@]}"; do
        echo "----------running $wl w/ gc-------------"
        ~/workspace/cpython/python ./workload/${wl}.py with_gc 1
    done
}

echo "Start running $solution ***************" >>$LOG_FILE 2>&1
gen_with_traces >>$LOG_FILE 2>&1

# dry_run >>out.txt 2>&1
