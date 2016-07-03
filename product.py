from urllib import unquote
from BeautifulSoup import BeautifulSoup
from common import open_url
from config import CONFIG


# noinspection PyBroadException
class Product(object):
    def __init__(self, product_item, browse_nodes):
        self.browse_nodes = browse_nodes
        self.ASIN = product_item.ASIN.text
        self.page_url = unquote(product_item.DetailPageURL.text)
        self.title = product_item.ItemAttributes.Title.text.encode('utf-8')
        html_text = open_url(self.page_url).text
        self.soup = BeautifulSoup(html_text)
        self.categories = []
        self.img_urls = {}
        self.price = ''
        self.rating = ''
        self.review = ''
        self.features = ''
        self.num_of_reviews = None
        self.five_stars_review_url = 'http://www.amazon.com/product-reviews/{0}/?ie=' \
                                     'UTF8&filterBy=addFiveStar&tag={1}'.format(self.ASIN, CONFIG['associate_tag'])
        try:
            self.manufacturer = str(product_item.ItemAttributes.Manufacturer)
        except:
            self.manufacturer = 'null'

    def get_features(self):
        if self.features:
            return self.features

        try:
            features = self.soup.find('div', id='feature-bullets')
            bullets = filter(lambda _: not _.get('id'), features.findAll('li'))
            bullets = [_.text for _ in bullets]
            try: bullets = [_.encode('utf-8') for _ in bullets]
            except: pass
            bullet_text = ['<li>{}</li>'.format(x) for x in bullets]
            self.features = '<ul>{}</ul>'.format('\n'.join(bullet_text))
            return self.features
        except:
            pass

    def get_num_of_reviews(self):
        if self.num_of_reviews:
            return self.num_of_reviews

        self.num_of_reviews = self.soup.find('span', id='acrCustomerReviewText').text.split()[0]
        return self.num_of_reviews

    def get_categories(self):
        """
        Loop through the ancestors name and append its to list
        :return: List with 2 categories.
        """
        if self.categories:
            return self.categories

        node = self.browse_nodes.Items.Item.BrowseNodes.BrowseNode
        index = 0
        while hasattr(node, 'Ancestors') and index < 2 and \
                hasattr(node.Ancestors.BrowseNode, 'Name'):
            self.categories.append(str(node.Name))
            node = node.Ancestors.BrowseNode
            index += 1

        return self.categories

    def get_review(self):
        """
        Find the longest review with five stars.
        :return: Review - str.
        """
        if self.review:
            return self.review

        html_text = open_url(self.five_stars_review_url).text
        soup = BeautifulSoup(html_text)
        all_reviews = soup.findAll("span", "a-size-base review-text")
        if len(all_reviews) > 0:
            all_reviews = [review.text for review in all_reviews]
            all_reviews = sorted(all_reviews, key=lambda word: len(word), reverse=True)
            self.review = all_reviews[0].encode('utf-8')
            return self.review

        self.review = 'null'
        return self.review

    def get_img_url(self, size='MediumImage'):
        """
        :param size: Must be one of the options:
        'SmallImage','MediumImage','LargeImage'. By default its MediumImage.
        :return: url
        """
        args = ['SmallImage', 'MediumImage', 'LargeImage']
        if size not in args:
            raise ValueError("Must be one of {0}, got {1}".format(args, size), size)

        if size in self.img_urls:
            return self.img_urls[size]

        if hasattr(self.browse_nodes.Items.Item, size):
            self.img_urls[size] = getattr(self.browse_nodes.Items.Item, size).URL
            return self.img_urls[size]

        self.img_urls[size] = 'null'
        return self.img_urls[size]

    def get_price(self):
        if self.price:
            return self.price

        node = self.browse_nodes.Items.Item.OfferSummary
        if hasattr(node, 'LowestNewPrice'):
            self.price = node.LowestNewPrice.FormattedPrice.text
            return self.price

        find_all = self.soup.findAll("span", id="priceblock_ourprice")
        if len(find_all) > 0:
            self.price = find_all[0].text
            return self.price

        self.price = 'null'
        return self.price

    def get_rating(self):
        if self.rating:
            return self.rating

        find_all = self.soup.findAll("div", id="avgRating")
        if len(find_all) > 0:
            self.rating = find_all[0].span.a.span.text[:3]
            return self.rating

        self.rating = 'null'
        return self.rating
