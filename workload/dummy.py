import sys
import os
import time

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

enable_tracing = False
if len(sys.argv) != 1:
    print("enable tracing")
    enable_tracing = True

print("start running wl")
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 7, 2_500_000)
time.sleep(4)
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
print("end running wl", file=sys.stderr)
