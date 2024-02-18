import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import indexer
import parser
import query
from query import ResDocs

class test_parser(unittest.TestCase):
    def test_query_basic(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, }[if you're having one or seeing someone having it, call an ambulance]<help>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure')
        self.assertEqual(res, [
            ResDocs(0, 0.5) #help = 1, I'm = /2, having = /2, seizure = 1
        ])

    def test_query_freqs(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, if you're having a seizure, call an ambulance}<help>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure')
        self.assertEqual(res, [
            ResDocs(0, 2.0) #help = 1, I'm = /2, having = 1, seizure = 2
        ])

    def test_query_freqs_div(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, if you're having a seizure, call an ambulance}<help>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure unrelated shit')
        self.assertEqual(res, [
            ResDocs(0, 0.5) #help = 1, I'm = /2, having = 1, seizure = 2, unrelated = /2, shit = /2
        ])

    def test_query_multi_docs(self):
        indexer.clear()

        parsed = parser.parse("""
            {seizure is a serious condition, if you're having a seizure, call an ambulance}<help>
            \n===\n
            {An epileptic seizure, informally known as a seizure, is a period of symptoms due to abnormally excessive or synchronous neuronal activity in the brain.}
        """)
        indexer.index(parsed)
        res = query.query('help i\'m having seizure')
        self.assertEqual(res, [
            ResDocs(0, 2.0), #help = 1, I'm = /2, having = 1, seizure = 2
            ResDocs(1, 0.25) #help = /2, I'm = /2, having = /2, seizure = 2
        ])

if __name__ == '__main__':
    unittest.main()
