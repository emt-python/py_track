import pandas as pd
import matplotlib.pyplot as plt

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

    # Plot the bar chart
    plt.figure(figsize=(30, 6))
    temperature_distribution.plot(kind='bar')
    plt.xlabel('Temperature')
    plt.ylabel('Occurrence')
    plt.title(f'Distribution of Page Temperatures at Time {time}')
    # plt.show()
    plt.savefig(f'page_temps/{time}.png')
