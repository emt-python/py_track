#!/bin/bash

pcm_mem_bin=pcm-memory
# pcm_mem_bin=/home/lyuze/workspace/pcm/build/bin/pcm-memory
pid=$1 # The PID of the target process
workload_name=$2
user=$(whoami)
raw_output_file=bw_raw_.csv
# parsed_file=traces/"$workload_name"_parsed_bw.txt
parsed_file=parsed_bw.txt

echo >$raw_output_file
echo >$parsed_file
sudo chown -R $user $raw_output_file
sudo chown -R $user $parsed_file
sed -i '1d' $parsed_file

source setup_pcm_col.sh

sudo $pcm_mem_bin -silent -nc -csv="$raw_output_file" &
sleep 3
while [ -d "/proc/${pid}" ]; do
    last_line=$(tail -n 1 "$raw_output_file")
    # echo "$last_line" | awk -F ',' '{print $7, $12}' >>"$output_file"
    # echo "$last_line" | awk -F ',' '{gsub(/^[ \t]+|[ \t]+$/, "", $7); gsub(/^[ \t]+|[ \t]+$/, "", $12); print $7, $12}' >"$parsed_file"
    echo "$last_line" | awk -v col1=$skt0_mem_col -v col2=$skt1_mem_col -F ',' '{
        gsub(/^[ \t]+|[ \t]+$/, "", $col1);
        gsub(/^[ \t]+|[ \t]+$/, "", $col2);
        print $col1, $col2
    }' >"$parsed_file"
    sleep 1.2
done
sudo pkill -9 pcm-memory >/dev/null 2>&1
echo "Process $pid has exited."

# reset
