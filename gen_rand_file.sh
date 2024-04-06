#!/bin/bash

output_file="500mb.txt"
max_size=$((500 * 1024 * 1024)) # 500 MB in bytes
current_size=0

# Clear the output file
>"$output_file"

while [ $current_size -lt $max_size ]; do
    # Append a line of random UTF-8 text
    head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 1000 >>"$output_file"
    echo '' >>"$output_file" # Newline

    # Update the current size
    current_size=$(stat -c%s "$output_file")
    echo "Current file size: $current_size bytes" # Display progress
done

echo "Finished. Final file size: $(stat -c%s "$output_file") bytes"
