#!/bin/bash
python_bin=/home/lyuze/workspace/cpython/python
# python_bin=python3
env=$1
workload_name=$2
workload_arg=$3
workload_file=$workload_name".py"
profile_name="${workload_name}_${workload_arg}"
echo "running test: "$workload_file

gen_bw() {
    local check_pid=$1
    BW_PCM_FILE=./bw_raw.csv
    MEM_FP_FILE=./fp_raw.csv
    rm -rf $MEM_FP_FILE
    sudo pcm-memory 0.1 -csv=$BW_PCM_FILE -silent &
    while [ -d "/proc/${check_pid}" ]; do
        numactl -H | grep free >>$MEM_FP_FILE
        sleep 0.1
    done
    sudo pkill -9 pcm-memory >/dev/null 2>&1
    sleep 1

    python3 ./process_numa_fp.py $MEM_FP_FILE $profile_name
    python3 ./process_numa_mem.py $BW_PCM_FILE $profile_name bw
    echo "gen bw,fp done"
    gnuplot -e "output_file='./traces/${profile_name}_bw.png'; input_file='./traces/${profile_name}_bw.csv'; wl_title='Memory Bandwidth'" ./plot_bw.gnuplot
    echo "plot bw done"
}

if [ "$env" = "cxl" ]; then
    cmd_prefix="numactl --cpunodebind 0 --membind 1 -- "
elif [ "$env" = "base" ]; then
    cmd_prefix="numactl  --cpunodebind 0 --membind 0 -- "
elif [ "$env" = "org" ]; then
    cmd_prefix=""
else
    echo "wrong env, pls try again!"
    exit 1
fi
# elif [ "$env" = "cpu0" ]; then
#     cmd_prefix="numactl --cpunodebind 0 -- "
# elif [ "$env" = "interleave" ]; then
#     cmd_prefix="numactl --cpunodebind 0 --interleave all -- "
echo "running in $env"
echo 1 | sudo tee /proc/sys/vm/drop_caches
sleep 10 &
# $cmd_prefix $python_bin /home/lyuze/workspace/py_track/workload/$workload_file $workload_arg &

check_pid=$!
gen_bw $check_pid
