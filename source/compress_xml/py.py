from search_string_in_all_files import search_str_in_all_files,\
    get_all_files_in_directory
import re


def compress_other_xml(other_xml):
    lines = []
    with open(other_xml, 'rb') as xml_file:
        for line in xml_file:
            lines.append(line.strip('\n'))
        lines = ''.join(lines)
    xml_tag = re.findall('<\?.+\?>', lines)
    other_open = re.findall('\<otherdata .+?"\>', lines)
    packages = re.findall('\<package pkgid=.+?\</package\>', lines, re.MULTILINE)
    with open(other_xml, 'wb') as xml_file:
        xml_file.write(xml_tag[0])
        xml_file.write(other_open[0])
        xml_file.write(''.join(packages[:3]))
        xml_file.write('</otherdata>')
# compress_other_xml('/home/rakesh/git/minecode-53-repomd-parser/discovery/tests/testfiles/repodata_rpms/repodata/pgpool_redhat/other2.xml')


def compress_primary_xml(primary_xml):
    lines = []
    with open(primary_xml, 'rb') as xml_file:
        for line in xml_file:
            lines.append(line.strip('\n'))
        lines = ''.join(lines)
    xml_tag = re.findall('<\?.+\?>', lines)
    metadata = re.findall('\<metadata .+?\>', lines)
    packages = re.findall('\<package type=.+?\</package\>', lines, re.MULTILINE)
    with open(primary_xml, 'wb') as xml_file:
        xml_file.write(xml_tag[0])
        xml_file.write(metadata[0])
        xml_file.write(''.join(packages[:3]))
        xml_file.write('</metadata>')


def compress_filelists_xml(filelists_xml):
    lines = []
    with open(filelists_xml, 'rb') as xml_file:
        for line in xml_file:
            lines.append(line.strip('\n'))
        lines = ''.join(lines)
    xml_tag = re.findall('<\?.+\?>', lines)
    metadata = re.findall('\<filelists .+?\>', lines)
    packages = re.findall('\<package pkgid=.+?\</package\>', lines, re.MULTILINE)
    with open(filelists_xml, 'wb') as xml_file:
        xml_file.write(xml_tag[0])
        xml_file.write(metadata[0])
        xml_file.write(''.join(packages[:3]))
        xml_file.write('</filelists>')

for name in get_all_files_in_directory('/home/rakesh/Documents/tempr/delete/redhat'):
    if 'other.xml' in name.split('/')[-1]:
        compress_other_xml(name)
    if 'filelists.xml' in name.split('/')[-1]:
        compress_filelists_xml(name)
    if 'primary.xml' in name.split('/')[-1]:
        compress_primary_xml(name)