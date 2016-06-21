from wordpress_xmlrpc import AnonymousMethod
from config import URL
import tldextract


class AddTableToTablepress(AnonymousMethod):
    """
    Wrap the XML-RPC Method addTableToTablePress.
    """
    method_name = '{}.addTableToTablePress'.format(tldextract.extract(URL).domain)
    method_args = ('name', 'data')
