#!/bin/bash
# cxl, base
DAMON=$HOME/damo/damo
# DAMON=damo
env=$1
workload_name=$2
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

if [ "$env" = "cxl" ]; then
    cmd_prefix="numactl --cpunodebind 0 --membind 1 -- "
elif [ "$env" = "base" ]; then
    cmd_prefix="numactl  --cpunodebind 0 --membind 0 -- "
elif [ "$env" = "org" ]; then
    cmd_prefix="numactl --cpunodebind 0 -- "
elif [ "$env" = "interleave" ]; then
    cmd_prefix="numactl --cpunodebind 0 --interleave all -- "
else
    echo "wrong env, pls try again!"
    exit 1
fi
echo "running in $env"
# if [ "$do_bk" = "" ]; then
#     exit 1
# fio
echo 1 | sudo tee /proc/sys/vm/drop_caches

cd $HOME/workspace/py_track
$cmd_prefix $HOME/workspace/cpython/python ./workload/$workload_name.py >out.txt 2>&1 &

check_pid=$!
echo "workload pid is" $check_pid
# gen_rss $check_pid "$func"
sudo $DAMON record \
    -o $HOME/workspace/py_track/$workload_name.data $check_pid
#  -o $HOME/workspace/py_track/eos_python_traced.data $check_pid
# -s 1000 -a 100000 -u 1000000 -n 5000 -m 6000
sleep 10
echo "post processing..."
sudo ~/damo/damo report heats -i ./$workload_name.data --abs_addr --heatmap $workload_name.png

# sudo $DAMON report heats -i $HOME/workspace/obj_heats/"$func".data --resol 1000 2000 \
#     --abs_addr --heatmap $HOME/workspace/obj_heats/"$func".png &

# sudo damo report heats -i $HOME/workspace/obj_heats/matmul_list.data --resol 1000 5000 \
#     --abs_addr --address_range 140737326235824  140737352876912 \
#     --heatmap $HOME/workspace/obj_heats/test.png

# sudo $DAMON report heats -i $HOME/workspace/obj_heats/"$func".data --resol 1000 2000 \
#     --abs_addr > $HOME/workspace/obj_heats/"$func"_abs_addr.txt

# sudo $DAMON report heats -i $HOME/workspace/obj_heats/matmul_list.data --resol 1000 2000 > $HOME/workspace/obj_heats/test.txt
# sudo $DAMON report heats -i ./matmul_400.data --abs_addr > ./matmul_400_damo.txt
