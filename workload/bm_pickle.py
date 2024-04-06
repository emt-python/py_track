
"""Script for testing the performance of pickling/unpickling.

This will pickle/unpickle several real world-representative objects a few
thousand times. The methodology below was chosen for was chosen to be similar
to real-world scenarios which operate on single objects at a time. Note that if
we did something like

    pickle.dumps([dict(some_dict) for _ in range(10000)])

this isn't equivalent to dumping the dict 10000 times: pickle uses a
highly-efficient encoding for the n-1 following copies.
"""

import datetime
import random
import sys
import time
import pickle
import string
import gc_count_module

IS_PYPY = '__pypy__' in sys.builtin_module_names

__author__ = "collinwinter@google.com (Collin Winter)"


DICT = {
    'ads_flags': 0,
    'age': 18,
    'birthday': datetime.date(1980, 5, 7),
    'bulletin_count': 0,
    'comment_count': 0,
    'country': 'BR',
    'encrypted_id': 'G9urXXAJwjE',
    'favorite_count': 9,
    'first_name': '',
    'flags': 412317970704,
    'friend_count': 0,
    'gender': 'm',
    'gender_for_display': 'Male',
    'id': 302935349,
    'is_custom_profile_icon': 0,
    'last_name': '',
    'locale_preference': 'pt_BR',
    'member': 0,
    'tags': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    'profile_foo_id': 827119638,
    'secure_encrypted_id': 'Z_xxx2dYx3t4YAdnmfgyKw',
    'session_number': 2,
    'signup_id': '201-19225-223',
    'status': 'A',
    'theme': 1,
    'time_created': 1225237014,
    'time_updated': 1233134493,
    'unread_message_count': 0,
    'user_group': '0',
    'username': 'collinwinter',
    'play_count': 9,
    'view_count': 7,
    'zip': ''
}

TUPLE = (
    [265867233, 265868503, 265252341, 265243910, 265879514,
     266219766, 266021701, 265843726, 265592821, 265246784,
     265853180, 45526486, 265463699, 265848143, 265863062,
     265392591, 265877490, 265823665, 265828884, 265753032], 60)


# def mutate_dict(orig_dict, random_source):
#     new_dict = dict(orig_dict)
#     for key, value in new_dict.items():
#         rand_val = random_source.random() * sys.maxsize
#         if isinstance(key, (int, bytes, str)):
#             new_dict[key] = type(key)(rand_val)
#     return new_dict


# random_source = random.Random(5)  # Fixed seed.
# DICT_GROUP = [mutate_dict(DICT, random_source) for _ in range(10)]


def generate_large_data_structure(size):
    """Generate a very large and complex data structure."""
    base_data = ''.join(random.choices(
        string.ascii_letters + string.digits, k=100))
    # Creating a large list of dictionaries, each containing large strings
    return [{'data': base_data * 100} for _ in range(size)]


def bench_pickle(loops, protocol=pickle.HIGHEST_PROTOCOL):
    range_it = range(loops)
    dumps = pickle.dumps
    # Creating an extremely large data structure; adjust '300000' based on your system's capability
    large_data = generate_large_data_structure(3000000)
    start_time = time.time()

    for _ in range_it:
        # Serializing the large data structure; this operation can be very resource-intensive
        dumps(large_data, protocol)

    elapsed_time = time.time() - start_time
    print(f"Total time for bench_pickle: {elapsed_time:.2f} seconds")


# LIST = [[list(range(10)), list(range(10))] for _ in range(10)]


# def bench_pickle_list(loops, pickle, options):
#     range_it = range(loops)
#     # micro-optimization: use fast local variables
#     dumps = pickle.dumps
#     obj = LIST
#     protocol = options.protocol
#     start_time = time.perf_counter()

#     for _ in range_it:
#         # 10 dumps list
#         for _ in range(100):
#             dumps(obj, protocol)

#     elapsed_time = time.perf_counter() - start_time
#     print(f"Total time for bench_pickle_list: {elapsed_time:.4f} seconds")
#     return elapsed_time


# MICRO_DICT = dict((key, dict.fromkeys(range(10))) for key in range(100))


# def bench_pickle_dict(loops, pickle, options):
#     range_it = range(loops)
#     # micro-optimization: use fast local variables
#     protocol = options.protocol
#     obj = MICRO_DICT
#     start_time = time.perf_counter()

#     for _ in range_it:
#         # 5 dumps dict
#         for _ in range(5):
#             pickle.dumps(obj, protocol)

#     elapsed_time = time.perf_counter() - start_time
#     print(f"Total time for bench_pickle_dict: {elapsed_time:.4f} seconds")
#     return elapsed_time

BENCHMARKS = {
    'pickle': (bench_pickle, 20)
    # 'pickle_list': (bench_pickle_list, 10),
    # 'pickle_dict': (bench_pickle_dict, 5),
}

if __name__ == "__main__":
    protocol = pickle.HIGHEST_PROTOCOL
    loops = 1
    # gc_count_module.start_count_gc_list(
    #     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 10, 1_000_000)
    bench_pickle(loops, protocol)
    # gc_count_module.close_count_gc_list()
