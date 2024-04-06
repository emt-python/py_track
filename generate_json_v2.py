import json
import os
import random
import string


def generate_random_string(length=8):
    """Generate a random string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_data(depth=0):
    """Generate random data with varying structures for JSON."""
    if depth > 3:  # Limit the depth of nesting
        return generate_random_string()

    # Randomly choose a structure: simple key-value, nested JSON, array, mixed
    choice = random.choice(['nested', 'array', 'mixed'])

    if choice == 'simple':
        # Simple key-value pair
        return {generate_random_string(5): random.randint(3000, 5000)}

    elif choice == 'nested':
        # Nested JSON
        return {generate_random_string(5): generate_random_data(depth + 1)}

    elif choice == 'array':
        # Array in JSON
        array_length = random.randint(2, 5)
        return {generate_random_string(5): [generate_random_data(depth + 1) for _ in range(array_length)]}

    elif choice == 'mixed':
        # Mixed content
        return {
            generate_random_string(5): generate_random_data(depth + 1),
            generate_random_string(5): generate_random_string(),
            # generate_random_string(5): random.randint(1, 100)
        }


def generate_large_json_file(output_file, target_size_mb):
    """Generate a large JSON file of approximately target_size_mb MB."""
    chunk_size = 1024 * 1024  # 1 MB chunks
    total_size = 0

    with open(output_file, 'w', encoding='utf-8') as file:
        # count = 0
        while total_size < target_size_mb * 1024 * 1024:
            # while count < 2900000:  # 2900000:500mb
            json_data = json.dumps(generate_random_data()) + "\n"
            file.write(json_data)
            total_size += len(json_data.encode('utf-8'))
            print(f"Written {total_size / (1024 * 1024)} MB", end='\r')
            # count += 1

    print(
        f"\nFinished writing. Total file size: {os.path.getsize(output_file) / (1024 * 1024)} MB")


# Usage example
output_file_path = '110mb_json.txt'  # Output file path
target_size_mb = 100  # Target file size in MB
generate_large_json_file(output_file_path, target_size_mb)
