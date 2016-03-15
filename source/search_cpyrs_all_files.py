import os
import json
import combine_data_json
import shutil

def get_results(folder_loc):
    keys = ['copyright', '(c)']
    if os.path.exists(folder_loc):
        all_files = []
        result_files = []
        for path, subdirs, files in os.walk(folder_loc):
            for sub_url in files:
                if 'scancode-scan' not in path and 'scancode-scan' not in sub_url:
                    all_files.append(os.path.join(path, sub_url))
        for file in all_files:
            with open(file, 'rb') as file_reader:
                lines = ''
                for line in file_reader:
                    lines = lines + line
                for key in keys:
                    if lines.lower().find(key) >= 0:
                        result_files.append(file)
                        break
        print "all files : " + str(len(all_files))
        fin_output = []
        for value in result_files:
            try:
                value = value.replace('/', '\\')
                fin_output.append(value)
            except:
                pass
        return fin_output
    else:
        print 'folder not found'


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
        if value['copyrights'] == []:
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
        shutil.copy(location, directory)

location = 'C:\\Users\\nexB\\Desktop\\tempo\\doc'


data_jsons = combine_data_json.get_data_json('C:\\Users\\nexB\\Desktop\\tempo\\doc')

all_locs = []
for data_json in data_jsons:
    all_locs = all_locs + get_json_data(data_json)
all_locs = get_abs_paths(all_locs)

output = get_abs_paths(get_results(location))

replaced_outputs = []
for value in output:
    replaced_outputs.append(value.replace('C:\\Users\\nexB\\Desktop\\tempo\\doc', 'C:\\doc'))

print len(replaced_outputs)
set_output = set(replaced_outputs)
set_all_locs = set(all_locs)
result = []
for value in set_all_locs:
    if value in set_output:
        result.append(value)
results = []
for value in result:
    results.append(value.replace('C:\\doc', 'C:\\Users\\nexB\\Desktop\\tempo\\doc'))

copy_filesto_directory(results, 'C:\\doc\\multiprocessing_test')
