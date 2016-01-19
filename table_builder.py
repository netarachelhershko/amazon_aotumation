import csv

from add_table_to_tablepress import AddTableToTablepress
from wordpress_xmlrpc import Client
from common import retry
from os import mkdir, listdir, path


class TableBuilder(object):
    IMG_FORMAT = '<a target="_blank" rel="nofollow" href="http://amzn.to/1F9ASJc"><img src={0} /></a>'
    TABLE_PATH = r'article.csv'
    ARTICLES_DIR = r'articles'

    def __init__(self, title, url, user_name, password):
        self.fieldnames_list = ['Picture', 'Name', 'Rating', 'Price']
        self.client = retry(Client, url, user_name, password)
        self.title = title
        if self.ARTICLES_DIR not in listdir('.'):
            mkdir(self.ARTICLES_DIR)

        self.article_dir = path.join(self.ARTICLES_DIR, title)
        if self.title not in listdir(self.ARTICLES_DIR):
            mkdir(self.article_dir)

    def build(self, products):
        fieldnames = {}
        full_path = path.join(self.article_dir, self.TABLE_PATH)
        with open(full_path, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames_list)
            writer.writeheader()
            for product in products:
                fieldnames['Picture'] = self.IMG_FORMAT.format(product.get_img_url('SmallImage'))
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
