import matplotlib.pyplot as plt

# Step 1: Read and Parse the Data
data_file_path = 'out.txt'
opcode_counts = {}

with open(data_file_path, 'r') as file:
    for line in file:
        opcode, count = line.strip().split(': ')
        opcode_counts[opcode] = int(count)

# Step 2: Sort the Data
sorted_opcodes = sorted(opcode_counts.items(),
                        key=lambda x: x[1], reverse=True)

# Extract opcodes and their counts for plotting
opcodes, counts = zip(*sorted_opcodes)
# Step 3: Plot the Data
plt.figure(figsize=(12, 6))
plt.bar(opcodes, counts, color='skyblue')
plt.xlabel('Opcode')
plt.ylabel('Count')
plt.title('Opcode Counts Distribution')
plt.xticks(rotation=90)
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

plt.savefig('110_ujson_parse_dist.png')
