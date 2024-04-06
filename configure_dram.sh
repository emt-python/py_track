#!/bin/bash

# inspect
# for i in {0..48}; do
#     # Check if the memory file exists before trying to cat it
#     if [ -f /sys/devices/system/node/node0/memory${i}/online ]; then
#         echo "Memory ${i} status:"
#         cat /sys/devices/system/node/node0/memory${i}/online
#     else
#         echo "Memory ${i} does not exist."
#     fi
# done

# bring online/offline
for i in {0..48}; do
    echo 1 | sudo tee /sys/devices/system/node/node0/memory${i}/online
done
