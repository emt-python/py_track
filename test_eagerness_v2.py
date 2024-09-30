import numpy as np
import matplotlib.pyplot as plt

output_path = "traces/test_eagerness.png"


def calculate_changing_extent(values, window_size):
    changing_extent_list = []

    # Loop through the sequence
    for i in range(len(values)):
        if i < window_size:
            # If there are not enough previous values, append 0 or None
            changing_extent_list.append(0)
        else:
            # Get the previous window_size values
            previous_values = values[i-window_size:i]

            # Calculate mean and standard deviation of the previous values
            mean_prev = np.mean(previous_values)
            std_dev_prev = np.std(previous_values)

            # Calculate the changing extent (instability)
            if std_dev_prev == 0:
                # Avoid division by zero
                changing_extent = 0
            else:
                numerator = max(0, values[i] - mean_prev)
                changing_extent = numerator / std_dev_prev

            # Append the changing extent for this point
            changing_extent_list.append(changing_extent)

    return changing_extent_list


# Example sequence of values
# values = [10, 12, 11, 13, 14, 15, 17, 16, 18, 19, 20, 15, 25, 30, 12,
#           10, 12, 11, 13, 14, 15, 17, 16, 18, 19, 20, 15, 25, 30, 12,
#           10, 12, 11, 13, 14, 15, 17, 16, 18, 19, 20, 15, 25, 30, 12,
#           10, 12, 11, 13, 14, 15, 17, 16, 18, 19, 20, 15, 25, 30, 12]
# values = ones_list = [1] * 60
# values = list(range(1, 61))
# values = [1 if i % 2 == 0 else 2 for i in range(60)]
pattern = [1, 5, 5, 5, 5]
values = (pattern * 12)[:60]
print(values)

# Window size (how many previous values to compare against)
window_size = 8

# Calculate changing extent for the sequence
changing_extent = calculate_changing_extent(values, window_size)

# Display the results
for i, extent in enumerate(changing_extent):
    print(f"Value: {values[i]}, Changing Extent: {extent:.3f}")

# min_length = min(len(llc_eager), len(dram_eager))

# # Truncate both lists to the shorter length
# llc_eager = llc_eager[:min_length]
# dram_eager = dram_eager[:min_length]

# Generate x-axis values (incrementing by 1)
x_values = list(range(1, len(values) + 1))
# x_values = list(range(1, len(dram_eager) + 1))

# Plot the two lists as two lines
plt.plot(x_values, values, label='values', marker='o', linestyle='-')
plt.plot(x_values, changing_extent, label='eagerness',
         marker='x', linestyle='--')

# Add labels and title
plt.xlabel('Time (s)')
plt.ylabel('Eagerness')
plt.title('Eagerness')

plt.legend()

plt.savefig(output_path)
