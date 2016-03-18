#
# Copyright (c) 2016 by nexB, Inc. http://www.nexb.com/ - All rights reserved.
#

from __future__ import absolute_import
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import json
import requests


"""
Collects metadata from all the nuget packages.
Using the URLs "https://www.nuget.org/packages?page={page_number}" to
get package names. In these pages we can look for HTML tags namely
"header" with attributes "class" : "package-list-header".
A unique URL for every package is obtained.

To get the versions of a specific package we can use the URL
"https://api.nuget.org/v3/registration1/package_name/index.json" which
has most of the metadata we need to create and download package.
"""


def del_empty_value(input):
    output = []
    for value in input:
        if value != '':
            output.append(value)
    return output


# all_sub_urls = collect_pkg_names('https://www.nuget.org/packages?page=')


def get_json_url(package_name):
    '''
    Return the URL with metadata for given nuget package name.
    '''
    url = 'https://api.nuget.org/v3/registration1/package_name/index.json'
    package_name = package_name.lower()
    return url.replace('package_name', package_name)


# def collect_download_urls(api_urls):
#     '''
#     Yield a download URL for all the nuget packages.
#     'api_urls' - list of all the URLs with metadata
#     like - https://api.nuget.org/v3/registration1/package_name/index.json
#     '''
#     for url in api_urls:
#         try:
#             data = json.loads(requests.get(url).content)
#             pkg_count = data['items'][0]['count']
#             pkgs = data['items'][0]['items']
#             for i in range(pkg_count):
# #                 print pkgs[i]['packageContent']
#                 continue
#         except Exception, e:
#             print url
#             print str(e)


def get_all_json_urls(location):
    with open(location) as json_file:
        json_data_dict = json.load(json_file)
        all_json_urls = []
        for i in range(json_data_dict['count']):
            all_json_urls.append(json_data_dict['items'][i].get('@id'))
        return all_json_urls


def append_nuget_parent(sub_url):
    return 'https://www.nuget.org' + sub_url
# # 
# # for sub_url in all_sub_urls:
# #     pkg_url = append_nuget_parent(sub_url)
# #     collect_download_urls(pkg_url)
# json_urls = []
# for name in all_sub_urls:
#     json_urls.append(get_json_url(name))
# collect_download_urls(json_urls)


def collect_download_urls(url):
    '''
    Visit the URL for a specific nuget package and return
    download URLs for all the versions of that package.
    '''
    html_data = requests.get(url).content
    soup = BeautifulSoup(html_data, 'lxml')
    sub_urls = []
    tbody = soup.find('tbody')
    tbody_soup = BeautifulSoup(str(tbody), 'lxml')
    for a_tag in tbody_soup.find_all('a'):
        a_tag_soup = BeautifulSoup(str(a_tag), 'lxml')
        pkg_url = a_tag_soup.a.attrs['href']
#     some packages are in the format /packages/package_name/version
        if 'packages' in pkg_url:
            pkg_url = pkg_url.replace('/packages', '')
        sub_urls.append(pkg_url)
    uris = []
    for url in sub_urls:
        url = url[1:].replace('/', '.').lower()
        uris.append('https://api.nuget.org/packages/' + url+'.nupkg')
    return uris


def collect_pkg_names(url):
    '''
    Visits https://www.nuget.org/packages?page={page_number} and collects
    all the package names.
    '''
    count = 0
    all_names = []
    while url:
        html_data = requests.get((url + str(count))).content
        soup = BeautifulSoup(html_data, 'lxml')
        attribs = {'class': 'package-list-header'}
        current_page_names = []
        for value in soup.find_all('header', attribs):
            soup1 = BeautifulSoup(str(value), 'lxml')
            pkg_name = soup1.a.attrs['href']
            pkg_url = 'https://www.nuget.org' + pkg_name
            current_page_names.append(pkg_url)
        count = count + 1
        print current_page_names
        if current_page_names == []:
            break
        all_names = all_names + current_page_names
    return all_names
collect_pkg_names('https://www.nuget.org/packages?page=')