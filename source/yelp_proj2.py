from bs4 import BeautifulSoup
import json

LOCATIONS = ['San Jose']
PLACES = ['Restaurants']


def replace_sp_with_plus(input):
    output = []
    for each in input:
        try:
            if ' ' in each:
                output.append(each.replace(' ', '+'))
            else:
                output.append(each)
        except Exception, e:
            print str(e)
    return output


def get_urls(LOCATIONS, PLACES):
    LOCATIONS = replace_sp_with_plus(LOCATIONS)
    PLACES = replace_sp_with_plus(PLACES)
    urls = []
    for location in LOCATIONS:
        for place in PLACES:
            urls.append('http://www.yelp.com/search?find_desc=' + place + '&find_loc=' + location)
    return urls
