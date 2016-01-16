from urllib import unquote
from BeautifulSoup import BeautifulSoup
from common import extract_HTML


class Product(object):
    def __init__(self, product_item, browse_nodes):
        self.browse_nodes = browse_nodes
        self.categories = []
        self.ASIN = product_item.ASIN
        self.parent_ASIN = product_item.ParentASIN
        self.page_url = unquote(product_item.DetailPageURL.text)
        self.title = product_item.ItemAttributes.Title
        self.product_group = product_item.ItemAttributes.ProductGroup
        html_text = extract_HTML(self.page_url)
        self.soup = BeautifulSoup(html_text)
        try:
            self.manufacturer = product_item.ItemAttributes.Manufacturer
        except:
            self.manufacturer = ''

    def get_categories(self, category_amount=3):
        node = self.browse_nodes.Items.Item.BrowseNodes.BrowseNode
        self.categories.append(node.Name)
        while hasattr(node, 'Ancestors'):
            self.categories.append(node.Ancestors.BrowseNode.Name)
            node = node.Ancestors.BrowseNode

        return self.categories[:category_amount]

    def get_review(self):
        five_stars_review_url = 'http://www.amazon.com/product-reviews/{0}/?ie=' \
                                'UTF8&filterBy=addFiveStar'.format(self.ASIN)

        html_text = extract_HTML(five_stars_review_url)
        soup = BeautifulSoup(html_text)
        all_reviews = soup.findAll("span", "a-size-base review-text")
        all_reviews = [review.text for review in all_reviews]
        all_reviews = sorted(all_reviews, key=lambda word: len(word), reverse=True)
        return all_reviews[0].encode('utf-8')

    def get_img_url(self, size='MediumImage'):
        '''
        :param size: must be uppercase, the options is
        'SmallImage','MediumImage','LargeImage'
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

