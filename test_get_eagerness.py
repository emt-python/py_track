from collections import deque

# Function to calculate the average of a list


def avg(arr):
    return sum(arr) / len(arr) if len(arr) > 0 else 0

# Function to calculate the changing extent


def calculate_changing_extent(arr, current_value):
    if len(arr) == 0:
        # print("returned1")
        return 0  # Avoid division by zero with an empty array

    avg_previous = avg(arr)

    max_val = max(arr)
    min_val = min(arr)
    print(buffer)

    # To avoid division by zero if max_val equals min_val
    if max_val == min_val:
        # print("returned2")
        return 0

    # Calculate changing extent
    changing_extent = (current_value - avg_previous) / (max_val - min_val)
    # print(
    # f"current: {current_value}, avg_previous: {avg_previous}, min_val: {min_val}, max_val: {max_val}")
    return changing_extent


# Main buffer size and deque initialization
buffer_size = 8
buffer = deque(maxlen=buffer_size)  # Deque to hold the most recent 8 elements

# Example list of values (this can be your dynamically updated list)
# values=[10, 12, 11, 13, 14, 15, 17, 16, 18, 19, 20, 21]
values = [6.75, 0.98, 0.79, 0.68, 0.71, 2.79, 0.95, 0.97, 22.96, 23.17, 23.67, 0.0, 0.0, 6.91, 0.97, 0.8, 0.98, 0.62, 0.79, 0.69, 0.87, 0.66, 18.47, 18.16, 17.84, 0.0, 0.0,
          29.0, 2.46, 3.45, 27.1, 20.8, 5.22, 35.09, 5.53, 37.14, 6.73, 36.97, 6.78, 6.88, 22.93, 15.24, 46.52, 6.73, 4.98, 41.29, 43.38, 36.68, 54.08, 1.33, 51.61, 44.25, 18.57]

# Process each value and calculate the changing extent
for i, value in enumerate(values):
    # Calculate changing extent even for the first 7 elements (buffer smaller than 8)
    changing_extent = calculate_changing_extent(buffer, value)
    print(f"Value: {value}, Changing Extent: {changing_extent:.3f}")
    # print()
    # Add the current value to the buffer
    buffer.append(value)
