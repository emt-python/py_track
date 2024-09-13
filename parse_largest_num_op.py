def find_largest_old_num_op(file_path):
    largest_value = None
    line_number_of_largest = None

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            # Look for the string "old_num_op: " in the line
            if "old_num_op: " in line:
                try:
                    # Extract the integer after "old_num_op: "
                    value_str = line.split("old_num_op: ")[1].strip()
                    value = int(value_str)

                    # Check if this is the largest value so far
                    if largest_value is None or value > largest_value:
                        largest_value = value
                        line_number_of_largest = line_number

                except (IndexError, ValueError):
                    # If the line doesn't have a valid integer after "old_num_op: ", skip it
                    pass

    return largest_value, line_number_of_largest


# Example usage
file_path = 'out.txt'  # Replace with your file path
largest_value, line_number = find_largest_old_num_op(file_path)

if largest_value is not None:
    print(f"Largest 'old_num_op' value: {largest_value} on line {line_number}")
else:
    print("No 'old_num_op' values found.")
