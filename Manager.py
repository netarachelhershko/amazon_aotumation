import Config
from ArticleBuilder import ArticleBuilder
from KeywordExtractor import KeywordExtractor
from ProductSearcher import ProductSearcher
from TableBuilder import TableBuilder
from WordPressUploader import WordPressUploader


class Manager(object):
    def __init__(self):
        self.searcher = ProductSearcher(Config.CONFIG)
        self.table = TableBuilder()

    def _upload_article(self, keyword):
        """
        Get a keyword and uploads an article.
        :param keyword:
        """
        products = self.searcher.search(Config.PRODUCT_GROUP, keyword)
        self.table.build(products)

        article_builder = ArticleBuilder(keyword, products)
        title = article_builder.get_title()
        wordpress_uploader = WordPressUploader(title, Config.URL,
                                               Config.USER_NAME, Config.PASSWORD)

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
        keywords = KeywordExtractor.extract(Config.KEYWORDS_PATH)
        for keyword in keywords:
            self._upload_article(keyword)


if '__main__' == __name__:
    manager = Manager()
    manager.run()
