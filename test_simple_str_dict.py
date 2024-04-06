import time
import sys
import gc_count_module
sys.setswitchinterval(0.0001)


def parse_json_and_combine_duplicates():
    combined_data = {}
    for i in range(200000):
        combined_data[i + 3456735] = str(i + 4574658)
        time.sleep(0.0001)


start = time.time()
gc_count_module.start_count_gc_list(
    250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 1, 10, 3500000)
parse_json_and_combine_duplicates()
gc_count_module.close_count_gc_list()
latency = time.time() - start
print("latency: {:.3f} seconds".format(latency), file=sys.stderr)
time.sleep(1)
