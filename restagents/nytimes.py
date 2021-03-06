import sys, rest
from config_helper import *
from printing_helper import *

def build_url(keyword):
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=[KEYWORD]&begin_date=[TODAY]&api-key=[MYKEY]"
    url=url.replace('[KEYWORD]', keyword)
    url=url.replace('[TODAY]', todays_date_iso().replace('-',''))
    url=url.replace('[MYKEY]', get_api_item('nytimes','key'))
    return url

def get_headlines():
    url = "http://api.nytimes.com/svc/topstories/v1/home.json?api-key=[MYKEY]"
    url=url.replace('[MYKEY]', get_api_item('nytimes','topstories'))
    results = rest.get(url)['results']
    hits = {}
    for result in results:
        hits[result['title']]=result['url']
    return hits

def get_stories(keyword):
    if keyword == "headlines":
        return get_headlines()
    hits = {}
    url = build_url(keyword)
    results = rest.get(url)['response']['docs']
    for story in results:
        if story['type_of_material']=='News':
            hits[story['headline']['main']] = story['web_url']
    return hits

def main():
    print_title_link_pairs(get_stories(raw_input('What are you searching for:\t')))

if __name__=="__main__":
    main()
