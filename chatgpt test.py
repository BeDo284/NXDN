import os
import pandas as pd

# Directory containing CSV files
directory = '/path/to/csv/files'

# List to store file names
file_names = []

# List to store dataframes
dataframes = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Append filename to list
        file_names.append(filename)
        # Read CSV file into a DataFrame
        df = pd.read_csv(os.path.join(directory, filename))
        # Append DataFrame to list
        dataframes.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes)

# Save combined DataFrame to CSV
combined_df.to_csv('combined.csv', index=False)

# Save file names to a text file
with open('file_names.txt', 'w') as f:
    for filename in file_names:
        f.write(filename + '\n')

print("CSV files combined and file names saved successfully.")
