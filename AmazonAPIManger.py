import amazonproduct


class AmazonAPIManger(object):
    def __init__(self, config):
        self.api = amazonproduct.API(cfg=config)

    def get_api(self):
        return self.api

