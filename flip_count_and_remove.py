import pandas as pd

def flip_cnt_rm(name):
    # Read the CSV file
    df = pd.read_csv(f'data/{name}.csv')

    # Find duplicates based on all columns
    duplicates = df[df.duplicated(keep=False)]  # `keep=False` keeps all duplicates

    num_duplicates = len(duplicates)

    print(f'Total number of duplicates: {num_duplicates}')

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save the DataFrame back to a CSV file (optional)
    df.to_csv(f'data/{name}.csv', index=False)
    print('duplicates removed for ', f'{name}')

    # Find duplicates based on all columns
    duplicates = df[df.duplicated(keep=False)]  # `keep=False` keeps all duplicates

    num_duplicates = len(duplicates)

    print(f'Total number of duplicates: {num_duplicates}')

    # print(f'Line numbers of duplicates: {duplicate_indices}')

    # Read the CSV file
    with open(f'data/{name}.csv', 'r') as file:
        lines = file.readlines()

    # Reverse the order of the lines
    lines = lines[::-1]

    # Write the reversed lines back to the file
    with open(f'data/{name}.csv', 'w') as file:
        file.writelines(lines)

    print('\n\n')

names = ['sapre', 'parity', 'bcone', 'emerd']

for name in names:
    flip_cnt_rm(name)
