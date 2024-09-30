#!/bin/bash

pid=$(pgrep -f run_knobs.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f test_knobs.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f run_bench.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f run_all.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f memeater)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f networkx_)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f sqlalchemy)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f perf)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

pid=$(pgrep -f pcm)
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi
echo 3 | sudo tee /proc/sys/vm/drop_caches
