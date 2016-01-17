import time

import Config
import Product
import unittest
import AmazonAPIManger

from BeautifulSoup import BeautifulSoup
from common import open_url


class ProductTest(unittest.TestCase):
    PRODUCT_GROUP = 'Shoes'
    KEYWORD = 'Boots'

    def setUp(self):
        self.api = AmazonAPIManger.AmazonAPIManger(Config.CONFIG).get_api()
        self.product_items = self.api.item_search(self.PRODUCT_GROUP, Keywords=self.KEYWORD)
        self.product_items = self.product_items.page(1)
        self.item = self.product_items.Items.Item
        self.browse_nodes = self.api.item_lookup(ItemId=self.item.ASIN, ResponseGroup='OfferListings,\
                                                                                      BrowseNodes,\
                                                                                      OfferSummary,\
                                                                                      Offers,\
                                                                                      Images')
        self.product = Product.Product(self.item, self.browse_nodes)

    def test_categories_sanity(self):
        our_categories = []
        categories = self.product.get_categories()
        node = self.browse_nodes.Items.Item.BrowseNodes.BrowseNode
        our_categories.append(str(node.Name))
        index = 1
        while hasattr(node, 'Ancestors') and index < 2 and \
                hasattr(node.Ancestors.BrowseNode, 'Name'):
            our_categories.append(node.Ancestors.BrowseNode.Name)
            node = node.Ancestors.BrowseNode
            index += 1

        our_categories = our_categories
        self.assertTrue(our_categories == categories)

    def test_review_sanity(self):
        review = self.product.get_review()
        five_stars_review_url = 'http://www.amazon.com/product-reviews/{0}/?ie=' \
                                'UTF8&filterBy=addFiveStar'.format(self.product.ASIN)

        html_text = open_url(five_stars_review_url).text
        soup = BeautifulSoup(html_text)
        all_reviews = soup.findAll("span", "a-size-base review-text")
        all_reviews = [review.text for review in all_reviews]
        all_reviews = sorted(all_reviews, key=lambda word: len(word), reverse=True)
        self.assertTrue(all_reviews[0], review)

    def test_img_url_sanity(self):
        our_url = self.browse_nodes.Items.Item.MediumImage.URL
        url = self.product.get_img_url()
        self.assertTrue(our_url == url)

    def test_price_sanity(self):
        price = self.product.get_price()
        node = self.browse_nodes.Items.Item.OfferSummary
        if hasattr(node, 'LowestNewPrice'):
            our_price = node.FormattedPrice

        else:
            html_text = open_url(self.product.page_url).text
            soup = BeautifulSoup(html_text)
            our_price = soup.findAll("span", id="priceblock_ourprice")[0].text

        self.assertTrue(our_price == price)

    def test_get_price(self):
        rating = self.product.get_rating()
        html_text = open_url(self.product.page_url).text
        soup = BeautifulSoup(html_text)
        our_rating = soup.findAll("div", id="avgRating")[0].span.a.span.text[:3]
        self.assertTrue(our_rating == rating)
