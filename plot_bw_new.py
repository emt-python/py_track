import matplotlib.pyplot as plt
import sys
from collections import deque
import numpy as np

buffer_size = 8


def avg(arr):
    return sum(arr) / len(arr) if len(arr) > 0 else 0


def calculate_changing_extent(arr, current_value):
    if len(arr) == 0:
        # print("returned1")
        return 0  # Avoid division by zero with an empty array
    avg_previous = avg(arr)
    max_val = max(arr)
    min_val = min(arr)
    if max_val == min_val:
        print("deno == 0")
        return 0
    changing_extent = (avg_previous) / (max_val - min_val)
    if changing_extent > 1:
        changing_extent = 1
    elif changing_extent < 0:
        changing_extent = 0
    # print(
    #     f"current: {current_value}, avg_previous: {avg_previous}, min_val: {min_val}, max_val: {max_val}, changing_extent: {changing_extent}")
    return changing_extent


def calculate_changing_extent_v2(values, window_size):
    changing_extent_list = []
    current_min = float('inf')
    current_max = float('-inf')

    for i in range(len(values)):
        if i < window_size:
            changing_extent_list.append(0)
        else:
            previous_values = values[i-window_size:i]

            mean_prev = np.mean(previous_values)
            std_dev_prev = np.std(previous_values)

            if std_dev_prev == 0:
                changing_extent = 0
            else:
                numerator = max(0, values[i] - mean_prev)
                changing_extent = numerator / std_dev_prev
                # changing_extent = abs(values[i] - mean_prev) / std_dev_prev
            # changing_extent = min(changing_extent, 10)
            current_min = min(current_min, changing_extent)
            current_max = max(current_max, changing_extent)

            if current_max > current_min:
                normalized_value = (
                    changing_extent - current_min) / (current_max - current_min)
            else:
                normalized_value = 0

            changing_extent_list.append(normalized_value)
            # changing_extent_list.append(changing_extent)

    return changing_extent_list


workload_name = sys.argv[1]
input_path_bw = "traces/"+workload_name+"_parsed_bw.txt"
input_path_llc = "traces/"+workload_name+"_perf_stat_parsed.txt"
output_path = "traces/"+workload_name+"_together.png"
dram_col = []
cxl_col = []
llc_col = []

llc_eager = []
dram_eager = []
cxl_eager = []


# Read the first file (two columns)
with open(input_path_bw, 'r') as file1:
    for line in file1:
        values = line.split()  # Split the line by whitespace
        if len(values) == 2:  # Ensure there are exactly two columns
            dram_col.append(float(values[0]))
            cxl_col.append(float(values[1]))

# Read the second file (one column)
with open(input_path_llc, 'r') as file2:
    for line in file2:
        value = line.strip()  # Remove any leading/trailing whitespace
        if value:  # If the line is not empty
            llc_col.append(float(value))

x_values_file1 = list(range(1, len(dram_col) + 1))
x_values_file2 = [1 * i for i in range(1, len(llc_col) + 1)]

fig, ax1 = plt.subplots()

# Plot the data from the first file (both columns) on the left y-axis
ax1.plot(x_values_file1, dram_col,
         label='Local DRAM', marker='o', color='b')
ax1.plot(x_values_file1, cxl_col,
         label='CXL', marker='x', color='g')

# Set the labels for the left y-axis and the x-axis
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Bandwidth (MB/s)', color='k')

# Create another y-axis (right side) that shares the same x-axis
ax2 = ax1.twinx()

# Plot the data from the second file on the right y-axis
ax2.plot(x_values_file2, llc_col,
         label='LLC miss rate', marker='s', color='r')

# Set the label for the right y-axis
ax2.set_ylabel('LLC miss rate')

# Combine the legends from both axes
fig.legend(loc="upper left", bbox_to_anchor=(
    0.1, 1), bbox_transform=ax1.transAxes)

# Set the title of the plot
plt.title('LLC miss rate and local DRAM/CXL bandwidth')

# Display the plot
plt.savefig(output_path)
plt.close()

# calculate eager_ness
llc_buffer = deque(maxlen=buffer_size)
dram_buffer = deque(maxlen=buffer_size)
cxl_buffer = deque(maxlen=buffer_size)
llc_eager = calculate_changing_extent_v2(llc_col, buffer_size)

dram_eager = calculate_changing_extent_v2(dram_col, buffer_size)
# for i, extent in enumerate(dram_eager):
#     print(f"Value: {llc_col[i]}, Changing Extent: {extent:.3f}")

# old way of calculating eagerness
# for i, value in enumerate(cxl_col):
#     changing_extent = calculate_changing_extent(cxl_buffer, value)
#     cxl_eager.append(changing_extent)
#     cxl_buffer.append(value)

print(f"len(llc_col): {len(llc_col)}, len(dram_col): {len(dram_col)}")
print(f"len(llc_eager): {len(llc_eager)}, len(dram_eager): {len(dram_eager)}")


output_path = "traces/"+workload_name+"_eagerness.png"

min_length = min(len(llc_eager), len(dram_eager))

# Truncate both lists to the shorter length
llc_eager = llc_eager[:min_length]
dram_eager = dram_eager[:min_length]

# Generate x-axis values (incrementing by 1)
x_values = list(range(1, min_length + 1))
x_values = list(range(1, len(dram_eager) + 1))

# Plot the two lists as two lines
plt.plot(x_values, llc_eager, label='LLC', marker='o', linestyle='-')
plt.plot(x_values, dram_eager, label='DRAM BW', marker='x', linestyle='--')
# plt.ylim(0, 1)

# Add labels and title
plt.xlabel('Time (s)')
plt.ylabel('Eagerness')
plt.title('Eagerness of LLC Miss and DRAM BW')

plt.legend()

plt.savefig(output_path)
