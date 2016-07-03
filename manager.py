import re
import config
from article_builder import ArticleBuilder
from keyword_extractor import KeywordExtractor
from product_searcher import ProductSearcher
from table_builder import TableBuilder
from wordpress_uploader import WordPressUploader


class Manager(object):
    MIN_PRODUCTS = 5

    def __init__(self):
        self.product_searcher = ProductSearcher(config.CONFIG)

    def _upload_article(self, keyword):
        """
        Get a keyword and uploads an article.
        :param keyword:
        """
        keyword, browse_node = re.findall('(.*)(?:\?bn=(\d+)?)', keyword)[0]
        products = self.product_searcher.search(config.PRODUCT_GROUP, keyword, browse_node=browse_node)
        if len(products) < self.MIN_PRODUCTS:
            return

        article_builder = ArticleBuilder(keyword, products)
        title = article_builder.get_title()
        table_builder = TableBuilder(title, config.URL, config.USER_NAME,
                                     config.PASSWORD)

        table_id = table_builder.build(products)
        wordpress_uploader = WordPressUploader(title, config.URL,
                                               config.USER_NAME, config.PASSWORD)

        content = article_builder.build(table_id)
        # Chose The size of the main image
        main_image_url = products[0].get_img_url('LargeImage')
        main_image_url = main_image_url if main_image_url != 'null' else products[0].get_img_url()
        categories = products[0].get_categories()
        wordpress_uploader.upload_article(content, main_image_url,
                                          article_builder.get_tags(), categories)

    def run(self):
        """
        Loops through the keywords, and uploads an article for each.
        """
        keywords = KeywordExtractor.extract(config.KEYWORDS_FILE_PATH)
        for keyword in keywords:
            self._upload_article(keyword)


if '__main__' == __name__:
    manager = Manager()
    manager.run()
