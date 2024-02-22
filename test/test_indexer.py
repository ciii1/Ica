import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import indexer
import parser
from indexer import IndexValue
from indexer import IndexPosition
from indexer import Keyword

class test_parser(unittest.TestCase):
    def test_extract_keyword(self):
        keywords = indexer.extract_keywords("test. this is the first keyword and yes this also keywords yay\n\t", 1)
        self.assertEqual(keywords, [
            Keyword("test", 1), 
            Keyword("this", 1), 
            Keyword("is", 1),
            Keyword("the", 1),
            Keyword("first", 1),
            Keyword("keyword", 1),
            Keyword("and", 1),
            Keyword("yes", 1),
            Keyword("this", 1),
            Keyword("also", 1),
            Keyword("keywords", 1),
            Keyword("yay", 1),
        ])

    def test_index_single(self):
        indexer.clear()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>")
        indexer.index(parsed)
        correct = {
            'this': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=0, weight=1), 
                    IndexPosition(position=5, weight=1)
                ], doc_length=9)
            }, 
            'is': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=1, weight=1), IndexPosition(position=6, weight=1)
                ], doc_length=9)
            }, 
            'a': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=2, weight=1), 
                    IndexPosition(position=7, weight=1)], doc_length=9)
            },
            'content': {
                0: IndexValue(freq=1, positions=[IndexPosition(position=3, weight=1)], doc_length=9), 
            }, 
            'keyword': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=4, weight=1), 
                    IndexPosition(position=8, weight=1)], doc_length=9), 
            }
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

    def test_index_multiple(self):
        indexer.clear()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>\n===\n{content keyword}")
        indexer.index(parsed)
        correct = {
            'this': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=0, weight=1), 
                    IndexPosition(position=5, weight=1)
                ], doc_length=9)
            }, 
            'is': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=1, weight=1), IndexPosition(position=6, weight=1)
                ], doc_length=9)
            }, 
            'a': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=2, weight=1), 
                    IndexPosition(position=7, weight=1)], doc_length=9)
                },
            'content': {
                0: IndexValue(freq=1, positions=[IndexPosition(position=3, weight=1)], doc_length=9), 
                1: IndexValue(freq=1, positions=[IndexPosition(position=0, weight=1)], doc_length=2)
            }, 
            'keyword': {
                0: IndexValue(freq=2, positions=[
                    IndexPosition(position=4, weight=1), 
                    IndexPosition(position=8, weight=1)], doc_length=9), 
                1: IndexValue(freq=1, positions=[IndexPosition(position=1, weight=1)], doc_length=2)
            }
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

if __name__ == '__main__':
    unittest.main()
