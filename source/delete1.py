import requests
import csv
import tempfile

def save_file_from_urls(input,location):
    for url in input:
        try:
            file_name = url.split('/')[-1]
            response = requests.get(url)
            tmp = tempfile.TemporaryFile(mode='wb',
                                          prefix=file_name.replace('.jar',''),
                                          suffix='.jar'
                                          )
            tmp.write(response.content)
            print tmp.name
        except Exception,e:
            print str(e)
            print url
name_ver = []
with open('/home/rakesh/Documents/tempr/comp_name_versions.csv','rb')as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        if row[1] == '(nv)':
            name_ver.append(row[0]+' '+row[1])
        else:
            name_ver.append(row[0]+row[1].replace('v',''))
results = []
secure = []
with open('/home/rakesh/Documents/tempr/securesphere_comp.txt','rb') as txt_file1:
    all_lines1 = []
    for line in txt_file1:
        secure.append(line.strip())
secure = ''.join(secure)
with open('/home/rakesh/Documents/tempr/counterbreach_comp.txt','rb') as txt_file:
    all_lines = [] 
    for line in txt_file:
        all_lines.append(line.strip())
    lines = ''.join(all_lines)
    for name in name_ver:
        if lines.lower().find(name.lower())<0:
            results.append(name)

results.sort()
for name in results:
    if name.lower() not in secure.lower():
        print name
