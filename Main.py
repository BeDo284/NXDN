import pandas as pd
import os

path = 'C:/Users/Brecht/OneDrive/Bureaublad/log files/'


# read all filenames
def get_filenames(file_path):
    file_names = []
    for filename in os.listdir(file_path):
        file_names.append(filename)
    return file_names

def get_data():
    new_file_names = get_filenames(path)
    old_file_names = []
    if not os.path.exists(path+'filenames.txt'):
        with open('filenames.txt','w') as f:
            f.write('test')

def create_dataframe():
    names = get_filenames(path)
    dfs = []
    for name in names:
        parts = name.split('_')
        site = parts[1]
        if name.startswith('CommunicationLog'):
            file_path = os.path.join(path, name)
            new_df = pd.read_csv(file_path, delimiter=',')
            new_df['Site'] = site
            dfs.append(new_df)
    log_df = pd.concat(dfs)
    return log_df


total_log_df = create_dataframe()
print('Kies de gewenste optie:')
print('\t1. Zoek op id nummer.')
print('\t2. Vrije id nummers.')
try:
    choice = int(input())
    if choice == 1:
        id = int(input('Geef id nummer:'))
        result = total_log_df[total_log_df['Calling ID'] == id][['Calling ID', 'Date', 'Site']].tail(3)
        print(result)
    elif choice == 2:
        free_ids = []
        for i in range(1, 1000):
            comparison_result = total_log_df['Calling ID'] == i
            if not comparison_result.any():
                free_ids.append(i)
        print(free_ids)
except Exception as e:
    print(f'Er is een fout opgetreden: {e}')
