def process_file(filename):
    # Initialize a global dictionary to store the results
    type_summary = {}

    # Open and read the file
    with open(filename, 'r') as file:
        for line in file:
            # Check if the line starts with 'starting '
            if line.startswith('starting: '):
                # Extract the string after 'starting '
                data = line[len('starting '):].strip()
                # Parse the extracted string into type and depth
                try:
                    type, depth_str = data.split('\t')
                    depth = int(depth_str)

                    # Update the global dictionary
                    if type in type_summary:
                        type_summary[type] = (
                            type_summary[type][0] + 1, type_summary[type][1] + depth)
                    else:
                        type_summary[type] = (1, depth)
                except ValueError:
                    # Handle any parsing errors
                    print(f"Error parsing line: {line}")

    return type_summary


# Example usage
# Replace 'path_to_file.txt' with the actual file path
file_path = 'out.txt'
result = process_file(file_path)
print(result)
