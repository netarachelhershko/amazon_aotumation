from urllib import unquote
from BeautifulSoup import BeautifulSoup
from common import open_url


class Product(object):
    def __init__(self, product_item, browse_nodes):
        self.browse_nodes = browse_nodes
        self.categories = []
        self.ASIN = str(product_item.ASIN)
        self.parent_ASIN = str(product_item.ParentASIN)
        self.page_url = unquote(product_item.DetailPageURL.text)
        self.title = str(product_item.ItemAttributes.Title)
        self.product_group = str(product_item.ItemAttributes.ProductGroup)
        html_text = open_url(self.page_url).text
        self.soup = BeautifulSoup(html_text)
        try:
            self.manufacturer = str(product_item.ItemAttributes.Manufacturer)
        except:
            self.manufacturer = ''

    def get_categories(self):
        """
        Loop through the the ancestors name and append its to list
        :return: Lise with 2 categories.
        """
        node = self.browse_nodes.Items.Item.BrowseNodes.BrowseNode
        self.categories.append(str(node.Name))
        index = 1
        while hasattr(node, 'Ancestors') and index < 2 and \
                hasattr(node.Ancestors.BrowseNode, 'Name'):
            self.categories.append(str(node.Ancestors.BrowseNode.Name))
            node = node.Ancestors.BrowseNode
            index += 1

        return self.categories

    def get_review(self):
        """
        Find the longest review with five stars.
        :return: Review - str.
        """
        five_stars_review_url = 'http://www.amazon.com/product-reviews/{0}/?ie=' \
                                'UTF8&filterBy=addFiveStar'.format(self.ASIN)

        html_text = open_url(five_stars_review_url).text
        soup = BeautifulSoup(html_text)
        all_reviews = soup.findAll("span", "a-size-base review-text")
        all_reviews = [review.text for review in all_reviews]
        all_reviews = sorted(all_reviews, key=lambda word: len(word), reverse=True)
        return all_reviews[0].encode('utf-8')

    def get_img_url(self, size='MediumImage'):
        '''
        :param size: Must be one of the options:
        'SmallImage','MediumImage','LargeImage'. By default its MediumImage.
        :return: url
        '''
        args = ['SmallImage', 'MediumImage', 'LargeImage']
        if size not in args:
            raise ValueError("must be uppercase, the options is:{0}".format(args))

        if hasattr(self.browse_nodes.Items.Item, size):
            return getattr(self.browse_nodes.Items.Item, size).URL

        return 'null'

    def get_price(self):
        node = self.browse_nodes.Items.Item.OfferSummary
        if hasattr(node, 'LowestNewPrice'):
            return node.FormattedPrice

        return self.soup.findAll("span", id="priceblock_ourprice")[0].text

    def get_rating(self):
        rating = self.soup.findAll("div", id="avgRating")[0].span.a.span.text[:3]
        return rating
