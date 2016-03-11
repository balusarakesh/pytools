#
#  Copyright (c) 2015 nexB Inc. and others. All rights reserved.
#


import csv
import requests
import url

'''
'input_file' is a CSV. If any column has the key word 'url', then all the 
values in that column are assumed as URLs and the 'output_file' file is returned which consists 
of the URLs and their corresponding status.
'''


def get_validity(input):
    '''
    Return True if a given string is a valid URI.
    '''
    return url.parse(input).absolute()


def get_status(input):
    '''
    Return the status of URL ('not a URL', 'not-working' and 'working').
    '''
    try:
        if get_validity(input):
            r = requests.head(input.strip(),verify = False )
            if r.status_code in [404, 500, 501, 502, 503, 504, 405, 408, 410]:
                return 'not-working'
            else:
                return 'working'
        else:
            return 'not a URL'
    except Exception, e:
        print str(e)
        return 'not-working'


def combine_dicts(input):
    '''
    Combine a list of dictionaries and returns a single dictionary.
    '''
    output = {}
    for single_dict in input:
        output = dict(output.items()+single_dict.items())
    return output


def get_url_status(input_file, output_file):
    '''
    Return the output_file which has the URL column and it's status column.
    Any column with the string 'URL' is considered as a column with URLs.
    '''
    rows_as_dicts = []
    all_keys = []
    with open(input_file, 'rb') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            temp = []
            for key,value in row.iteritems():
                if 'url' in key.lower():
                    if value != '':
                        all_keys.append(key) if key not in all_keys else None
                        all_keys.append(key+'_STATUS') if key + '_STATUS' not in all_keys else None
                        temp.append({key:value, key + '_STATUS':get_status(value)})
            rows_as_dicts.append(combine_dicts(temp))

    with open(output_file, 'wb') as csv_file:
        csv_write = csv.writer(csv_file, delimiter=',')
        csv_write.writerow(all_keys)  # header
        for row in rows_as_dicts:
            temp = []
            for key in all_keys:
                temp.append(row.get(key))
            csv_write.writerow(temp)


if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    get_url_status(input_file, output_file)
