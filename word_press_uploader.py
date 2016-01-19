from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from add_table_to_tablepress import AddTableToTablepress
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media

from common import open_url, retry

TABLE_PATH = r'article.csv'


class WordPressUploader(object):
    def __init__(self, title, url, user_name, password):
        """
        :param title: str - title of the article
        :param url: str - url of the wordpress web
        :param user_name: str
        :param password: str
        """
        self.client = retry(Client, url, user_name, password)
        self.title = title

    def upload_table(self):
        """
        :return: table id
        """
        with open(TABLE_PATH) as f:
            content = f.read()

        return self.client.call(AddTableToTablepress(self.title, content))

    def upload_article(self, article, img_url, tags, categories):
        """
        Create a post object, initialize its properties and upload it.
        :param article: HTML string
        :param img_url: the url to img
        :param tags: list with tags
        :param categories: list with categories
        """
        post = WordPressPost()
        post.title = self.title
        post.content = article
        post.thumbnail = self._upload_image(img_url)
        post.terms_names = {'post_tag': tags,
                            'category': categories}

        post.post_status = 'publish'
        post.id = self.client.call(NewPost(post))

    def _upload_image(self, img_url):
        """
        Read the binary img and let the XMLRPC library encode it into base64.
        :param img_url: The url to img file.
        :return: attachment_id.
        """
        content_file = open_url(img_url).content
        data = {
            'name': 'picture.jpg',
            'type': 'image/jpeg',
            'bits': xmlrpc_client.Binary(content_file)
        }

        response = self.client.call(media.UploadFile(data))
        return response['id']
