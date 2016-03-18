#
# Copyright (c) 2014 by nexB, Inc. http://www.nexb.com/ - All rights reserved.
#


import requests
import url as urlpy

from bs4 import BeautifulSoup


ARCHIVE_EXTENSIONS = tuple('''.7z .7zip .apack .apk .apkg .app .ar .arc .arj
.bz2 .deb .dmg .ear .exe .gz .gzip .ipa .ipk .iso .jar .js .lz .lzma .lzo .lzw
.lzx .mpkg .pkg .rar .rpm .rpms .sar .shar .sit .sitx .srpm .tar .tar.bz2
.tar.gz .tarbz2 .tarz .tbz .tbz2 .tgz .ttf .txx .txz .tz .tz2 .tzar .tzf .tzg
.upk .war .xz .z .zip .zoo'''.split())


def validate_url(url):
    if urlpy.parse(url).absolute():
        if skip_ext(url) and check_special_char(url):
            return str(urlpy.parse(url).abspath())
    else:
        return None


skip_extensions = ['.html', '.mirrorlist', '.php', '.gz', 'xz', '.7z', '.7zip', '.apack', '.apk', '.apkg', '.app', '.ar', '.arc', '.arj', '.bz2', '.deb', '.dmg', '.ear', '.exe', '.gz', '.gzip', '.ipa', '.ipk', '.iso', '.jar', '.js', '.lz', '.lzma', '.lzo', '.lzw', '.lzx', '.mpkg', '.pkg', '.rar', '.sar', '.shar', '.sit', '.sitx', '.srpm', '.tar', '.tar', '.bz2', '.tar', '.gz', '.tarbz2', '.tarz', '.tbz', '.tbz2', '.tgz', '.ttf', '.txx', '.txz', '.tz', '.tz2', '.tzar', '.tzf', '.tzg', '.upk', '.war', '.xz', '.z', '.zip', '.zoo']
need_extensions = ['.rpm', 'repomd.xml']
special_characters = ['?', '=', '+', '%', '@', '#', '$', '!', '*', '(', ')', ':', ';', '"', "'"]


def skip_ext(url):
    for extension in skip_extensions:
        if url.endswith(extension):
            return False
    return True



def check_special_char(url):
    components = url.split('/')
    for character in special_characters:
        if character in components[-1]:
            return False
    return True

def check_ext(url):
    for extension in need_extensions:
        if url.endswith(extension):
            return True
        else:
            return False


def get_href_links(url):
    hrefs = []
#     print 'href : ' + url
    html_data = requests.get(url).content
    soup = BeautifulSoup(html_data, 'lxml')
    for value in soup.findAll('a'):
        try:
            href_url = value.attrs.get('href')
            validated_href = validate_url(href_url)
            if validated_href:
#                 if check_ext(validated_href):
#                     hrefs.append(validate_url(href_url))
                pass
            else:
                if validate_url(url + href_url):
                    print validate_url(url + href_url)
                    hrefs.append(validate_url(url + href_url))
        except:
            pass
#     print hrefs
#     print '$$$$$$$$'
#     print validate_urls(hrefs, url)
    try:
        i = hrefs.index(url)
        del hrefs[i]
    except:
        pass
    return hrefs


def get_all_hrefs2(url):
    try:
#         print url
        output = []
        if get_href_links(url) == []:
            return [url]
        else:
            for each_url in get_href_links(url):
                if check_ext(each_url):
#                     print each_url
                    output = output + [each_url]
                else:
                    output = output + get_all_hrefs2(each_url)
        return output
    except Exception, e:
        print str(e) + url

all_urls = get_all_hrefs2('http://mirrors.kernel.org/centos/')
print '============================================='
with open('C://doc//rpm_output.txt', 'wb') as write_file:
    for url in all_urls:
        write_file.write(url + '\n')
