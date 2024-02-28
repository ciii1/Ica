import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import indexer
import parser
from indexer import IndexValue
from indexer import Keyword

class test_indexer(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        indexer.delete_docs()

    def test_extract_keyword(self):
        keywords = indexer.extract_keywords("test. this is the first keyword and yes this also keywords yay\n\t", 1)
        correct = [
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
        ]

        self.assertEqual(keywords, correct)

    def test_index_single(self):
        indexer.init()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>")
        indexer.index(parsed)
        correct = {
            'content': {
                0: IndexValue(weight=1, positions=[3]), 
            }, 
            'keyword': {
                0: IndexValue(weight=1, positions=[4, 8]), 
            }
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

    def test_index_multiple(self):
        indexer.init()

        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>\n===\n{content keyword}")
        indexer.index(parsed)
        correct = {
            'content': {
                0: IndexValue(weight=1, positions=[3]), 
                1: IndexValue(weight=1, positions=[0])
            }, 
            'keyword': {
                0: IndexValue(weight=1, positions=[4, 8]), 
                1: IndexValue(weight=1, positions=[1])
            }
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])
            
    def test_index_syn1(self):
        indexer.init()

        parsed = parser.parse("{idiot}[ sorry]")
        indexer.index(parsed)
        correct = {
            'idiot': {
                0: IndexValue(weight=1, positions=[0]), 
            }, 
            'stupid': {
                0: IndexValue(weight=0.5, positions=[0]), 
            }, 
        }
        for elem in correct:
            compare = indexer.get_index(elem)
            self.assertEqual(compare, correct[elem])

if __name__ == '__main__':
    unittest.main()
