import os
import json
import shutil
import requests


def save_file_from_url(url, file_path):
    """
   Downloads a file using the given url to a specific location(file_path).
   If the file_path is invalid then a temp_file 
        is created and its path is returned.
   """

    if os.path.exists(file_path.replace(os.path.basename(file_path), '')):
        with open(file_path, 'wb') as file_writer:
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024, decode_unicode=False):
                file_writer.write(block)
            return file_path
    else:
        print "invalid file location"


def get_all_files_in_directory(directory):
    if os.path.exists(directory):
        all_files = []
        for path, subdirs, files in os.walk(directory):
            for sub_url in files:
                all_files.append(os.path.join(path, sub_url))
        return all_files
    else:
        print 'folder not found'

# lic_keys = ['license','distribute','distribution','proprietary','copyright']
lic_keys = ['1865']
def search_str_in_all_files(folder_loc):
    import re
    result_files = []
    for file in get_all_files_in_directory(folder_loc):
        with open(file, 'rb') as file_reader:
            lines = ''
            for line in file_reader:
                lines = lines + line
            for key in lic_keys:
                try:
                    if lines.lower().find(key.lower()) >= 0:
                        result_files.append(file)
                        break
                except:
                    pass
                
    fin_output = []
    for value in result_files:
        try:
            value = value.replace('/','\\')
            fin_output.append(value)
        except:
            pass
    return fin_output
search_patterns = [r'http://.{0,150}.xpi']
def search_pattern_in_all_files(folder_loc):
    import re
    result_files = []
    for file in get_all_files_in_directory(folder_loc):
        with open(file, 'rb') as file_reader:
            lines = ''
            for line in file_reader:
                lines = lines + line
            for key in search_patterns:
                try:
                    lines = lines.replace('\n', '')
                    if len(re.findall(key, lines.lower()))>0:
                        for value in re.findall(key, lines.lower()):
                            print value
                        result_files.append(file)
                except:
                    pass
                
    fin_output = []
    for value in result_files:
        try:
            value = value.replace('/','\\')
            fin_output.append(value)
        except:
            pass
    return fin_output


def get_json_data(location):
    with open(location, 'rb') as json_file:
        data = ''
        for line in json_file:
            data = data + line
    data = data.replace('data=', '')
    locations = []
    json_dump = json.dumps(data)
    json_data = json.loads(json_dump)
    for value in json.loads(json_data):
        if value['copyrights'] == [] and value['licenses'] == []:
            locations.append(value['location'])
    fin_locs = []
    for file_loc in locations:
        try:
            file_loc = file_loc.replace('/', '\\')
            fin_locs.append(file_loc)
        except:
            pass
    return fin_locs

def get_abs_paths(paths):
    output = []
    for path in paths:
        if os.path.exists(path):
            output.append(os.path.abspath(path))
    return output

def copy_filesto_directory(locations, directory):
    for location in locations:
        shutil.copy(location.replace('\\','/'), directory)

def get_100_chars(loc):
    all_lines = []
    loc = loc.replace('\\','/')
    with open(loc,'rb') as txt_file:
        for line in txt_file:
            all_lines.append(line.strip('/n'))
    txt = ''.join(all_lines)
    for key in lic_keys:
        try:
            print txt[txt.index(key)-200:txt.index(key)+300]
            print loc
            print '============================================================='
            break
        except:
            pass

#  
locations = get_all_files_in_directory('/home/rakesh/Documents/tempr/assign/venv.zip-extract')
print '========================'
for loc in locations:
    if 'manage.py' in loc:
        print loc