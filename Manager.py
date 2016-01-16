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
        products = self.searcher.search(Config.PRODUCT_GROUP, keyword)
        self.table.build(products)
        article_builder = ArticleBuilder(keyword)
        title = article_builder.get_title()
        wordpress_uploader = WordPressUploader(title, Config.URL,
                                                    Config.USER_NAME, Config.PASSWORD)

        table_id = wordpress_uploader.upload_table()
        content = article_builder.build(products, table_id)
        wordpress_uploader.upload_article(content)

    def run(self):
        keywords = KeywordExtractor.extract(Config.KEYWORDS_PATH)
        for keyword in keywords:
            self._upload_article(keyword)


if '__main__' == __name__:
    manager = Manager()
    manager.run()