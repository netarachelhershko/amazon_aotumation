import time
import requests
import bitly_api
import tldextract
from config import URL
from requests.adapters import HTTPAdapter


BITLY_ACCESS_TOKEN = 'd3f2a7bf8e9590d4d6cace4631bc96b28c7022cb'
BROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36' \
             ' (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'


def get_short_url(url):
    """
    :param url: Full url.
    :return: Shorten url.
    """
    bitly = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)
    return bitly.shorten(url)['url']


def open_url(url):
    """
    :param url: url
    :return: Request's response object.
    """
    headers = {'User-Agent': BROWSER_UA}
    s = requests.Session()
    s.mount(url, HTTPAdapter(max_retries=5))
    r = s.get(url, timeout=30, headers=headers)
    time.sleep(1)
    return r


# noinspection PyBroadException
def retry(func, *args):
    """
    Takes a function and its args, and tries to call it several times.
    :param func: any function.
    :param args: the args of your function.
    :return:
    """
    for _ in xrange(5):
        try:
            return func(*args)
        except:
            time.sleep(1)


def get_internal_url_redirect(short_url, product_title):
    domain = tldextract.extract(URL).registered_domain
    shorten_id = short_url.split('/')[1]
    dashed_title = '-'.join(product_title.lower().split())
    internal_url = 'http://{domain}/{dashed_title}/get_product/{shorten_id}'.format(
                    domain=domain, dashed_title=dashed_title, shorten_id=shorten_id)
    return internal_url