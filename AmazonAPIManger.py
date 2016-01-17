import amazonproduct


class AmazonAPIManger(object):
    def __init__(self, config):
        """
        :param config: Dict for example- {'access_key': '',
                                          'secret_key': '',
                                          'associate_tag': '',
                                          'locale': 'us'}
        """
        self.api = amazonproduct.API(cfg=config)

    def get_api(self):
        return self.api
