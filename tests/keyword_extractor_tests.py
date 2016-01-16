import KeywordExtractor
import unittest
import csv
import types

CSV_PATH = 'test_keywords.csv'


class KeywordExtractorTests(unittest.TestCase):

    def setUp(self):
        self.extractor = KeywordExtractor.KeywordExtractor()

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

        keyword_list.sort()
        our_list.sort()
        self.assertTrue(keyword_list == our_list)


