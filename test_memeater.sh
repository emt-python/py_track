#!/bin/bash
test_func() {
    echo 3 | sudo tee /proc/sys/vm/drop_caches
    trap 'echo "starting running benchmark"; sleep 8 & check_pid=$!; wait $check_pid' SIGUSR1
    stdbuf -oL ./memeater 81920 $$ &
    MEMAETER_PID=$!
    # echo "Waiting for memeater to reach the memory threshold..."
    wait $MEMAETER_PID

    # while kill -0 "$SECOND_PROGRAM_PID" 2>/dev/null; do
    #     sleep 0.5
    # done
    echo "killing memeater"
    kill -9 $MEMAETER_PID
}

test_func >>out.txt 2>&1
