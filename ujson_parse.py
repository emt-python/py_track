# import ujson
import dis
import json
import sys
import os
import time
import gc_count_module
import gc
# gc.disable()

CUR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def parse_json_and_combine_duplicates(file_path):
    """Parse each line of the file as a separate JSON object and combine duplicates."""
    combined_data = {}
    found_key = 0
    not_found_key = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # try:
            json_object = json.loads(line)
            for key, value in json_object.items():
                if key in combined_data:
                    #     # If the key already exists, append the value to the existing list
                    if not isinstance(combined_data[key], list):
                        combined_data[key] = [combined_data[key]]
                        # combined_data[key].append(value)
                    found_key += 1
                else:
                    # If the key doesn't exist, just add it
                    combined_data[key] = value
                # print(id(key))
                    not_found_key += 1
            # except ujson.JSONDecodeError as e:
            #     print(f"Error parsing JSON: {e}")
    print(f"found_key: {found_key}, not_found_key: {not_found_key}")
    return combined_data


opcode_counts = {opname: 0 for opname in dis.opname}


def trace(frame, event, arg):
    if event == 'call':
        # Get bytecode for the current frame
        code_obj = frame.f_code
        bytecode = code_obj.co_code

        # Iterate through bytecode instructions
        for offset in range(0, len(bytecode), 2):  # Assuming Python 3.6+
            opcode = bytecode[offset]
            opcode_counts[dis.opname[opcode]] += 1
    return trace


gc.collect()
# gc.disable()

json_size = sys.argv[1]
file_path = os.path.join(CUR_DIR, '{}_json.txt'.format(json_size))

start = time.time()
gc_count_module.start_count_gc_list(
    250_000, "obj_dump.txt", 0, 10, 1_000_000)
# sys.settrace(trace)
combined_data = parse_json_and_combine_duplicates(file_path)
# del (combined_data)
# gc.collect()
first_end = time.time()
# print("doing second", file=sys.stderr)
# combined_data = parse_json_and_combine_duplicates(file_path)
# sys.settrace(None)
# for opcode, count in opcode_counts.items():
# if count > 0:
# print(f"{opcode}: {count}")
# dis.dis(parse_json_and_combine_duplicates)
# byte_code = parse_json_and_combine_duplicates.__code__.co_code
# dis.dis(byte_code)
first_latency = first_end - start
second_latency = time.time() - start
gc_count_module.close_count_gc_list()
print("latency: {:.3f} , 2nd: {:.3f}".format(
    first_latency, second_latency), file=sys.stderr)
time.sleep(2)

# Print the combined data
# for key, value in combined_data.items():
#     print(f"{key}: {value}")
