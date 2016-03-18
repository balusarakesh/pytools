import csv
import hashlib
import os

from search_string_in_all_files import get_all_files_in_directory


def get_sha1sum(location):
    s = hashlib.sha1(open(location, 'rb').read())
    return s.hexdigest()

sha1_data = {}

# codebase must be a directory
codebase = '/home/rakesh/Desktop'
sha1_file = '/home/rakesh/Documents/doc/jenkins_project/sha1_data.csv'


def save_codebase(codebase, code_loc):
    if not os.path.exists(sha1_file):
        print "Scanning codebase for the first time... Bear with me it'll take a lot of time"
        with open(sha1_file, 'wb') as csv_file:
            csv_file.write('Empty for now')
        save_codebase(codebase, sha1_file)
    all_files = get_all_files_in_directory(codebase)
    for location in all_files:
        sha1_data[get_sha1sum(location)] = location
    with open(code_loc, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        csv_writer.writerow(['SHA1SUM','LOCATION'])
        for key, value in sha1_data.iteritems():
            csv_writer.writerow([key, value])


def check_codebase_sha(location):
    save_codebase(codebase, location)
    if get_sha1sum(sha1_file) != get_sha1sum(location):
        print 'You have changed something'
        save_codebase(codebase, sha1_file)
    else:
        print 'Same codebase'

check_codebase_sha('/home/rakesh/Documents/tempr/sha1.csv')