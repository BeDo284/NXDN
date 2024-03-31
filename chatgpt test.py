import csv
import os


def merge_csv_files(input_dir, output_file, processed_file):
    # Load processed files from the processed_file
    processed_files = set()
    if os.path.exists(processed_file):
        with open(processed_file, 'r') as f:
            processed_files = set(f.read().splitlines())

    # Open the output CSV file in append mode
    with open(output_file, 'a', newline='') as output_csvfile:
        output_writer = csv.writer(output_csvfile)

        # Iterate through each file in the input directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.csv') and filename not in processed_files:  # Check if it's a new CSV file
                input_csvfile = os.path.join(input_dir, filename)
                # Open each input CSV file in read mode
                with open(input_csvfile, 'r', newline='') as input_csv:
                    input_reader = csv.reader(input_csv)
                    # Write each row from the input file to the output file
                    for row in input_reader:
                        output_writer.writerow(row)
                # Add the filename to the set of processed files
                processed_files.add(filename)

    # Write processed files back to the processed_file
    with open(processed_file, 'w') as f:
        for filename in processed_files:
            f.write(filename + '\n')


# Example usage
input_directory = 'path/to/your/input/files'  # Specify the directory containing CSV files
output_csv_file = 'path/to/your/output/merged_file.csv'  # Specify the output file path
processed_file = 'path/to/your/processed_files.txt'  # Specify the file to store processed filenames
merge_csv_files(input_directory, output_csv_file, processed_file)
