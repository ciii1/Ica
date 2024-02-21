import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import indexer
import parser
import query
from query import ResDocs

class test_query(unittest.TestCase):
    def test_query_basic(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, }[if you're having one or seeing someone having it, call an ambulance]<help im>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure')
        self.assertEqual(res, [
            ResDocs(0, 1.466747618158042) #help = 1, I'm = 1, having = /2, seizure = 1 divided by some proximity stuff
        ])

    def test_query_freqs(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, if you're having a seizure, call an ambulance}<help>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure')
        self.assertEqual(res, [
            ResDocs(0, 2.357934425914448) #help = 1, I'm = is = 1, having = 1, seizure = 2 divided by some proximity stuff
        ])

    def test_query_freqs_div(self):
        indexer.clear()

        parsed = parser.parse("{seizure is a serious condition, if you're having a seizure, call an ambulance}<help>")
        indexer.index(parsed)
        res = query.query('help i\'m having seizure unrelated shit')
        self.assertEqual(res, [
            ResDocs(0, 0.589483606478612) #help = 1, i'm = is = 1/2, having = 1, seizure = 2, unrelated = /2, shit = /2
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
            ResDocs(0, 1.952090270070292), #help = 1, I'm = /2, having = 1, seizure = 2 divided by some proximity thing
            ResDocs(1, 0.25) #help = /2, I'm = /2, having = /2, seizure = 2 not divided by proximity because only one token exists
        ])

    def test_query_case_insensitive(self):
        indexer.clear()

        parsed = parser.parse("""
            {die}
        """)
        indexer.index(parsed)
        res = query.query('DIE')
        self.assertEqual(res, [
            ResDocs(0, 1/1.3) #DiE = (D,E)1 / (i)1.1
        ])

    def test_query_proximity(self):
        indexer.clear()

        parsed = parser.parse("""
            {hello how are you}
            \n===\n
            {hello you are how}
        """)
        indexer.index(parsed)
        res = query.query('hello you')
        self.assertEqual(res[0].index, 1)

    def test_normalize_distance(self):
        self.assertEqual(0.123, query.normalize_distance(123))

    def test_normalize_distance2(self):
        self.assertEqual(0, query.normalize_distance(0))

if __name__ == '__main__':
    unittest.main()
