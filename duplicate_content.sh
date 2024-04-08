#!/bin/bash

# Define the source and destination files
SOURCE_FILE="workload/telco-bench-dupped.bin"
DESTINATION_FILE="workload/telco-bench-dupped-large.bin"

# Ensure the destination file is empty or does not exist
>"$DESTINATION_FILE"

# Loop to append the content 10 times
for i in {1..10}; do
    cat "$SOURCE_FILE" >>"$DESTINATION_FILE"
done

echo "Content duplicated successfully."
