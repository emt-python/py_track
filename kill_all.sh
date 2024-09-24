#!/bin/bash

kill -9 $(pgrep -f run_knobs.sh)
kill -9 $(pgrep -f test_knobs.sh)
kill -9 $(pgrep -f run_bench.sh)
kill -9 $(pgrep -f run_all.sh)
kill -9 $(pgrep -f memeater)
kill -9 $(pgrep -f networkx_)
echo 3 | sudo tee /proc/sys/vm/drop_caches