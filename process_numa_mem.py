import pandas as pd
import os
import csv
import glob
import sys


def main():
    file_to_process = sys.argv[1]  # xx_bw_raw.csv
    workload_name = sys.argv[2]
    gc_stat = sys.argv[3]
    output_dir = os.path.dirname(file_to_process)

    print(file_to_process)
    cur_df = pd.read_csv(file_to_process)
    cur_df = cur_df.drop(cur_df.index[0])
    # column for Memory (MB/s) for sock0
    cur_skt_0_mem = cur_df.iloc[:, -1]
    cur_skt_0_rd = cur_df.iloc[:, 26]
    cur_skt_0_wt = cur_df.iloc[:, 27]
    # column for Memory (MB/s) for sock1
    # cur_skt_1_mem = cur_df.iloc[:, 59]
    cur_skt_0_mem = cur_skt_0_mem.tolist()
    # cur_skt_1_mem = cur_skt_1_mem.tolist()

    cur_skt_0_rd = cur_skt_0_rd.tolist()
    cur_skt_0_wt = cur_skt_0_wt.tolist()
    timestamp = []
    for i in range(len(cur_skt_0_mem)):
        timestamp.append(i / 10)
    # del timestamp[0]
    # del cur_skt_0_mem[0]
    # del cur_skt_1_mem[0]
    cur_mem = {"Time": timestamp,
               "Bandwidth": cur_skt_0_mem}
    # print(timestamp)
    # print(len(timestamp))
    processed_df = pd.DataFrame(cur_mem)

    processed_df.to_csv(output_dir + "/traces/" +
                        workload_name + "_" + gc_stat + "_bw.csv", index=False)


main()
