import matplotlib.pyplot as plt
import numpy as np

# Initialize lists to store the lengths
list_lengths = []
dict_lengths = []
set_lengths = []
str_lengths = []

# Read the file and populate the lists
data_file = 'inspect_len'
with open(data_file + '.txt', 'r') as file:
    for line in file:
        # Split the line into type and length
        row_type, length_str = line.split('\t')
        # Convert length to int and remove newline
        length = int(length_str.strip())

        # Append the length to the appropriate list
        if length > 20:
            # print("skipping", length)
            continue
        # elif length > 4000:
        #     print(length)
        if row_type == 'list':
            list_lengths.append(length)
        elif row_type == 'dict':
            dict_lengths.append(length)
        elif row_type == 'set':
            set_lengths.append(length)
        elif row_type == 'str':
            str_lengths.append(length)

# Function to calculate the CDF


def calculate_cdf(data):
    # Sort the data in ascending order
    x = np.sort(data)
    # Calculate the CDF values
    # cdf = np.arange(1, len(data_sorted) + 1) / float(len(data_sorted))
    y = np.arange(1, len(x) + 1) / len(x)
    return x, y


# Calculate CDF for both lists and dicts
list_data_sorted, list_cdf = calculate_cdf(list_lengths)
dict_data_sorted, dict_cdf = calculate_cdf(dict_lengths)
set_data_sorted, set_cdf = calculate_cdf(set_lengths)
str_data_sorted, str_cdf = calculate_cdf(str_lengths)

# Plotting the CDFs
plt.figure(figsize=(10, 6))
# plt.plot(list_data_sorted, list_cdf, label='List Lengths',
#          marker='.', linestyle='none')
plt.plot(list_data_sorted, list_cdf, label='List PyObj Length Distribution',
         marker='.', markersize=5, linestyle='none')
# plt.plot(dict_data_sorted, dict_cdf, label='Dict Lengths',
#          marker='.', linestyle='none')
plt.plot(dict_data_sorted, dict_cdf, label='Dict PyObj Length Distribution',
         marker='.', markersize=5, linestyle='none')
plt.plot(set_data_sorted, set_cdf, label='Set PyObj Length Distribution',
         marker='.', markersize=5, linestyle='none')
plt.plot(str_data_sorted, str_cdf, label='Str PyObj Length Distribution',
         marker='.', markersize=5, linestyle='none')
plt.legend()
plt.xlabel('Length of PyVarObjects')
plt.ylabel('CDF')
plt.title('CDF Distribution of PyVarObject Lengths')
# plt.grid(True)
plt.savefig(data_file + '_cdf.png')
