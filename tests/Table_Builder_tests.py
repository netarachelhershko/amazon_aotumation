import unittest
import csv

from TableBuilder import TableBuilder
from ProductSearcher import ProductSearcher

TABLE_PATH = r'article.csv'
OUR_TABLE_PATH = r'article2.csv'


class TableBuilderTests(unittest.TestCase):
    def setUp(self):
        self.fieldnames_list = ['Picture', 'Name', 'Rating','Price']
        self.fieldnames = {'Picture': '',
                           'Name': '',
                           'Rating': '',
                           'Price': ''}

        self.product_group = 'Shoes'
        self.keyword = 'Boots'
        self.seach = ProductSearcher()
        self.table = TableBuilder()

    def test_build_sanity(self):
        products = self.seach.search(self.product_group, self.keyword)
        self.table.build(products)
        with open(OUR_TABLE_PATH,'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames_list)
            writer.writeheader()
            for product in products:
                self.fieldnames['Picture'] = product.get_img_url('SmallImage')
                self.fieldnames['Name'] = product.title
                self.fieldnames['Rating'] = product.get_rating()
                self.fieldnames['Price'] = product.get_price()
                writer.writerow(self.fieldnames)

        with open(TABLE_PATH) as f:
            content = f.read()

        with open(OUR_TABLE_PATH) as f:
            out_content = f.read()

        self.assertTrue(content == out_content)
