'''
Given 2 CSV files each with two lists, compare them and send the results.
old_csv 
 - column 1  - SHA1
 - column 2 - file_name
new_csv
 - column 1 - SHA1
 - column 2  - file_name
Return the files which are new and also the one's whose SHA1 is changed.
'''

import csv


def get_key_using_value(input_dict, input_value):
    for key, value in input_dict.iteritems():
        if input_dict[key] == input_value:
            return key
    return None


def compare_csvs(old_csv, new_csv):
    old = {}
    new = {}
    with open(old_csv, 'rb') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        for row in csv_reader:
            old[row['SHA1SUM']] = row['file_name']
    with open(new_csv, 'rb') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        for row in csv_reader:
            old[row['SHA1SUM']] = row['file_name']
    modified_new = []
    for file_name in new.values():
        if file_name not in old.values():
            modified_new.append(file_name)
        elif get_key_using_value(new, file_name) == get_key_using_value(old, file_name):
            modified_new.append(file_name)
    return  modified_new

for value in compare_csvs('/home/rakesh/Desktop/sha1_data.csv', '/home/rakesh/Desktop/sha1.csv'):
    print value