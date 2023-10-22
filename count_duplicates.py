import pandas as pd

# Read the CSV file
df = pd.read_csv('data/emerd.csv')

# Find duplicates based on all columns
duplicates = df[df.duplicated(keep=False)]  # `keep=False` keeps all duplicates

num_duplicates = len(duplicates)

print(f'Total number of duplicates: {num_duplicates}')

# # Get the line numbers of the duplicates
# duplicate_indices = duplicates.index.tolist()

# print(f'Line numbers of duplicates: {duplicate_indices}')
