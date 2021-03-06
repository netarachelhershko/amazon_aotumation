import unittest
import csv
import types
from keyword_extractor import KeywordExtractor

CSV_PATH = 'test_keywords.csv'


class KeywordExtractorTests(unittest.TestCase):

    def setUp(self):
        self.extractor = KeywordExtractor()

    def tearDown(self):
        pass

    def test_extract_sanity(self):
        keyword_list = self.extractor.extract(CSV_PATH)
        self.assertEqual(type(keyword_list), types.ListType)
        our_list = []
        with open(CSV_PATH) as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                our_list.append(row[0])

        self.assertItemsEqual(keyword_list, our_list)


