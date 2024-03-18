import csv
import os

import pandas as pd

path = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/'
old_file_path = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/filenames.txt'

output_file = 'output_merged.csv'


def get_filenames(file_path):
    file_names = []
    for filename in os.listdir(file_path):
        file_names.append(filename)
    return file_names


def get_old_file_names():
    file_names = []
    with open(old_file_path, 'r') as f:
        for name in f:
            file_names.append(name.strip())
    return file_names


def compare_file_names():
    new_file_names = get_filenames(path)
    old_file_names = get_old_file_names()
    no_corresponding_file_names = []
    for file_name in new_file_names:
        if file_name.startswith('CommunicationLog'):
            if file_name not in old_file_names:
                no_corresponding_file_names.append(file_name)
    if os.path.isfile(old_file_path):
        with open(old_file_path, 'a') as f:
            for name in no_corresponding_file_names:
                f.write(name + '\n')
    else:
        with open(old_file_path, 'w') as f:
            for name in no_corresponding_file_names:
                f.write(name + '\n')
    return no_corresponding_file_names


def get_data():
    total_df = pd.DataFrame()
    files_to_read = compare_file_names()



# print(get_old_file_names())
