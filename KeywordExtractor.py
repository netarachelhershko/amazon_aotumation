import csv


class KeywordExtractor(object):
    @staticmethod
    def extract(path):
        '''
        Get a list with keywords from the file.
        :param path: Path to csv file.
        :return list: Keywords list
        '''

        keywords = []
        with open(path) as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                keywords.append(row[0])

        return keywords

