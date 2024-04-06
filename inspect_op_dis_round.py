import pandas as pd
import matplotlib.pyplot as plt


def parse_file(filename):
    # Read the file using pandas
    df = pd.read_csv(filename, sep='\t', header=None,
                     names=['Address', 'Round'])

    condition_93 = df['Address'].astype(str).str.startswith('9')
    df = df[~condition_93]
    # df['Address'] = df['Address'].apply(lambda x: x / (1024*1024))
    # print(df.dtypes)
    # print(df)

    df_sorted = df.sort_values(by=[df.columns[1], df.columns[0]])

    # Group by the second column
    grouped = df_sorted.groupby(df_sorted.columns[1])
    for name, group in grouped:
        print(f"Group: {name}")
        print("start: ", group.iloc[0]['Address'],
              "last: ", group.iloc[-1]['Address'])

    return df


def plot_data(df):
    plt.scatter(df['Round'], df['Address'], s=10)
    plt.xlabel('Round')
    plt.ylabel('Addresses')
    plt.title('Distribution of Addresses by Round')
    # plt.show()
    plt.savefig('dis_round.png')


filename = 'obj_dump.txt'  # Replace with your file name
df = parse_file(filename)
plot_data(df)
