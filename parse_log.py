# Function to filter lines and write to a new file
def parse_file(input_file, output_file):
    # Open the input file to read and output file to write
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Iterate through each line in the input file
        for line in infile:
            # Check if the line starts with the specified strings
            if (line.startswith("testing") or 
                line.startswith("Compute time: ") or
                line.startswith("Summary: ") or
                line.startswith("----------running networkx_") or
                line.startswith("global_demo_size: ")):
                # Write the matching line to the output file
                outfile.write(line)

# Specify the input and output file names
input_file = "out.txt"
output_file = "parsed.txt"

# Call the function to parse the file
parse_file(input_file, output_file)

print(f"Filtered lines have been written to {output_file}")