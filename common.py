import time

import bitly_api
import requests
from requests.adapters import HTTPAdapter

ACCESS_TOKEN = 'd3f2a7bf8e9590d4d6cace4631bc96b28c7022cb'
BROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36' \
             ' (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'


def get_short_url(url):
    bitly = bitly_api.Connection(access_token=ACCESS_TOKEN)
    data = bitly.shorten(url)
    return data['url']


def extract_HTML(url):
    headers = {'User-Agent': BROWSER_UA}
    s = requests.Session()
    s.mount(url, HTTPAdapter(max_retries=5))
    r = s.get(url, timeout=30, headers=headers)
    time.sleep(1)
    return r.text
