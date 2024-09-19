def parse_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if (line.startswith("testing")):
                outfile.write(line)
            elif(line.startswith("Compute time: ")):
                parts = line.split()
                outfile.write(parts[2] + '\n')
            elif(line.startswith("Summary: ")):
                if ("total_migration_time:" in line):
                    parts = line.split(',')
                    for part in parts:
                        if "total_migration_time:" in part:
                            migration_time = part.split(":")[1].strip()
                            outfile.write(migration_time + '\n')
            elif "global_demo_size:" in line and "global_promo_size:" in line:
                parts = line.split(',')
                demo_size = parts[0].split(':')[1].strip()
                promo_size = parts[1].split(':')[1].strip()
                outfile.write(demo_size + '\n')
                outfile.write(promo_size + '\n')
            elif line.startswith("----------running networkx_"):
                outfile.write(line)

input_file = "out.txt"
output_file = "parsed_fini.txt"

parse_file(input_file, output_file)

print(f"Filtered lines have been written to {output_file}")