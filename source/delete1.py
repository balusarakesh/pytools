import hashlib
import json
import commands
import subprocess
import os
import time
import tempfile


emulatorList = [
        {
         'location' : '/home/rakesh/Desktop/test.txt',
         'email' : 'rake@nexb.com',
         'status' : 'NOT STARTED'
         },
        {
         'location' : '/home/rakesh/Desktop/test1.txt',
         'email' : 'rakes@nexb.com',
         'status' : 'NOT STARTED'
         }
        ]


def scan_in_sub_process(infos):
        location = infos['location']
        file_loc = os.path.dirname(location)
        full_name = location.replace(file_loc, '')
        no_ext = full_name.split('.')[-2]
        if no_ext.startswith('/'):
            no_ext = no_ext[1:]
        html_loc = os.path.join(file_loc, no_ext + '.html')
        process = subprocess.Popen("/home/rakesh/Documents/tempr/scan_app/scancode-toolkit-1.6.1/scancode --format=html-app --license "+location + " " + html_loc, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        print out
        if err:
            infos['status'] = 'ERROR'
        else:
            infos['status'] = 'FINISHED'
        print 'sub processes started'


if len(emulatorList) > 0:
    for infos in emulatorList:
        if infos['status'] == 'NOT STARTED':
            temp_file = '/tmp/' + infos['email']
            with open(temp_file, 'wb') as json_file:
                json.dump(infos, json_file)
            subprocess.Popen('python /home/rakesh/git/pytools/source/delete2.py ' + temp_file, stdout=subprocess.PIPE, shell=True)

