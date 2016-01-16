from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from AddTableToTablepress import AddTableToTablepress


TABLE_PATH = r'article.csv'

class WordPressUploader(object):
    def __init__(self, title, url, user_name, password):
        self.client = Client(url, user_name, password)
        self.title = title

    def upload_table(self):
        """
        :return: table id
        """
        with open(TABLE_PATH) as f:
            content = f.read()

        return self.client.call(AddTableToTablepress(self.title, content))

    def upload_article(self, article):
        post = WordPressPost()
        post.title = self.title
        post.content = article
        post.id = self.client.call(NewPost(post))
        post.post_status = 'publish'

