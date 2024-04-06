import pandas as pd

# Load the data (replace 'file_path.txt' with your actual file path)
# Adjust the sep parameter based on your file's delimiter (e.g., ',', '\t', etc.)
filename = 'obj_dump.txt'
df = pd.read_csv(filename, sep='\t', header=None, names=['address', 'round'])

# Find duplicated addresses
duplicated_addresses = df[df.duplicated(
    'address', keep=False)].address.unique().tolist()

print(len(duplicated_addresses))
