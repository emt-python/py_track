#!/bin/bash

LOG_FILE=out.txt

echo "testing 1 1 1" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 1 1 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 1 2" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 1 2 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 1 3" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 1 3 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 2 0" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 2 0 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 2 1" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 2 1 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 2 2" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 2 2 >/dev/null 2>&1
popd
./test_knobs.sh

echo "testing 1 2 3" >>$LOG_FILE
EMT_DIR=/home/cc/workspace/cpython
pushd $EMT_DIR
./rebuild.sh 1 2 3 >/dev/null 2>&1
popd
./test_knobs.sh
