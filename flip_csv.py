# Read the CSV file
with open('data/emerd.csv', 'r') as file:
    lines = file.readlines()

# Reverse the order of the lines
lines = lines[::-1]

# Write the reversed lines back to the file
with open('data/emerd.csv', 'w') as file:
    file.writelines(lines)
