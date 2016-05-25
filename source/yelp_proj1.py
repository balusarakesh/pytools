import json
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
    data = get_text_from_url(url)
    pg_data = BeautifulSoup(data, 'lxml').find('div', class_='page-of-pages arrange_unit arrange_unit--fill').text
    return re.findall('of[\s]*[0-9]*',pg_data)[0].replace('of', '').replace(' ','')


def get_all_pgs_infos(url):
    try:
        infos = []
        count = 0
        out = get_no_of_pages(url)
        pg_count = int(out)
        url = url + '?start='
        for i in range(pg_count):
            index = url.find('?start=')
            url = url[0:index]
            url = url + '?start=' + str(count)
            current_pg_infos = get_infos(get_text_from_url(url))
            infos = infos + current_pg_infos
            count = count + 20
        return infos
    except Exception, e:
        print str(e)


def get_user_review_description(review_data):
    return BeautifulSoup(str(review_data), 'lxml').find('p', itemprop='description').text


def get_user_rating(review_data):
    rating_div = BeautifulSoup(str(review_data), 'lxml').find('div', class_='rating-very-large')
    return BeautifulSoup(str(rating_div), 'lxml').find('i').attrs['title']


def get_user_name(review_data):
    user_li = BeautifulSoup(str(review_data), 'lxml').find('li', class_='user-name')
    return BeautifulSoup(str(user_li), 'lxml').find('a').text


def get_infos(data):
    """
    class="review review--with-sidebar"
    """
    try:
        infos = []
        for review in BeautifulSoup(str(data), 'lxml').findAll('div', class_='review review--with-sidebar'):
            tmp = {}
            user_li = BeautifulSoup(str(review), 'lxml').find('li', class_='user-name')
            tmp['name'] = BeautifulSoup(str(user_li), 'lxml').find('a').text
            rating_div = BeautifulSoup(str(review), 'lxml').find('div', class_='rating-very-large')
            tmp['rating'] = BeautifulSoup(str(rating_div), 'lxml').find('i').attrs['title']
            tmp['review'] = BeautifulSoup(str(review), 'lxml').find('p', itemprop='description').text
            infos.append(tmp)
        return infos
    except Exception, e:
        print str(e) 
        return []
    pass


def get_text_from_url(url):
    try:
        return str(requests.get(url).content)
    except Exception, e:
        print str(e)


# infos = get_all_pgs_infos('http://www.yelp.com/biz/signature-print-services-san-jose')

# json.dump(infos, open('/home/rakesh/Desktop/json_user_data.json', 'wb'))

