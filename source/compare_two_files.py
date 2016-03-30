def compare_2_files(location1, location2):
    lines1 = []
    lines2 = []
    with open(location1, 'rb') as txt_file1:
        for line in txt_file1:
            lines1.append(line.strip())
    with open(location2, 'rb') as txt_file2:
        for line in txt_file2:
            lines2.append(line.strip())
    print 'lines in file1 but not in file2'
    print '========='
    for line in lines1:
        if line not in lines2:
            print line
    print 'lines in file2 but not in file1'
    print '========='
    for line in lines2:
        if line not in lines1:
            print line

compare_2_files('/home/rakesh/Desktop/test1.txt', '/home/rakesh/Desktop/test2.txt')