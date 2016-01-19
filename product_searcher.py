from amazon_api_manger import AmazonAPIManger
from product import Product


class ProductSearcher(object):
    MAX_RESULTS = 13

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
            if index == self.MAX_RESULTS:
                break

            browse_nodes = self.api.item_lookup(ItemId=item.ASIN, ResponseGroup='OfferListings,\
                                                                                      BrowseNodes,\
                                                                                      OfferSummary,\
                                                                                      Offers,\
                                                                                      Images')
            product = Product(item, browse_nodes)
            if (product.get_img_url('SmallImage') == 'null') or \
                    (product.get_img_url('MediumImage') == 'null' and product.get_img_url('LargeImage') == 'null'):
                index -= 1
                continue

            if product.get_rating() == 'null' or \
                            product.get_review() == 'null' or product.get_price() == 'null':
                index -= 1
                continue

            products.append(product)

        return products
