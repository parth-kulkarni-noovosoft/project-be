import requests
import json 
from extractors.extractors import Extractor

from pprint import pprint

extractor = Extractor()

URLS = []
REVIEWS = []
LIMIT = 5

def scrape_page_data(url):    
    headers = {
        'authority': 'www.amazon.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }

    print(f"Downloading {url}")

    r = requests.get(url, headers=headers)

    if r.status_code > 500:
        print("Request has been blocked by Amazon. Please try again")
        return None
    return r.text

def get_product_urls():
    return open("urls.txt",'r').readlines()

def fetch_data(url):
    global URLS
    data = scrape_page_data(url)
    json_data = extractor.amazon(data)
    if 'next_link' in json_data:
        URLS.append(json_data['next_link'])
    return json_data

def store_data(data):
    global REVIEWS
    REVIEWS += data['reviews']

def fetch_and_save_data(url):
    d = fetch_data(url)
    store_data(d)

def save_data():
    with open('data.json', 'w') as outfile:
        json.dump(REVIEWS, outfile)

if __name__ == '__main__':
    URLS.append(*get_product_urls())
    count = 0
    for url in URLS:
        print(count)
        if count >= LIMIT:
            break

        fetch_and_save_data(url)
        count += 1
    save_data()