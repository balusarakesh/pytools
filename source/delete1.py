import json
import subprocess
import os
import re

requests = [
        {
         'url' : 'https://s3.amazonaws.com/scanapprakesh/test.txt',
         'location' : '/home/rakesh/Desktop/test.txt',
         'email' : 'rake@nexb.com',
         'status' : 'NOT STARTED'
         },
        {
         'url' : 'https://s3.amazonaws.com/scanapprakesh/test1.txt',
         'location' : '/home/rakesh/Desktop/test1.txt',
         'email' : 'rakes@nexb.com',
         'status' : 'NOT STARTED'
         }
        ]


def get_char_from_email(email):
    if email:
        return ''.join(re.findall('[a-zA-Z]*', email))


def create_temp_directory(dirname):
    try:
        if dirname[0] == '/':
            dirname = dirname[1:]
        location = os.path.join('/tmp/', dirname)
        if not os.path.exists(location):
            os.mkdir(location)
        return location
    except Exception, e:
        print str(e)


def run_scan_app(requests):
    if len(requests) > 0:
        for infos in requests:
            if infos['status'] == 'NOT STARTED':
                only_chars = get_char_from_email(infos['email'])
                temp_dir = create_temp_directory(only_chars)
                request_file = os.path.join(temp_dir, only_chars+'.json')
                infos['working_dir'] = temp_dir
                with open(request_file, 'wb') as json_file:
                    json.dump(infos, json_file)
                subprocess.Popen('python /home/rakesh/git/pytools/source/delete2.py ' + request_file, stdout=subprocess.PIPE, shell=True)

run_scan_app(requests)