import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

import parser
from parser import ParseError
from parser import Node
from parser import NodeType

class test_parser(unittest.TestCase):
    def test_parse_basic(self):
        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>")
        self.assertEqual(parsed, [
            [
                Node(NodeType.CONTENT_KEYWORD, "this is a content keyword", 1),
                Node(NodeType.CONTENT, "pure content", 1),
                Node(NodeType.KEYWORD, "this is a keyword", 1),
            ]
        ])

    def test_parse_multiline(self):
        parsed = parser.parse("{this is a content\nkeyword}[pure\ncontent]\n<this is a keyword>")
        self.assertEqual(parsed, [
            [
                Node(NodeType.CONTENT_KEYWORD, "this is a content\nkeyword", 1),
                Node(NodeType.CONTENT, "pure\ncontent", 1),
                Node(NodeType.KEYWORD, "this is a keyword", 1),
            ]
        ])

    def test_parse_multidocs(self):
        parsed = parser.parse("{this is a content keyword}[pure content]<this is a keyword>\n===\n<keyword2>[pure content]")
        self.assertEqual(parsed, [
            [
                Node(NodeType.CONTENT_KEYWORD, "this is a content keyword", 1),
                Node(NodeType.CONTENT, "pure content", 1),
                Node(NodeType.KEYWORD, "this is a keyword", 1),
            ],
            [
                Node(NodeType.KEYWORD, "keyword2", 1),
                Node(NodeType.CONTENT, "pure content", 1),
            ]
        ])

    def test_parse_empty(self):
        parsed = parser.parse("")
        self.assertEqual(parsed, [[]])

    def test_parse_empty2(self):
        parsed = parser.parse("\n===\n===")
        self.assertEqual(parsed, [[],[]])

    def test_parse_error(self):
        try:
            parser.parse("{this is an errornous input")
        except ParseError as err:
            self.assertEqual(err.line_num, 1)
            self.assertEqual(err.char_num, 27)
            self.assertEqual(err.message, "An error encountered while parsing: Unclosed '{' at (" + str(err.line_num) + "," + str(err.char_num) + ")")

    def test_parse_error_multiline(self):
        try:
            parser.parse("{this is not an errornous input}\n===\n{not errornous}\n{not yet}\n===\n[errornous}")
        except ParseError as err:
            self.assertEqual(err.line_num, 6)
            self.assertEqual(err.char_num, 11)
            self.assertEqual(err.message, "An error encountered while parsing: The closing '}' doesn't match the opening '[' at (" + str(err.line_num) + "," + str(err.char_num) + ")")

    def test_parse_error_multiline2(self):
        try:
            parser.parse("{this is not an errornous input}\n===\n{not errornous}\n{not yet}\n===\n(errornous}")
        except ParseError as err:
            self.assertEqual(err.line_num, 6)
            self.assertEqual(err.char_num, 11)
            self.assertEqual(err.message, "An error encountered while parsing: The closing '}' is not opened at (" + str(err.line_num) + "," + str(err.char_num) + ")")

if __name__ == '__main__':
    unittest.main()
