#
# Copyright (c) 2016 by nexB, Inc. http://www.nexb.com/ - All rights reserved.
#

from __future__ import absolute_import
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests

"""
Collects metadata from all the nuget packages.
Using the URLs "https://www.nuget.org/packages?page={page_number}" to
get package names. In these pages we can look for HTML tags namely
"header" with attributes "class" : "package-list-header".
A unique URL for every package is obtained.

To get the versions of a specific package we can use the URL
"https://www.nuget.org/packages/package_name" which
has all the versions available for a package.
"""


def collect_pkg_urls(url):
    '''
    Visits https://www.nuget.org/packages?page={page_number} and collects
    all the package URLs.
    starts with page number '0' and stops when there are no packages
    found in a page.
    '''
    count = 2580
    all_urls = []
    while url:
        html_data = requests.get(((url + str(count)))).content
        soup = BeautifulSoup(html_data, 'lxml')
        attribs = {'class': 'package-list-header'}
        current_page_urls = []
        for value in soup.find_all('header', attribs):
            soup1 = BeautifulSoup(str(value), 'lxml')
            pkg_name = soup1.a.attrs['href']
            pkg_url = 'https://www.nuget.org' + pkg_name
            current_page_urls.append(pkg_url)
        count = count + 1
        if current_page_urls == []:
            break
        all_urls = all_urls + current_page_urls
    return all_urls


def collect_download_urls(url):
    '''
    Visit the URL for a specific nuget package and return
    download URLs for all the versions of that package.
    '''
    html_data = requests.get((url)).content
    soup = BeautifulSoup(html_data, 'lxml')
    name_versions = []
#     links for packages are represented in 'tbody' attribute
    tbody_attr = soup.find('tbody')
    tbody_data = BeautifulSoup(str(tbody_attr), 'lxml')
    for a_tag in tbody_data.find_all('a'):
        a_tag_data = BeautifulSoup(str(a_tag), 'lxml')
        name_version = a_tag_data.a.attrs['href']
#     some pkg_url are in the format /packages/package_name/version
        if 'packages' not in name_version:
            print '&&&&&&&&&'
            print name_version
        name_versions.append(name_version)
    uris = []
    for url in name_versions:
        url = url[1:].replace('/', '.').lower()
        uris.append('https://api.nuget.org/packages/' + url+'.nupkg')
    return uris

for url in collect_pkg_urls('https://www.nuget.org/packages?page='):
    print collect_download_urls(url)
