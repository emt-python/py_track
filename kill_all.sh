#!/bin/bash

pid=$(pgrep -f run_knobs.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed run_knobs"

pid=$(pgrep -f test_knobs.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed test_knobs"

pid=$(pgrep -f run_bench.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed run_bench"

pid=$(pgrep -f run_all.sh)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed run_all"

pid=$(pgrep -f memeater)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed memeater"

pid=$(pgrep -f networkx_)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed networkx_"

pid=$(pgrep -f bm_sqlalchemy)
if [ -n "$pid" ]; then
    kill -9 "$pid" || true
fi
echo "killed sqlalchemy"

pid=$(pgrep -f perf)
if [ -n "$pid" ]; then
    sudo kill -9 "$pid" || true
fi
echo "killed perf"

pid=$(pgrep -f pcm)
if [ -n "$pid" ]; then
    sudo kill -9 "$pid" || true
fi
echo "killed pcm"
echo "killed everything!"

echo 3 | sudo tee /proc/sys/vm/drop_caches
