import Product
from AmazonAPIManger import AmazonAPIManger


class ProductSearcher(object):
    def __init__(self, config):
        self.api = AmazonAPIManger(config).get_api()

    def search(self, product_group, keyword):
        '''
        :param api: amazonproduct item
        :param product_group: search_index(string)
        :param keyword: free keyword (string)
        :return: list of Products instance
        '''

        product_items = self.api.item_search(product_group, Keywords=keyword)
        products = []
        for index, item in enumerate(product_items):
            browse_nodes = self.api.item_lookup(ItemId=item.ASIN, ResponseGroup='OfferListings,\
                                                                                      BrowseNodes,\
                                                                                      OfferSummary,\
                                                                                      Offers,\
                                                                                      Images')
            product = Product.Product(item, browse_nodes)
            if (product.get_img_url('SmallImage') == 'null') or \
                    (product.get_img_url('MediumImage') == 'null' and product.get_img_url('LargeImage') == 'null'):
                index -= 1
                continue

            products.append(product)
            if index == 12:
                break

        return products

