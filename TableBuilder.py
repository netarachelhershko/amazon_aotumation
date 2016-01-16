import csv

TABLE_PATH = r'article.csv'
IMG_FORMAT = '<a target="_blank" rel="nofollow" href="http://amzn.to/1F9ASJc"><img src={0} /></a>'

class TableBuilder(object):
    def __init__(self):
        self.fieldnames = {'Picture': '',
                           'Name': '',
                           'Rating': '',
                           'Price': ''}

    def build(self, products):
        with open(TABLE_PATH, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames.keys())
            writer.writeheader()
            for product in products:
                self.fieldnames['Picture'] = IMG_FORMAT.format(product.get_img_url('SmallImage'))
                self.fieldnames['Name'] = product.title
                self.fieldnames['Rating'] = product.get_rating()
                self.fieldnames['Price'] = product.get_price()
                writer.writerow(self.fieldnames)