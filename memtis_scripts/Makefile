CC = gcc
CFLAGS = -g -Wall -O3

default: launch_bench launch_bench_nopid kill_ksampled

launch_bench_nopid: launch_bench.c
	${CC} ${CFLAGS} -D __NOPID launch_bench.c -o launch_bench_nopid

launch_bench: launch_bench.c
	${CC} ${CFLAGS} launch_bench.c -o launch_bench

kill_ksampled: kill_ksampled.c
	${CC} ${CFLAGS} kill_ksampled.c -o kill_ksampled

clean:
	rm launch_bench launch_bench_nopid kill_ksampled