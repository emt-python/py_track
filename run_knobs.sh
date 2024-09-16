#!/bin/bash

LOG_FILE=out.txt

echo "testing 0 0 0" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 0 0 0 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 0 0" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 0 0 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 0 1" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 0 1 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 0 2" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 0 2 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 0 3" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 0 3 >/dev/null 2>&1
popd
./test_knobs.sh
