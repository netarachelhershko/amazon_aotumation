from wordpress_xmlrpc import AnonymousMethod


class AddTableToTablepress(AnonymousMethod):
    """
    Wrap the XML-RPC Method addTableToTablePress.
    """
    method_name = 'theshoesforme.addTableToTablePress'
    method_args = ('name', 'data')

