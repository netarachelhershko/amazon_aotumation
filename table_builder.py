import csv

from add_table_to_tablepress import AddTableToTablepress
from wordpress_xmlrpc import Client
from common import retry, get_short_url
from os import mkdir, path, makedirs


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
                fieldnames['Picture'] = self.IMG_FORMAT.format(get_short_url(product.page_url), product.get_img_url('SmallImage'))
                fieldnames['Name'] = product.title
                fieldnames['Rating'] = product.get_rating()
                fieldnames['Price'] = product.get_price()
                writer.writerow(fieldnames)

        return self._upload_table(full_path)

    def _upload_table(self, path):
        """
        :return: table id
        """
        with open(path) as f:
            content = f.read()

        return self.client.call(AddTableToTablepress(self.title, content))
