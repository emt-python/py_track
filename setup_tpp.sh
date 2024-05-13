#!/bin/bash

if [ "$1" = "enable" ]; then
    echo 1 | sudo tee /sys/kernel/mm/numa/demotion_enabled
    echo 3 | sudo tee /proc/sys/kernel/numa_balancing
    echo 200 | sudo tee /proc/sys/vm/demote_scale_factor
    echo enabled tpp
elif [ "$1" = "disable" ]; then
    echo 0 | sudo tee /sys/kernel/mm/numa/demotion_enabled
    echo 0 | sudo tee /proc/sys/kernel/numa_balancing
    echo disabled tpp
elif [ "$1" = "autonuma" ]; then
    echo 0 | sudo tee /sys/kernel/mm/numa/demotion_enabled
    echo 1 | sudo tee /proc/sys/kernel/numa_balancing
    echo disabled autonuma
else
    echo "specify you want to enable/disable"
    exit 1
fi

sleep 1
