import unittest
from amazon_api_manger import AmazonAPIManger
from config import CONFIG
from product import Product
from product_searcher import ProductSearcher


class ProductSearcherTests(unittest.TestCase):
    MAX_RESULTS = 13
    def setUp(self):
        self.api = AmazonAPIManger(CONFIG).get_api()
        self.product_group = 'Shoes'
        self.keyword = 'Boots'
        self.seach = ProductSearcher(CONFIG)

    def test_search_sanity(self):
        our_products = []
        products = self.seach.search(self.product_group, self.keyword)
        our_products_item = self.api.item_search(self.product_group, Keywords=self.keyword)
        for index, item in enumerate(our_products_item):
            if index == self.MAX_RESULTS:
                break

            browse_nodes = self.api.item_lookup(ItemId=item.ASIN, ResponseGroup='OfferListings,\
                                                                                BrowseNodes,\
                                                                                OfferSummary,\
                                                                                Offers,\
                                                                                Images')
            product = Product(item, browse_nodes)
            if (product.get_img_url('SmallImage') == 'null') or \
                    (product.get_img_url('MediumImage') == 'null' and product.get_img_url('LargeImage') == 'null'):
                index -= 1
                continue

            if product.get_rating() == 'null' or \
                            product.get_review() == 'null' or product.get_price() == 'null':
                index -= 1
                continue

            our_products.append(product)

        products_ASIN = [product.ASIN for product in products]
        our_products_ASIN = [product.ASIN for product in our_products]
        products_ASIN.sort()
        our_products_ASIN.sort()
        self.assertTrue(products_ASIN == our_products_ASIN)



