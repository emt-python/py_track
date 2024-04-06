import json
import time
import sys
import gc
import os
import gc_count_module
sys.setswitchinterval(0.0001)


def add_or_append_to_dict(source_dict, result_dict):
    for key, value in source_dict.items():
        # Check if the value is a dictionary (nested JSON object)
        if isinstance(value, dict):
            # For nested dictionaries, call this function recursively
            add_or_append_to_dict(value, result_dict)
        elif isinstance(value, list):
            # If the value is a list, set the corresponding result_dict key to ""
            result_dict[key] = ""
        else:
            # If the key already exists in result_dict, add the value to the existing value
            if key in result_dict and isinstance(result_dict[key], int):
                result_dict[key] += value
            else:
                # Otherwise, set the value for the key in result_dict
                result_dict[key] = value


def parse_json_file(filename):
    result_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            # try:
            # Parse the JSON object from the line
            json_obj = json.loads(line)
            # Update the result_dict with the values from the json_obj
            add_or_append_to_dict(json_obj, result_dict)
            # except json.JSONDecodeError as e:
            #     print(f"Error parsing JSON from line: {e}")

    return result_dict


CUR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
json_size = sys.argv[1]
file_path = os.path.join(CUR_DIR, '{}_json_int.txt'.format(json_size))
gc.collect()
start = time.time()

# gc_count_module.start_count_gc_list(
#     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 1, 10, 3500000)

result = parse_json_file(file_path)
# gc_count_module.close_count_gc_list()
latency = time.time() - start
print("latency: {:.3f} seconds".format(latency), file=sys.stderr)
