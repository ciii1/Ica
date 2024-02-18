import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import indexer
import parser

class test_parser(unittest.TestCase):
    def test_extract_keyword(self):
        keywords = indexer.extract_keywords("test. this is the first keyword and yes this also keywords yay\n\t")
        self.assertEqual(keywords, [
            "test", 
            "this", 
            "is",
            "the",
            "first",
            "keyword",
            "and",
            "yes",
            "this",
            "also",
            "keywords",
            "yay",
        ])

    def test_index_single(self):
        indexer.clear()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>")
        indexer.index(parsed)
        correct = {
            'this': {0: 2},
            'is': {0: 2}, 
            'a': {0: 2}, 
            'content': {0: 1}, 
            'keyword': {0: 2},
            'pure': None,
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

    def test_index_multiple(self):
        indexer.clear()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>\n===\n{content keyword}")
        indexer.index(parsed)
        correct = {
            'this': {0: 2},
            'is': {0: 2}, 
            'a': {0: 2}, 
            'content': {0: 1, 1: 1}, 
            'keyword': {0: 2, 1: 1},
            'pure': None,
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

if __name__ == '__main__':
    unittest.main()
