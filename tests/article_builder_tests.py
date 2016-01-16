import unittest
import common
from ArticleBuilder import ArticleBuilder
from ProductSearcher import ProductSearcher

PRODUCT_GROUP = 'Shoes'
ALIGNRIGTH = 'alignrigth'

TABLE_FORMAT = '[table id={0} /]'
REVIEW_FORMAT = '<em><strong>Testimonial:</strong></em> <blockquote><em>{0}</em></blockquote>'
IMG_FORMAT = '<a href="{0}" target="_blank" rel="nofollow"><img class="{1}" src="{2}" alt="{3}" width="300" height="187" /></a></h3>'
TITLE_FORMAT = '<h3><a href={0} target="_blank" rel="nofollow">{1}</a></h3>'
PRODUCT_FORMAT = '{0} {1} {2} &nbsp; &nbsp; &nbsp;'


class ArticleBuilderTests(unittest.TestCase):
    def setUp(self):
        self.keyword = 'boots'
        self.article_builder = ArticleBuilder(self.keyword)
        self.product_searcher = ProductSearcher()

    def test_title_sanity(self):
        our_title = "The Best {0}".format(self.keyword.title())
        title = self.article_builder.get_title()
        self.assertTrue(title == our_title)

    def test_build_sanity(self):
        table_id = 5
        products = self.product_searcher.search(PRODUCT_GROUP, self.keyword)
        article = self.article_builder.build(products, table_id)
        our_article = TABLE_FORMAT.format(table_id)

        for index, product in enumerate(products):
            sorten_url = common.get_short_url(product.page_url)
            alignment = ALIGNLEFT if index % 2 == 0 else ALIGNRIGTH
            title = TITLE_FORMAT.format(sorten_url, product.title)
            img = IMG_FORMAT.format(sorten_url, alignment, product.get_img_url('LargeImage'), product.title)
            review = REVIEW_FORMAT.format(product.get_review())
            our_article += PRODUCT_FORMAT.format(title, img, review)

        self.assertTrue(our_article == article)
