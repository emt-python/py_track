import json
import os
import random
import string


def generate_random_string(length=6):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_value():
    """Generate a random value of various types."""
    return random.choice([
        random.randint(1, 100),
        generate_random_string(),
        random.random(),
        bool(random.getrandbits(1)),
        None
    ])


def generate_complex_data(depth=0):
    """Recursively generate complex and nested JSON data."""
    # Limit the recursion depth to avoid excessively deep nesting
    if depth > 3:
        return generate_random_value()

    data_type = random.choice(['dict', 'list', 'value'])

    if data_type == 'dict':
        return {generate_random_string(): generate_complex_data(depth + 1) for _ in range(random.randint(1, 5))}

    elif data_type == 'list':
        return [generate_complex_data(depth + 1) for _ in range(random.randint(1, 5))]

    else:  # 'value'
        return generate_random_value()


def generate_large_json_file(output_file, target_size_mb):
    """Generate a large JSON file of approximately target_size_mb MB."""
    chunk_size = 1024 * 1024  # 1 MB chunks
    total_size = 0

    with open(output_file, 'w', encoding='utf-8') as file:
        while total_size < target_size_mb * 1024 * 1024:
            json_data = json.dumps(generate_complex_data()) + "\n"
            file.write(json_data)
            total_size += len(json_data.encode('utf-8'))
            print(f"Written {total_size / (1024 * 1024)} MB", end='\r')

    print(
        f"\nFinished writing. Total file size: {os.path.getsize(output_file) / (1024 * 1024)} MB")


# Usage example
output_file_path = '2mb_json.txt'  # Output file path
target_size_mb = 2  # Target file size in MB
generate_large_json_file(output_file_path, target_size_mb)
