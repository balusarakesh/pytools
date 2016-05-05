from collections import OrderedDict
import unittest
from search_string_in_all_files import search_str_in_all_files
import os
from zipfile import ZipFile
import subprocess
import tempfile


# for name in search_str_in_all_files('/home/rakesh/git/scancode-toolkit', ['to_primitive']):
#     if '.git' not in name and 'python2.7' not in name and 'thirdparty' not in name and '.pyc' not in name:
#         print name


def create_temp_directory(dirname):
    if '/' in dirname:
        dirname = dirname.replace('/', '') + '_dir'
    try:
        location = os.path.join('/tmp/', dirname)
        os.mkdir(location)
        return location
    except:
        print 'unable to create directory'


def create_zip_file(input, zip_name):
    with ZipFile(zip_name, 'w') as zip_file:
        for full_loc in input:
            if os.path.exists(full_loc):
                if full_loc.endswith('/'):
                    full_loc = full_loc[:len(full_loc)-2]
                full_loc = full_loc.replace(os.path.dirname(full_loc), '')
                zip_file.write(full_loc)
        zip_file.close()


def return_results(message, results=None):
    create_temp_directory()
    create_zip_file(results)
    pass


def scan_in_sub_process(json_file):
    import json
    infos = json.loads(open(json_file, 'rb').read())
    location = infos['location']

    file_loc = os.path.dirname(location)
    full_name = location.replace(file_loc, '')
    no_ext = full_name.split('.')[-2]
    if no_ext.startswith('/'):
        no_ext = no_ext[1:]
    html_loc = os.path.join(file_loc, no_ext + '.html')

    process = subprocess.Popen("/home/rakesh/Documents/tempr/scan_app/scancode-toolkit-1.6.1/scancode --format=html-app --license "+location + " " + html_loc, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if err:
        return_results('ERROR')
    else:
        return_results('FINISHED', html_loc)


import sys
infos = sys.argv[1]
scan_in_sub_process(infos)
