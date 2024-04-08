import subprocess
import pandas as pd
import os
import matplotlib.pyplot as plt

org_heats_dir = "/home/lyuze/workspace/py_track"
interested_file = "obj_dump.txt"
org_heats_file = os.path.join(org_heats_dir, interested_file)

# columns = ["timestamp", "addr"]
# adjst header as needed
columns = ["timestamp", "addr", "his0", "his1", "his2", "his3", "his4",
           "his5", "his6", "his7", "his8", "his9"]
org_df = pd.read_csv(org_heats_file, sep="\t", header=None, names=columns)
print(org_df.dtypes)

condition_no93 = org_df['addr'].astype(str).str.startswith('9')
with_93 = org_df[condition_no93]
org_df = org_df[~condition_no93]
# org_df = with_93

# sort by time and addr and dump to file, probably no need at this time
org_df_sorted = org_df.sort_values(by=['timestamp', 'addr'])
sorted_file = "obj_dump_sorted.txt"
sorted_file_path = os.path.join(org_heats_dir, sorted_file)
org_df_sorted.to_csv(sorted_file_path, sep='\t', index=False, header=False)

org_df = org_df_sorted


def plot_scatter_map(output_file, data_file, x_relative, y_relative, x_min, y_min):
    x_range = [0, x_relative]
    y_range = [0, y_relative]
    gnuplot_cmd = """
        set terminal pngcairo;
        set output '%s';
        set key off;
        set xlabel 'Time (s)';
        set ylabel 'Address (mb)';
        plot '%s' using ($1 - %f):(($2 - %d)/ (1024 * 1024)) with points pointtype 1 pointsize 0.8""" % (output_file,
                                                                                                         data_file, x_min, y_min)
    subprocess.call(['gnuplot', '-e', gnuplot_cmd])


# plot all
x_rela_all = org_df_sorted['timestamp'].max(
) - org_df_sorted['timestamp'].min()
y_rela_all = (org_df_sorted['addr'].max() -
              org_df_sorted['addr'].min()) / (1024 * 1024)
x_min_all = org_df_sorted['timestamp'].min()
y_min_all = org_df_sorted['addr'].min()
print("y_min_all:", y_min_all)
plot_scatter_map("bm_meteor_contest.png", sorted_file_path,
                 x_rela_all, y_rela_all, x_min_all, y_min_all)
