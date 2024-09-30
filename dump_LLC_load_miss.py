import re
import sys

workload_name = sys.argv[1]
input_path = "traces/"+workload_name+"_perf_stat.log"
output_path = "traces/"+workload_name+"_perf_stat_parsed.txt"

# Regular expression to capture the percentage from the target line
pattern = r'LLC-load-misses:u\s+#\s+([0-9.]+)%'

# Open the input file and output file
with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
    # Loop through each line in the input file
    for line in infile:
        # Search for the line that contains "LLC-load-misses:u" and the percentage
        match = re.search(pattern, line)
        if match:
            # Extract the percentage value
            llc_miss_percent = match.group(1)
            # Write the percentage value to the output file
            outfile.write(f"{llc_miss_percent}\n")

print(f"LLC-load-miss percentages written to {output_path}")
