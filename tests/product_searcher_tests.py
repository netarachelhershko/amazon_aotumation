import unittest

import Product
import ProductSearcher
import AmazonAPIManger


class ProductSearcherTests(unittest.TestCase):
    def setUp(self):
        self.api = AmazonAPIManger.AmazonAPIManger().get_api()
        self.product_group = 'Shoes'
        self.keyword = 'Boots'
        self.seach = ProductSearcher.ProductSearcher()

    def test_search_sanity(self):
        our_products = []
        products = self.seach.search(self.product_group, self.keyword)
        our_products_item = self.api.item_search(self.product_group, Keywords=self.keyword)
        for index, item in enumerate(our_products_item):
            browse_nodes = self.api.item_lookup(ItemId=item.ASIN, ResponseGroup='OfferListings,'
                                                                                'BrowseNodes,'
                                                                                'OfferSummary,'
                                                                                'Offers')
            our_products.append(Product.Product(item, browse_nodes))
            if index == 12:
                break

        products_ASIN = [product.ASIN for product in products]
        our_products_ASIN = [product.ASIN for product in our_products]
        products_ASIN.sort()
        our_products_ASIN.sort()
        self.assertTrue(products_ASIN == our_products_ASIN)


