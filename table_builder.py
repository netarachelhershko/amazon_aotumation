import csv
from wordpress_xmlrpc import Client
from os import mkdir, path, makedirs

from config import INTERNAL_REDIRECT_SHORTEN_URLS
from add_table_to_tablepress import AddTableToTablepress
from common import retry, get_short_url, get_internal_url_redirect


class TableBuilder(object):
    IMG_FORMAT = '<a target="_blank" rel="nofollow" href="{}"><img src={} /></a>'
    TABLE_PATH = r'article.csv'
    ARTICLES_DIR = r'articles'

    def __init__(self, title, url, user_name, password):
        self.fieldnames_list = ['Picture', 'Name', 'Rating', 'Price']
        self.client = retry(Client, url, user_name, password)
        self.title = title
        self.article_dir = path.join(self.ARTICLES_DIR, title)
        if not path.isdir(self.ARTICLES_DIR):
            makedirs(self.article_dir)

        if not path.isdir(self.article_dir):
            mkdir(self.article_dir)

    def build(self, products):
        full_path = path.join(self.article_dir, self.TABLE_PATH)
        with open(full_path, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames_list)
            writer.writeheader()
            fieldnames = {}
            for product in products:
                product_url = get_short_url(product.page_url)
                product_url = get_internal_url_redirect(product_url, product.title) if INTERNAL_REDIRECT_SHORTEN_URLS else product_url
                fieldnames['Picture'] = self.IMG_FORMAT.format(product_url,
                                                               product.get_img_url('SmallImage'))
                fieldnames['Name'] = product.title
                fieldnames['Rating'] = product.get_rating()
                fieldnames['Price'] = product.get_price()
                writer.writerow(fieldnames)

        return self._upload_table(full_path)

    def _upload_table(self, table_path):
        """
        :return: table id
        """
        with open(table_path) as f:
            content = f.read()

        return self.client.call(AddTableToTablepress(self.title, content))
