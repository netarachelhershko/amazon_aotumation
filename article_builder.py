import common


class ArticleBuilder(object):
    TABLE_FORMAT = '[table id={0} /]'
    REVIEW_FORMAT = '<em><strong>Testimonial:</strong></em> <blockquote><em>{0}</em></blockquote>&nbsp;<p style="text-align: center;"><a ref="nofollow" target="_blank" href="{review_url}">&gt;&gt; Read More Reviews On {title} Here &lt;&lt;</a></p>'
    IMG_FORMAT = '<a href="{0}" target="_blank" rel="nofollow"><img class="{1}" src="{2}" alt="{3}" width="300" height="187" /></a></h3>'
    TITLE_FORMAT = '<h3><a href={0} target="_blank" rel="nofollow">{1}</a></h3>'
    FEATURES_FORMAT = '<h6>Scored {score}/5.0 - From {num_of_reviews} Customer Reviews</h6>\n<h6>Priced From {price}</h6>\n<h6>Features:</h6>{features}'
    PRODUCT_FORMAT = '{0} {1} {2} {3} &nbsp;\n&nbsp;'
    CLASS_FORMAT = "{0} wp-image-785 size-medium"

    def __init__(self, keyword, products):
        """
        :param keyword: keyword search
        :param products: list with Product items
        :return:
        """
        self.keyword = keyword
        self.products = products
        self.title = ''
        self.tags = []
        self.article = ''

    def get_title(self):
        if self.title:
            return self.title

        self.title = "The Best {0}".format(self.keyword.title())
        return self.title

    def get_tags(self):
        if self.tags:
            return self.tags

        for product in self.products:
            if product.manufacturer != 'null':
                self.tags.append(product.manufacturer)

        self.tags = list(set(self.tags))
        return self.tags

    def build(self, table_id):
        """
        Builds an article, written in HTML, the article includes the table,
        title, review and image for all the products.
        :param table_id: wordpress table id
        :return article: html string
        """
        if self.article:
            return self.article

        self.article = self.TABLE_FORMAT.format(table_id)
        for index, product in enumerate(self.products):
            shorten_url = common.get_short_url(product.page_url)
            alignment = self.CLASS_FORMAT.format('alignleft' if index % 2 == 0 else 'alignright')
            title = self.TITLE_FORMAT.format(shorten_url, product.title)
            features = self.FEATURES_FORMAT.format(price=product.get_price(), score=product.get_rating(),
                                                   num_of_reviews=product.get_num_of_reviews(),
                                                   features=product.get_features())
            img = self.IMG_FORMAT.format(shorten_url, alignment, product.get_img_url('LargeImage'), product.title)
            review = self.REVIEW_FORMAT.format(product.get_review(), review_url=common.get_short_url(product.five_stars_review_url),
                                               title=product.title)
            self.article += self.PRODUCT_FORMAT.format(title, features, img, review)

        return self.article
