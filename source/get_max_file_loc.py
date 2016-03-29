import re


def get_max_loc(location, input_ext):
    all_exts = list(set(re.findall('\.\w+', location)))
    all = []
    for ext in all_exts:
        if ext == input_ext:
            all = re.findall('[a-zA-Z0-9/\\\]+'+ext, location)
    mx = 0
    for each in all:
        if mx <len(each):
            mx = len(each)
    return mx

example = 'dir/file/folder/name.jpeg \n \n dir/folder2/file1/folder1/name.jpeg \n dir/file/folder34/folder/name.png \n dir/file/folder34/folder/dir/file/folder34/folder/name.png \n dir/file/folder/folder4/name.jpeg'
print get_max_loc(example, '.png')