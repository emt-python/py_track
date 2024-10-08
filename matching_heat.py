import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

df1_name = 'obj_dump_sorted.txt'
df2_name = 'matmul_new.txt'

columns_1 = ["timestamp", "addr", "diff0", "diff1",
             "diff2", "diff3", "diff4", "diff5", "diff6", "hotness"]
df1 = pd.read_csv(df1_name, sep="\t", header=None, names=columns_1)

columns_2 = ["timestamp", "addr", "temperature"]
df2 = pd.read_csv(df2_name, sep="\t", header=None, names=columns_2)


def find_closest_temperature_v2(row, df2):
    # if row_number % (len(df1) // 100) == 0:
    #     print(f"Processing row {row_number + 1} / {len(df1)}")
    closest_row = df2.iloc[(df2['addr'] - row['addr']).abs().argsort()[:1]]

    return closest_row['temperature'].mean()


def process_chunk(chunk, df2):
    chunk['real_heat'] = chunk.apply(
        lambda row: find_closest_temperature_v2(row, df2), axis=1)
    return chunk


def parallel_process(df1, df2, num_chunks=20):
    chunks = np.array_split(df1, num_chunks)
    with Pool(processes=num_chunks) as pool:
        result_chunks = pool.starmap(
            process_chunk, [(chunk, df2) for chunk in chunks])

    result_df = pd.concat(result_chunks)
    return result_df


df1_result = parallel_process(df1, df2, num_chunks=24)

sorted_file = "obj_dump_real_heat_all.txt"
df1_result.to_csv(sorted_file, sep='\t', index=False, header=False)
