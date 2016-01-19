import unittest
import csv

from table_builder import TableBuilder
from product_searcher import ProductSearcher
from os import path
from config import URL,USER_NAME,PASSWORD, CONFIG


class TableBuilderTests(unittest.TestCase):
    TITLE = 'title'
    TABLE_PATH = r'article.csv'
    OUR_TABLE_PATH = r'articles\{0}\article2.csv'
    IMG_FORMAT = '<a target="_blank" rel="nofollow" href="http://amzn.to/1F9ASJc"><img src={0} /></a>'

    def setUp(self):
        self.product_group = 'Shoes'
        self.keyword = 'Boots'
        self.seach = ProductSearcher(CONFIG)
        self.table_builder = TableBuilder(self.TITLE, URL, USER_NAME, PASSWORD)
        self.article_dir = self.table_builder.article_dir

    def test_build_sanity(self):
        products = self.seach.search(self.product_group, self.keyword)
        fieldnames = {}
        self.table_builder.build(products)
        our_table_path = self.OUR_TABLE_PATH.format(self.TITLE)
        with open(our_table_path, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.table_builder.fieldnames_list)
            writer.writeheader()
            for product in products:
                fieldnames['Picture'] = self.IMG_FORMAT.format(product.get_img_url('SmallImage'))
                fieldnames['Name'] = product.title
                fieldnames['Rating'] = product.get_rating()
                fieldnames['Price'] = product.get_price()
                writer.writerow(fieldnames)

        with open(path.join(self.article_dir, self.TABLE_PATH)) as f:
            content = f.read()

        with open(our_table_path) as f:
            out_content = f.read()

        self.assertTrue(content == out_content)
