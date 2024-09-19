#!/bin/bash
# echo 2 | sudo tee /proc/sys/vm/panic_on_oom
solution=pypper
LOG_FILE=out.txt
EMT_METADATA="no_extra"

python_bin=$HOME/workspace/cpython/python
source ./setup_env.sh pypper

workloads=("networkx_astar" "networkx_bellman" "networkx_bidirectional" "networkx_kc" "networkx_sp")
# workloads=("networkx_astar")
mem_splits=("25" "50" "75")
# mem_splits=("25")
gen_with_traces() {
    for wl in "${workloads[@]}"; do
        for split in "${mem_splits[@]}"; do
            for runs in {1..3}; do
                if [ "$split" != "100" ]; then
                    EMT_METADATA="reserve_extra"
                fi
                source bench_cmds/${wl}.sh $split
                echo "----------running $wl w/ $split-------------"
                pkill -9 memeater
                echo 3 | sudo tee /proc/sys/vm/drop_caches

                trap '$cmd_prefix $python_bin $SCRIPT with_gc 1 & check_pid=$!; wait $check_pid' SIGUSR1
                # trap './eat & check_pid=$!; wait $check_pid' SIGUSR1
                stdbuf -oL ./memeater $BENCH_DRAM $KERN_RESERVE $EMT_METADATA $$ &
                MEMAETER_PID=$!
                echo memeater_pid: $MEMAETER_PID
                wait $MEMAETER_PID
                echo "killing memeaterr"
                kill -9 $MEMAETER_PID

                sleep 10
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
