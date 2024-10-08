import pandas as pd
import matplotlib.pyplot as plt
import os


def remove_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # Remove the file
            elif os.path.isdir(file_path):
                # If it's a directory, skip it (to only delete files)
                pass
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


# Example usage
folder_path = 'page_temps'
remove_all_files_in_folder(folder_path)

# Load the file into a pandas DataFrame (assuming a space or tab-delimited file)
df = pd.read_csv('page_hotness.txt', delim_whitespace=True,
                 header=None, names=['Time', 'Temperature'])

# Group the data by 'Time'
grouped = df.groupby('Time')

# Iterate over each group (each timestamp) and plot the distribution of temperatures
for time, group in grouped:
    # group = group[group['Temperature'] != 0]
    # Get the frequency distribution of temperatures for this particular timestamp
    temperature_distribution = group['Temperature'].value_counts().sort_index()

    # Plot the bar chartge
    plt.figure(figsize=(30, 6))
    temperature_distribution.plot(kind='bar')
    plt.xlabel('Temperature')
    plt.ylabel('Occurrence')
    plt.title(f'Distribution of Page Temperatures at Time {time}')
    # plt.show()
    plt.savefig(f'page_temps/{time}.png')
