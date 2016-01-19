import config
from article_builder import ArticleBuilder
from keyword_extractor import KeywordExtractor
from product_searcher import ProductSearcher
from table_builder import TableBuilder
from word_press_uploader import WordPressUploader


class Manager(object):
    MIN_PRODUCTS = 8
    def __init__(self):
        self.searcher = ProductSearcher(config.CONFIG)
        self.table_builder = TableBuilder()

    def _upload_article(self, keyword):
        """
        Get a keyword and uploads an article.
        :param keyword:
        """
        products = self.searcher.search(config.PRODUCT_GROUP, keyword)
        if len(products) < self.MIN_PRODUCTS:
            return

        self.table_builder.build(products)

        article_builder = ArticleBuilder(keyword, products)
        title = article_builder.get_title()
        wordpress_uploader = WordPressUploader(title, config.URL,
                                               config.USER_NAME, config.PASSWORD)

        table_id = wordpress_uploader.upload_table()
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
