import csv
from itertools import izip

def my_fun(location='/home/rakesh/Documents/doc/inventory/fileinfo.csv'):
    rpms = []
    with open(location, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            if '.rpm' in row[0]:
                rpms.append(row[0])
        
    return list(set(rpms))

def get_n_column_from_csv(n,location='/home/rakesh/Documents/doc/inventory/fileinfo.csv'):
    n_column = []
    with open(location, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            n_column.append(row[n])
    return n_column
        

def split_fun(input):
    values = input.split('/')
    for value in values:
        if '.rpm' in value:
            return value
def my_func2(location='/home/rakesh/Downloads/deployed-rpm-query-all.txt'):
    rpms = []
    with open(location,'rb') as file_read:
        for line in file_read:
            line = line.strip()
            rpms.append(line)
    return list(set(rpms))


def my_func3(location='/home/rakesh/Documents/doc/castor/category/deployed-rpm-filesbypkg.lst'):
    key_pairs = {}
    all_lines = []
    with open(location,'rb') as read_file:
        for line in read_file:
            line = line.strip()
            if line.index('/')>=0:
                key_pairs[line[0:line.index('/')]] = ''
    
    with open(location,'rb') as read_file:
        for line in read_file:
            line = line.strip()
            if line.index('/')>=0:
                key_pairs[line[0:line.index('/')]] = key_pairs[line[0:line.index('/')]] + line[line.index('/')-1:] + '\n'                 
    
    
    return key_pairs

def strip_dict_keys(input):
    output = {}
    for key,pair in input.iteritems():
        key = key.strip()
        output[key] = pair
    return output
def two_lists_to_csv(list1,list2,location):
    with open(location, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(izip(list1, list2))

# key_pairs = strip_dict_keys(my_func3())
# two_lists_to_csv(key_pairs.keys(), key_pairs.values(), '/home/rakesh/Documents/doc/castor/category/rpm_locations.csv')

# rpm_loc_rows = get_n_column_from_csv(1,'/home/rakesh/Documents/doc/castor/category/rpm_locations.csv')
# output_rows = get_n_column_from_csv(0,'/home/rakesh/Documents/doc/castor/analyse_rpms2/output.csv')
# for row in output_rows:
#     if row not in rpm_loc_rows:
#         print row