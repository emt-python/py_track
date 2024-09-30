#!/bin/bash
# python_bin=$HOME/workspace/cpython/python
# python_bin=python3
# Example: ./test_numa_traffic.sh base normal bm_sqlalchemy with_gc
env=$1
source setup_env.sh $2
workload_name=$3
gc_stat=$4
enable_pypper=$5
workload_file=$workload_name".py"
profile_name="${workload_name}"
echo running $workload_file in $env using $2

gen_fp() {
    local check_pid=$1
    MEM_FP_FILE=./fp_raw.csv
    rm -rf $MEM_FP_FILE
    while [ -d "/proc/${check_pid}" ]; do
        numactl -H | grep free >>$MEM_FP_FILE
        sleep 0.1
    done
    sleep 1

    python3 ./process_numa_fp.py $MEM_FP_FILE $profile_name $gc_stat
}

gen_bw() {
    local check_pid=$1
    BW_PCM_FILE=./bw_raw.csv
    rm -rf $BW_PCM_FILE
    sudo pcm-memory 0.1 -csv=$BW_PCM_FILE -silent &
    while [ -d "/proc/${check_pid}" ]; do
        sleep 0.1
    done
    sudo pkill -9 pcm-memory >/dev/null 2>&1
    python3 ./process_numa_mem.py $BW_PCM_FILE $profile_name $gc_stat
    gnuplot -e "output_file='./traces/${profile_name}_${gc_stat}_bw.png'; input_file='./traces/${profile_name}_${gc_stat}_bw.csv'; wl_title='Memory Bandwidth'" ./plot_bw.gnuplot

}
get_all_rss() {
    local rss_file="rss_values.txt"
    rm $rss_file
    local check_pid=$1

    while kill -0 $check_pid 2>/dev/null; do
        ps -p $check_pid -o rss= >>$rss_file
        sleep 0.5
    done

    local max_rss=$(sort -n $rss_file | tail -1)
    local rss_MB=$((max_rss / 1024))
    echo "Max RSS: $rss_MB" MB
}

get_DRAM_size() {
    local check_pid=$1

    local MIN_MEMORY=999999999
    local MAX_MEMORY=0

    while kill -0 $check_pid 2>/dev/null; do
        local CURRENT_FREE=$(numactl -H | grep "node 0 free:" | awk '{print $4}')
        # echo $CURRENT_FREE

        if [[ "$CURRENT_FREE" -lt "$MIN_MEMORY" ]]; then
            MIN_MEMORY=$CURRENT_FREE
        fi
        if [[ "$CURRENT_FREE" -gt "$MAX_MEMORY" ]]; then
            MAX_MEMORY=$CURRENT_FREE
        fi

        sleep 0.5
    done

    local DIFFERENCE=$(($MAX_MEMORY - $MIN_MEMORY))

    echo "Min memory: $MIN_MEMORY MB"
    echo "Max memory: $MAX_MEMORY MB"
    echo "Difference: $DIFFERENCE MB"
}

if [ "$env" = "cxl" ]; then
    cmd_prefix="numactl --cpunodebind 0 --membind 1 -- "
elif [ "$env" = "base" ]; then
    cmd_prefix="numactl --cpunodebind 0 --membind 0 -- "
elif [ "$env" = "org" ]; then
    if [ "$2" = "pypper" ] || [ "$2" = "normal" ]; then
        cmd_prefix="numactl --cpunodebind 0 --preferred 0 -- "
    else
        cmd_prefix=""
    fi
else
    echo "wrong env, pls try again!"
    exit 1
fi
echo "cmd_prefix: " $cmd_prefix
# elif [ "$env" = "cpu0" ]; then
#     cmd_prefix="numactl --cpunodebind 0 -- "
# elif [ "$env" = "interleave" ]; then
#     cmd_prefix="numactl --cpunodebind 0 --interleave all -- "
echo 3 | sudo tee /proc/sys/vm/drop_caches
$cmd_prefix $python_bin $HOME/workspace/py_track/workload/$workload_file $gc_stat $enable_pypper &
check_pid=$!

# gen_bw $check_pid &
# spawn_perf_stat.sh $check_pid $workload_name &
# sudo ./spawn_pcm.sh $check_pid $workload_name
# sleep 2
gen_fp $check_pid &
get_all_rss $check_pid
# get_DRAM_size $check_pid

# if [ -n "$enable_pypper" ]; then
#     echo "Stop hogger"
#     kill -9 $hogger_pid
# fi
