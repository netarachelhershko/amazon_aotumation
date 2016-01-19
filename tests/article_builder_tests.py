import unittest

import config
import common
from article_builder import ArticleBuilder
from product_searcher import ProductSearcher

TABLE_FORMAT = '[table id={0} /]'
REVIEW_FORMAT = '<em><strong>Testimonial:</strong></em> <blockquote><em>{0}</em></blockquote>'
IMG_FORMAT = '<a href="{0}" target="_blank" rel="nofollow"><img class="{1}" src="{2}" alt="{3}" width="300" height="187" /></a></h3>'
TITLE_FORMAT = '<h3><a href={0} target="_blank" rel="nofollow">{1}</a></h3>'
PRODUCT_FORMAT = '{0} {1} {2} &nbsp; &nbsp; &nbsp;'
CLASS_FORMAT = "{0} wp-image-785 size-medium"


class ArticleBuilderTests(unittest.TestCase):
    def setUp(self):
        self.keyword = 'boots'
        self.product_searcher = ProductSearcher(config.CONFIG)
        self.products = self.product_searcher.search(config.PRODUCT_GROUP, self.keyword)
        self.article_builder = ArticleBuilder(self.keyword, self.products)

    def test_title_sanity(self):
        our_title = "The Best {0}".format(self.keyword.title())
        title = self.article_builder.get_title()
        self.assertTrue(title == our_title)

    def test_get_tags_sanity(self):
        our_tags = []
        for product in self.products:
            if product.manufacturer != 'null':
                our_tags.append(product.manufacturer)

        tags = self.article_builder.get_tags()
        self.assertTrue(tags == list(set(our_tags)))

    def test_build_sanity(self):
        table_id = 5
        article = self.article_builder.build(table_id)
        our_article = TABLE_FORMAT.format(table_id)

        for index, product in enumerate(self.products):
            sorten_url = common.get_short_url(product.page_url)
            alignment = CLASS_FORMAT.format('alignleft' if index % 2 == 0 else 'alignright')
            title = TITLE_FORMAT.format(sorten_url, product.title)
            img = IMG_FORMAT.format(sorten_url, alignment, product.get_img_url('LargeImage'), product.title)
            review = REVIEW_FORMAT.format(product.get_review())
            our_article += PRODUCT_FORMAT.format(title, img, review)

        self.assertTrue(our_article == article)
