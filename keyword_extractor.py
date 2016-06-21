import csv


class KeywordExtractor(object):
    @staticmethod
    def extract(path):
        """
        Get a list with keywords from the file.
        :param path: Path to csv file.
        :return list: Keywords list
        """

        with open(path) as f:
            reader = csv.reader(f)
            reader.next()
            return [row[0] for row in reader]


