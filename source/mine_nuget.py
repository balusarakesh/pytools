from bs4 import BeautifulSoup
import requests
import json
from spats import analyze_repodata
from commoncode.fileutils import parent_directory
from commoncode.fileutils import resource_name

def get_all_nuget_package_names(url):
    count = 2481
    all_sub_urls = []
    while url:
        print count
        html_data = requests.get(url + str(count)).content
        soup = BeautifulSoup(html_data, 'lxml')
        attribs = {'class':'package-list-header'}
        current_page_names = []
        for value in soup.find_all('header', attribs):
            soup1 = BeautifulSoup(str(value), 'lxml')
            current_page_names.append(soup1.a.attrs['href'])
        count = count + 1
        if current_page_names == []:
            break
        all_sub_urls = all_sub_urls + current_page_names
        print current_page_names
    return all_sub_urls

all_sub_urls = get_all_nuget_package_names('https://www.nuget.org/packages?page=')

def get_json_url(package_name):
    url = 'https://api.nuget.org/v3/registration1/package_name/index.json'
    package_name = package_name.lower()
    return url.replace('package_name/', package_name)


def collect_download_urls(url):
    html_data = requests.get(url).content
    soup = BeautifulSoup(html_data, 'lxml')
    sub_urls = []
    tbody = soup.find('tbody')
    tbody_soup = BeautifulSoup(str(tbody), 'lxml')
    for a_tag in tbody_soup.find_all('a'):
        a_tag_soup = BeautifulSoup(str(a_tag), 'lxml')
        sub_urls.append(a_tag_soup.a.attrs['href'])
    for url in sub_urls:
        print resource_name(url)
    return sub_urls


def get_all_json_urls(location):
    with open(location) as json_file:
        json_data_dict = json.load(json_file)
        all_json_urls = []
        for i in range(json_data_dict['count']):
            all_json_urls.append(json_data_dict['items'][i].get('@id'))
        return all_json_urls

def append_nuget_parent(sub_url):
    return 'https://www.nuget.org' + sub_url

for sub_url in all_sub_urls:
    pkg_url = append_nuget_parent(sub_url)
    collect_download_urls(pkg_url)
