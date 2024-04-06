import json
import os
import random


def generate_random_integer(min_value=1, max_value=100):
    """Generate a random integer."""
    return random.randint(min_value, max_value)


def generate_random_data(depth=0):
    """Generate random data with varying structures for JSON."""
    if depth > 3:  # Limit the depth of nesting
        return generate_random_integer()

    # Randomly choose a structure: simple key-value, nested JSON, array, mixed
    choice = random.choice(['simple', 'nested', 'array'])

    if choice == 'simple':
        # Simple key-value pair
        return {f"key_{generate_random_integer(1, 10000)}": generate_random_integer(3000, 5000)}

    elif choice == 'nested':
        # Nested JSON
        return {f"key_{generate_random_integer(1, 10000)}": generate_random_data(depth + 1)}

    elif choice == 'array':
        # Array in JSON
        array_length = random.randint(2, 5)
        return {f"key_{generate_random_integer(1, 10000)}": [generate_random_integer(400000, 800000) for _ in range(array_length)]}


def generate_large_json_file(output_file, target_size_mb):
    """Generate a large JSON file of approximately target_size_mb MB."""
    chunk_size = 1024 * 1024  # 1 MB chunks
    total_size = 0

    with open(output_file, 'w', encoding='utf-8') as file:
        while total_size < target_size_mb * 1024 * 1024:
            json_data = json.dumps(generate_random_data()) + "\n"
            file.write(json_data)
            total_size += len(json_data.encode('utf-8'))
            print(f"Written {total_size / (1024 * 1024)} MB", end='\r')

    print(
        f"\nFinished writing. Total file size: {os.path.getsize(output_file) / (1024 * 1024)} MB")


# Usage example
output_file_path = '500mb_json_int.txt'  # Output file path
target_size_mb = 500  # Target file size in MB
generate_large_json_file(output_file_path, target_size_mb)
