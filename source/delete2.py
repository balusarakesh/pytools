import json
import sys
import commands
import unittest
import os
from zipfile import ZipFile
import subprocess
import re
import shutil
from __builtin__ import True

# for name in search_str_in_all_files('/home/rakesh/git/scancode-toolkit', ['to_primitive']):
#     if '.git' not in name and 'python2.7' not in name and 'thirdparty' not in name and '.pyc' not in name:
#         print name


SCANCODE_LOC = '/home/rakesh/Documents/tempr/scan_app/scancode-toolkit-1.6.1/'


def get_char_from_email(email):
    if email:
        return ''.join(re.findall('[a-zA-Z]*', email))


def create_temp_directory(dirname):
    if '/' in dirname:
        dirname = dirname.replace('/', '') + '_dir'
    try:
        location = os.path.join('/tmp', dirname)
        if not os.path.exists(location):
            os.mkdir(location)
        return location
    except Exception, e:
        print str(e)


def create_zip_file(dirname, zip_name):
    if dirname and zip_name:
        shutil.make_archive(os.path.join('/tmp/', zip_name), 'zip', dirname)


def delete_directory(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def return_results(infos, message, working_dir):
    if working_dir:
        zip_name = get_char_from_email(infos['email'])
        try:
            create_zip_file(working_dir, zip_name)
            delete_directory(working_dir)
        except Exception, e:
            print str(e)
            print 'Error while compressing'
        return os.path.join('/tmp/', zip_name + '.zip')

def get_file_name(location):
    file_loc = os.path.dirname(location)
    name = location.replace(file_loc, '')
    return name


def get_file_name_with_no_ext(name):
    no_ext = name.split('.')[-2]
    if no_ext.startswith('/'):
        no_ext = no_ext[1:]
    return no_ext


def configure_scancode(scancode_loc):
    result = commands.getstatusoutput(scancode_loc + 'scancode --help')
    try:
        if result:
            return True
    except:
        return


def scan_in_sub_process(json_file):
    infos = json.loads(open(json_file, 'rb').read())
    os.remove(json_file)
    location = infos['location']
    working_dir = infos['working_dir']
    full_name = get_file_name(location)

    html_loc = os.path.join(working_dir, get_file_name_with_no_ext(full_name) + '.html')
    if configure_scancode(SCANCODE_LOC):
        process = subprocess.Popen(SCANCODE_LOC + 'scancode --format=html-app --license '+location + ' ' + html_loc, stdout=subprocess.PIPE, shell=True)
    else:
        print 'Scancode configuration error'
    out, err = process.communicate()
    if err:
        return_results(infos, 'ERROR')
    else:
        return_results(infos, 'FINISHED', working_dir)


infos = sys.argv[1]
scan_in_sub_process(infos)
