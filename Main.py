import csv
import os

import pandas as pd

input_directory = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/'  # Specify the directory containing CSV files
output_csv_file = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/2merged_file.csv'  # Specify the output file path
processed_file = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/1processed_files.txt'  # Specify the file to store processed filenames
file_names = []
new_files = []


def get_old_filenames():
    try:
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                for line in f:
                    file_names.append(line.strip())
        else:
            with open(processed_file, 'w'):
                pass
            with open(processed_file, 'r') as f:
                for line in f:
                    file_names.append(line)
    except Exception as e:
        print(f'An error occurred: {e}')
    return file_names


def get_new_filenames():
    try:
        processed_files = get_old_filenames()
        for filename in os.listdir(input_directory):
            if filename not in processed_files:
                if filename.startswith('CommunicationLog'):
                    print(filename)
                    new_files.append(filename)
                    file_names.append(filename)
        with open(processed_file, 'w') as f:
            for name in file_names:
                f.write(name + '\n')
    except Exception as e:
        print(f'An error occurred: {e}')


def merge_csv_files():
    get_new_filenames()
    print(new_files)
    if len(new_files) > 0:
        try:
            with open(output_csv_file, 'a', newline='') as output_csvfile:
                output_writer = csv.writer(output_csvfile)
                for filename in new_files:
                    site = filename[17]
                    row_0 = True
                    input_csvfile = os.path.join(input_directory, filename)
                    with open(input_csvfile, 'r', newline='') as input_csv:
                        input_reader = csv.reader(input_csv, delimiter=',')
                        for row in input_reader:
                            if row_0:
                                row_0 = False
                                row.insert(10, 'Site')
                            else:
                                row.insert(10, site)
                            output_writer.writerow(row)
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print(f'There are {len(new_files)} new files. The {output_csv_file} is up to date!')

merge_csv_files()
total_df = pd.read_csv(output_csv_file)
