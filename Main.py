import csv
import os
from datetime import datetime

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
    if len(new_files) > 0:
        print(f'There are {len(new_files)} new files. The file {output_csv_file} is updated!')
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
        print(f'There are {len(new_files)} new files. The file {output_csv_file} is up to date!')


merge_csv_files()
total_df = pd.read_csv(output_csv_file)
total_df[['Date', 'Time']] = total_df['Date'].str.split(' ', expand=True)
total_df['Date'] = pd.to_datetime(total_df['Date'], errors='coerce', format='%m/%d/%y', dayfirst=True)
total_df['Time'] = pd.to_datetime(total_df['Time'], format='%H:%M:%S').dt.time
total_sorted_df = total_df.sort_values(by=['Date', 'Time'])

print('Kies de gewenste optie:')
print('\t1. Zoek op id nummer.')
print('\t2. Vrije id nummers.')
print('\t3. Geef id nummers die in een jaar niet geregistreerd zijn.')
print('\t4. Zoek op datum.')
print('\t5. ??')

try:
    today = datetime.now().date()
    total_sorted_df['Difference'] = (pd.Timestamp(today) - total_sorted_df['Date']).dt.days
    total_sorted_df.dropna(subset=['Difference'], inplace=True)
    total_sorted_df.dropna(subset=['Calling ID'], inplace=True)
    try:
        total_sorted_df['Calling ID'] = total_sorted_df['Calling ID'].astype(int)
    except ValueError:
        print("Error: 'id' column contains non-integer values.")

    while True:
        choice = int(input('optie: '))
        if choice == 1:
            radio_id = int(input('Geef id nummer:'))
            result = total_sorted_df[total_sorted_df['Calling ID'] == radio_id][
                ['Calling ID', 'Date', 'Time', 'Difference', 'Site']].tail()
            print(result)
        elif choice == 2:
            existing_ids = set(total_sorted_df['Calling ID'])
            missing_ids = set(range(1, 800)) - existing_ids
            print("Missing IDs:")
            print("\n".join(map(str, sorted(missing_ids))))
        elif choice == 3:
            # get id nuymber that haven't been used in over a year
            total_sorted_df = total_sorted_df[total_sorted_df['Difference'] >= 365]
            result = total_sorted_df.groupby('Calling ID')['Difference'].min()
            result_dict = result.to_dict()
            for key, value in result_dict.items():
                print(f'ID: {key}, Difference: {value}')
        else:
            break
except Exception as e:
    print(f'Er is een fout opgetreden: {e}')
