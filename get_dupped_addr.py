def find_duplicate_lines(file_path):
    line_count = {}
    duplicate_lines = set()

    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and end-of-line characters for a fair comparison
            cleaned_line = line.strip()
            # Increment the count for the cleaned line
            if cleaned_line in line_count:
                line_count[cleaned_line] += 1
                duplicate_lines.add(cleaned_line)
            else:
                line_count[cleaned_line] = 1

    return duplicate_lines


# Replace 'your_file.txt' with the path to the file you want to check
duplicates = find_duplicate_lines('out.txt')

if duplicates:
    print("Duplicate lines found:")
    for line in duplicates:
        print(line)
else:
    print("No duplicate lines found.")
