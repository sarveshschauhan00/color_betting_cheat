import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('data/emerd.csv')

# Remove duplicate rows
data = data.drop_duplicates()

# Save the DataFrame back to a CSV file (optional)
data.to_csv('data/emerd.csv', index=False)