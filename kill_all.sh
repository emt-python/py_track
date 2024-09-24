#!/bin/bash

kill -9 $(pgrep -f run_knobs.sh)
kill -9 $(pgrep -f test_knobs.sh)
kill -9 $(pgrep -f memeater)
kill -9 $(pgrep -f networkx_)
