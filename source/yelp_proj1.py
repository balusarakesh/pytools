import requests


"""
class="rating-very-large"
class="arrange arrange--middle manage-following manage-following-add"
itemprop="description"
"""
from bs4 import BeautifulSoup
import re

def get_only_ratings_block(data):
    recc_index = str(data).find('<h2>Recommended Reviews')
    pagination_index = str(data).find('<div class="pagination-block">')
    return str(data)[recc_index:pagination_index]

def get_no_of_pages(url):
    data = requests.get(url).content
    pg_data =BeautifulSoup(data).find('div', class_='page-of-pages arrange_unit arrange_unit--fill').text
    return re.findall('of[\s]*[0-9]*',pg_data)[0].replace('of', '').replace(' ','')

def get_all_ratings_urls(url):
    
    try:
        all_ratings = []
        over_all = []
        count = 0
        out = get_no_of_pages(url)
        print out
        pg_count = int(out)
        print pg_count
        url = url + '?start='
        for i in range(pg_count):
            index = url.find('?start=')
            url = url[0:index]
            url = url + '?start=' + str(count)
            print url
            
            data = get_only_ratings_block(requests.get(url).content)
            ratings =  BeautifulSoup(data).find_all('div', class_='rating-very-large')
            over_all.append(BeautifulSoup(str(ratings[0])).findAll('i')[0].attrs['title'])
            ratings = ratings[1:]
            for rating in ratings:
                all_ratings.append(BeautifulSoup(str(rating)).findAll('i')[0].attrs['title'])
            count = count + 20
        return all_ratings
    except:
        return all_ratings
all = get_all_ratings_urls('http://www.yelp.com/biz/safeway-san-jose')
print len(all)