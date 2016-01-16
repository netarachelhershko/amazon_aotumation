import common

TABLE_FORMAT = '[table id={0} /]'
REVIEW_FORMAT = '<em><strong>Testimonial:</strong></em> <blockquote><em>{0}</em></blockquote>'
IMG_FORMAT = '<a href="{0}" target="_blank" rel="nofollow"><img class="{1}" src="{2}" alt="{3}" width="300" height="187" /></a></h3>'
TITLE_FORMAT = '<h3><a href={0} target="_blank" rel="nofollow">{1}</a></h3>'
PRODUCT_FORMAT = '{0} {1} {2} &nbsp; &nbsp; &nbsp;'
CLASS_FORMAT = "{0} wp-image-785 size-medium"


class ArticleBuilder(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def get_title(self):
        title = "The Best {0}".format(self.keyword.title())
        return title

    def build(self, products, table_id):
        '''

        :param : list with Product items.
        :return article: html string
        '''

        article = TABLE_FORMAT.format(table_id)
        for index, product in enumerate(products):
            shorten_url = common.get_short_url(product.page_url)
            alignment = CLASS_FORMAT.format('alignleft' if index % 2 == 0 else 'alignright')
            title = TITLE_FORMAT.format(shorten_url, product.title)
            img = IMG_FORMAT.format(shorten_url, alignment, product.get_img_url('LargeImage'), product.title)
            review = REVIEW_FORMAT.format(product.get_review())
            article += PRODUCT_FORMAT.format(title, img, review)

        return article

